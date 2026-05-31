---
layout: post
title: Spring HTTP 클라이언트 선택 가이드 - OpenFeign, RestTemplate, WebClient, RestClient 비교
summary: Spring에서 자주 비교되는 OpenFeign, RestTemplate, WebClient, RestClient의 용도와 공통점, 차이점, 같은 기능의 구현 예시, 지금 기준의 선택 기준을 한 번에 정리합니다.
date: 2026-05-31 14:30:00 +0900
updated: 2026-05-31 14:30:00 +0900
tag: spring http client openfeign webclient resttemplate restclient
toc: true
comment: false
public: true
---
- TOC
  {:toc}

## 1. 왜 이 네 가지가 자주 같이 언급될까

Spring에서 외부 HTTP API를 호출하려고 하면 `OpenFeign`, `RestTemplate`, `WebClient`, `RestClient`가 자주 같이 등장한다.

헷갈리는 이유는 이 네 가지가 모두 "외부 HTTP 호출"과 관련은 있지만, 같은 층위의 개념은 아니기 때문이다.

- `RestTemplate`, `RestClient`, `WebClient`는 실제 HTTP 요청을 보내는 클라이언트이다.
- `OpenFeign`은 인터페이스 기반의 선언형 클라이언트 스타일에 가깝다.

즉, 어떤 것은 직접 HTTP 요청 코드를 쓰는 방식이고, 어떤 것은 인터페이스를 선언해두고 구현을 위임하는 방식이다.

이 글에서는 아래 다섯 가지를 정리해보겠다.

- 각각의 용도
- 공통점
- 차이점
- 같은 기능을 각 방식으로 구현한 코드
- 지금 당장 새 클라이언트를 만든다면 무엇을 선택할지

## 2. 먼저 한 줄씩 요약하면

- `RestTemplate`
  전통적인 동기식 HTTP 클라이언트
- `RestClient`
  Spring 6.1+에서 사용하는 최신 동기식 HTTP 클라이언트
- `WebClient`
  비동기 / 논블로킹 및 reactive 처리에 적합한 HTTP 클라이언트
- `OpenFeign`
  인터페이스 기반으로 HTTP API를 선언적으로 정의하는 방식

가장 먼저 기억할 포인트는 이것이다.

- 동기식 일반 백엔드 호출이면 `RestClient`
- reactive 체인이나 스트리밍이 필요하면 `WebClient`
- `RestTemplate`은 유지보수 대상
- `OpenFeign`은 "선언형 인터페이스"가 필요할 때 검토

## 3. 공통점

이 네 가지는 모두 외부 HTTP API를 호출할 때 사용된다는 점에서 공통점이 있다.

예를 들면 아래 같은 작업을 할 수 있다.

- `GET`, `POST`, `PUT`, `DELETE` 요청 전송
- 헤더 설정
- 요청 바디 전송
- 응답 바디 역직렬화
- 인증 토큰 전달
- 예외 처리 및 타임아웃 설정

즉, 결국 목적은 같다.

> 다른 시스템의 HTTP API를 안정적으로 호출하는 것

차이는 주로 아래에서 갈린다.

- 동기냐 비동기냐
- 직접 호출형이냐 선언형이냐
- 최신 권장 방식이냐 레거시 호환 방식이냐
- reactive 생태계와 연결되느냐

## 4. 차이점은 어떤 기준으로 보면 될까

### 4.1 호출 스타일

- `RestTemplate`
  메서드 중심 호출
- `RestClient`
  fluent API 기반 직접 호출
- `WebClient`
  fluent API 기반 비동기 호출
- `OpenFeign`
  인터페이스 선언 기반 호출

### 4.2 실행 모델

- `RestTemplate`
  동기 / blocking
- `RestClient`
  동기 / blocking
- `WebClient`
  비동기 / non-blocking
- `OpenFeign`
  보통 동기 / blocking으로 사용

### 4.3 현재 시점의 포지션

- `RestTemplate`
  신규 선택 우선순위가 낮다
- `RestClient`
  Spring의 최신 동기식 선택지
- `WebClient`
  reactive 및 고동시성 요구에 적합
- `OpenFeign`
  Spring Cloud 생태계에서 선언형 클라이언트로 많이 사용

## 5. 각각의 용도는 어떻게 이해하면 될까

### 5.1 RestTemplate

`RestTemplate`은 오랫동안 많이 사용된 전통적인 방식이다.

장점은 단순하고 익숙하다는 점이다. 다만 신규 코드에서 우선적으로 선택할 이유는 크지 않다.

주로 아래 상황에서 보게 된다.

- 기존 레거시 서비스 유지보수
- 이미 `RestTemplate` 기반 공통 모듈이 많음
- 빠른 수정만 필요하고 구조 변경 여유가 없음

### 5.2 RestClient

`RestClient`는 현재 Spring에서 동기식 HTTP 호출을 더 현대적으로 작성할 수 있게 해주는 선택지이다.

주로 아래 상황에 잘 맞는다.

- Spring MVC 기반 서버
- 대부분의 외부 API 호출이 요청당 1~2회 정도인 일반 백엔드
- reactive를 도입할 계획은 없지만 `RestTemplate`보다 읽기 좋은 API를 원함

즉, "일반적인 서버 애플리케이션에서 외부 HTTP 호출이 필요하다"면 가장 먼저 검토할 선택지이다.

### 5.3 WebClient

`WebClient`는 비동기 / non-blocking 모델을 사용한다.

주로 아래 상황에서 강점이 있다.

- Spring WebFlux 사용
- `Mono`, `Flux` 기반으로 처리 흐름이 이어짐
- SSE, 스트리밍, 대량 fan-out 호출
- 높은 동시성과 적은 스레드 점유가 중요함

반대로 단순한 동기식 MVC 서비스에서 `.block()`을 붙여 쓰기 시작하면 장점을 많이 잃는다.

### 5.4 OpenFeign

`OpenFeign`은 인터페이스에 API 명세를 선언하고 구현은 프레임워크에 맡기는 방식이다.

장점은 API 스펙이 인터페이스에 모여서 읽기 쉽다는 점이다.

잘 맞는 경우는 아래와 같다.

- 팀이 선언형 클라이언트 스타일을 선호함
- 호출 대상 API가 많고 인터페이스 수준의 명세 관리가 중요함
- 이미 Spring Cloud를 사용하고 있음

다만 `OpenFeign`은 Spring Framework의 기본 HTTP 클라이언트라기보다 Spring Cloud 계열 선택지에 가깝다.

## 6. 같은 요구사항을 각 방식으로 구현해보면

예시는 아래 요구사항으로 통일하겠다.

> `GET /users/{id}` 로 사용자 1명을 조회한다.

응답 DTO는 다음처럼 가정한다.

```kotlin
data class UserResponse(
    val id: Long,
    val name: String,
)
```

### 6.1 RestTemplate 구현

```kotlin
class UserClient(
    private val restTemplate: RestTemplate,
) {
    fun getUser(id: Long): UserResponse {
        return restTemplate.getForObject(
            "https://api.example.com/users/{id}",
            UserResponse::class.java,
            id
        )!!
    }
}
```

특징은 단순하다. 다만 API가 커질수록 메서드 조합이 다소 투박하게 느껴질 수 있다.

### 6.2 RestClient 구현

```kotlin
class UserClient(
    private val restClient: RestClient,
) {
    fun getUser(id: Long): UserResponse {
        return restClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .body(UserResponse::class.java)!!
    }
}
```

`RestClient`는 요청 생성 흐름이 더 자연스럽다.

- HTTP 메서드 선택
- URI 지정
- 헤더나 바디 설정
- 응답 추출

이 흐름이 fluent API로 이어져서 읽기 쉽다.

### 6.3 WebClient 구현

```kotlin
class UserClient(
    private val webClient: WebClient,
) {
    fun getUser(id: Long): Mono<UserResponse> {
        return webClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(UserResponse::class.java)
    }
}
```

반환 타입이 `UserResponse`가 아니라 `Mono<UserResponse>`라는 점이 핵심 차이이다.

즉, 결과를 바로 받는 것이 아니라 비동기 파이프라인 안에서 다룬다.

### 6.4 OpenFeign 구현

```kotlin
@FeignClient(
    name = "userClient",
    url = "\${clients.user.url}"
)
interface UserClient {

    @GetMapping("/users/{id}")
    fun getUser(@PathVariable id: Long): UserResponse
}
```

호출하는 쪽은 아래처럼 쓴다.

```kotlin
val user = userClient.getUser(1L)
```

직접 HTTP 호출 코드를 쓰지 않아도 인터페이스 메서드 호출처럼 사용할 수 있다는 점이 가장 큰 특징이다.

## 7. POST 요청도 보면 차이가 더 잘 보인다

요청 DTO는 다음처럼 가정하겠다.

```kotlin
data class CreateUserRequest(
    val name: String,
)
```

### 7.1 RestClient

```kotlin
fun createUser(request: CreateUserRequest): UserResponse {
    return restClient.post()
        .uri("/users")
        .body(request)
        .retrieve()
        .body(UserResponse::class.java)!!
}
```

### 7.2 WebClient

```kotlin
fun createUser(request: CreateUserRequest): Mono<UserResponse> {
    return webClient.post()
        .uri("/users")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(UserResponse::class.java)
}
```

### 7.3 OpenFeign

```kotlin
@PostMapping("/users")
fun createUser(@RequestBody request: CreateUserRequest): UserResponse
```

같은 기능을 구현해도 다음처럼 관점이 달라진다.

- `RestClient`, `WebClient`는 요청 조립 과정을 코드로 직접 드러낸다.
- `OpenFeign`은 API 형태를 인터페이스에 선언한다.

## 8. 무엇이 더 좋은가가 아니라 어떤 상황에 맞는가가 중요하다

이 네 가지를 절대적인 우열로 보면 판단이 꼬인다.

예를 들어 아래처럼 보는 것이 더 정확하다.

### 8.1 단순한 Spring MVC 서버

대부분의 경우 `RestClient`가 가장 무난하다.

이유는 다음과 같다.

- blocking 모델과 잘 맞음
- 코드가 읽기 쉬움
- `RestTemplate`보다 현대적인 API
- Spring 기본 스택 안에서 해결 가능

### 8.2 이미 WebFlux를 쓰는 서비스

이 경우는 `WebClient`가 자연스럽다.

`Mono`, `Flux` 체인 안에서 외부 호출 결과를 이어 붙일 수 있기 때문이다.

여기서 굳이 동기식 클라이언트를 섞으면 전체 모델이 어색해질 수 있다.

### 8.3 선언형 인터페이스가 특히 중요한 팀

이 경우는 `OpenFeign`도 좋은 선택이 될 수 있다.

특히 외부 API 수가 많고 각 API 명세를 인터페이스 단위로 정리해두고 싶다면 생산성이 올라간다.

다만 이것은 "Spring 기본 선택"이라기보다 "Spring Cloud 기반의 팀 선택"에 가깝다.

### 8.4 레거시 코드 유지보수

이미 `RestTemplate`이 널리 퍼져 있다면 바로 전면 교체할 필요는 없다.

다만 새로 추가하는 클라이언트까지 굳이 `RestTemplate`로 만들 이유는 크지 않다.

## 9. 지금 당장 새 클라이언트를 구현한다면 무엇을 쓸까

내 기준의 추천은 꽤 단순하다.

### 9.1 기본값

특별한 이유가 없다면 `RestClient`를 먼저 선택하겠다.

이유는 다음과 같다.

- 대부분의 Spring 서버는 아직도 동기식 MVC 모델이 많다
- 실제 현업 외부 API 호출은 blocking으로도 충분한 경우가 많다
- `RestTemplate`보다 API가 읽기 좋다
- Spring의 현재 방향성과도 잘 맞는다

즉, "새로운 일반 백엔드 서비스에서 외부 API 클라이언트 하나를 만든다"면 `RestClient`가 기본 선택지이다.

### 9.2 예외 1: reactive가 핵심인 경우

아래 중 하나라도 핵심 요구사항이면 `WebClient`를 선택하겠다.

- `Mono`, `Flux` 기반 서비스
- 논블로킹 end-to-end 처리
- 스트리밍 응답
- 매우 높은 동시성

이 경우 `RestClient`보다 `WebClient`가 구조적으로 더 잘 맞는다.

### 9.3 예외 2: 선언형 인터페이스가 핵심인 경우

팀이 인터페이스 기반 선언형 HTTP 클라이언트를 강하게 선호하고, 이미 Spring Cloud를 잘 사용하고 있다면 `OpenFeign`을 선택할 수 있다.

다만 신규 프로젝트에서 이것을 기본값으로 둘지는 팀의 기술 스택과 운영 기준을 보고 정해야 한다.

### 9.4 피하고 싶은 선택

신규 코드에서 `RestTemplate`를 기본 선택으로 두지는 않겠다.

못 쓰는 도구라서가 아니라, 지금은 더 나은 기본 선택지가 있기 때문이다.

## 10. 빠르게 결정해야 한다면 이렇게 정리할 수 있다

### 10.1 추천 순서

1. Spring MVC 기반 일반 서버면 `RestClient`
2. WebFlux / reactive 중심이면 `WebClient`
3. 선언형 인터페이스와 Spring Cloud 선호가 강하면 `OpenFeign`
4. `RestTemplate`은 기존 코드 유지보수 중심

### 10.2 한 문장 결론

> 지금 새로 HTTP 클라이언트를 만든다면, 대부분의 경우 `RestClient`를 먼저 선택하고 reactive가 필요할 때만 `WebClient`로 가는 판단이 가장 무난하다.

## 11. 마무리

정리하면 네 가지 모두 HTTP 호출을 위한 도구이지만, 역할과 선택 기준은 꽤 다르다.

- `RestTemplate`
  과거의 표준
- `RestClient`
  현재의 기본 동기식 선택지
- `WebClient`
  reactive / non-blocking 선택지
- `OpenFeign`
  선언형 인터페이스 중심 선택지

중요한 것은 최신 도구 이름을 고르는 것이 아니라, 내 서비스의 실행 모델과 팀의 개발 방식에 맞는 클라이언트를 고르는 것이다.

실무에서는 대부분 아래 한 줄로 정리해도 크게 틀리지 않는다.

> 그냥 새로 만든다면 `RestClient`부터 검토하고, reactive가 필요할 때만 `WebClient`를 선택하면 된다.
