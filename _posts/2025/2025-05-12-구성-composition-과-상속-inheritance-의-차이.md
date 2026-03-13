---
layout  : post
title   : 구성(Composition)과 상속(Inheritance)의 차이
summary : '구성(Composition)과 상속(Inheritance)의 차이'
date    : 2025-05-12 22:14:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : 프로그래밍
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 구성(Composition)과 상속(Inheritance)의 차이
Created: 2025년 5월 12일 오후 10:14
Tags: 프로그래밍
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

**구성(Composition)과 상속(Inheritance)의 차이**

구성과 상속은 객체 지향 프로그래밍에서 **코드를 재사용**하고 **객체의 관계를 정의**하는 두 가지 주요 방법입니다. 각 방법은 서로 다른 철학과 구조를 가지고 있습니다.

---

**📦 1. 구성 (Composition)**

•	**객체가 다른 객체를 포함하는 방식**으로 코드를 재사용하는 방법입니다.

•	**“has-a” 관계**로 표현되며, 객체가 다른 객체의 **기능을 포함**할 수 있게 합니다.

•	**유연하고 확장 가능**하며, 변경에 강한 구조를 제공합니다.

•	런타임에 **객체의 기능을 동적으로 변경**할 수 있는 이점이 있습니다.

**📝 예시 (Go)**

```
package main

import "fmt"

// 기본 커피
type Coffee struct {
	Name string
}

func (c Coffee) GetDescription() string {
	return c.Name
}

// 시럽을 추가하는 데코레이터
type SyrupDecorator struct {
	Coffee
	Flavor string
}

func (s SyrupDecorator) GetDescription() string {
	return s.Coffee.GetDescription() + " with " + s.Flavor + " Syrup"
}

func main() {
	basicCoffee := Coffee{Name: "Espresso"}
	vanillaCoffee := SyrupDecorator{Coffee: basicCoffee, Flavor: "Vanilla"}

	fmt.Println(basicCoffee.GetDescription())  // Espresso
	fmt.Println(vanillaCoffee.GetDescription()) // Espresso with Vanilla Syrup
}
```

•	**장점:**

•	코드의 재사용성이 높음

•	의존성이 적어 유지보수가 용이

•	다형성을 쉽게 구현 가능

•	객체를 동적으로 구성하여 기능을 추가할 수 있음

•	**단점:**

•	**상속**에 비해 초기 설정이 복잡할 수 있음

•	객체 간의 의존 관계가 깊어질 수 있음

---

**🗂️ 2. 상속 (Inheritance)**

•	**클래스가 다른 클래스의 특성과 메서드를 물려받는 방식**으로 코드를 재사용하는 방법입니다.

•	**“is-a” 관계**로 표현되며, 부모 클래스의 **모든 속성과 메서드를 자식 클래스가 상속**받습니다.

•	코드가 **더 간단**해지고, 부모-자식 관계가 명확해집니다.

**📝 예시 (Python)**

```
class Coffee:
    def __init__(self, name):
        self.name = name

    def get_description(self):
        return self.name

class VanillaCoffee(Coffee):
    def __init__(self):
        super().__init__("Vanilla Coffee")

basic_coffee = Coffee("Espresso")
vanilla_coffee = VanillaCoffee()

print(basic_coffee.get_description())  # Espresso
print(vanilla_coffee.get_description())  # Vanilla Coffee
```

•	**장점:**

•	코드의 간결성

•	계층 구조의 명확성

•	부모의 기능을 그대로 상속 가능

•	**단점:**

•	**강한 결합** (Tight Coupling)

•	다중 상속의 복잡성

•	코드의 유연성 감소

---

**🔄 3. 구성 vs 상속의 주요 차이점**

| **특성** | **구성 (Composition)** | **상속 (Inheritance)** |
| --- | --- | --- |
| **관계** | **“has-a”** | **“is-a”** |
| **유연성** | 높음 (런타임 변경 가능) | 낮음 (컴파일 타임 고정) |
| **의존성** | 낮음 | 높음 (부모-자식 의존) |
| **코드 재사용성** | 높음 | 중간 |
| **다형성** | 지원 (인터페이스 기반) | 지원 (클래스 기반) |
| **확장성** | 뛰어남 | 제한적 (계층 깊이에 따른 복잡성) |

---

**📊 언제 구성(Composition)을 쓰고, 언제 상속(Inheritance)을 써야 할까?**

•	**구성 (Composition)**

•	동적인 기능 추가가 필요한 경우

•	상속 계층이 너무 깊어지는 것을 방지하고 싶을 때

•	인터페이스를 통한 유연한 설계를 원할 때

•	**상속 (Inheritance)**

•	계층 구조가 명확하고 변화 가능성이 낮을 때

•	기본적인 속성이나 메서드를 모든 하위 클래스가 공유해야 할 때

•	자식 클래스가 부모 클래스의 모든 기능을 필요로 할 때

---
