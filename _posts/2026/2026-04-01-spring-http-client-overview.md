---
layout: post
title: Spring HTTP Client 정리 - RestTemplate, RestClient, WebClient, Feign, HttpExchange, Flux
summary: Spring에서 자주 언급되는 HTTP 클라이언트와 선언형 인터페이스 방식, Flux와 Mono의 의미를 한 번에 비교 정리합니다.
date: 2026-04-01 09:10:00 +0900
updated: 2026-04-01 09:10:00 +0900
tag: spring http client webflux
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 전체 구조를 먼저 보면 이해가 쉽다

Spring에서 HTTP 호출 관련 용어가 헷갈리는 이유는 서로 다른 종류의 개념이 같이 섞여서 등장하기 때문이다.

예를 들면 어떤 것은 실제 HTTP 요청을 보내는 도구이고, 어떤 것은 인터페이스 선언 방식이며, 어떤 것은 비동기 결과를 담는 타입이다.

큰 그림으로 보면 아래처럼 정리할 수 있다.

```text
[ HTTP 호출 방식 ]

1) 직접 호출 (imperative)
- RestTemplate
- RestClient
- WebClient

2) 선언형 호출 (declarative)
- OpenFeign
- @HttpExchange


[ 데이터 처리 방식 ]

- 동기 (blocking)
- 비동기 (non-blocking, reactive)
  - Mono: 0~1개
  - Flux: 0~N개
```

즉, 먼저 **직접 호출인지 선언형인지**를 나누고, 그 다음 **동기인지 비동기인지**를 나누면 구조가 선명해진다.

## 2. 핵심 개념 한 줄 요약

가장 짧게 요약하면 아래와 같다.

- `RestTemplate`
  과거 방식의 동기 HTTP 클라이언트
- `RestClient`
  현재 Spring에서 권장하는 동기 HTTP 클라이언트
- `WebClient`
  비동기 / 논블로킹 HTTP 클라이언트
- `OpenFeign`
  인터페이스 기반 선언형 HTTP 클라이언트
- `@HttpExchange`
  Spring 기본 제공 선언형 HTTP 인터페이스 방식
- `Flux`
  비동기 스트림을 표현하는 Reactor 타입

여기서 중요한 포인트는 다음 두 가지이다.

- `RestClient`, `WebClient`는 실제 HTTP 호출 도구이다.
- `Flux`, `Mono`는 HTTP 클라이언트가 아니라 결과를 담는 타입이다.

## 3. 카페 시스템으로 비유해보면

이 개념들은 카페 주문 시스템에 비유하면 훨씬 직관적이다.

- `RestClient`
  직원이 주문을 받아서 한 번에 주방으로 전달하는 방식
- `WebClient + Flux`
  주문이 들어오는 대로 전광판에 계속 표시되는 방식
- `OpenFeign`, `@HttpExchange`
  주문 API를 인터페이스처럼 미리 정의해두고 실제 전달은 뒤에서 처리하는 방식

즉, 선언형 방식은 "어떻게 HTTP를 호출할지"보다 "이 시스템에 어떤 API가 있는지"를 먼저 드러내는 방식이라고 보면 된다.

## 4. 같은 요구사항으로 코드 비교

예시는 아래 요구사항 하나로 통일하겠다.

> `GET /menus/{id}` 호출로 메뉴 1개 조회

### 4.1 RestTemplate

`RestTemplate`은 가장 전통적인 방식이다.

```kotlin
val restTemplate = RestTemplate()

fun getMenu(id: Long): MenuResponse {
    return restTemplate.getForObject(
        "https://api.cafe.com/menus/{id}",
        MenuResponse::class.java,
        id
    )!!
}
```

특징은 아래와 같다.

- 사용법이 단순하다
- 동기 방식이다
- 신규 코드에서는 우선순위가 많이 낮아졌다

## 4.2 RestClient

`RestClient`는 `RestTemplate`보다 더 현대적인 fluent API를 제공한다.

```kotlin
val restClient = RestClient.create("https://api.cafe.com")

fun getMenu(id: Long): MenuResponse {
    return restClient.get()
        .uri("/menus/{id}", id)
        .retrieve()
        .body(MenuResponse::class.java)!!
}
```

이 방식의 장점은 다음과 같다.

- 코드 흐름이 읽기 쉽다
- 동기 호출이 필요한 일반적인 백엔드 코드와 잘 맞는다
- Spring에서 현재 표준에 가깝게 보는 방향이다

## 4.3 WebClient

`WebClient`는 비동기 / 논블로킹 모델을 사용한다.

결과가 1건이면 `Mono`, 여러 건이면 `Flux`를 반환한다.

```kotlin
val webClient = WebClient.create("https://api.cafe.com")

fun getMenu(id: Long): Mono<MenuResponse> {
    return webClient.get()
        .uri("/menus/{id}", id)
        .retrieve()
        .bodyToMono(MenuResponse::class.java)
}
```

여러 개를 받을 때는 이렇게 표현할 수 있다.

```kotlin
fun getMenus(): Flux<MenuResponse> {
    return webClient.get()
        .uri("/menus")
        .retrieve()
        .bodyToFlux(MenuResponse::class.java)
}
```

즉, `WebClient`는 호출 도구이고 `Mono` / `Flux`는 그 결과를 담는 타입이다.

## 4.4 OpenFeign

`OpenFeign`은 HTTP API를 인터페이스처럼 선언해서 사용하는 방식이다.

```kotlin
@FeignClient(name = "menuClient", url = "https://api.cafe.com")
interface MenuClient {

    @GetMapping("/menus/{id}")
    fun getMenu(@PathVariable id: Long): MenuResponse
}
```

호출할 때는 일반 함수처럼 사용하면 된다.

```kotlin
menuClient.getMenu(1)
```

장점은 API 명세가 인터페이스에 모여서 관리가 쉬워진다는 점이다.

## 4.5 @HttpExchange + RestClient

`@HttpExchange`는 Spring이 제공하는 선언형 HTTP 인터페이스 방식이다.

다만 혼자서는 동작하지 않고, 반드시 실제 HTTP를 수행할 클라이언트가 필요하다.

먼저 인터페이스를 정의한다.

```kotlin
interface MenuHttpClient {

    @GetExchange("/menus/{id}")
    fun getMenu(@PathVariable id: Long): MenuResponse
}
```

그 다음 `RestClient`를 연결해서 프록시 클라이언트를 생성한다.

```kotlin
val restClient = RestClient.create("https://api.cafe.com")

val factory = HttpServiceProxyFactory
    .builderFor(RestClientAdapter.create(restClient))
    .build()

val client = factory.createClient(MenuHttpClient::class.java)
```

사용은 아래처럼 하면 된다.

```kotlin
client.getMenu(1)
```

즉, 구조는 다음처럼 나뉜다.

- 인터페이스 선언: `@HttpExchange`
- 실제 동기 HTTP 실행: `RestClient`
- 둘을 연결해서 구현체 생성: `HttpServiceProxyFactory`

## 4.6 @HttpExchange + WebClient

`@HttpExchange`는 `WebClient`와도 연결할 수 있다.

이 경우 반환 타입은 `Mono`나 `Flux`가 된다.

```kotlin
interface MenuHttpClient {

    @GetExchange("/menus/{id}")
    fun getMenu(@PathVariable id: Long): Mono<MenuResponse>
}
```

생성 코드는 아래와 같다.

```kotlin
val webClient = WebClient.create("https://api.cafe.com")

val factory = HttpServiceProxyFactory
    .builderFor(WebClientAdapter.create(webClient))
    .build()

val client = factory.createClient(MenuHttpClient::class.java)
```

이 조합에서는 선언형 인터페이스와 논블로킹 HTTP 호출을 함께 사용할 수 있다.

## 5. 핵심 차이 정리

### 5.1 직접 호출 vs 선언형

직접 호출 방식은 호출 로직을 코드에서 직접 조립한다.

- `RestTemplate`
- `RestClient`
- `WebClient`

선언형 방식은 인터페이스로 API를 먼저 표현한다.

- `OpenFeign`
- `@HttpExchange`

즉, 직접 호출은 "내가 요청을 구성해서 보낸다"에 가깝고, 선언형은 "이 API가 존재한다를 선언한다"에 가깝다.

### 5.2 동기 vs 비동기

동기(blocking) 계열은 아래와 같다.

- `RestTemplate`
- `RestClient`
- `OpenFeign`
- `@HttpExchange + RestClient`

비동기(non-blocking) 계열은 아래와 같다.

- `WebClient`
- `Mono`
- `Flux`
- `@HttpExchange + WebClient`

다만 `Mono`, `Flux`는 클라이언트 자체가 아니라 결과 타입이라는 점을 다시 기억하면 좋다.

## 6. 가장 중요한 개념은 레이어 분리이다

실무에서는 이 구조를 레이어로 나눠서 이해하는 것이 가장 중요하다.

```text
[ 인터페이스 선언 레이어 ]
- OpenFeign
- @HttpExchange

[ 실제 HTTP 실행 레이어 ]
- RestClient
- WebClient
```

즉, `@HttpExchange`는 실행 엔진이 아니라 인터페이스 표현 방식이다.

그래서 핵심 문장은 아래 하나로 요약된다.

> `@HttpExchange`는 혼자 쓸 수 없고, 반드시 `RestClient` 또는 `WebClient` 위에 얹어서 사용해야 한다.

이 점을 이해하면 `HttpServiceProxyFactory`, `RestClientAdapter`, `WebClientAdapter`의 역할도 같이 정리된다.

## 7. Flux / Mono의 정확한 의미

`Mono`와 `Flux`는 Reactor에서 제공하는 비동기 타입이다.

- `Mono`
  결과가 0개 또는 1개
- `Flux`
  결과가 0개 이상 여러 개

중요한 점은 이 둘이 HTTP 도구가 아니라는 것이다.

즉,

- `WebClient`는 HTTP 요청을 보낸다
- `Mono`, `Flux`는 그 결과를 비동기적으로 표현한다

예를 들어 `Flux<MenuResponse>`는 메뉴 목록 응답이 여러 건 흘러온다는 의미이지, `Flux`가 HTTP를 호출한다는 뜻은 아니다.

## 8. 실무에서 무엇을 고르면 좋은가

상황별로 단순하게 정리하면 아래 정도로 볼 수 있다.

### 8.1 단순한 외부 API 호출

`RestClient`

동기 호출이면 충분하고, 선언형 인터페이스까지는 과하다고 느껴질 때 가장 무난하다.

### 8.2 API 수가 많고 구조화가 필요한 경우

`OpenFeign` 또는 `@HttpExchange`

외부 연동 API를 인터페이스 중심으로 모아둘 수 있어서 관리가 쉬워진다.

### 8.3 고성능 / 스트리밍 / 논블로킹 처리

`WebClient + Flux`

스트리밍 응답, 대량 비동기 처리, 리액티브 파이프라인이 필요한 경우에 적합하다.

## 9. 최종 정리

정리하면 관계는 아래처럼 이해하면 된다.

- `RestClient`, `WebClient`
  실제 HTTP 호출 도구
- `OpenFeign`, `@HttpExchange`
  인터페이스 선언 방식
- `Mono`, `Flux`
  비동기 결과 타입

결국 헷갈리는 이유는 선언 방식, 실행 방식, 결과 타입이 한 문맥 안에서 같이 등장하기 때문이다.

이 셋을 분리해서 보면 전체 구조가 훨씬 명확해진다.

## 10. 한 줄 요약

- `RestClient` = 최신 동기 HTTP 클라이언트
- `WebClient` = 비동기 HTTP 클라이언트
- `Feign`, `@HttpExchange` = 선언형 클라이언트 방식
- `Flux` = 비동기 데이터 흐름 타입
