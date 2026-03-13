---
layout  : post
title   : AOP (Aspect Oriented Programming)
summary : 'AOP는 Aspect-Oriented Programming (관점 지향 프로그래밍)을 의미합니다.'
date    : 2025-06-27 18:59:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : 스프링
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# AOP (Aspect Oriented Programming)
Created: 2025년 6월 27일 오후 6:59
Tags: 스프링
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## AOP란?

AOP는 **Aspect-Oriented Programming (관점 지향 프로그래밍)**을 의미합니다.

핵심 비즈니스 로직과 **공통 기능(부가 기능)**을 분리하여, **중복 없이** 코드에 적용할 수 있도록 해주는 프로그래밍 패러다임입니다.

### 💡 요약

- **공통 관심사 (cross-cutting concern)** 를 따로 분리
- 핵심 로직 외의 반복 작업을 모듈화 (예: 트랜잭션, 로깅, 보안)
- 코드 가독성과 유지보수성 향상

---

## 예시

### ✨ AOP 미적용 시

```kotlin
class MemberService {
    fun join(member: Member) {
        println("트랜잭션 시작") // 공통 기능
        println("회원 가입 로직 실행") // 핵심 로직
        println("트랜잭션 커밋") // 공통 기능
    }
}

```

→ 모든 서비스 메서드에 **중복 코드** 발생

---

### ✅ AOP 적용 시

```kotlin
@Aspect
class TransactionAspect {

    @Before("execution(* com.example..*Service.*(..))")
    fun startTransaction() {
        println("트랜잭션 시작")
    }

    @AfterReturning("execution(* com.example..*Service.*(..))")
    fun commitTransaction() {
        println("트랜잭션 커밋")
    }
}

```

→ 실제 서비스 로직은 아래처럼 **깔끔하게 유지**됨:

```kotlin
class MemberService {
    fun join(member: Member) {
        println("회원 가입 로직 실행")
    }
}

```

---

## AOP 핵심 용어 정리

| 용어 | 설명 | 예시 |
| --- | --- | --- |
| **Aspect** | 공통 기능을 정의한 모듈 | `TransactionAspect` 클래스 |
| **Advice** | 언제 실행할지를 정의하는 기능 코드 | `@Before`, `@AfterReturning` |
| **Pointcut** | 어떤 메서드에 적용할지 지정하는 규칙 | `"execution(* com.example..*Service.*(..))"` |
| **Join point** | Advice가 적용 가능한 모든 지점 | `join()` 메서드 실행 시점 |
| **Weaving** | Advice를 실제 코드에 연결하는 과정 | 런타임 시 프록시 적용 |

---

## 스프링 AOP의 동작 방식

- **프록시 기반**으로 동작
- 대상 객체를 감싸는 프록시가 메서드 실행 전후로 Advice를 실행함
- 기본적으로 **런타임 기반 AOP** (AspectJ는 컴파일 타임도 가능)

---

## 요약 정리

- 공통 로직(트랜잭션, 로깅 등)을 **모듈화**할 수 있음
- 핵심 비즈니스 로직을 **깨끗하게 유지**할 수 있음
- **스프링에서 널리 사용**됨

---

## 참고자료

- [스프링 공식 AOP 문서](https://docs.spring.io/spring-framework/reference/core/aop.html)
- [Baeldung: Introduction to Spring AOP](https://www.baeldung.com/spring-aop)
