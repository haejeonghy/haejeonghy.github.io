---
layout: post
title: Spring Boot 캐싱 완전 정리
summary: Spring Boot 캐싱의 활성화 방식, CacheManager 자동 구성, Redis와 Caffeine 선택 기준, 실무에서 반드시 봐야 할 캐시 전략 포인트를 정리합니다.
date: 2026-04-02 14:48:15 +0900
updated: 2026-04-02 14:48:15 +0900
tag: spring boot cache redis caffeine
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. Spring Boot 캐싱을 먼저 어떻게 봐야 하는가

Spring Boot에서 캐싱은 단순히 `@Cacheable` 하나 붙이면 끝나는 기능이 아니다.

실무에서는 캐시를 "비싼 연산을 줄이기 위한 최적화 레이어"로 보지만, 실제로는 데이터 조회 흐름과 일관성을 함께 다뤄야 하는 전략에 가깝다.

즉, 캐싱을 잘못 적용하면 성능은 좋아지는 대신 오래된 데이터가 남거나, 테스트가 불안정해지거나, 장애 원인 추적이 어려워질 수 있다.

이번 글에서는 Spring Boot 캐싱의 기본 구조부터, `Redis`와 `Caffeine` 선택 기준, 그리고 실무에서 특히 조심해야 할 포인트까지 한 번에 정리한다.

## 2. 캐싱 활성화는 `@EnableCaching`부터 시작한다

캐싱 기능을 사용하려면 먼저 Spring의 캐시 기능을 활성화해야 한다.

```kotlin
@Configuration
@EnableCaching
class CacheConfig
```

이 애노테이션의 역할은 아래와 같다.

- `@Cacheable`
- `@CachePut`
- `@CacheEvict`

위 애노테이션이 실제로 동작하도록 Spring의 캐시 인프라를 활성화한다.

### 2.1 메인 클래스에 붙이지 않는 것이 좋은 이유

아래처럼 `@SpringBootApplication`이 붙은 메인 클래스에 바로 선언하는 경우가 있다.

```kotlin
@SpringBootApplication
@EnableCaching // 비추천
class Application
```

이 방식이 늘 틀린 것은 아니지만, 실무에서는 별도 설정 클래스로 분리하는 편이 안전하다.

이유는 다음과 같다.

- 테스트 환경에서도 캐싱이 예상보다 쉽게 활성화될 수 있다
- 디버깅 시 실제 메서드가 호출되지 않아 흐름을 놓치기 쉽다
- 오래된 데이터가 남아 원인 파악이 어려워질 수 있다

보통은 아래처럼 분리하는 방식을 더 많이 사용한다.

- 별도 `Configuration` 클래스에 선언
- 필요하면 `Profile`로 제어

## 3. `@Cacheable`의 실제 동작은 이렇게 이해하면 된다

가장 기본적인 예시는 아래와 같다.

```kotlin
@Cacheable("piDecimals")
fun computePiDecimal(precision: Int): BigDecimal
```

동작 흐름은 단순하다.

1. 캐시에서 key를 조회한다
2. 값이 있으면 메서드를 실행하지 않는다
3. 값이 없으면 메서드를 실행한 뒤 결과를 캐시에 저장한다

여기서 기본 key는 보통 메서드 인자를 기반으로 만들어진다.

즉, 같은 입력이 들어오면 같은 결과를 다시 계산하지 않도록 메서드 실행 자체를 생략하는 것이다.

### 3.1 카페 주문 시스템으로 비유하면

예를 들어 라떼 주문 시스템을 떠올리면 이해가 쉽다.

- 같은 주문이 다시 들어오면 이미 준비된 음료를 바로 제공
- 없으면 새로 만들고 보관

캐시는 결국 "같은 요청에 대해 이미 계산한 결과가 있으면 재사용하는 장치"라고 보면 된다.

### 3.2 key는 항상 인자 그대로가 아니다

중요한 점은 캐시 key가 반드시 메서드 인자 전체와 동일한 것은 아니라는 점이다.

Spring Cache는 `SpEL`로 key를 직접 지정할 수 있다.

```kotlin
@Cacheable(value = "user", key = "#userId")
```

```kotlin
@Cacheable(key = "'fixedKey'")
```

즉, 기본은 인자 기반이지만 실제 운영에서는 key 설계를 직접 통제하는 경우가 많다.

이 지점이 실무에서 매우 중요하다. 캐시 문제의 상당수는 저장소 종류보다 key 설계에서 시작되기 때문이다.

## 4. Spring의 캐시 구조는 추상화와 구현이 같이 있다

Spring Cache의 구조를 단순하게 보면 아래와 같다.

```text
@Cacheable
   ↓
CacheManager
   ↓
Cache
```

각 구성요소의 역할은 다음과 같다.

| 구성           | 역할              |
| -------------- | ----------------- |
| `CacheManager` | 캐시 생성 및 관리 |
| `Cache`        | 실제 데이터 저장  |
| Annotation     | 캐싱 동작 트리거  |

여기서 자주 나오는 설명 중 하나가 "Spring은 캐시 추상화만 제공한다"는 말인데, 이 표현은 절반만 맞다.

Spring은 추상화 계층을 제공하는 동시에 기본 구현도 일부 제공한다.

예를 들면 다음과 같다.

- `ConcurrentMapCache`
- `SimpleCacheManager`

다만 실무에서는 기본 구현보다 외부 캐시 구현체를 더 많이 사용한다.

- `Redis`
- `Caffeine`

즉, Spring Cache는 추상화 위에 여러 구현을 끼워 넣을 수 있는 구조라고 보는 편이 정확하다.

## 5. `CacheManager`는 자동 생성되지만 조건부다

Spring Boot는 캐시 관련 라이브러리와 설정 상태를 보고 `CacheManager`를 자동 구성한다.

핵심은 무조건 하나를 만드는 것이 아니라, 조건에 따라 다른 구현을 선택한다는 점이다.

| 조건                    | 생성되는 `CacheManager` |
| ----------------------- | ----------------------- |
| Redis 관련 구성 존재    | `RedisCacheManager`     |
| Caffeine 관련 구성 존재 | `CaffeineCacheManager`  |
| 별도 구현 없음          | `SimpleCacheManager`    |

즉, 이것은 단순 자동 구성이라기보다 조건 기반 자동 구성이라고 이해하는 편이 맞다.

실무에서는 "왜 이 캐시 구현이 잡혔는지"를 항상 의식해야 한다. 의존성 하나 추가했는데 캐시 동작이 바뀌는 경우도 있기 때문이다.

## 6. Redis 캐시는 분산 환경에서 주로 선택한다

`Redis` 기반 캐시는 대표적인 분산 캐시다.

특징은 아래와 같다.

- 여러 서버 인스턴스가 같은 캐시를 공유할 수 있다
- MSA나 멀티 인스턴스 환경에서 일관된 캐시 접근이 가능하다

설정 예시는 다음과 같다.

```yaml
spring:
  cache:
    cache-names: "cache1,cache2"
    redis:
      time-to-live: "10m"
```

이 설정의 의미는 아래와 같다.

- `cache1`, `cache2` 캐시 생성
- TTL 10분 적용

### 6.1 언제 Redis를 쓰는가

실무에서는 보통 아래 같은 경우에 많이 사용한다.

- 유저 정보 캐시
- 인증 또는 토큰 검증 결과 캐시
- 외부 API 응답 캐시

즉, 여러 애플리케이션 서버가 동일한 캐시 결과를 봐야 하는 경우라면 Redis가 훨씬 자연스럽다.

## 7. Caffeine 캐시는 단일 JVM에서 매우 빠르다

`Caffeine`은 JVM 내부 메모리를 사용하는 로컬 캐시다.

특징은 다음과 같다.

- 매우 빠르다
- 프로세스 내부 메모리에서 동작한다
- 서버 간 공유되지 않는다

설정 예시는 아래와 같다.

```yaml
spring:
  cache:
    cache-names: "cache1,cache2"
    caffeine:
      spec: "maximumSize=500,expireAfterAccess=600s"
```

의미는 다음과 같다.

- 최대 500개 저장
- 600초 동안 사용되지 않으면 제거

### 7.1 언제 Caffeine을 쓰는가

다음과 같은 경우에 적합하다.

- 계산 결과 캐싱
- 단일 인스턴스 환경의 DB 조회 캐싱
- 매우 빠른 응답이 중요한 경우

즉, 분산 공유가 필요 없고 로컬 메모리 캐시만으로 충분하다면 Caffeine은 매우 좋은 선택이다.

## 8. Redis를 쓸 때 Lettuce 커넥션 풀도 같이 봐야 한다

Spring Boot에서 Redis 클라이언트로 `Lettuce`를 사용할 때는 커넥션 풀 설정을 함께 보게 된다.

핵심은 아래 두 가지다.

- `Lettuce`는 Redis 클라이언트다
- `lettuce.pool` 설정을 사용하면 커넥션 풀을 구성할 수 있다

그리고 이때는 `commons-pool2` 의존성이 필요하다.

즉, Redis 캐시를 붙였다고 끝나는 것이 아니라, 실제 접속 자원 관리까지 같이 봐야 한다.

## 9. 필요하면 `CacheManager`를 직접 정의할 수 있다

자동 구성이 편리하긴 하지만, 상황에 따라 직접 `CacheManager`를 정의해야 할 때가 있다.

```java
@Bean
CacheManager cacheManager() {
    SimpleCacheManager cacheManager = new SimpleCacheManager();
    cacheManager.setCaches(Set.of(new ConcurrentMapCache("default")));
    return cacheManager;
}
```

이 방식이 필요한 경우는 보통 아래와 같다.

- 캐시 전략을 직접 제어하고 싶을 때
- 특정 환경에서 캐싱을 비활성화하거나 단순화하고 싶을 때
- 테스트 환경을 운영 환경과 분리하고 싶을 때

즉, 자동 구성이 기본값이라면 직접 정의는 의도를 명확히 드러내는 방법이라고 볼 수 있다.

## 10. Spring 캐시는 조회 캐시만 있는 것이 아니다

Spring Cache를 `@Cacheable`만으로 이해하면 절반만 이해한 것이다.

실무에서 자주 보는 핵심 애노테이션은 세 가지다.

### 10.1 조회 후 저장: `@Cacheable`

```kotlin
@Cacheable
```

- 캐시에 값이 있으면 메서드를 실행하지 않는다
- 없으면 실행 후 저장한다

### 10.2 강제 갱신: `@CachePut`

```kotlin
@CachePut
```

- 메서드를 항상 실행한다
- 실행 결과를 캐시에 저장한다

### 10.3 삭제: `@CacheEvict`

```kotlin
@CacheEvict
```

- 캐시를 제거한다

정리하면 다음과 같다.

| 애노테이션    | 동작                |
| ------------- | ------------------- |
| `@Cacheable`  | 조회 후 없으면 저장 |
| `@CachePut`   | 무조건 실행 후 저장 |
| `@CacheEvict` | 삭제                |

즉, 캐싱은 조회 최적화만이 아니라 조회, 갱신, 무효화까지 포함하는 데이터 관리 전략이다.

## 11. 실무에서 가장 중요한 것은 성능보다 데이터 전략이다

캐시는 성능 최적화 도구이기도 하지만, 실무에서는 그보다 데이터 전략으로 보는 편이 더 안전하다.

잘못 사용하면 아래와 같은 문제가 생긴다.

- 오래된 데이터를 계속 반환한다
- 장애 원인 추적이 어려워진다
- 테스트가 환경 의존적으로 흔들린다

그래서 아래 항목은 반드시 함께 설계해야 한다.

- TTL 설정
- 캐시 key 설계
- 캐시 무효화 전략
- 분산 캐시와 로컬 캐시 선택 기준

결국 캐싱의 핵심은 "값을 어디에 저장할까"보다 "언제 재사용하고 언제 버릴까"에 더 가깝다.

## 12. 정리

Spring 캐싱은 메서드 실행을 생략하는 편의 기능이 아니라, 데이터 접근 흐름을 제어하는 레이어다.

그래서 `@Cacheable` 하나만 기억하는 것보다 아래를 같이 이해해야 한다.

- 캐시 활성화 위치
- `CacheManager` 자동 구성 방식
- `Redis`와 `Caffeine`의 차이
- key, TTL, 무효화 전략

이 구조를 이해하고 나면 캐싱은 단순 최적화가 아니라, 시스템 일관성과 응답 성능을 동시에 다루는 설계 포인트라는 점이 더 선명해진다.
