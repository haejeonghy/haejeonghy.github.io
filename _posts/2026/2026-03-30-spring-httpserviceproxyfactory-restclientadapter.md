---
layout: post
title: Spring의 HttpServiceProxyFactory와 RestClientAdapter 쉽게 이해하기
summary: Spring의 HttpServiceProxyFactory와 RestClientAdapter가 어떤 역할을 하고, 왜 인터페이스 기반 HTTP 클라이언트 구조가 유용한지 쉽게 정리합니다.
date: 2026-03-30 19:39:56 +0900
updated: 2026-03-30 19:39:56 +0900
tag: spring http client
toc: true
comment: false
public: true
---
* TOC
{:toc}

## 1. 예시 코드

```kotlin
val proxyFactory = HttpServiceProxyFactory
    .builderFor(RestClientAdapter.create(restClient))
    .build()

return proxyFactory.createClient<PeopleSleepAccountClient>()
```

위 코드는 외부 HTTP API를 호출하는 클라이언트 객체를 자동으로 만들어주는 코드이다.

직접 HTTP 요청 코드를 매번 작성하는 대신, 인터페이스를 하나 정의해두고 그 인터페이스의 구현체를 Spring이 런타임에 자동 생성하게 만든다.

즉, 목표는 다음과 같다.

- 외부 API를 호출할 때
- `restClient.get().uri(...).retrieve()` 같은 저수준 코드를 반복하지 않고
- 일반 함수 호출처럼 사용할 수 있게 만들기

## 2. 핵심 개념 한 줄 요약

HTTP 호출을 정의한 인터페이스를 기반으로, Spring이 그 인터페이스의 클라이언트 구현체를 자동 생성해주는 구조이다.

## 3. 구성요소별 역할

### 3.1 RestClient

`RestClient`는 실제 HTTP 요청을 보내는 객체이다.

쉽게 말하면 다음 역할을 맡는다.

- URL로 요청 보냄
- 헤더 추가
- 요청 바디 전달
- 응답 수신
- 응답 바디 파싱

즉, 실제 통신 담당이다.

### 3.2 RestClientAdapter

`RestClientAdapter`는 `RestClient`를 `HttpServiceProxyFactory`가 사용할 수 있도록 연결해주는 어댑터이다.

여기서 어댑터(adapter)는 서로 바로 연결되지 않는 두 대상을 이어주는 중간 다리라고 보면 된다.

즉, 역할은 다음과 같이 나뉜다.

- `RestClient`는 실제 HTTP 호출 담당
- `HttpServiceProxyFactory`는 인터페이스 구현체 생성 담당
- `RestClientAdapter`는 둘을 연결

### 3.3 HttpServiceProxyFactory

`HttpServiceProxyFactory`는 인터페이스 기반 HTTP 클라이언트 구현체를 만들어주는 공장이다.

예를 들어 `PeopleSleepAccountClient`라는 인터페이스가 있으면, 그 인터페이스를 구현한 객체를 런타임에 동적으로 만들어준다.

즉, 내가 직접 구현 클래스를 만들지 않아도 Spring이 대신 만들어준다.

### 3.4 createClient<PeopleSleepAccountClient>()

이 코드는 `PeopleSleepAccountClient`의 구현체를 생성하는 부분이다.

여기서 중요한 점은 다음과 같다.

- 이 시점에 바로 API를 호출하는 것은 아니다.
- 이 시점에는 클라이언트 객체를 생성할 뿐이다.
- 실제 HTTP 호출은 나중에 그 객체의 메서드를 호출할 때 일어난다.

예를 들면 다음과 같다.

```kotlin
val client = proxyFactory.createClient<PeopleSleepAccountClient>()
client.getSleepAccounts()
```

이 경우 실제 HTTP 요청은 `createClient()`가 아니라 `getSleepAccounts()` 호출 시점에 발생한다.

## 4. 왜 이런 구조를 쓰는가

이 구조가 없으면 외부 API를 호출할 때마다 이런 코드를 직접 써야 한다.

```kotlin
val response = restClient.post()
    .uri("/sleep-accounts")
    .body(request)
    .retrieve()
    .body(Response::class.java)
```

이 방식의 문제는 다음과 같다.

- 호출 코드가 여기저기 흩어진다
- URL, header, body, retrieve 코드가 반복된다
- 서비스 코드가 HTTP 세부 구현에 오염된다
- 어떤 API가 있는지 한눈에 보기 어렵다

반대로 인터페이스 기반으로 만들면, API 명세를 한 곳에 모을 수 있다.

예를 들면 다음과 같다.

```kotlin
interface PeopleSleepAccountClient {
    fun getSleepAccounts(): SleepAccountsResponse
}
```

이렇게 하면 사용하는 쪽은 그냥 함수 호출처럼 쓸 수 있다.

## 5. 없으면 어떤 불편함이 있나

이 구조가 없더라도 외부 API 호출 자체는 가능하다. 다만 불편해진다.

### 5.1 HTTP 호출 코드를 매번 직접 작성해야 한다

매 요청마다 다음 같은 요소를 직접 적어야 한다.

- endpoint
- header
- body
- retrieve
- 응답 파싱

즉, 저수준 HTTP 호출 코드가 반복된다.

### 5.2 서비스 코드가 지저분해진다

서비스 로직 안에 HTTP 호출 코드가 계속 섞이면 비즈니스 로직보다 요청 조립 코드가 더 눈에 띄게 된다.

예를 들어 외부 기관 연동 로직을 작성한다고 했을 때, 원래 보고 싶은 것은 다음과 같은 내용이다.

- 어떤 외부 시스템에 호출하는가
- 어떤 조건에서 요청하는가
- 실패 시 어떻게 처리하는가

그런데 실제 코드는 아래 같은 세부 구현으로 가득 차기 쉽다.

- URL 문자열
- 헤더 세팅
- 요청 바디 작성
- 응답 바디 파싱
- 에러 처리

### 5.3 API 명세가 한눈에 안 보인다

인터페이스로 모아두면 이 시스템이 어떤 외부 API를 쓰는지 보기 쉽다.

반면 직접 `RestClient`를 여기저기 호출하면 외부 API의 구조가 서비스 코드 속에 흩어져 버린다.

### 5.4 중복 코드가 늘어난다

외부 API가 여러 개일수록 공통 요소가 많다.

예를 들면 다음과 같다.

- base URL
- 인증 헤더
- timeout
- 공통 에러 처리
- 공통 직렬화 / 역직렬화

이런 요소를 통일하기가 인터페이스 기반 구조에서 더 쉽다.

## 6. 카페 시스템 비유

이 구조를 카페 시스템으로 비유하면 이해하기 쉽다.

- `PeopleSleepAccountClient` = 메뉴판
- `RestClient` = 실제 주문을 전달하는 직원
- `HttpServiceProxyFactory` = 메뉴판을 보고 주문 처리 직원을 만들어주는 공장
- `RestClientAdapter` = 공장과 직원을 연결하는 통역기

즉, 손님은 메뉴판에서 메뉴를 고르기만 하면 된다.

직접 호출 방식은 손님이 매번 이런 걸 직접 해야 하는 것과 비슷하다.

- 주문서 손으로 작성
- 전달 직원 호출
- 주소 적기
- 응답 확인
- 문제 생기면 직접 처리

반면 지금 구조는 손님이 메뉴 이름만 말하면 뒤에서 다 처리되는 방식이다.

## 7. 내가 이해한 핵심 정리

### 7.1 이 구조의 목적

외부 HTTP API를 인터페이스 기반으로 선언하고, 그 인터페이스의 구현체를 자동 생성해서 일반 함수 호출처럼 사용할 수 있게 하는 것이다.

### 7.2 각 객체의 역할

- `RestClient`
실제 HTTP 요청을 보내고 응답을 받는 객체
- `RestClientAdapter`
`RestClient`를 `HttpServiceProxyFactory`가 사용할 수 있도록 연결하는 객체
- `HttpServiceProxyFactory`
인터페이스 기반 HTTP 클라이언트 구현체를 만들어주는 공장

### 7.3 이 구조가 없을 때의 문제

- endpoint, header, body, retrieve 같은 코드를 매번 직접 써야 함
- 서비스 코드가 중복되고 지저분해짐
- 외부 API 명세가 흩어짐
- 유지보수가 불편해짐

## 8. 헷갈리기 쉬운 포인트

### 8.1 인터페이스를 생성하는 게 아니다

정확히 말하면 인터페이스의 구현체를 생성하는 것이다.

틀린 표현은 다음과 같다.

- 인터페이스를 생성한다

맞는 표현은 다음과 같다.

- 인터페이스의 구현체를 생성한다
- 프록시 객체를 생성한다

### 8.2 createClient()가 API 호출은 아니다

`createClient()`는 클라이언트 객체를 만드는 단계이다.

실제 API 호출은 그 객체의 메서드를 호출할 때 발생한다.

즉, 다음처럼 이해하면 된다.

- `createClient()` = 전화기 개통
- `client.someMethod()` = 실제 통화

## 9. 마무리

처음 보면 이 구조는 추상적이고 어렵게 느껴질 수 있다. 하지만 본질은 단순하다.

외부 HTTP API 호출을 직접 저수준 코드로 반복하지 않고, 인터페이스 기반으로 선언해서 더 읽기 쉽고 유지보수하기 쉬운 구조로 바꾸는 것이다.

실무에서는 특히 다음 조건이 많을수록 유용하다.

- 연동 API가 여러 개다
- 공통 헤더가 있다
- 공통 에러 처리가 필요하다
- 요청 / 응답 DTO가 많다
- 서비스 코드에서 HTTP 세부 구현을 숨기고 싶다

이럴 때 `HttpServiceProxyFactory` 기반 구조가 깔끔하게 작동한다.
