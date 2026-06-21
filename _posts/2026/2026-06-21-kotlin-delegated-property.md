---
layout: post
title: Kotlin 위임 프로퍼티는 왜 쓰는가
summary: Kotlin 위임 프로퍼티를 카페 주문 예제로 정리합니다. 단순한 변수로 충분한 경우와, 검증·정규화·변경 추적 같은 공통 규칙을 재사용해야 할 때 위임 프로퍼티가 왜 유용한지 설명합니다.
date: 2026-06-21 15:40:00 +0900
updated: 2026-06-21 15:40:00 +0900
tag: kotlin oop delegated-property delegation property
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 처음엔 이런 생각이 든다

위임 프로퍼티를 처음 보면 보통 이런 생각이 먼저 든다.

- 그냥 변수 쓰면 되는 거 아닌가
- 왜 굳이 `by`를 붙여서 복잡하게 쓰지

이 반응은 맞다.  
단순히 값 하나 저장하는 용도라면 그냥 변수 쓰는 게 맞다.

```kotlin
var requestNote: String = "얼음은 보통으로 주세요."
```

이 경우 위임 프로퍼티를 쓸 이유는 거의 없다.

## 2. 그럼 언제 그냥 변수로 부족해지는가

실무에서는 프로퍼티가 단순히 값만 들고 있는 경우보다, 값을 읽거나 바꿀 때 규칙이 필요한 경우가 많다.

예를 들면:

- 값을 넣기 전에 공백을 정리하고 싶다
- 빈 문자열은 막고 싶다
- 값이 바뀔 때 로그를 남기고 싶다
- 여러 프로퍼티에 같은 규칙을 반복 적용하고 싶다

이런 로직을 일반 변수로 처리하려면 보통 setter를 직접 만들거나, 값을 바꿀 때마다 수동으로 검증 코드를 넣게 된다.

그렇게 되면:

- 규칙이 여러 곳에 복붙되고
- 누군가는 빠뜨리게 되고
- 나중에 정책이 바뀌면 수정할 위치가 늘어난다

## 3. 카페 주문 예제로 보기

카페 주문을 받는다고 하자.  
`menuName`과 `customerName` 모두 아래 규칙을 따라야 한다.

- 앞뒤 공백 제거
- 빈 문자열 금지
- 값 변경 시 로그 출력

그 규칙을 위임 프로퍼티로 분리하면 이렇게 만들 수 있다.

```kotlin
class TrimmedNonEmptyText(
    private var value: String,
) {
    init {
        value = normalize(value, "initial value")
    }

    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return value
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, newValue: String) {
        val normalized = normalize(newValue, property.name)
        println("${property.name} 변경: '$value' -> '$normalized'")
        value = normalized
    }

    private fun normalize(text: String, fieldName: String): String {
        val trimmed = text.trim()
        require(trimmed.isNotEmpty()) { "$fieldName 값은 비어 있을 수 없습니다." }
        return trimmed
    }
}
```

이제 주문 객체는 이렇게 쓸 수 있다.

```kotlin
class CafeDrinkOrder(
    menuName: String,
    customerName: String,
) {
    var menuName: String by TrimmedNonEmptyText(menuName)
    var customerName: String by TrimmedNonEmptyText(customerName)
}
```

핵심은 이 부분이다.

```kotlin
var menuName: String by TrimmedNonEmptyText(menuName)
var customerName: String by TrimmedNonEmptyText(customerName)
```

즉 `menuName`, `customerName`은 값을 직접 들고 있는 것이 아니라, 읽기/쓰기 규칙을 `TrimmedNonEmptyText`에게 맡긴다.

## 4. 왜 이게 그냥 변수보다 나은가

이 구조의 장점은 "값"이 아니라 "프로퍼티 접근 규칙"을 재사용할 수 있다는 점이다.

만약 일반 변수로 처리하면 보통 이런 식이 된다.

```kotlin
class CafeDrinkOrder(
    menuName: String,
    customerName: String,
) {
    var menuName: String = menuName
        set(value) {
            val trimmed = value.trim()
            require(trimmed.isNotEmpty()) { "menuName 값은 비어 있을 수 없습니다." }
            println("menuName 변경: '$field' -> '$trimmed'")
            field = trimmed
        }

    var customerName: String = customerName
        set(value) {
            val trimmed = value.trim()
            require(trimmed.isNotEmpty()) { "customerName 값은 비어 있을 수 없습니다." }
            println("customerName 변경: '$field' -> '$trimmed'")
            field = trimmed
        }
}
```

문제는 규칙이 거의 같은데 코드가 반복된다는 점이다.

- `trim()`
- 빈 값 검사
- 로그 출력

이 로직이 프로퍼티마다 복붙된다.

위임 프로퍼티를 쓰면:

- 규칙은 한 곳에만 쓴다
- 여러 프로퍼티에 붙일 수 있다
- 정책이 바뀌면 delegate만 고치면 된다

즉 단순한 문법 장식이 아니라, 공통 정책을 부품처럼 재사용하는 방법이다.

## 5. 위임 프로퍼티는 무엇을 위임하는가

클래스 위임과 비교하면 더 이해가 쉽다.

- 클래스 위임
  클래스 전체 기능을 다른 객체에 맡긴다
- 위임 프로퍼티
  특정 프로퍼티의 읽기/쓰기 동작을 다른 객체에 맡긴다

이번 예시에서 `menuName`은 문자열 값을 직접 처리하지 않는다.  
값을 읽거나 바꾸는 규칙을 `TrimmedNonEmptyText`가 대신 처리한다.

즉:

- 프로퍼티는 "보이는 창구"
- delegate 객체는 "실제 처리 담당자"

라고 이해하면 된다.

## 6. 왜 실무에서 자주 쓰이는가

위임 프로퍼티가 자주 쓰이는 이유는 이런 공통 규칙이 실제 코드에서 매우 자주 등장하기 때문이다.

예를 들면:

- 처음 접근할 때만 생성하고 싶은 값
- 값이 바뀌면 화면을 갱신해야 하는 상태
- 변경 이력을 남겨야 하는 설정값
- 여러 필드에 공통으로 적용해야 하는 검증 규칙

이런 요구가 많기 때문에 Kotlin은 아예 내장 위임 프로퍼티도 제공한다.

- `lazy`
  처음 사용할 때만 생성
- `Delegates.observable`
  값이 바뀔 때 알림
- `Delegates.vetoable`
  잘못된 변경 거부

즉 위임 프로퍼티는 "드문 특수 기능"이 아니라, 프로퍼티에 붙는 공통 로직을 깔끔하게 분리하기 위한 실용 기능에 가깝다.

## 7. 언제 쓰고 언제 안 쓰면 되는가

그냥 변수가 더 나은 경우:

- 단순히 값만 저장하면 된다
- 검증이나 로깅이 필요 없다
- 한 군데에서만 잠깐 쓰는 데이터다

위임 프로퍼티가 나은 경우:

- 읽기/쓰기 규칙이 있다
- 같은 규칙을 여러 프로퍼티에 재사용해야 한다
- 정책을 한 곳에서 관리하고 싶다
- `lazy`, `observable` 같은 표준 위임 기능이 바로 맞는다

## 8. 정리

위임 프로퍼티는 "변수를 대신하는 멋있는 문법"이 아니다.

오히려 이렇게 이해하는 편이 정확하다.

- 그냥 변수
  값 저장
- 위임 프로퍼티
  값 저장 + 읽기/쓰기 규칙 재사용

그래서 "왜 이렇게 써야 하지?"라는 질문에 대한 답은 단순하다.

- 단순한 값이면 굳이 안 써도 된다
- 하지만 프로퍼티에 붙는 규칙이 반복되기 시작하면 위임 프로퍼티가 훨씬 낫다

즉 위임 프로퍼티의 핵심은 값이 아니라 정책의 재사용이다.
