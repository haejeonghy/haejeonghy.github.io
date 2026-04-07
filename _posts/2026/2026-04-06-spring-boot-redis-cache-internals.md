---
layout: post
title: Spring Boot + Redis Cache 내부 동작 정리 - Proxy, CGLIB, Serialization, Supplier
summary: Spring Cache가 프록시로 동작하는 이유부터 CGLIB, Redis 직렬화 방식, lazy loader 개념까지 한 번에 정리합니다.
date: 2026-04-06 09:00:00 +0900
updated: 2026-04-06 09:00:00 +0900
tag: spring boot redis cache proxy cglib serialization
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 왜 Redis Cache를 붙이다 보면 Proxy, CGLIB, Serialization, Supplier까지 같이 보게 되는가

Spring Boot에서 Redis Cache를 적용하다 보면 단순히 `@Cacheable`만 아는 것으로는 흐름이 잘 잡히지 않는다.

실제로는 아래 개념들이 한 번에 연결되어 있기 때문이다.

- Spring Cache는 AOP 기반 프록시로 동작한다
- Spring Boot에서는 보통 CGLIB 기반 subclass proxy가 생성된다
- Redis에 값을 넣으려면 직렬화 방식이 필요하다
- 캐시 miss일 때만 값을 계산하려면 lazy loader 개념이 필요하다

즉, 캐시는 단순한 저장 기능이 아니라 **메서드 호출 가로채기 + 값 계산 시점 제어 + 직렬화 저장**이 한 흐름으로 이어진다.

이번 글에서는 이 흐름을 한 번에 정리한다.

## 2. `@Cacheable`을 붙이면 실제로는 프록시가 동작한다

예를 들어 아래와 같은 메서드가 있다고 하자.

```kotlin
@Cacheable("organization")
fun getOrganization(id: Long): Organization
```

겉으로 보면 단순히 애노테이션 하나가 붙은 것처럼 보이지만, 실제 동작은 메서드를 직접 호출하는 구조가 아니다.

```text
Client
  ↓
Spring Cache Proxy
  ↓
cache hit ?
  ├─ yes → 캐시 값 반환
  └─ no  → 실제 메서드 실행
              ↓
            결과 저장
              ↓
            반환
```

핵심은 다음과 같다.

- 클라이언트는 원본 빈을 직접 호출하지 않는다
- Spring이 만든 프록시 객체를 통해 메서드가 호출된다
- 프록시가 먼저 캐시 hit/miss를 판단한다
- miss일 때만 실제 메서드를 실행한다

즉, `@Cacheable`의 본질은 "메서드 앞단에서 캐시 여부를 판단하는 interception"이다.

이 구조는 `@Transactional`과도 매우 비슷하다.

```kotlin
@Transactional
@Cacheable
```

둘 다 프록시 기반 AOP로 동작한다.

## 3. 왜 프록시가 꼭 필요한가

캐시는 메서드 실행 전후에 개입해야 한다.

즉, 아래 과정이 필요하다.

1. 메서드 호출을 가로챈다
2. 캐시 key를 만든다
3. 캐시를 조회한다
4. 값이 있으면 실제 메서드를 실행하지 않는다
5. 값이 없으면 메서드를 실행하고 결과를 저장한다

이 흐름은 원본 객체만으로는 구현할 수 없고, 호출 사이에 끼어드는 프록시가 있어야 가능하다.

그래서 Spring Cache는 인터페이스 유무와 관계없이 프록시가 필요하다.

## 4. CGLIB subclass proxy는 무엇인가

Spring에서 프록시를 만드는 방식은 대표적으로 두 가지다.

### 4.1 JDK Dynamic Proxy

- 인터페이스 기반 프록시
- 인터페이스가 있어야 만들기 쉽다
- 실제로는 인터페이스 타입을 감싸는 방식이다

### 4.2 CGLIB subclass proxy

- 클래스를 상속해서 프록시를 만든다
- 인터페이스가 없어도 가능하다
- 원본 클래스의 하위 클래스를 동적으로 생성한다

예를 들어 원본 클래스가 아래처럼 있다면,

```kotlin
class OrganizationService
```

개념적으로는 이런 식의 프록시가 만들어진다고 이해하면 쉽다.

```kotlin
class OrganizationService$$SpringProxy : OrganizationService()
```

즉, 원본 클래스를 상속한 뒤 메서드 호출을 가로채는 subclass proxy가 생성되는 것이다.

Spring Boot 3 계열에서는 일반적으로 클래스 기반 프록시, 즉 CGLIB 방식으로 이해하면 흐름을 잡기 쉽다.

정리하면 아래와 같다.

- 인터페이스가 있으면 JDK Dynamic Proxy도 가능하다
- 인터페이스가 없어도 CGLIB이면 프록시를 만들 수 있다
- Spring Cache가 동작하려면 어떤 형태로든 프록시가 필요하다

## 5. 그래서 인터페이스가 없어도 캐시는 동작한다

많이 헷갈리는 지점이 바로 이것이다.

"인터페이스가 없는데도 왜 `@Cacheable`이 동작하지?"

답은 간단하다.

- 캐시는 프록시 기반이다
- 프록시는 꼭 인터페이스 프록시일 필요가 없다
- 클래스 기반 프록시(CGLIB)로도 충분히 동작한다

즉, 중요한 것은 인터페이스 존재 여부가 아니라 **Spring이 호출을 가로챌 수 있느냐**이다.

## 6. Redis Cache를 쓰면 직렬화 방식도 같이 봐야 한다

메서드 결과를 Redis에 저장하려면 결국 객체를 바이트나 문자열 형태로 바꿔야 한다.

즉, 아래 과정이 필요하다.

```text
object → serialized value → Redis 저장
Redis 조회 → deserialized object
```

Spring Redis Cache에서 기본 설정을 그대로 사용할 경우, value serializer가 `JdkSerializationRedisSerializer`인 경우가 많다.

즉, Java의 `Serializable` 기반 직렬화가 사용된다.

```text
object → byte[]
byte[] → object
```

이 방식은 동작은 단순하지만 실무에서는 조심해야 할 포인트가 많다.

## 7. `Serializable` 기반 직렬화가 위험한 이유

### 7.1 역직렬화 보안 이슈

Java 기본 직렬화는 오래전부터 역직렬화 공격 벡터로 자주 언급되어 왔다.

신뢰할 수 없는 데이터를 역직렬화하는 구조는 보안상 좋지 않다.

Redis를 내부 저장소처럼만 사용하더라도, 운영 환경에서는 가능한 한 더 안전하고 예측 가능한 포맷을 선택하는 편이 낫다.

즉, 실무에서는 `Serializable`을 기본 선택지로 두지 않는 경우가 많다.

### 7.2 `serialVersionUID` 문제

`Serializable` 클래스는 버전 정보를 함께 가진다.

```kotlin
class Organization : Serializable {
    companion object {
        private const val serialVersionUID = 1L
    }
}
```

직렬화 시에는 대략 아래 정보가 저장된다.

- class name
- `serialVersionUID`
- field 정보
- field 값

문제는 배포 후 클래스 구조가 바뀌면 이전에 저장된 캐시를 다시 읽는 과정에서 버전 불일치가 발생할 수 있다는 점이다.

```text
serialVersionUID mismatch
→ InvalidClassException
```

즉, 애플리케이션을 배포한 뒤 클래스 필드를 조금만 바꿔도 기존 Redis 캐시가 깨질 수 있다.

캐시라서 지우면 된다고 생각할 수도 있지만, 운영 중에는 이런 예외가 장애처럼 보이기 쉽다.

## 8. 그래서 JSON Serializer를 더 많이 권장한다

실무에서는 보통 아래 serializer를 더 자주 사용한다.

- `GenericJackson2JsonRedisSerializer`
- `Jackson2JsonRedisSerializer`

동작은 아래처럼 이해하면 된다.

```text
object → JSON
JSON → object
```

이 방식의 장점은 다음과 같다.

- 클래스 구조 변경에 상대적으로 유연하다
- Java 기본 직렬화보다 보안 부담이 낮다
- 저장된 값을 사람이 직접 확인할 수 있다
- 다른 언어와의 호환성이 좋다

즉, Redis를 캐시로 사용할 때는 "그냥 저장된다"보다 **어떤 포맷으로 저장되는가**를 먼저 확인하는 것이 중요하다.

## 9. 실무에서는 이런 Redis Cache 설정을 많이 쓴다

아래처럼 value serializer를 JSON 기반으로 바꿔두면 훨씬 예측 가능한 캐시 구성이 된다.

```kotlin
@Bean
fun redisCacheConfiguration(): RedisCacheConfiguration =
    RedisCacheConfiguration.defaultCacheConfig()
        .serializeValuesWith(
            RedisSerializationContext.SerializationPair.fromSerializer(
                GenericJackson2JsonRedisSerializer()
            )
        )
```

이 설정의 의미는 단순하다.

- 기본 캐시 설정을 가져온다
- value serializer를 JSON serializer로 교체한다
- Redis에는 Java 기본 직렬화 대신 JSON 형태로 저장된다

## 10. Supplier는 왜 같이 공부하게 되는가

캐시의 핵심은 "값이 필요할 때만 계산한다"는 점이다.

여기서 lazy evaluation 개념이 자연스럽게 등장한다.

자바에서 이 개념을 설명할 때 가장 직관적인 인터페이스가 `Supplier<T>`다.

```java
@FunctionalInterface
public interface Supplier<T> {
    T get();
}
```

의미는 간단하다.

- 지금 바로 값을 넘기는 것이 아니라
- 필요해질 때 실행할 함수를 넘긴다

### 10.1 즉시 실행 방식

```kotlin
val value = load()
cache.put(key, value)
```

이 방식의 문제는 캐시 hit 여부와 관계없이 `load()`가 먼저 실행된다는 점이다.

즉, 이미 캐시에 값이 있어도 비싼 연산이 불필요하게 수행될 수 있다.

### 10.2 lazy 실행 방식

```kotlin
cache.get(key) {
    load()
}
```

개념적으로는 아래처럼 동작한다.

- cache hit → `load()` 실행 안 함
- cache miss → `load()` 실행

즉, 계산 비용이 큰 작업을 정말 필요할 때만 수행하게 된다.

엄밀히 말하면 Spring Cache의 public API에서는 `Callable` 같은 형태가 더 직접적으로 보이기도 한다. 하지만 핵심 개념은 같다.

**캐시 miss 시점에만 값을 계산하는 지연 로더 함수**라는 관점에서 보면 `Supplier`로 이해해도 충분하다.

## 11. 전체 흐름을 한 번에 보면 이렇게 연결된다

지금까지 내용을 하나로 묶으면 아래 흐름이다.

```text
@Cacheable
   ↓
Spring Proxy (주로 CGLIB 기반으로 이해)
   ↓
Cache lookup
   ↓ miss
지연 로더 실행
   ↓
DB 조회 또는 외부 호출
   ↓
직렬화
   ↓
Redis 저장
```

즉, `@Cacheable`은 단순한 메서드 장식이 아니라 다음이 동시에 연결된 구조다.

- 프록시가 호출을 가로챈다
- 캐시 hit/miss를 판단한다
- miss일 때만 값을 계산한다
- 계산 결과를 직렬화해서 Redis에 저장한다

이 흐름을 이해하고 나면 `@Cacheable`이 훨씬 덜 추상적으로 보인다.

## 12. 핵심만 다시 정리

- Spring Cache는 프록시 기반으로 동작한다
- Spring Boot에서는 보통 CGLIB 기반 subclass proxy로 이해하면 된다
- Redis Cache를 쓰면 직렬화 방식까지 함께 봐야 한다
- Java 기본 `Serializable` 직렬화는 보안과 호환성 측면에서 아쉬움이 있다
- 실무에서는 JSON serializer를 더 많이 권장한다
- lazy evaluation을 이해하면 캐시 miss 시점의 값 계산 구조가 명확해진다
- `Supplier`는 그 lazy loader 개념을 이해하는 데 가장 직관적인 도구다

결국 Spring Boot + Redis Cache를 이해한다는 것은 애노테이션 하나를 외우는 것이 아니라, **프록시, 호출 흐름, 직렬화, 지연 실행을 함께 보는 것**에 가깝다.
