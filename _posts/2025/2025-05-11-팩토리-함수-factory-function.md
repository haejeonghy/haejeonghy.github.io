---
layout  : post
title   : 팩토리 함수 (Factory Function)
summary : 'package main import "fmt"'
date    : 2025-05-11 15:23:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang 프로그래밍
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 팩토리 함수 (Factory Function)
Created: 2025년 5월 11일 오후 3:23
Tags: golang, 프로그래밍
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## 📚 팩토리 함수란?

- *팩토리 함수 (Factory Function)**는 **특정 객체나 구조체(Struct) 인스턴스를 생성하는 함수**를 의미합니다. 일반적으로 **복잡한 초기화 과정**이 필요한 객체를 생성하거나, **공통된 로직**을 재사용하기 위해 사용됩니다.

---

### ✅ 팩토리 함수의 특징

1. **객체 생성 로직 캡슐화**
2. **다양한 설정 옵션 지원**
3. **추상화된 생성 패턴**
4. **코드 재사용성 증가**

---

### 🚀 팩토리 함수의 장점

- **복잡한 초기화 단순화**
- **코드 중복 제거**
- **인터페이스를 통한 유연성 제공**
- **테스트 편의성 증가**

---

## 🛠️ Golang에서 팩토리 함수 예시

### **1. 기본 팩토리 함수**

```go
package main
import "fmt"

// User 구조체 정의
type User struct {
    Name  string
    Email string
    Age   int
}

// 팩토리 함수
func NewUser(name, email string, age int) *User {
    return &User{
        Name:  name,
        Email: email,
        Age:   age,
    }
}

func main() {
    user := NewUser("Alice", "alice@example.com", 30)
    fmt.Println(user) // &{Alice alice@example.com 30}
}

```

---

### **2. 기본값을 설정하는 팩토리 함수**

```go
package main
import "fmt"

type Config struct {
    Host string
    Port int
}

// 기본값을 설정하는 팩토리 함수
func NewConfig() *Config {
    return &Config{
        Host: "localhost",
        Port: 8080,
    }
}

func main() {
    config := NewConfig()
    fmt.Println(config) // &{localhost 8080}
}

```

---

### **3. 인터페이스와 함께 사용하기**

```go
package main
import "fmt"

// Animal 인터페이스 정의
type Animal interface {
    Speak() string
}

// Dog 구조체 정의
type Dog struct {
    Name string
}

// Dog는 Animal 인터페이스를 구현
func (d Dog) Speak() string {
    return d.Name + " says Woof!"
}

// 팩토리 함수
func NewAnimal(name string) Animal {
    return Dog{Name: name}
}

func main() {
    dog := NewAnimal("Buddy")
    fmt.Println(dog.Speak()) // Buddy says Woof!
}

```

---

## 🔍 Java의 생성자와의 차이점

| **특징** | **Java 객체 초기화** | **Golang 팩토리 함수** |
| --- | --- | --- |
| **기본 개념** | 생성자 (Constructor) | 팩토리 함수 (Factory Function) |
| **메모리 할당** | 힙 (Heap) | 힙 (Heap) 또는 스택 (Stack) |
| **상속 지원** | O (클래스 상속) | X (구조체 내장, 인터페이스) |
| **다형성** | 클래스 계층 | 인터페이스 |
| **객체 반환** | 암시적 참조 | 명시적 포인터 반환 |
| **객체 라이프사이클** | 가비지 컬렉션 | 가비지 컬렉션 |
| **기본값 설정** | 생성자 오버로딩 | 팩토리 함수 내부 로직 |

---

## 📌 팩토리 함수를 사용하는 이유

- **복잡한 초기화가 필요한 경우**
- **구조체의 기본값을 설정해야 할 때**
- **인터페이스 기반 객체 생성이 필요한 경우**
- **테스트 편의성**을 위해 객체 생성을 단순화하고자 할 때

---

태그: #프로그래밍 #golang #팩토리함수 #객체초기화 #Java #Go #생성자
