---
layout: post
title: Kotlin의 `by` 클래스 위임은 상속이 아니라 부품 조립에 가깝다
summary: Kotlin의 `by` 클래스 위임을 핫초코 예제로 이해해 보고, 상속과 무엇이 다른지, 왜 유연한지, 장단점은 무엇인지 정리합니다.
date: 2026-06-21 15:20:00 +0900
updated: 2026-06-21 15:20:00 +0900
tag: kotlin oop delegation composition inheritance
toc: true
comment: false
public: true
---

- TOC
  {:toc}

## 1. 왜 `by`가 처음엔 상속처럼 보이는가

Kotlin의 `by` 클래스 위임을 처음 보면 이런 식으로 이해하기 쉽다.

- 이미 구현된 클래스를 재사용한다
- 내가 원하는 메서드만 바꾼다
- 나머지는 기존 구현을 그대로 쓴다

겉으로 보면 상속과 꽤 비슷하다.  
하지만 정확히는 상속이 아니라 위임이다.

- 상속
  부모 클래스를 물려받는다
- 위임
  다른 객체를 들고 있고, 대부분의 일을 그 객체에게 맡긴다

즉 `by`는 "부모를 이어받는 것"보다는 "기본 부품을 사 와서 필요한 부품만 갈아끼우는 것"에 더 가깝다.

## 2. 핫초코 예제로 보면 더 쉽다

예를 들어 핫초코를 만드는 인터페이스가 있다고 하자.

```kotlin
interface HotChocoMaker {
    fun prepareBase()
    fun addTopping()
}
```

기본 핫초코는 이렇게 만들 수 있다.

```kotlin
class BasicHotChocoMaker : HotChocoMaker {
    override fun prepareBase() {
        println("컵에 따뜻한 우유와 초코 파우더를 넣는다.")
    }

    override fun addTopping() {
        println("아무 토핑도 올리지 않는다.")
    }
}
```

이제 마시멜로 핫초코를 만들고 싶다고 하자.  
핫초코 베이스는 그대로 쓰고, 토핑만 바꾸고 싶다.

```kotlin
class MarshmallowHotChocoMaker(
    private val baseMaker: HotChocoMaker,
) : HotChocoMaker by baseMaker {
    override fun addTopping() {
        println("마시멜로를 듬뿍 올린다.")
    }
}
```

핵심은 이 줄이다.

```kotlin
: HotChocoMaker by baseMaker
```

이 뜻은 다음과 같다.

- `HotChocoMaker`의 메서드를 전부 직접 구현하지 않겠다
- 기본 구현은 `baseMaker`에게 맡기겠다
- 대신 내가 바꾸고 싶은 메서드만 직접 구현하겠다

그래서:

- `prepareBase()`는 `BasicHotChocoMaker`의 구현을 그대로 사용한다
- `addTopping()`만 `MarshmallowHotChocoMaker`가 직접 바꾼다

## 3. 상속과는 뭐가 다른가

비슷해 보이지만 관계의 의미가 다르다.

상속 방식은 보통 이런 느낌이다.

```kotlin
open class BasicHotChocoMaker {
    open fun prepareBase() { ... }
    open fun addTopping() { ... }
}

class MarshmallowHotChocoMaker : BasicHotChocoMaker() {
    override fun addTopping() { ... }
}
```

이 경우 `MarshmallowHotChocoMaker`는 `BasicHotChocoMaker`의 자식이다.

- "나는 기본 핫초코 메이커의 한 종류다"

반면 위임 방식은 이런 의미다.

- "나는 핫초코를 만드는 객체다"
- "기본 제조 과정은 저 객체에게 맡긴다"
- "대신 토핑 부분만 내가 바꾼다"

즉:

- 상속은 `is-a` 관계에 가깝다
- 위임은 `has-a` 또는 "맡긴다"에 가깝다

## 4. 왜 Kotlin에서 이 방식이 더 자주 눈에 띄는가

Kotlin 클래스는 기본이 `final`이다.  
그래서 아무 클래스나 Java처럼 바로 상속할 수 없다.

상속하려면 `open`을 붙여야 한다.

```kotlin
open class BasicHotChocoMaker
```

하지만 `by`가 단순히 상속 제한을 우회하려고 만든 기능은 아니다.  
더 중요한 이유는 상속보다 느슨하고 유연한 재사용 방식을 제공하기 때문이다.

상속은 부모 구현에 강하게 묶인다.  
부모가 바뀌면 자식이 의도치 않게 영향을 받을 수 있다.

반면 위임은:

- 인터페이스에 의존하기 쉽고
- 구현체를 갈아끼우기 쉽고
- 공통 기능은 재사용하면서 일부만 바꾸기 좋다

## 5. 내가 이해한 비유: 기본템을 사서 원하는 부품만 갈아끼우기

이 비유가 가장 잘 맞는다.

- 상속
  기본템 몸체를 물려받아 개조하는 느낌
- 위임
  기본템은 그대로 두고, 필요한 부품만 교체하는 느낌

핫초코 예시로 보면:

- `BasicHotChocoMaker`
  기본템
- `MarshmallowHotChocoMaker`
  기본템을 들고 와서
- 베이스 제조는 그대로 맡기고
- 토핑만 교체한 버전

즉 `by`는 "전체를 다시 만들지 않고, 필요한 부분만 바꾸기"에 아주 잘 맞는다.

## 6. `by` 클래스 위임의 장점

### 6.1 결합도가 낮다

부모 클래스 구현에 강하게 묶이기보다, 인터페이스와 위임 대상에 의존한다.

### 6.2 필요한 부분만 바꾸기 쉽다

공통 동작은 위임하고, 내가 원하는 메서드만 직접 구현하면 된다.

### 6.3 구현체를 갈아끼우기 쉽다

`HotChocoMaker`를 구현한 다른 객체를 넣으면 같은 구조를 재사용할 수 있다.

### 6.4 의도가 더 정확할 때가 많다

"나는 저 클래스의 자식이다"보다  
"나는 저 객체의 기능을 활용한다"가 더 자연스러운 경우가 많다.

## 7. 단점도 있다

### 7.1 객체 구조가 한 단계 더 생긴다

상속보다 처음 구조가 약간 더 번거롭게 느껴질 수 있다.

### 7.2 호출 흐름을 따라가야 한다

이 메서드가 내 구현인지, 위임된 객체 구현인지 한 번 더 봐야 할 수 있다.

### 7.3 진짜 부모-자식 관계라면 상속이 더 자연스러울 수 있다

언제나 위임이 정답은 아니다.  
명확한 계층 구조가 필요하다면 상속이 더 읽기 쉬운 경우도 있다.

## 8. 언제 쓰면 좋은가

다음 상황이라면 `by` 클래스 위임이 잘 맞는다.

- 기본 기능은 재사용하고 싶다
- 일부 동작만 바꾸고 싶다
- 인터페이스 기반으로 느슨하게 설계하고 싶다
- 상속보다 조합이 더 자연스러운 모델이다

반대로 이런 경우는 상속이 더 자연스러울 수 있다.

- 부모-자식 관계가 매우 명확하다
- 상태를 깊게 공유해야 한다
- 단순 상속이 훨씬 읽기 쉽다

## 9. 정리

Kotlin의 `by` 클래스 위임은 "상속의 대체 문법"으로 보기보다, "구성을 더 쉽게 쓰게 해 주는 문법"으로 이해하는 편이 정확하다.

한 줄로 줄이면 이렇다.

- 상속
  몸체를 이어받는다
- 위임
  부품을 조립한다

그래서 `by`를 이해할 때는 "부모 클래스"보다 "기본템과 교체 가능한 부품"을 떠올리는 편이 훨씬 잘 와 닿는다.
