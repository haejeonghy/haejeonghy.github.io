---
layout: post
title: Kotlin, Spring Boot, JPA, H2, Hibernate, static, main을 한 번에 다시 정리하기
summary: Kotlin과 Spring Boot로 JPA를 공부하면서 헷갈리기 쉬운 static, main 함수, H2, Hibernate, EntityManager, ddl-auto, EntityManagerFactory 관리 방식을 한 흐름으로 정리합니다.
date: 2026-06-06 14:40:00 +0900
updated: 2026-06-06 14:33:29 +0900
tag: kotlin spring boot jpa hibernate h2 java static main
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 왜 이 개념들이 한 번에 헷갈렸는가

Kotlin과 Spring Boot로 JPA를 공부하다 보면 의외로 서로 다른 층위의 개념이 동시에 튀어나온다.

- `static`
- `main`
- `H2`
- `Hibernate`
- `JPA`
- `Spring Boot`

겉으로 보면 전부 애플리케이션 실행과 데이터 저장에 관련된 것 같지만, 실제 역할은 꽤 다르다.

- `static`, `main`
  JVM이 프로그램을 어떻게 시작하는지와 관련된 개념
- `H2`
  실제 데이터를 저장하는 데이터베이스
- `Hibernate`
  객체와 데이터베이스를 연결해 주는 JPA 구현체
- `Spring Boot`
  위 요소들을 애플리케이션 안에서 자동 구성하고 실행하게 해 주는 프레임워크

이 글은 이 개념들을 한 흐름으로 다시 정리한 기록이다.

## 2. `static`은 미리 리소스를 깔아두는 기능이라기보다 클래스 소속 멤버다

처음에는 `static`을 "미리 리소스를 마련해서 할당해 두는 것"으로 이해하기 쉽다. 완전히 틀린 방향은 아니지만 핵심은 아니다.

`static`의 핵심은 다음이다.

- 인스턴스가 아니라 클래스에 속한다
- 객체를 만들지 않아도 접근할 수 있다
- 객체를 여러 개 만들어도 `static` 멤버는 하나를 공유한다

예를 들어 Java에서는 아래와 같이 생각할 수 있다.

```java
class Example {
    static int count = 0;
    int value = 0;
}
```

- `count`
  클래스 전체가 공유하는 값
- `value`
  객체마다 따로 생기는 값

즉 `static`은 "객체가 생기기 전에 사용할 수 있는 클래스 수준의 값 또는 기능"으로 이해하는 편이 더 정확하다.

### 2.1 붕어빵 비유로 다시 정리하기

- 클래스
  붕어빵 틀
- 인스턴스
  틀로 찍어낸 붕어빵 하나
- `static`
  붕어빵 하나하나에 붙은 기능이 아니라 붕어빵 틀에 붙은 공용 장치

이 비유로 보면 `static`은 붕어빵이 아직 하나도 없어도 틀 쪽에서 바로 접근할 수 있는 기능이다.

## 3. 왜 `main`은 일반 클래스 멤버가 아니라 `static`이어야 하는가

JVM이 프로그램을 시작할 때는 아직 객체를 만들지 않았다. 그런데도 시작점을 바로 호출해야 한다.

그래서 Java는 아래 형태를 요구한다.

```java
public static void main(String[] args)
```

핵심은 `main`이 특정 객체의 기능이면 안 된다는 점이다. 객체가 아직 없기 때문이다.

즉 `main`은 아래처럼 이해할 수 있다.

- 붕어빵이 만들어진 뒤에만 사용할 수 있는 기능이 아니라
- 붕어빵 틀을 세팅하는 단계에서 바로 누를 수 있는 시작 버튼

### 3.1 왜 Kotlin은 파일 밖에 `main`이 보이는가

Java는 모든 함수를 클래스 안에 둬야 한다. 반면 Kotlin은 top-level function을 허용한다.

예를 들어 Kotlin에서는 이렇게 쓸 수 있다.

```kotlin
fun main(args: Array<String>) {
}
```

하지만 JVM은 여전히 클래스 기반으로만 실행한다. 그래서 Kotlin 컴파일러가 내부적으로는 이것을 클래스 안의 `static main` 형태로 변환해 준다.

즉 소스 코드가 달라 보일 뿐, JVM 관점에서는 여전히 "클래스 수준 시작점"이다.

### 3.2 왜 `class JpaMain { fun main() }`는 실행되지 않는가

이 코드는 일반 클래스의 인스턴스 메서드일 뿐이다.

```kotlin
class JpaMain {
    fun main(args: Array<String>) {
    }
}
```

이 경우 `main`은 객체에 속해 있기 때문에 JVM이 시작점으로 사용할 수 없다.

실행 가능한 형태는 보통 아래 둘 중 하나다.

```kotlin
fun main(args: Array<String>) {
}
```

```kotlin
object JpaMain {
    @JvmStatic
    fun main(args: Array<String>) {
    }
}
```

## 4. `H2`와 `Hibernate`는 서로 다른 역할을 한다

JPA를 공부할 때 가장 자주 섞여서 들리는 두 단어가 `H2`와 `Hibernate`다.

### 4.1 `H2`는 데이터베이스다

`H2`는 실제로 데이터를 저장하는 데이터베이스다.

- 테이블을 만든다
- SQL을 실행한다
- 데이터를 저장하고 읽는다

예를 들어 아래 설정은 H2 인메모리 데이터베이스를 뜻한다.

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:jpaplayground
```

여기서 중요한 점은 `mem`이라는 단어다. 이는 디스크 파일이 아니라 메모리 기반 데이터베이스라는 의미다.

### 4.2 `Hibernate`는 JPA 구현체다

`Hibernate`는 데이터베이스 자체가 아니다. JPA 표준을 실제로 동작하게 만드는 구현체다.

역할은 아래와 같다.

- 엔티티를 읽는다
- SQL을 만든다
- DB에 맞는 dialect를 선택한다
- JDBC를 통해 SQL을 실행한다

즉 관계를 단순화하면 아래와 같다.

```text
애플리케이션 코드
  -> JPA API
  -> Hibernate
  -> JDBC
  -> H2
```

정리하면:

- `H2`
  데이터를 저장하는 실제 DB
- `Hibernate`
  객체를 SQL로 바꿔 DB에 전달하는 JPA 구현체

## 5. 메모리 DB인데 왜 `member` 테이블이 재시작 후에도 다시 보였는가

처음에는 "메모리 DB면 재시작하면 다 사라져야 하는데 왜 테이블이 남아 있지?"라는 의문이 생긴다.

여기서 핵심은 "남아 있는 것처럼 보인다"는 점이다.

만약 설정이 아래와 같다면:

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: create-drop
```

애플리케이션이 다시 시작될 때 Hibernate가 엔티티를 읽고 테이블을 다시 만든다.

즉 실제 흐름은 이렇다.

1. JVM 종료
2. 인메모리 H2 DB도 사라짐
3. 애플리케이션 재시작
4. Hibernate가 엔티티를 읽음
5. `member` 테이블을 다시 생성

그래서 테이블이 "보존된 것처럼" 보이지만, 사실은 새로 만들어진 것이다.

## 6. Hibernate는 무엇을 보고 테이블을 만드는가

Hibernate는 JPA 엔티티 메타데이터를 읽고 테이블 스키마를 추론한다.

대표적으로 아래 어노테이션을 읽는다.

- `@Entity`
- `@Table`
- `@Id`
- `@Column`
- `@OneToMany`
- `@ManyToOne`

예를 들어 아래 엔티티가 있다면:

```kotlin
@Entity
@Table(name = "member")
data class Member(
    @Id
    @Column(name = "id")
    val id: Long,

    @Column(name = "name")
    val name: String,

    val age: Int,
)
```

Hibernate는 이를 보고 `member` 테이블과 `id`, `name`, `age` 컬럼 구성을 해석한다.

### 6.1 실제 DB를 별도로 관리한다면 `ddl-auto`를 조절해야 한다

학습용 로컬 환경에서는 `create`나 `create-drop`이 편하다.

하지만 운영처럼 별도 DB를 관리하는 환경에서는 이 설정이 위험할 수 있다.

- `create`
  시작 시 새로 생성
- `create-drop`
  시작 시 생성, 종료 시 삭제
- `update`
  엔티티 기준으로 변경 시도
- `validate`
  엔티티와 DB가 맞는지 검사만 함
- `none`
  아무것도 하지 않음

보통은 아래처럼 생각하면 된다.

- 학습/로컬
  `create`, `create-drop`
- 개발 공유 DB
  `update`, `validate`
- 운영
  `validate`, `none`

운영에서는 스키마 변경을 Hibernate 자동 DDL보다 마이그레이션 도구로 관리하는 편이 안전하다.

## 7. Kotlin + Spring Boot에서 순수 JPA 예제를 그대로 쓰면 어색해지는 이유

JPA 예제 책에서는 보통 아래 같은 코드를 먼저 보여준다.

```kotlin
val emf = Persistence.createEntityManagerFactory("jpabook")
val em = emf.createEntityManager()
val tx = em.transaction
```

이 방식은 "순수 JPA"를 설명할 때는 적절하다. 하지만 Spring Boot 프로젝트 안에서는 보통 이렇게 하지 않는다.

왜냐하면 Spring Boot가 이미 아래를 관리하기 때문이다.

- `DataSource`
- `EntityManagerFactory`
- `EntityManager`
- 트랜잭션

즉 Spring Boot 환경에서는 직접 `Persistence.createEntityManagerFactory(...)`를 만들기보다 Spring이 생성한 `EntityManager`를 주입받아 쓰는 편이 맞다.

## 8. `EntityManager`는 정확히 무엇인가

`EntityManager`는 JPA에서 엔티티를 실제로 다루는 핵심 인터페이스다.

쉽게 말하면 아래 작업을 담당하는 "JPA 작업 창구"라고 보면 된다.

- 엔티티 저장
- 엔티티 조회
- 엔티티 수정 추적
- 엔티티 삭제
- JPQL 실행
- 영속성 컨텍스트 관리

예를 들어 아래 메서드가 대표적이다.

- `persist(...)`
  엔티티 저장
- `find(...)`
  PK로 엔티티 조회
- `remove(...)`
  엔티티 삭제
- `createQuery(...)`
  JPQL 생성

예를 들어 이런 식으로 사용할 수 있다.

```kotlin
val member = Member(1L, "kim", 20)
entityManager.persist(member)

val foundMember = entityManager.find(Member::class.java, 1L)
```

즉 `EntityManager`는 "엔티티를 DB에 저장하는 객체"라기보다, 엔티티를 영속성 컨텍스트 안에서 관리하고 그 결과를 적절한 시점에 DB에 반영하게 하는 진입점에 가깝다.

### 8.1 Spring Boot에서는 왜 `EntityManager`를 직접 만들지 않는가

Spring Boot는 이미 JPA 관련 인프라를 구성해 준다.

- `DataSource`
- `EntityManagerFactory`
- 트랜잭션
- 필요한 시점의 `EntityManager`

그래서 애플리케이션 코드는 보통 `EntityManager`를 직접 생성하지 않고 주입받아 사용한다.

이 방식의 장점은 아래와 같다.

- 생성/반납 라이프사이클을 직접 관리하지 않아도 된다
- 트랜잭션과 자연스럽게 연결된다
- Spring이 요청 단위 또는 트랜잭션 단위로 적절한 `EntityManager`를 연결해 준다

### 8.2 Spring은 `EntityManager`를 어디서 만들어 주입하는가

Spring Boot에서 `spring-boot-starter-data-jpa`를 추가하면 JPA 자동 설정이 켜진다. 이 자동 설정은 내부적으로 `EntityManagerFactory`를 구성하고, 애플리케이션 코드에는 `EntityManager`를 바로 사용할 수 있게 연결해 준다.

개념적으로는 아래 흐름으로 보면 된다.

```text
DataSource
  -> EntityManagerFactory 생성
  -> Spring 관리용 EntityManager 프록시 준비
  -> 서비스/리포지토리에 주입
```

여기서 중요한 점은 애플리케이션 코드에 주입되는 `EntityManager`가 항상 "지금 막 생성된 순수 객체" 그 자체는 아니라는 점이다.

보통은 아래처럼 이해하면 된다.

- Spring Boot가 `EntityManagerFactory`를 bean으로 등록한다
- Spring은 그 팩토리를 바탕으로 `EntityManager` 프록시를 만든다
- 실제 메서드 호출 시점에 현재 트랜잭션에 연결된 진짜 `EntityManager`로 위임한다

즉 내가 코드에서 받는 `EntityManager`는 "현재 트랜잭션에 맞는 실제 `EntityManager`를 찾아 연결해 주는 창구"에 가깝다.

그래서 서비스에서는 아래처럼 주입받아도 된다.

```kotlin
@Service
class MemberService(
    private val entityManager: EntityManager
)
```

이때 개발자가 직접 아래 코드를 쓸 필요는 없다.

```kotlin
val emf = Persistence.createEntityManagerFactory("jpabook")
val em = emf.createEntityManager()
```

왜냐하면 이 생명주기와 연결 관계를 Spring이 대신 관리하기 때문이다.

## 9. `@Transactional`이 시작될 때 실제 `EntityManager`는 어떻게 연결되는가

이제 한 단계 더 들어가 보면, 주입된 `EntityManager` 프록시가 실제로 언제 진짜 작업 객체와 연결되는지가 궁금해진다.

핵심은 `@Transactional`이다.

서비스 메서드에 `@Transactional`이 붙어 있으면 Spring은 그 메서드 호출 앞뒤에 트랜잭션 처리를 끼워 넣는다. 이 시점에 실제 `EntityManager`가 현재 실행 흐름에 연결된다.

흐름은 대략 아래와 같다.

```text
서비스 메서드 호출
  -> @Transactional 프록시 개입
  -> 트랜잭션 시작
  -> 실제 EntityManager 생성 또는 획득
  -> 현재 스레드에 바인딩
  -> 주입된 EntityManager 프록시가 실제 EntityManager로 위임
  -> commit 또는 rollback
  -> 바인딩 해제
```

예를 들어 이런 코드가 있다고 하자.

```kotlin
@Service
class MemberService(
    private val entityManager: EntityManager
) {
    @Transactional
    fun save() {
        val member = Member(1L, "kim", 20)
        entityManager.persist(member)
    }
}
```

여기서 `entityManager.persist(...)`를 호출한다고 해서 필드에 들어온 객체가 곧바로 실제 JPA 구현체 인스턴스라는 뜻은 아니다.

실제로는 다음처럼 동작한다고 이해하면 된다.

1. `@Transactional` 프록시가 먼저 메서드 호출을 감싼다
2. 트랜잭션을 시작한다
3. 그 트랜잭션에 연결된 실제 `EntityManager`를 준비한다
4. `entityManager.persist(...)` 호출 시, 주입된 프록시가 현재 트랜잭션에 연결된 실제 `EntityManager`로 위임한다
5. 메서드가 끝나면 commit 또는 rollback 한다

즉 내가 코드에서 받는 `EntityManager`는 "항상 같은 실체 객체"라기보다, "현재 트랜잭션에 맞는 실제 `EntityManager`를 찾아 연결해 주는 진입점"이라고 보는 편이 정확하다.

### 9.1 왜 이 구조가 중요한가

이 구조 덕분에 같은 트랜잭션 안에서는 보통 같은 `EntityManager`와 같은 영속성 컨텍스트를 사용하게 된다.

그래서 아래 같은 JPA 동작이 자연스럽게 성립한다.

- 1차 캐시
- 변경 감지
- 쓰기 지연
- 지연 로딩

즉 `@Transactional`은 단순히 "DB commit 하게 해 주는 어노테이션"이 아니라, JPA가 하나의 작업 단위처럼 동작할 수 있게 실제 `EntityManager`를 묶어 주는 경계라고 볼 수 있다.

### 9.2 그런데 왜 그냥 실제 `EntityManager`를 바로 필드에 넣지 않는가

여기서 자연스럽게 드는 의문이 있다.

"어차피 `@Transactional` 시점에 실제 `EntityManager`를 준비한다면, 그냥 그 실제 객체를 서비스 필드에 넣어두면 되는 것 아닌가?"

하지만 이 방식은 Spring bean의 수명주기와 `EntityManager`의 성격이 맞지 않는다.

보통 서비스 bean은 싱글톤이다.

```kotlin
@Service
class MemberService(
    private val entityManager: EntityManager
)
```

이 서비스 객체는 애플리케이션 전체에서 하나만 만들어져 오래 살아 있는 경우가 많다. 반면 `EntityManager`는 보통 호출 시점의 트랜잭션, 현재 스레드, 현재 작업 단위에 맞춰 달라지는 객체다.

즉 실제 `EntityManager`를 서비스 필드에 고정해서 넣어버리면 아래 같은 문제가 생긴다.

- 여러 요청이 같은 `EntityManager`를 공유할 수 있다
- 트랜잭션 A와 트랜잭션 B가 섞일 수 있다
- 이미 종료된 `EntityManager`를 계속 참조할 수 있다
- 어떤 호출은 트랜잭션 안이고, 어떤 호출은 트랜잭션 밖일 수 있는데 이를 유연하게 대응하기 어렵다

그래서 Spring은 서비스 필드에 "진짜 작업 객체"를 고정 주입하지 않고 프록시를 넣는다.

이 프록시는 메서드 호출 시점마다 아래 작업을 한다.

- 지금 트랜잭션이 있는지 확인
- 현재 실행 흐름에 연결된 실제 `EntityManager`를 찾음
- 그 객체로 호출을 위임

즉 서비스 입장에서는 같은 필드처럼 보이지만, 실제로는 매번 현재 상황에 맞는 진짜 `EntityManager`를 찾아 연결해 주는 창구를 들고 있는 셈이다.

이렇게 보면 프록시는 부가 기능이 아니라, `EntityManager`를 Spring bean 구조 안에서 안전하게 쓰기 위한 필수 장치에 가깝다.

## 10. `EntityManager`에 왜 `save()`가 없고, 조회한 엔티티는 값만 바꿔도 되는가

JPA를 처음 볼 때는 아래 코드가 자연스럽게 떠오르기 쉽다.

```kotlin
foundMember.age = 40
entityManager.save(foundMember)
```

하지만 `EntityManager`에는 `save()` 메서드가 없다.

이유는 `save()`가 JPA 표준 `EntityManager` API가 아니라, Spring Data JPA의 `JpaRepository` 같은 상위 추상화에서 제공하는 메서드이기 때문이다.

`EntityManager` 쪽에서 대표적으로 쓰는 메서드는 아래와 같다.

- `persist(...)`
- `find(...)`
- `merge(...)`
- `remove(...)`

즉 `EntityManager`를 직접 다룰 때는 `save()`를 기대하기보다, 엔티티가 지금 어떤 상태인지와 JPA가 변경을 어떻게 반영하는지를 이해하는 편이 중요하다.

### 10.1 조회한 엔티티는 왜 값만 바꿔도 반영되는가

예를 들어 아래 코드를 보자.

```kotlin
@Transactional
fun update() {
    val foundMember = entityManager.find(Member::class.java, 1L)
    foundMember.age = 40
}
```

이 코드에는 `save()`도 없고 `update()` SQL도 직접 쓰지 않는다. 그런데도 트랜잭션이 끝날 때 DB 반영이 일어날 수 있다.

이유는 `find()`로 조회한 엔티티가 영속성 컨텍스트가 관리하는 영속 상태가 되기 때문이다.

Spring과 Hibernate는 이 엔티티의 변경을 추적하다가 트랜잭션이 끝나는 시점에 변경 감지(dirty checking)를 통해 필요한 SQL을 만든다.

즉 흐름은 대략 아래와 같다.

```text
find()로 조회
  -> 영속 상태 엔티티가 됨
  -> 필드 값 변경
  -> 트랜잭션 종료 시점에 변경 감지
  -> update SQL 실행
```

그래서 영속 상태 엔티티를 수정할 때는 "다시 저장"보다 "상태를 변경"하는 것이 핵심이다.

### 10.2 그럼 `merge()`는 언제 쓰는가

`merge()`는 보통 이미 영속성 컨텍스트 밖으로 나온 준영속(detached) 엔티티 상태를 다시 반영하고 싶을 때 사용한다.

예를 들어 이런 식이다.

```kotlin
val detachedMember = Member(1L, "kim", 40)
entityManager.merge(detachedMember)
```

하지만 JPA를 공부하는 초반 단계에서는 업데이트를 아래처럼 이해하는 편이 더 단순하고 중요하다.

1. 엔티티를 조회한다
2. 조회한 객체의 필드를 바꾼다
3. 트랜잭션이 끝난다
4. Hibernate가 변경 감지를 통해 반영한다

즉 JPA 업데이트의 핵심은 `save()` 호출이 아니라, 영속성 컨텍스트가 관리 중인 엔티티의 상태 변경이다.

## 11. JPQL과 SQL의 가장 큰 차이는 무엇인가

JPA를 공부하다 보면 결국 JPQL도 같이 마주치게 된다. 이때 가장 먼저 잡아야 할 차이는 "무엇을 기준으로 조회하느냐"다.

- SQL
  테이블과 컬럼 기준
- JPQL
  엔티티와 엔티티 필드 기준

예를 들어 SQL은 데이터베이스 스키마를 직접 바라본다.

```sql
select id, name
from member
where age > 20
```

반면 JPQL은 객체 모델을 기준으로 작성한다.

```jpql
select m
from Member m
where m.age > 20
```

여기서 중요한 차이는 아래와 같다.

- SQL의 `member`
  실제 테이블 이름
- JPQL의 `Member`
  엔티티 클래스 이름
- SQL의 `age`
  컬럼 이름
- JPQL의 `m.age`
  엔티티 필드 접근

즉 SQL은 데이터베이스에 직접 말하는 언어이고, JPQL은 엔티티 모델 기준으로 질의하면 Hibernate 같은 JPA 구현체가 이를 SQL로 번역해 실행하는 언어다.

흐름은 대략 아래처럼 볼 수 있다.

```text
JPQL 작성
  -> JPA/Hibernate가 해석
  -> DB에 맞는 SQL 생성
  -> 실행
```

그래서 가장 큰 차이를 한 줄로 요약하면 이렇다.

SQL은 데이터베이스 스키마를 대상으로 하고, JPQL은 자바/코틀린 엔티티 모델을 대상으로 한다.

## 12. Kotlin + Spring Boot 식으로 JPA를 쓰려면 어떻게 해야 하는가

`main()`에서는 애플리케이션만 띄운다.

```kotlin
@SpringBootApplication
class JpaMain

fun main(args: Array<String>) {
    runApplication<JpaMain>(*args)
}
```

그리고 실제 JPA 작업은 Spring Bean 안에서 수행한다.

예를 들어 서비스에서 `EntityManager`를 주입받아 사용한다.

```kotlin
@Service
class MemberInitService(
    private val entityManager: EntityManager
) {
    @Transactional
    fun init() {
        val member = Member(
            id = 1L,
            name = "kim",
            age = 20
        )

        entityManager.persist(member)
    }
}
```

앱 시작 시 한 번 실행하고 싶다면 `CommandLineRunner`를 연결할 수 있다.

```kotlin
@Configuration
class JpaRunnerConfig {
    @Bean
    fun jpaRunner(memberInitService: MemberInitService) = CommandLineRunner {
        memberInitService.init()
    }
}
```

이 방식의 장점은 다음과 같다.

- `EntityManagerFactory`를 직접 만들 필요가 없다
- 트랜잭션을 직접 열고 닫지 않아도 된다
- Spring Boot가 관리하는 라이프사이클 안에서 JPA를 사용할 수 있다

## 13. 이번에 다시 정리하면서 잡힌 핵심

한 번에 다시 요약하면 아래와 같다.

- `static`
  객체가 아니라 클래스에 속한 값 또는 기능
- `main`
  객체 생성 전에도 호출 가능해야 하므로 클래스 수준 시작점이어야 함
- Kotlin의 top-level `main`
  소스 문법은 달라도 JVM에서는 결국 `static main`으로 변환됨
- `H2`
  실제 데이터를 저장하는 데이터베이스
- `Hibernate`
  JPA 구현체로서 엔티티를 읽고 SQL을 만들어 DB에 전달함
- `EntityManager`
  엔티티를 다루는 JPA의 핵심 작업 인터페이스
- `@Transactional`
  현재 실행 흐름에 실제 `EntityManager`와 영속성 컨텍스트를 묶어 주는 작업 경계
- 변경 감지
  영속 상태 엔티티는 필드 값만 바꿔도 트랜잭션 종료 시점에 DB 반영 가능
- JPQL
  테이블이 아니라 엔티티와 엔티티 필드를 기준으로 쓰는 객체 중심 질의 언어
- `ddl-auto`
  Hibernate가 스키마를 어떻게 다룰지 결정하는 설정
- Spring Boot 환경
  `EntityManagerFactory`를 직접 만들지 말고 Spring이 관리하는 `EntityManager`와 `@Transactional`을 사용

JPA를 처음 공부할 때는 이 개념들이 전부 비슷한 위치에 있다고 느껴진다. 하지만 실행 시작점, 언어 개념, ORM, DB, 프레임워크 자동 구성을 분리해서 보면 훨씬 덜 헷갈린다.
