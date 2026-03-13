---
layout  : post
title   : Go에서 import cycle이 금지되는 이유
summary : 'A 패키지가 B를 import하고, B가 다시 A를 import하는 순환 참조 관계를 뜻함. >'
date    : 2025-05-17 20:46:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Go에서 import cycle이 금지되는 이유
Created: 2025년 5월 17일 오후 8:46
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# 🔄 Go에서 import cycle이 금지되는 이유

## 📌 import cycle이란?

> A 패키지가 B를 import하고, B가 다시 A를 import하는 순환 참조 관계를 뜻함.
> 

### 예시

```go
// a/a.go
package a
import "myapp/b"

// b/b.go
package b
import "myapp/a"

```

### 컴파일 시 오류

```
import cycle not allowed

```

---

## 🚫 왜 금지되는가?

| 이유 | 설명 |
| --- | --- |
| ❌ 정적 분석 불가 | 어떤 패키지를 먼저 컴파일할지 결정할 수 없음 |
| ❌ 컴파일 타이밍 문제 | 초기화 순서가 꼬여서 오류 발생 가능 |
| ❌ 의존성 혼란 | 유지보수, 테스트, 리팩터링이 어려워짐 |
| ❌ Go 철학 위배 | 단순하고 명확한 구조를 지향하는 Go의 철학에 반함 |

---

## 📊 다른 언어와의 차이

| 언어 | 특징 |
| --- | --- |
| Java, Python | 런타임 기반으로 이론상 순환 참조 허용 |
| Go | **정적 컴파일 기반**으로 순서 보장 필요 → 순환 불가 |

---

## ✅ 해결 방법

### 1. 공통 인터페이스 분리

```go
// common/common.go
package common

type Service interface {
    DoSomething()
}

```

→ `a`, `b`가 공통 인터페이스만 참조하도록 설계

---

### 2. 의존 방향 재설계

- handler → service → repository 순으로 흐르도록 고정
- 하위 레이어가 상위 레이어를 import하지 않도록 주의

---

### 3. 의존성 역전 (DIP)

- 인터페이스를 사용해 **의존 방향을 반대로 전환**
- 상위 레이어에 인터페이스 정의, 하위가 구현

---

## 🎯 결론

- Go는 **정적 컴파일과 빠른 빌드**를 위해 import cycle을 금지함
- 의존성 구조를 명확히 하고, 인터페이스 분리 등으로 해결할 것

---

## 🗂️ 태그 추천

`#Go` `#ImportCycle` `#패키지구조` `#의존성관리` `#CleanArchitecture`
