---
layout: post
title: Reactive와 Async의 차이 정리
summary: Reactive와 Async가 왜 자주 같이 언급되는지, 무엇이 공통점이고 어디서 갈라지는지, blocking과 non-blocking까지 포함해 상세하게 정리합니다.
date: 2026-05-31 15:20:00 +0900
updated: 2026-05-31 15:20:00 +0900
tag: reactive async webflux mono flux non-blocking blocking
toc: true
comment: false
public: true
---
- TOC
  {:toc}

## 1. 왜 `reactive`와 `async`가 자꾸 헷갈릴까

`reactive`와 `async`는 둘 다 "결과를 지금 바로 받지 않는다"는 느낌을 주기 때문에 자주 같이 언급된다.

예를 들어 아래 같은 말들은 일상적으로 섞여서 사용된다.

- 비동기 처리
- 논블로킹 처리
- `Mono`, `Flux`
- 이벤트 스트림
- `CompletableFuture`
- callback

문제는 이것들이 전부 같은 층위의 개념은 아니라는 점이다.

어떤 것은 실행 방식이고, 어떤 것은 프로그래밍 모델이며, 어떤 것은 구체적인 타입이다.

그래서 먼저 결론부터 짧게 말하면 이렇다.

- `async`
  결과를 나중에 받는 실행 방식
- `reactive`
  나중에 도착하는 값의 흐름을 선언적으로 다루는 프로그래밍 모델

즉, 둘은 겹치는 부분이 있지만 같은 말은 아니다.

## 2. 가장 짧게 요약하면

한 줄씩만 먼저 정리하면 다음과 같다.

- `async`
  작업 완료를 기다리지 않고, 나중에 결과를 받는다.
- `reactive`
  나중에 도착하는 값이나 이벤트의 흐름을 조합하고 전파하고 처리한다.

이 두 문장을 비교하면 차이가 보인다.

- `async`는 "언제 결과를 받느냐"에 가깝다.
- `reactive`는 "그 결과의 흐름을 어떻게 다루느냐"에 가깝다.

## 3. 공통점부터 보면 이해가 쉽다

`reactive`와 `async`는 완전히 무관한 개념은 아니다.

둘 다 아래 같은 문제를 다루는 데 자주 등장한다.

- 응답이 늦게 오는 작업
- 네트워크 호출
- 파일 I/O
- 메시지 처리
- 이벤트 기반 처리
- 여러 작업을 병렬로 처리해야 하는 상황

즉 둘 다 "지금 당장 값이 손에 없는 상황"과 자주 연결된다.

그래서 실무에서는 둘 다 아래 특징을 공유하는 것처럼 보인다.

- 결과를 바로 반환하지 않을 수 있다
- 작업 완료 시점이 늦을 수 있다
- 콜백이나 후속 처리 개념이 등장한다
- 여러 작업을 겹쳐 처리할 수 있다

바로 이 공통점 때문에 둘을 같은 뜻처럼 오해하기 쉽다.

## 4. 하지만 초점은 다르다

핵심 차이는 초점이 다르다는 것이다.

### 4.1 Async의 초점

`async`의 초점은 "작업이 끝날 때까지 현재 흐름을 붙잡아 두지 않는 것"이다.

예를 들면:

- 함수를 호출한다
- 결과는 아직 준비되지 않았다
- 호출한 쪽은 계속 다른 일을 한다
- 결과가 준비되면 나중에 전달받는다

즉, `async`는 실행 타이밍과 대기 방식에 더 가깝다.

### 4.2 Reactive의 초점

`reactive`의 초점은 "값이 흘러오는 과정을 하나의 흐름으로 보고 조합하는 것"이다.

예를 들면:

- 값 하나가 나중에 올 수 있다
- 값 여러 개가 계속 올 수 있다
- 그 값을 `map`, `filter`, `flatMap`, `zip`으로 가공할 수 있다
- 에러도 흐름 안에서 처리할 수 있다
- 여러 흐름을 합치거나 분기할 수 있다

즉, `reactive`는 단순히 "나중에 받는다"에서 끝나지 않고, 그 나중에 오는 데이터 흐름 전체를 다루는 방식이다.

## 5. 비유로 보면 더 분명해진다

카페 주문 시스템으로 비유해보자.

### 5.1 Async

손님이 주문을 하고 자리에 앉아서 잡지를 본다.

주문 직후 커피를 받는 것은 아니고, 나중에 준비가 되면 전달받는다.

이 상황의 핵심은 다음과 같다.

- 손님은 결과를 바로 받지 않는다
- 손님은 기다리는 동안 다른 행동을 할 수 있다
- 결과는 나중에 온다

이건 `async`를 설명하기 좋은 비유이다.

### 5.2 Reactive

주문이 들어오면 내부에서는 여러 흐름이 동시에 움직일 수 있다.

- 결제 흐름
- 음료 제조 흐름
- 빵 준비 흐름
- 포장 흐름
- 전달 흐름

어떤 주문은 빵이 없을 수도 있고, 어떤 주문은 음료 두 잔일 수도 있다.

각 흐름은 준비된 결과를 다음 단계로 넘기고, 마지막에는 한 주문 단위로 다시 조합된다.

이 상황의 핵심은 다음과 같다.

- 작업이 흐름으로 나뉜다
- 흐름이 분기될 수 있다
- 다시 합쳐질 수 있다
- 준비된 것부터 다음 단계로 전달된다
- 주문이 여러 건 연속으로 흘러들어올 수 있다

이건 `reactive`를 설명하기 좋은 비유이다.

즉:

- `async`는 손님이 나중에 결과를 받는다는 관점
- `reactive`는 내부 처리 흐름을 어떻게 모델링하느냐의 관점

이라고 보면 된다.

## 6. 코드로 보면 차이가 더 분명하다

같은 사용자 조회라는 요구사항을 두 방식으로 비교해보자.

### 6.1 Async 스타일 예시

`CompletableFuture`를 사용하면 이런 식이다.

```kotlin
fun getUserAsync(id: Long): CompletableFuture<UserResponse> {
    return CompletableFuture.supplyAsync {
        userApi.getUser(id)
    }
}
```

호출하는 쪽은 아래처럼 사용할 수 있다.

```kotlin
getUserAsync(1L)
    .thenApply { user -> user.name }
    .thenAccept { name -> println(name) }
```

이 코드는 분명 비동기이다.

하지만 여기서 핵심은 "작업 하나의 완료를 나중에 받는다"는 점이다.

즉 `async` 특성이 강하다.

### 6.2 Reactive 스타일 예시

`Mono`를 사용하면 이런 식이다.

```kotlin
fun getUser(id: Long): Mono<UserResponse> {
    return webClient.get()
        .uri("/users/{id}", id)
        .retrieve()
        .bodyToMono(UserResponse::class.java)
}
```

호출하는 쪽은 아래처럼 이어서 조합한다.

```kotlin
getUser(1L)
    .map { user -> user.name }
    .flatMap { name -> auditService.write(name) }
    .onErrorResume { ex -> Mono.empty() }
```

여기서 핵심은 단순히 비동기라는 것만이 아니다.

- 결과를 흐름으로 다룬다
- 후속 단계를 조합한다
- 에러를 흐름 안에서 처리한다
- 다른 흐름과 합칠 수 있다

즉 `reactive` 특성이 강하다.

## 7. 여러 작업을 합칠 때 차이가 더 잘 보인다

실무에서는 사용자 정보와 주문 정보를 같이 조회해야 할 때가 많다.

### 7.1 Async에서의 조합

```kotlin
fun getUserAndOrders(id: Long): CompletableFuture<UserWithOrders> {
    val userFuture = getUserAsync(id)
    val ordersFuture = getOrdersAsync(id)

    return userFuture.thenCombine(ordersFuture) { user, orders ->
        UserWithOrders(user, orders)
    }
}
```

이것도 충분히 강력하다.

여러 비동기 작업을 병렬로 돌리고 합칠 수 있다.

즉, `async`가 단일 작업만 다룬다는 뜻은 아니다.

### 7.2 Reactive에서의 조합

```kotlin
fun getUserAndOrders(id: Long): Mono<UserWithOrders> {
    val userMono = getUser(id)
    val ordersMono = getOrders(id)

    return Mono.zip(userMono, ordersMono)
        .map { tuple ->
            UserWithOrders(tuple.t1, tuple.t2)
        }
}
```

reactive에서도 여러 흐름을 합칠 수 있다.

다만 느낌이 조금 다르다.

- `CompletableFuture`는 완료될 작업들을 합치는 느낌
- `Mono`, `Flux`는 데이터 흐름 자체를 연산으로 조합하는 느낌

이 차이가 작아 보일 수 있지만, 복잡한 처리에서는 꽤 크게 느껴진다.

## 8. `Flux`가 등장하면 차이는 더 커진다

`CompletableFuture`는 보통 "미래의 결과 하나"를 다룬다.

반면 reactive는 결과가 여러 개일 수도 있다.

```kotlin
fun getOrders(id: Long): Flux<OrderResponse> {
    return webClient.get()
        .uri("/users/{id}/orders", id)
        .retrieve()
        .bodyToFlux(OrderResponse::class.java)
}
```

이 경우 주문 목록은 하나의 결과 객체가 아니라, 여러 값이 흘러오는 스트림처럼 다뤄진다.

즉, reactive는 다음을 자연스럽게 다룬다.

- 0개 이상의 값
- 지속적으로 들어오는 이벤트
- 스트리밍 응답
- 실시간 데이터 흐름

이 지점에서 `async`와 `reactive`의 차이가 더 분명해진다.

`async`는 흔히 "나중에 올 하나의 완료"에 강하고, `reactive`는 "나중에 올 하나 또는 여러 개의 흐름"에 강하다.

## 9. `async`는 곧 `non-blocking`일까

이 부분도 많이 헷갈린다.

정답은 항상 그렇지는 않다는 것이다.

### 9.1 Async와 blocking

비동기로 작업을 시작했더라도 내부 구현이 다른 스레드에서 blocking I/O를 할 수 있다.

예를 들어 `CompletableFuture.supplyAsync` 안에서 동기 HTTP 호출을 하면:

- 호출한 현재 스레드는 바로 반환받는다
- 하지만 작업을 수행하는 다른 스레드는 내부에서 기다릴 수 있다

즉:

- 호출자 입장에서는 async
- 내부 자원 사용 관점에서는 blocking

일 수 있다.

### 9.2 Reactive와 non-blocking

reactive는 흔히 non-blocking과 같이 언급되지만, 이것도 자동으로 보장되는 것은 아니다.

예를 들어 reactive 체인 안에서 `.block()`을 호출하거나, blocking JDBC 호출을 무심코 섞으면 장점이 줄어든다.

즉:

- reactive는 non-blocking과 잘 맞는다
- 하지만 reactive 코드라고 해서 항상 non-blocking인 것은 아니다

이 점을 분리해서 보는 것이 중요하다.

## 10. 그러면 관계를 어떻게 이해해야 할까

관계를 한 번에 정리하면 아래처럼 볼 수 있다.

### 10.1 Async

- 실행 방식에 가깝다
- 결과를 나중에 받는다
- 하나의 미래 결과를 다루는 경우가 많다

### 10.2 Reactive

- 프로그래밍 모델에 가깝다
- 값의 흐름을 다룬다
- 하나 또는 여러 개의 비동기 데이터를 다룬다
- 조합, 전파, 에러 처리, 흐름 제어가 중요하다

### 10.3 겹치는 지점

- reactive 코드는 비동기적으로 동작하는 경우가 많다
- async 작업도 체이닝과 조합을 할 수 있다
- 둘 다 I/O 중심 시스템에서 자주 등장한다

즉, 둘은 교집합이 있지만 포함 관계로 단순화하면 오해가 생긴다.

## 11. "`reactive`가 `async`보다 더 상위 개념인가?"라는 질문

이 질문도 자주 나온다.

완전히 수학적으로 딱 잘라 말하기는 어렵지만, 실무 감각으로는 아래처럼 이해하는 편이 편하다.

- `async`는 "기다리지 않고 나중에 결과를 받는 실행 방식"
- `reactive`는 "그 나중에 오는 값을 흐름으로 조합하는 모델"

그래서 보통은:

- 모든 reactive가 async 성격을 포함할 수는 있다
- 하지만 모든 async 코드가 reactive는 아니다

라고 이해하면 큰 무리는 없다.

예를 들어:

- callback
- `Future`
- `CompletableFuture`

는 async라고 말하기 좋다.

반면:

- `Mono`
- `Flux`
- Rx 스트림

은 reactive라고 말하기 좋다.

## 12. 파이프라인과는 또 어떻게 다를까

이것도 같이 많이 헷갈린다.

- 파이프라인
  단계를 순서대로 거치며 처리하는 구조
- reactive
  비동기적으로 도착하는 값의 흐름을 조합하고 제어하는 모델

즉 파이프라인은 구조이고, reactive는 더 큰 처리 방식이다.

동기식 문자열 처리도 파이프라인일 수 있다.

```kotlin
val result = raw
    .trim()
    .uppercase()
    .replace("A", "B")
```

이건 파이프라인이지만 reactive는 아니다.

반면 `Flux` 체인은 reactive 파이프라인이라고 부를 수 있다.

즉, reactive는 파이프라인을 포함할 수 있지만 파이프라인과 같은 뜻은 아니다.

## 13. 실무에서는 언제 무엇을 떠올리면 좋을까

### 13.1 Async가 먼저 떠오르는 경우

- 백그라운드 작업 하나를 비동기로 실행하고 싶다
- 오래 걸리는 작업 완료 시점만 나중에 받으면 된다
- `Future`, `CompletableFuture`, callback 정도면 충분하다

### 13.2 Reactive가 먼저 떠오르는 경우

- `Mono`, `Flux` 기반 시스템을 쓰고 있다
- 여러 비동기 흐름을 합치고 싶다
- 스트리밍 응답이나 지속적인 이벤트를 다뤄야 한다
- backpressure 같은 흐름 제어가 중요하다

즉, 단순히 "비동기면 다 reactive"는 아니다.

## 14. 헷갈리지 않기 위한 실전 문장

아래 문장들로 구분해두면 실무에서 꽤 편하다.

- `async`
  "이 작업은 결과를 나중에 돌려준다."
- `reactive`
  "이 값은 나중에 오며, 그 흐름을 연산으로 조합한다."
- `non-blocking`
  "스레드가 작업 완료까지 묶여서 기다리지 않는다."
- `blocking`
  "결과가 올 때까지 스레드가 대기한다."

즉, 이 네 개는 서로 관련은 있지만 같은 단어가 아니다.

## 15. 마무리

정리하면 `async`와 `reactive`는 비슷해 보이지만 질문의 방향이 다르다.

- `async`
  결과를 언제 받는가
- `reactive`
  나중에 오는 값을 어떤 흐름으로 다룰 것인가

둘 다 I/O 중심 시스템에서 강력한 도구이지만, 같은 개념으로 취급하면 구조를 잘못 이해하게 된다.

실무적으로는 아래 한 줄로 기억해도 괜찮다.

> `async`는 나중에 결과를 받는 실행 방식이고, `reactive`는 나중에 오는 값의 흐름을 다루는 프로그래밍 모델이다.
