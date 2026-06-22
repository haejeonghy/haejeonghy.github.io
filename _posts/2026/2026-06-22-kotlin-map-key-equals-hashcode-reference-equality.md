---
layout: post
title: Kotlin Map Key와 equals, hashCode, 참조 동등성 정리
summary: 일반 클래스를 Kotlin Map의 key로 사용할 때 equals와 hashCode가 조회 결과와 API 의미에 어떤 영향을 주는지 정리합니다.
date: 2026-06-22 18:52:43 +0900
updated: 2026-06-22 18:52:43 +0900
tag: kotlin jvm map equals hashcode
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. PR 리뷰에서 시작된 질문

다음과 같은 반환 타입을 가진 함수를 리뷰한다고 해보자.

```kotlin
fun run(
    assets: List<SyncAsset>,
    trigger: SyncTrigger,
): Map<SyncAsset, Map<DetailType, SlotResult>>
```

처음에는 `SyncAsset`이 Map의 key이므로 같은 자산을 나타내는 객체라면 결과를 조회할 수 있을 것처럼 보인다.

하지만 실제 동작은 `SyncAsset`의 `equals`와 `hashCode` 구현에 따라 달라진다. `SyncAsset`이 일반 클래스이고 두 메서드를 직접 재정의하지 않았다면, 이 Map은 자산 식별자가 아니라 객체 인스턴스를 기준으로 key를 구분한다.

이번 글에서는 이 동작이 왜 발생하는지와 반환 타입이 어떤 API 의미를 가지게 되는지 정리한다.

## 2. 일반 클래스는 기본적으로 값 동등성을 제공하지 않는다

Kotlin의 일반 클래스는 `equals`와 `hashCode`를 직접 재정의하지 않으면 `Any`의 기본 구현을 사용한다. JVM에서 이 기본 `equals`는 객체의 프로퍼티 값을 비교하지 않고 같은 인스턴스인지 비교한다.

```kotlin
class SyncAsset(
    val id: Long,
)

val a = SyncAsset(1)
val b = SyncAsset(1)

println(a == b)  // false
println(a === b) // false
```

Kotlin의 `==`는 구조적 동등성 비교이며 내부적으로 `equals`를 호출한다. 반면 `===`는 두 참조가 같은 객체를 가리키는지 직접 비교한다.

이 예제에서 `a`와 `b`의 `id`는 같지만 서로 다른 인스턴스다. `SyncAsset`이 `equals`를 재정의하지 않았으므로 `a == b`와 `a === b`가 모두 `false`가 된다.

즉, 일반 클래스의 프로퍼티 값이 같다고 해서 자동으로 같은 객체로 취급되는 것은 아니다.

## 3. Map은 hashCode와 equals로 key를 찾는다

Map은 일반적으로 다음 과정으로 key를 찾는다.

1. `hashCode`를 사용해 key가 있을 만한 위치를 찾는다.
2. 해당 위치의 후보들과 `equals`를 비교해 같은 key인지 판단한다.

따라서 Map의 key 동작은 key 타입의 `equals`와 `hashCode` 계약에 영향을 받는다.

`SyncAsset`이 두 메서드를 재정의하지 않았다면 객체의 값이 아니라 인스턴스를 기준으로 동작한다.

```kotlin
val result = mapOf(
    a to "slot-success"
)

println(result[a]) // slot-success
println(result[b]) // null
```

`result[a]`는 Map에 넣었던 동일한 인스턴스로 조회하므로 값을 얻는다. `result[b]`는 `id`가 같더라도 다른 인스턴스이므로 조회에 실패한다.

## 4. 같은 id를 가진 객체도 서로 다른 key가 된다

같은 `id`를 가진 두 객체를 Map에 넣어도 결과는 덮어써지지 않는다.

```kotlin
val asset1 = SyncAsset(1)
val asset2 = SyncAsset(1)

val map = mutableMapOf<SyncAsset, String>()
map[asset1] = "first"
map[asset2] = "second"

println(map.size)          // 2
println(map[asset1])       // first
println(map[asset2])       // second
println(map[SyncAsset(1)]) // null
```

`asset1`과 `asset2`는 서로 다른 key다. 조회 시점에 새로 만든 `SyncAsset(1)`도 기존 key와 다른 인스턴스이므로 값을 찾지 못한다.

여기서 중요한 것은 `id`가 같은지가 아니다. Map이 같은 key라고 판단할 수 있도록 `equals`와 `hashCode`가 정의되어 있는지가 중요하다.

## 5. hashCode 충돌은 이 문제의 핵심이 아니다

서로 다른 객체가 같은 해시 값을 반환하는 해시 충돌은 발생할 수 있다. 하지만 해시 값이 같다고 해서 Map이 두 객체를 같은 key로 취급하는 것은 아니다.

Map은 `hashCode`로 후보를 좁힌 뒤 `equals`로 최종 확인한다.

```text
hashCode가 다름 → 다른 후보 위치
hashCode가 같음 → equals로 같은 key인지 최종 확인
```

따라서 `asset1`과 `asset2`의 해시 값이 우연히 같더라도 기본 `equals`가 `false`라면 서로 다른 key로 남는다.

이 사례의 핵심은 해시 충돌이 아니라 `SyncAsset`이 값 동등성을 정의하지 않았다는 점이다.

## 6. 반환 타입이 표현하는 실제 의미

다시 `run` 함수의 시그니처를 보자.

```kotlin
fun run(
    assets: List<SyncAsset>,
    trigger: SyncTrigger,
): Map<SyncAsset, Map<DetailType, SlotResult>>
```

함수 내부에서 `associateWith`를 사용하면 전달받은 리스트의 각 요소가 그대로 key가 된다.

```kotlin
return assets.associateWith { asset ->
    runSlots(asset, trigger)
}
```

호출자가 `run`에 넘긴 동일한 `SyncAsset` 인스턴스를 보관하고 있다면 결과를 조회할 수 있다.

```kotlin
val asset = SyncAsset(1)
val result = run(listOf(asset), trigger)

result[asset] // 조회 가능
```

하지만 같은 자산 식별자를 가진 새 객체로는 조회할 수 없다.

```kotlin
result[SyncAsset(1)] // null
```

따라서 이 API의 실제 의미는 "자산 식별자별 실행 결과"가 아니라 "`run`에 전달된 `SyncAsset` 인스턴스별 실행 결과"에 가깝다.

코드 작성자는 동일 인스턴스를 계속 사용한다는 전제를 알고 있을 수 있다. 그러나 반환 타입만 보는 호출자는 같은 자산을 나타내는 객체라면 key로 조회할 수 있다고 해석할 가능성이 있다. PR 리뷰에서 확인해야 할 지점도 현재 코드가 당장 동작하는지가 아니라 이 API의 동등성 기준이 충분히 드러나는지다.

## 7. 의도에 따라 해결 방법이 달라진다

### 7.1 객체 인스턴스가 기준이라면 문서화한다

동일 인스턴스로만 결과를 조회하는 것이 의도라면 현재 타입을 유지할 수 있다. 대신 KDoc에 제약을 명시해야 한다.

```kotlin
/**
 * 반환 Map은 assets에 전달된 동일한 SyncAsset 인스턴스로 조회해야 한다.
 */
fun run(...): Map<SyncAsset, Map<DetailType, SlotResult>>
```

이 방식은 구현 변경이 가장 작지만, 호출자가 입력 객체를 계속 보관해야 한다는 결합이 남는다.

### 7.2 자산 식별자가 기준이라면 key 타입을 바꾼다

호출자가 자산 식별자로 결과를 조회해야 한다면 반환 타입에 그 의도를 직접 드러내는 편이 명확하다.

```kotlin
fun run(...): Map<Long, Map<DetailType, SlotResult>>
```

원시 타입 사용을 피하고 싶다면 별도의 식별자 타입을 사용할 수도 있다.

```kotlin
@JvmInline
value class AssetId(val value: Long)
```

```kotlin
fun run(...): Map<AssetId, Map<DetailType, SlotResult>>
```

이 방식은 Map의 의미를 "자산 식별자별 결과"로 분명하게 만든다.

### 7.3 SyncAsset이 값 객체라면 값 동등성을 정의한다

`SyncAsset` 자체가 같은 프로퍼티 값으로 동등성을 판단해야 하는 값 객체라면 `data class`가 자연스럽다.

```kotlin
data class SyncAsset(
    val id: Long,
)
```

또는 도메인 규칙에 맞게 `equals`와 `hashCode`를 직접 구현할 수 있다.

이 경우에는 어떤 필드가 객체의 동등성을 결정하는지 먼저 정해야 한다. 단순히 Map 조회를 편하게 만들기 위해 도메인 객체 전체의 동등성 규칙을 바꾸면 다른 컬렉션과 비교 로직에도 영향을 줄 수 있다.

## 8. equals와 hashCode는 함께 설계해야 한다

값 동등성을 직접 구현한다면 `equals`만 바꾸고 `hashCode`를 그대로 두면 안 된다.

동등한 두 객체는 반드시 같은 해시 값을 반환해야 한다.

```text
a == b 이면 a.hashCode() == b.hashCode()
```

이 계약이 깨지면 `equals`로는 같은 객체인데 Map이나 Set에서는 찾지 못하는 문제가 생길 수 있다. `data class`는 주 생성자의 프로퍼티를 기준으로 두 메서드를 함께 생성하므로 일반적인 값 객체에 적합하다.

또한 Map에 key를 넣은 뒤 동등성이나 해시 계산에 사용되는 값을 변경해서는 안 된다. 삽입 당시와 조회 당시의 해시 값이 달라지면 같은 인스턴스를 가지고도 정상적으로 조회하지 못할 수 있다.

## 9. Map key로 도메인 객체를 쓸 때 확인할 것

- 이 객체는 엔티티인가, 값 객체인가?
- 같은 key를 판단하는 기준은 객체 인스턴스인가, 식별자인가, 전체 값인가?
- `equals`와 `hashCode`가 의도한 기준으로 함께 구현되어 있는가?
- 호출자가 원본 인스턴스가 아닌 새 객체로 조회할 가능성이 있는가?
- key의 동등성이나 해시 값에 사용되는 필드가 삽입 후 변경될 수 있는가?
- `Map<Long, ...>` 또는 `Map<AssetId, ...>`가 API 의미를 더 명확하게 표현하지 않는가?
- 인스턴스 기반 조회가 의도라면 그 제약이 KDoc에 명시되어 있는가?

## 10. 정리

Kotlin에서 `==`는 `equals`를 호출하고 `===`는 참조 동등성을 비교한다. 일반 클래스가 `equals`와 `hashCode`를 재정의하지 않으면 Map의 key도 사실상 객체 인스턴스를 기준으로 구분된다.

따라서 `Map<SyncAsset, ...>`이라는 타입만 보고 자산 식별자 기준의 결과 Map이라고 단정할 수 없다. 실제 의미는 `SyncAsset`의 동등성 구현이 결정한다.

PR 리뷰에서는 현재 호출 코드가 같은 인스턴스를 사용해서 동작하는지만 확인하는 데 그치지 않아야 한다. 미래의 호출자가 반환 타입을 어떻게 해석할지, 그리고 API가 의도한 key 기준을 타입이나 문서로 충분히 표현하는지도 함께 확인해야 한다.
