---
layout: post
title: Gradle Configuration Cache와 캐시 친화적인 빌드 스크립트
summary: Gradle Configuration Cache가 무엇인지, 왜 build.gradle을 project.property 대신 Provider API로 바꿔야 하는지, 그리고 Jib처럼 아직 호환되지 않는 플러그인을 어떻게 격리하는지 정리합니다.
date: 2026-07-24 15:30:00 +0900
updated: 2026-07-24 15:30:00 +0900
tag: gradle build configuration-cache provider jvm
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 시작: "Configuration Cache 친화 설정 변경" PR

어느 날 아래 같은 PR을 봤다고 하자. 제목은 **"Gradle Configuration Cache 친화 설정 변경"**, 변경 파일은 `build.gradle.kts` 하나다.

```kotlin
// Before
jib {
    val dockerRepository = project.property("docker.repository")
    val dockerfileTag = project.property("dockerfile.tag")
    // ...
}

tasks.withType<com.google.cloud.tools.jib.gradle.JibTask> {
    notCompatibleWithConfigurationCache("Jib plugin is not yet fully compatible with configuration cache")
}
```

```kotlin
// After
import com.google.cloud.tools.jib.gradle.JibTask

jib {
    val dockerRepository = providers.gradleProperty("docker.repository").getOrElse("dev/app")
    val dockerfileTag = providers.gradleProperty("dockerfile.tag").getOrElse("1.0")
    // ...
}

tasks.withType<JibTask> {
    notCompatibleWithConfigurationCache("because https://github.com/GoogleContainerTools/jib/issues/3132")
}
```

거기에 `gradle.properties`에서 기본값 몇 줄이 삭제됐다. 별것 아닌 것 같은 이 diff 안에 Gradle 빌드의 꽤 깊은 개념이 다 들어있다. 하나씩 풀어보자.

## 2. 그 전에: Gradle 빌드의 3단계

Configuration Cache를 이해하려면 먼저 Gradle 빌드가 어떤 단계로 도는지 알아야 한다.

```
1. Initialization  →  2. Configuration  →  3. Execution
```

### Initialization (초기화)

어떤 프로젝트를 빌드할지 결정한다. `settings.gradle`을 읽어 멀티모듈 구조를 파악하고, 각 프로젝트마다 `Project` 객체를 생성한다.

### Configuration (설정)

**모든 프로젝트의 `build.gradle` 스크립트를 처음부터 끝까지 실행**한다. 이때 task를 실제로 "실행"하는 게 아니라, task를 정의하고 설정하고, 서로의 의존 관계를 엮어서 **task 그래프(DAG)**를 만든다.

핵심은 **build.gradle의 대부분 코드가 이 단계에서 돈다**는 것이다.

```groovy
// 이 println은 configuration phase에서 실행됨
// task를 돌리든 안 돌리든 무조건 출력됨
println "설정 중..."

task hello {
    // 이 블록(설정)도 configuration phase에서 실행됨
    println "hello task 설정 중"

    doLast {
        // 반면 이 안은 execution phase에서 실행됨
        println "hello task 실제 실행!"
    }
}
```

`./gradlew help` 하나만 쳐도 모든 build.gradle이 전부 평가된다. 실행하지도 않을 task의 설정 코드까지 전부. 그래서 프로젝트가 크고 플러그인이 많으면 이 단계 자체가 느려질 수 있다.

### Execution (실행)

Configuration에서 만든 task 그래프를 보고, 실제로 요청한 task와 그 의존 task들만 실행한다. 위 예시의 `doLast { }` 안 코드가 여기서 돈다.

## 3. Configuration Cache란

Configuration Cache는 **2번 Configuration 단계의 결과물(완성된 task 그래프)을 직렬화해서 디스크에 저장**해두는 기능이다. 입력이 바뀌지 않으면 다음 빌드에서 configuration phase를 **통째로 건너뛰고** 캐시된 task 그래프를 바로 재사용한다.

혼동하기 쉬운데, 캐시가 저장하는 것은 **컴파일된 `.class` 결과물이 아니라 "어떤 task를 어떤 순서로 돌릴지에 대한 계획"**이다. 다음 빌드는 이 계획을 바로 읽어 곧장 execution phase로 점프한다.

이걸 이해하면 재미있는 사실이 하나 따라온다. 위 예시에서 build.gradle 최상단의 `println "설정 중..."`은 캐시가 켜진 상태로 **두 번째 실행하면 찍히지 않는다.** configuration phase를 통째로 스킵하기 때문이다. 오히려 "찍히던 게 안 찍히는" 것이 캐시가 작동한다는 증거다.

활성화는 간단하다.

```properties
# gradle.properties
org.gradle.configuration-cache=true
```

## 4. 캐시 가능하려면: "선언된 입력의 순수 함수"여야 한다

무언가를 캐시하려면 그것은 **"선언된 입력 → 출력"이 결정적인 함수**여야 한다.

```
출력 = f(입력)   ← 입력이 같으면 출력이 같다는 보장이 있어야 캐시 가능
```

그래서 Gradle은 configuration phase의 **입력**을 추적한다. `build.gradle`, `gradle.properties` 내용, 환경변수, 시스템 프로퍼티, 참조한 파일 내용, 커맨드라인 인자 등이다. 이 중 하나라도 바뀌면 캐시를 버리고 configuration phase를 다시 실행한다.

문제는 **선언되지 않은 숨은 입력(hidden dependency)**이다. configuration phase에서 `System.getenv()`를 직접 부르면, Gradle은 "이 환경변수가 바뀌면 캐시를 무효화해야 한다"는 사실을 모른다. 그래서 캐시가 부정확해지거나 아예 불가능해진다.

## 5. 핵심 변경: `project.property()` → `providers.gradleProperty()`

이제 PR의 알맹이로 돌아오자. 둘 다 "`docker.repository`라는 이름의 값을 가져와라"는 같은 목적이다. 차이는 **"어떻게" 가져오느냐**에 있다.

### `project.property()` — "지금 당장 값을 꺼내줘"

```kotlin
val dockerRepository = project.property("docker.repository")
```

- **`Project` 객체를 통해** 값을 읽는다.
- 읽는 시점이 **즉시(eager)** — 이 코드가 평가되는 그 순간(configuration phase) 값을 확정한다.
- 결과가 실제 값 그 자체다.

무엇이 문제일까? Configuration Cache는 다음 빌드에서 configuration phase를 스킵한다. 스킵한다는 건 **`Project` 객체 자체가 만들어지지 않는다**는 뜻이다. 그런데 `project.property()`는 바로 그 `Project`에 의존한다. 캐시에서 복원할 때 `Project`가 없으니 이 코드를 실행할 수 없다. 그래서 Gradle은 Configuration Cache에서 `Project` 접근을 금지한다.

### `providers.gradleProperty()` — "값을 가져오는 방법을 감싼 상자"

```kotlin
val dockerRepository = providers.gradleProperty("docker.repository").getOrElse("dev/app")
```

- **`Provider<String>`**라는 "값을 감싼 상자"를 돌려준다. 값 자체가 아니라 "값을 가져오는 방법"에 가깝다.
- **지연 평가(lazy)** — 상자를 만들 때가 아니라 실제로 값이 필요한 순간에 꺼낸다.
- `Project`가 아니라 **`providers`(ProviderFactory)**를 통해 접근한다. 이 통로는 Configuration Cache가 안전하게 추적할 수 있게 설계되어 있다.

즉 Provider로 감싸는 것이 해결책이 되는 이유는 "Provider니까 캐시된다"가 아니라, **Provider가 `Project` 접근이라는 문제 원인 자체를 제거**하기 때문이다. 값 읽기를 지연시켜 configuration phase에 `Project`를 건드리지 않고, 동시에 "이 property가 내 입력이다"라고 Gradle에 등록한다.

### `getOrElse("dev/app")`는 왜 등장했나

Provider(상자)에서 값을 꺼내되, 값이 없으면 기본값을 쓰라는 뜻이다.

```kotlin
providers.gradleProperty("docker.repository")  // Provider<String> (상자)
    .getOrElse("dev/app")                        // 비어있으면 "dev/app"
```

이 기본값이 이 PR에 등장한 것은 우연이 아니라 **`gradle.properties`에서 기본값을 삭제한 변경 때문에 필연적으로 따라온 것**이다. 원래 거기 값이 박혀 있었는데, 이제는 CI가 빌드할 때 `-P`로 주입하는 구조로 바뀌었다. 그래서:

- CI 빌드 → `-Pdocker.repository=...`로 주입된 값 사용
- 로컬 빌드 → 주입 안 됨 → 기본값 `"dev/app"` 사용

만약 `getOrElse` 없이 뒀다면 CI가 아니라 **로컬 개발자의 빌드가 깨진다.** 로컬에선 주입을 안 하니 property가 비어서, 값을 꺼내는 순간 터지기 때문이다. `project.property()`는 값이 없으면 예외를 던지지만, Provider API는 `getOrElse`로 이 케이스를 깔끔하게 처리한다.

### 정리

| | `project.property()` | `providers.gradleProperty()` |
|---|---|---|
| 방식 | 지금 냉장고 열어서 우유 꺼내와 | 우유 가져오는 심부름 쪽지를 줄게 |
| 평가 시점 | 즉시(eager) | 지연(lazy) |
| 접근 통로 | `Project`(캐시 금지 대상) | `providers`(캐시 안전) |
| 반환 | 실제 값 | `Provider<T>`(값을 감싼 상자) |
| 값 없을 때 | 예외 | `getOrElse`로 기본값 지정 |
| Config Cache | 깨짐 | 호환 |

## 6. 고칠 수 없는 것은 격리한다: Jib 예외 처리

PR에는 이런 줄이 있었다.

```kotlin
tasks.withType<JibTask> {
    notCompatibleWithConfigurationCache("because https://github.com/GoogleContainerTools/jib/issues/3132")
}
```

Jib는 Dockerfile 없이 Gradle task로 컨테이너 이미지를 빌드해주는 플러그인이다. 그런데 이 플러그인은 아직 Configuration Cache를 완전히 지원하지 못한다. "예전엔 됐다가 빠진" 게 아니라, Configuration Cache 자체가 비교적 최근에 안정화된 기능이라 오래된 플러그인들이 아직 못 따라온 것이다.

플러그인이 Configuration Cache에서 깨지는 전형적인 이유는 두 가지다.

1. **Execution phase에서도 `Project` 객체를 붙잡고 있음** — 우리가 `project.property()`에서 본 문제의 확장판이다. 캐시된 빌드에선 `Project`가 복원되지 않는다.
2. **직렬화 불가능한 상태를 들고 있음** — Configuration Cache는 task 그래프를 디스크에 직렬화한다. 그런데 네트워크 커넥션, 레지스트리 인증 핸들 같은 **런타임 자원**은 "파일로 저장했다 복원한다"는 개념 자체가 성립하지 않는다.

여기서 중요한 사고가 나온다. Jib는 내가 고칠 수 없는 **서드파티 코드**다. 그렇다고 캐시를 포기하지 않는다. 대신 **문제를 최소 단위로 격리하고 나머지는 이득을 취한다.**

`notCompatibleWithConfigurationCache(...)`의 의미는 "이 Jib task가 실행되는 빌드에서는 Configuration Cache를 얌전히 비활성화하라"이다. 그 결과:

- `./gradlew build`, `./gradlew test`처럼 **Jib를 안 쓰는 대부분의 빌드** → 캐시 정상 작동, 빨라짐
- `./gradlew jib`처럼 **이미지 빌드하는 빌드** → 그 빌드만 캐시가 꺼짐

주의할 점은 이때 꺼지는 것은 **캐시**이지 Jib가 아니라는 것이다. Jib task는 정상적으로 잘 돈다. `notCompatibleWithConfigurationCache`는 Jib를 막는 게 아니라, Jib가 돌 때 캐시를 끄는 것이다. 손해(캐시 못 씀)의 반경을 최소화한, 서킷 브레이커나 bulkhead 패턴과 같은 결의 격리다.

그리고 사유 메시지를 막연한 문장 대신 **GitHub 이슈 링크로** 바꾼 것도 의도적이다. Jib가 그 이슈를 해결하면 이 예외 처리를 지우면 된다. 임시방편에 **"언제 제거할 수 있는지"의 조건**을 함께 남긴 것이다. 미래의 나에게 남기는 빵부스러기다.

## 7. 준비와 활성화를 나누는 이유

이런 작업은 보통 브랜치나 PR이 두 단계로 나뉜다.

```
1단계: 코드를 캐시-safe하게 리팩터링  (기능은 그대로, 스위치는 아직 OFF)
2단계: org.gradle.configuration-cache=true 로 스위치 ON
```

앞서 본 PR은 사실 1단계, 즉 **캐시를 켤 준비만** 한 것이다. 스위치는 아직 올리지 않았다. 왜 굳이 나눌까? "순서대로 하면 깔끔해서"가 아니라 **디버깅 가능성** 때문이다.

만약 리팩터링과 스위치 ON을 한 PR에 합쳤는데 빌드가 깨졌다고 하자. 그러면 용의자가 둘이다.

1. Provider 마이그레이션을 어디선가 빠뜨렸나?
2. 아니면 캐시를 켠 것이 상관없는 딴 데서 문제를 터뜨렸나?

한 커밋에서 변수를 두 개 동시에 건드렸으니 **구분이 안 된다.**

반대로 나누면, 1단계 PR은 **동작이 안 바뀌어야 정상**이다. 여기서 뭔가 깨지면 범인은 무조건 리팩터링이다. 그다음 2단계에서 깨지면, 1단계는 이미 멀쩡함이 확인됐으니 범인은 무조건 캐시 스위치다. 과학 실험처럼 **한 번에 변수 하나만 바꾸니, 깨지는 순간 범인이 자동으로 특정된다.**

## 8. 한 줄 요약과, 가져갈 사고구조

이 PR의 표면은 build.gradle 몇 줄이지만, 그 밑에는 빌드/시스템 엔지니어링에 반복해서 등장하는 사고구조가 깔려있다.

- **계획 단계 vs 실행 단계를 분리한다** — 이 코드는 설정할 때 도는가, 일할 때 도는가? (compile time vs runtime, 쿼리 플래닝 vs 실행에도 그대로 적용된다)
- **값 vs 값을 만드는 레시피(eager vs lazy)** — 지금 확정할까, 계산 방법만 넘길까? (`Provider`, `Future`/`Promise`, `Stream`이 같은 구조다)
- **캐시 가능 = 선언된 입력의 순수 함수** — 이 결과가 무엇에 의존하는지 시스템이 알고 있는가? 숨은 입력은 없는가?
- **직렬화 경계** — 이 상태는 저장했다 복원할 수 있는 데이터인가, 아니면 프로세스에 묶인 살아있는 자원인가?
- **못 고치는 것은 격리한다** — 전부 아니면 전무가 아니라, 문제만 도려내고 이득은 지킨다.
- **준비와 활성화를 나눈다** — 동작을 바꾸는 변경과 스위치를 켜는 변경을 한 커밋에 섞지 않는다. 나중에 원인을 격리하기 위해서다.
- **임시방편엔 만료 조건을 남긴다** — `// remove when X fixed`, 이슈 링크.

한 문장으로 꿰면 이렇다.

> 시스템을 계획/실행으로 나눠 보고, 값을 지금 vs 나중으로 구분하며, 무엇이든 선언된 입력의 함수로 만들어 캐시 가능하게 하고, 그러려면 상태가 저장 가능한 데이터여야 하며, 못 고치는 건 격리하고, 전환은 준비와 활성화로 쪼개며, 임시방편엔 만료 조건을 남긴다.

Gradle Configuration Cache 이야기는 이 사고구조의 한 가지 구체적 사례일 뿐이다. 같은 렌즈로 캐싱, 비동기, 마이그레이션 문제를 만나면 똑같이 풀 수 있다.
