---
layout: post
title: Spring Boot JPA에서 camelCase 필드가 왜 snake_case 컬럼으로 생성될까
summary: Spring Boot와 Hibernate를 함께 쓸 때 modifiedTime 같은 엔티티 필드가 왜 modified_time 컬럼으로 생성되는지, implicit naming strategy와 physical naming strategy 차이까지 정리합니다.
date: 2026-06-07 16:20:00 +0900
updated: 2026-06-07 16:20:00 +0900
tag: spring boot jpa hibernate naming strategy kotlin
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 문제 상황

JPA 엔티티를 작성하다 보면 아래처럼 필드명은 camelCase인데, 실제 생성된 컬럼은 snake_case인 경우가 있다.

```kotlin
@Entity
@Table(name = "member")
data class Member(
    @Id
    @Column(name = "id")
    val id: Long,

    @Column(name = "name")
    val name: String,

    var age: Int,

    @Enumerated(EnumType.STRING)
    var role: RoleType,

    var createdTime: LocalDateTime = LocalDateTime.now(),

    var modifiedTime: LocalDateTime = LocalDateTime.now()
)
```

예를 들어 `modifiedTime`으로 작성했는데 DDL을 보면 `modified_time`으로 생성된다.

처음 보면 "Hibernate 기본 정책이 snake_case인가?"라는 질문이 자연스럽게 나온다.

결론부터 말하면, 이 동작은 보통 **순수 Hibernate 자체의 단순 기본값**이라기보다 **Spring Boot가 Hibernate에 적용하는 기본 naming strategy** 때문에 발생한다.

## 2. 어디서 `modifiedTime -> modified_time` 변환이 일어나는가

핵심은 두 단계다.

1. 이름을 먼저 정한다.
2. 그 이름을 실제 DB 식별자 형태로 변환한다.

Spring Boot와 Hibernate 조합에서는 이 과정에 naming strategy가 개입한다.

- `implicit naming strategy`
  이름을 명시하지 않았을 때 기본 이름을 무엇으로 볼지 정하는 규칙
- `physical naming strategy`
  그렇게 정해진 이름을 실제 DB 컬럼명이나 테이블명으로 어떻게 바꿀지 정하는 규칙

즉 `modifiedTime`이 바로 DB로 가는 것이 아니라, 중간에 전략이 이름을 해석하고 바꾸는 단계가 있다.

## 3. `implicit naming strategy`와 `physical naming strategy` 차이

이 둘을 헷갈리기 쉬운데 역할이 다르다.

### 3.1 `implicit naming strategy`

이 전략은 **이름을 안 썼을 때** 동작한다.

예를 들어 아래처럼 `@Column(name = "...")`을 생략했다고 하자.

```kotlin
var modifiedTime: LocalDateTime = LocalDateTime.now()
```

이 경우 Hibernate는 우선 이 프로퍼티를 보고 컬럼의 논리 이름 후보를 정해야 한다.
이 단계에서 보통 `modifiedTime` 같은 이름이 잡힌다.

즉 `implicit naming strategy`는 아래 질문에 답한다.

- 컬럼명을 명시하지 않았을 때 기본 이름을 무엇으로 볼 것인가
- 테이블명을 명시하지 않았을 때 기본 이름을 무엇으로 볼 것인가

### 3.2 `physical naming strategy`

이 전략은 앞 단계에서 정해진 이름을 **실제 DB 식별자 이름으로 변환**한다.

예를 들어 논리 이름이 `modifiedTime`이면, physical strategy가 이것을 `modified_time`으로 바꿀 수 있다.

즉 `physical naming strategy`는 아래 질문에 답한다.

- DB에 실제로 생성할 컬럼명을 어떤 형식으로 만들 것인가
- 대문자를 소문자로 바꿀 것인가
- camelCase를 snake_case로 바꿀 것인가

실제로 눈에 띄는 `camelCase -> snake_case` 변화는 대부분 이 단계에서 발생한다.

## 4. Spring Boot에서는 왜 기본적으로 snake_case가 보이는가

Spring Boot는 Hibernate 설정을 자동 구성할 때 기본 naming strategy를 함께 넣어준다.

Spring Boot 3.x 기준으로 많이 보게 되는 기본 조합은 아래와 같다.

- implicit naming strategy: `SpringImplicitNamingStrategy`
- physical naming strategy: `CamelCaseToUnderscoresNamingStrategy`

이 조합 때문에 엔티티에서 별도 컬럼명을 지정하지 않은 필드는 보통 다음처럼 보인다.

- `createdTime` -> `created_time`
- `modifiedTime` -> `modified_time`

그래서 이 현상을 두고 "Hibernate 기본 정책이 snake_case다"라고 말하면 반쯤만 맞다.
좀 더 정확히는 다음처럼 말해야 한다.

- 순수 Hibernate 자체의 일반론이라기보다
- **Spring Boot가 Hibernate에 기본 적용한 physical naming strategy 때문에 snake_case가 된다**

## 5. `@Column(name = "modifiedTime")`를 줘도 왜 그대로 안 갈 수 있을까

이 부분도 자주 헷갈린다.

많이들 `@Column(name = "modifiedTime")`를 주면 최종 컬럼명이 반드시 `modifiedTime`이 될 거라고 생각한다.
하지만 실제로는 그렇지 않을 수 있다.

```kotlin
@Column(name = "modifiedTime")
var modifiedTime: LocalDateTime = LocalDateTime.now()
```

이 경우 `implicit naming strategy`는 사실상 우회했다고 볼 수 있다. 이미 이름을 명시했기 때문이다.

그런데도 `physical naming strategy`는 마지막 단계에서 여전히 적용될 수 있다.
그러면 `modifiedTime`이 다시 `modified_time`으로 변환될 수 있다.

즉 중요한 포인트는 이렇다.

- `@Column(name = "...")`
  이름을 명시하는 역할은 한다.
- 하지만 그것이 항상 **최종 DB 물리 이름을 절대 고정한다**는 뜻은 아니다.
- physical naming strategy가 마지막에 한 번 더 개입할 수 있다.

반대로 아래처럼 쓰면 보통 그대로 간다.

```kotlin
@Column(name = "modified_time")
var modifiedTime: LocalDateTime = LocalDateTime.now()
```

이미 snake_case이기 때문에 physical strategy가 추가로 바꿀 것이 거의 없기 때문이다.

## 6. 예제로 다시 보면 어떻게 이해하면 좋은가

아래 엔티티를 보자.

```kotlin
@Entity
@Table(name = "member")
data class Member(
    @Id
    @Column(name = "id")
    val id: Long,

    @Column(name = "name")
    val name: String,

    var age: Int,

    var modifiedTime: LocalDateTime = LocalDateTime.now()
)
```

여기서 각 필드가 처리되는 방식은 다르다.

- `id`
  이미 `@Column(name = "id")`를 명시했으므로 그 이름을 기준으로 간다.
- `name`
  역시 명시 이름이 있다.
- `age`
  별도 지정이 없으니 기본 규칙을 탄다.
- `modifiedTime`
  별도 지정이 없으니 기본 규칙을 탄 뒤 `modified_time`으로 변환될 수 있다.

즉 camelCase 필드가 snake_case 컬럼으로 생성되는 가장 직접적인 이유는 **컬럼명을 안 쓴 필드가 Spring Boot 기본 physical naming strategy를 타기 때문**이다.

## 7. 설정을 바꾸고 싶다면

방법은 크게 두 가지다.

### 7.1 필드별로 직접 컬럼명을 명시하기

```kotlin
@Column(name = "modified_time")
var modifiedTime: LocalDateTime = LocalDateTime.now()
```

이 방식은 가장 명시적이다.
엔티티를 읽는 사람도 실제 컬럼명을 바로 알 수 있다.

### 7.2 전역 naming strategy를 바꾸기

`application.yml`에서 Hibernate naming strategy를 직접 지정할 수도 있다.

```yaml
spring:
  jpa:
    hibernate:
      naming:
        physical-strategy: org.hibernate.boot.model.naming.CamelCaseToUnderscoresNamingStrategy
        implicit-strategy: org.springframework.boot.orm.jpa.hibernate.SpringImplicitNamingStrategy
```

반대로 다른 전략을 넣으면 camelCase 유지 방식으로도 바꿀 수 있다.

다만 실무에서는 팀 전체의 스키마 네이밍 규칙과 맞추는 것이 더 중요하다.
대부분의 프로젝트는 DB 컬럼명을 snake_case로 두기 때문에 Spring Boot 기본값을 그대로 쓰는 편이 자연스럽다.

## 8. 정리

이 내용을 한 줄씩 정리하면 다음과 같다.

- `modifiedTime -> modified_time` 변환은 보통 Spring Boot 기본 naming strategy 때문에 발생한다.
- `implicit naming strategy`는 이름을 안 썼을 때 기본 이름을 정하는 규칙이다.
- `physical naming strategy`는 그 이름을 실제 DB 이름으로 변환하는 규칙이다.
- 눈에 띄는 snake_case 변환은 대체로 `physical naming strategy`가 담당한다.
- `@Column(name = "modifiedTime")`를 줘도 physical strategy 때문에 최종 DB 이름이 그대로 유지되지 않을 수 있다.

따라서 이 현상을 이해할 때는 "Hibernate가 그냥 그렇게 한다"라고 외우기보다, **Spring Boot가 Hibernate에 어떤 naming strategy를 기본 적용하는지**까지 같이 기억하는 편이 정확하다.
