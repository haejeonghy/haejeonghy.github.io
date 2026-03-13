---
layout  : post
title   : Chain of Responsibility 패턴 (책임 연쇄 패턴
summary : '요청을 처리할 수 있는 객체들을 > > > 연결된 체인 형태 >'
date    : 2025-05-13 17:04:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : 디자인패턴
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Chain of Responsibility 패턴 (책임 연쇄 패턴
Created: 2025년 5월 13일 오후 5:04
Tags: 디자인패턴
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

## **🧩 Chain of Responsibility 패턴 (책임 연쇄 패턴)**

### **📌 핵심 개념**

> 요청을 처리할 수 있는 객체들을
> 
> 
> **연결된 체인 형태**
> 

> 요청이 전달되었을 때 각 객체가
> 
> 
> **처리하거나**
> 
> **다음 객체에게 위임**
> 

---

### **🛠️ 특징 및 목적**

| **항목** | **설명** |
| --- | --- |
| **패턴 분류** | 행동(Behavioral) 패턴 |
| **목적** | 요청을 처리할 책임을 여러 객체에 **분산**하고, 각 객체가 순차적으로 처리 |
| **장점** | 결합도 낮음, 객체 추가/삭제 용이, 유연한 처리 흐름 |
| **단점** | 디버깅 어려움, 처리 순서 의존도 존재 |

---

### **⚙️ 구성 요소**

| **구성 요소** | **역할** |
| --- | --- |
| Handler (인터페이스) | 요청 처리 메서드 정의 + 다음 처리자 설정 |
| ConcreteHandler (구체 처리자) | 조건에 맞는 요청을 처리하거나 다음으로 넘김 |
| SetNext(handler) | 체인 구성 (다음 책임자 연결) |
| Handle(request) | 요청 처리 메서드 |

---

### **🧪 Golang 예시 코드**

### **인터페이스 및 처리자 정의**

```
type Handler interface {
	SetNext(handler Handler) Handler
	Handle(request string)
}

type BaseHandler struct {
	next Handler
}

func (b *BaseHandler) SetNext(handler Handler) Handler {
	b.next = handler
	return handler
}

func (b *BaseHandler) HandleNext(request string) {
	if b.next != nil {
		b.next.Handle(request)
	}
}

type AuthHandler struct{ BaseHandler }
func (a *AuthHandler) Handle(request string) {
	if request == "unauthenticated" {
		fmt.Println("인증 실패")
		return
	}
	fmt.Println("인증 통과")
	a.HandleNext(request)
}

type RoleHandler struct{ BaseHandler }
func (r *RoleHandler) Handle(request string) {
	if request == "no-role" {
		fmt.Println("권한 없음")
		return
	}
	fmt.Println("권한 확인 완료")
	r.HandleNext(request)
}

type BusinessHandler struct{ BaseHandler }
func (b *BusinessHandler) Handle(request string) {
	fmt.Println("비즈니스 로직 처리 완료")
}
```

### **체인 구성 및 실행**

```
func main() {
	auth := &AuthHandler{}
	role := &RoleHandler{}
	business := &BusinessHandler{}

	auth.SetNext(role).SetNext(business)

	fmt.Println("== 테스트 1: 정상 요청 ==")
	auth.Handle("valid-user")

	fmt.Println("\n== 테스트 2: 인증 실패 ==")
	auth.Handle("unauthenticated")

	fmt.Println("\n== 테스트 3: 권한 없음 ==")
	auth.Handle("no-role")
}
```

---

### **🧾 요약**

- Handler는 인터페이스로 책임자 역할을 정의
- 각 처리자(ConcreteHandler)는 처리 여부를 판단 후 다음으로 넘김
- SetNext()를 통해 체인을 유연하게 구성 가능

---

### **🏷️ 태그 제안**

#Go #디자인패턴 #행동패턴 #ChainOfResponsibility #책임분산 #GoF패턴

---
