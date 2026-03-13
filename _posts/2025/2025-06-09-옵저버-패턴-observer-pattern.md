---
layout  : post
title   : 옵저버 패턴 (Observer Pattern)
summary : '옵저버 패턴 > > > 일대다 관계 >'
date    : 2025-06-09 21:09:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : 디자인패턴
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 옵저버 패턴 (Observer Pattern)
Created: 2025년 6월 9일 오후 9:09
Tags: 디자인패턴
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## **📘 옵저버 패턴 (Observer Pattern)**

### **✅ 개념 정의**

> 옵저버 패턴
> 
> 
> **일대다 관계**
> 

> 하나의 객체 상태가 변경되면
> 
> 
> **그에 의존하는 여러 객체에 자동으로 알림**
> 

---

### **📌 주요 개념 구성**

| **용어** | **설명** |
| --- | --- |
| **Subject** (주제) | 상태 변화가 발생하는 주체. 옵저버들을 등록/관리 |
| **Observer** (관찰자) | Subject의 상태 변화를 감지하고 반응하는 객체 |
| **Notify()** | 상태가 바뀔 때 등록된 모든 옵저버에게 알림 전송 |

---

### **☕ 예시 시나리오: 카페 시스템**

- 손님들이 음료를 주문하면, 카페가 음료 완성 시 손님에게 알림을 보냄
- 카페: **Subject** 역할
- 손님: **Observer** 역할
- 음료 준비 완료 시 → 모든 손님에게 NotifyAll()

---

### **🧱 Go 코드 예시**

```
package main

import "fmt"

// Observer 인터페이스
type Customer interface {
	Update(drink string)
	GetName() string
}

// Subject 구조체
type Cafe struct {
	customers []Customer
}

// Observer 등록
func (c *Cafe) AddCustomer(customer Customer) {
	c.customers = append(c.customers, customer)
}

// 알림 전송
func (c *Cafe) NotifyAll(drink string) {
	for _, customer := range c.customers {
		customer.Update(drink)
	}
}

// 구체적 Observer 구현
type RegularCustomer struct {
	name string
}

func (rc *RegularCustomer) Update(drink string) {
	fmt.Printf("[알림] %s님! 주문하신 '%s' 준비되었습니다 ☕\n", rc.name, drink)
}

func (rc *RegularCustomer) GetName() string {
	return rc.name
}

// 메인 함수
func main() {
	cafe := &Cafe{}

	alice := &RegularCustomer{name: "앨리스"}
	bob := &RegularCustomer{name: "밥"}

	cafe.AddCustomer(alice)
	cafe.AddCustomer(bob)

	cafe.NotifyAll("아메리카노")
}
```

---

### **💡 실행 결과**

```
[알림] 앨리스님! 주문하신 '아메리카노' 준비되었습니다 ☕
[알림] 밥님! 주문하신 '아메리카노' 준비되었습니다 ☕
```

---

### **✅ 정리 요약**

| **항목** | **설명** |
| --- | --- |
| 패턴 목적 | 상태 변경 시, 관련 객체에 알림 자동 전파 |
| 장점 | 느슨한 결합, 유연한 확장성 |
| 단점 | 옵저버가 많아질수록 복잡도 증가 |
| 활용 사례 | UI 이벤트, Pub/Sub, 상태 알림 시스템 등 |

---
