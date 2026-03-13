---
layout  : post
title   : 데코레이터 패턴 (Decorator Pattern)
summary : '데코레이터(Decorator) 패턴은 객체 지향 설계에서 자주 사용되는 구조적 디자인 패턴 중 하나로, 기존 객체에 새로운 기능을 동적으로 추가할 때 사용됩니다. 이 패턴은 상속을 사용하지 않고 객체의 기능을 확장할'
date    : 2025-05-10 21:34:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : 디자인패턴
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 데코레이터 패턴 (Decorator Pattern)
Created: 2025년 5월 10일 오후 9:34
Tags: 디자인패턴
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# 데코레이터 패턴 (Decorator Pattern)

데코레이터(Decorator) 패턴은 객체 지향 설계에서 자주 사용되는 구조적 디자인 패턴 중 하나로, 기존 객체에 새로운 기능을 동적으로 추가할 때 사용됩니다. 이 패턴은 상속을 사용하지 않고 객체의 기능을 확장할 수 있다는 점에서 매우 유용합니다. 특히 다음과 같은 상황에서 효과적입니다.

---

## 🔍 데코레이터 패턴의 특징

1. **동적 기능 추가** - 런타임 시 객체의 기능을 자유롭게 조합하여 확장할 수 있습니다.
2. **유연성** - 상속보다 유연하게 객체의 기능을 확장할 수 있습니다.
3. **개방-폐쇄 원칙(OCP) 준수** - 기존 코드를 수정하지 않고 기능을 확장할 수 있습니다.

---

## 🏛️ 구성 요소

1. **Component (구성요소)**
    - 기본 인터페이스로, 데코레이터와 구체적인 객체가 구현하는 공통 인터페이스입니다.
2. **ConcreteComponent (구체적인 구성요소)**
    - 기본 기능을 제공하는 실제 객체입니다.
3. **Decorator (데코레이터)**
    - `Component` 인터페이스를 구현하며, `ConcreteComponent`의 인스턴스를 포함하여 기능을 확장합니다.
4. **ConcreteDecorator (구체적인 데코레이터)**
    - 실제로 기능을 추가하는 데코레이터 클래스로, `Decorator` 클래스를 상속받습니다.

---

## 🛠️ 예시 (Golang)

```go
// Component
type Coffee interface {
	GetCost() int
	GetDescription() string
}

// ConcreteComponent
type BasicCoffee struct{}

func (c *BasicCoffee) GetCost() int {
	return 3000
}

func (c *BasicCoffee) GetDescription() string {
	return "Basic Coffee"
}

// Decorator
type CoffeeDecorator struct {
	coffee Coffee
}

func (d *CoffeeDecorator) GetCost() int {
	return d.coffee.GetCost()
}

func (d *CoffeeDecorator) GetDescription() string {
	return d.coffee.GetDescription()
}

// ConcreteDecorator
type MilkDecorator struct {
	CoffeeDecorator
}

func NewMilkDecorator(coffee Coffee) *MilkDecorator {
	return &MilkDecorator{CoffeeDecorator{coffee}}
}

func (m *MilkDecorator) GetCost() int {
	return m.coffee.GetCost() + 500
}

func (m *MilkDecorator) GetDescription() string {
	return m.coffee.GetDescription() + ", Milk"
}

// ConcreteDecorator
type SugarDecorator struct {
	CoffeeDecorator
}

func NewSugarDecorator(coffee Coffee) *SugarDecorator {
	return &SugarDecorator{CoffeeDecorator{coffee}}
}

func (s *SugarDecorator) GetCost() int {
	return s.coffee.GetCost() + 300
}

func (s *SugarDecorator) GetDescription() string {
	return s.coffee.GetDescription() + ", Sugar"
}

// 사용 예시
func main() {
	// 기본 커피
	var coffee Coffee = &BasicCoffee{}
	fmt.Println(coffee.GetDescription(), "-", coffee.GetCost(), "원")

	// 밀크 추가
	coffee = NewMilkDecorator(coffee)
	fmt.Println(coffee.GetDescription(), "-", coffee.GetCost(), "원")

	// 설탕 추가
	coffee = NewSugarDecorator(coffee)
	fmt.Println(coffee.GetDescription(), "-", coffee.GetCost(), "원")
}

```

### **🗝️ 실행 결과**

```
Basic Coffee - 3000 원
Basic Coffee, Milk - 3500 원
Basic Coffee, Milk, Sugar - 3800 원

```

---

## 🌱 장점

- **확장성** - 기존 코드를 수정하지 않고 기능을 확장할 수 있습니다.
- **유연성** - 여러 데코레이터를 조합하여 다양한 기능을 쉽게 추가할 수 있습니다.
- **단일 책임 원칙(SRP) 준수** - 각 데코레이터는 단일 기능에 집중할 수 있습니다.

## ❗️ 단점

- **복잡도 증가** - 데코레이터가 많아지면 코드의 복잡도가 높아질 수 있습니다.
- **성능 오버헤드** - 호출이 중첩되면서 약간의 성능 저하가 발생할 수 있습니다.
- **기능 확장 추적 어려움** - 데코레이터 체인이 길어질수록 객체의 최종 기능을 추적하기 어려워집니다.

---

## 💡 개선 방안

- **명시적인 데코레이터 체인 관리**
- **데코레이터 레지스트리 사용**
- **테스트 커버리지 강화**
