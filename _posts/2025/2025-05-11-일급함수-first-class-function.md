---
layout  : post
title   : 일급함수(First-Class Function)
summary : '프로그래밍에서 일급 함수 (First-Class Function)는 다른 변수처럼 자유롭게 다룰 수 있는 함수를 의미합니다. 즉, 함수가 일급 객체 (First-Class Citizen)로 취급된다는 것입니다.'
date    : 2025-05-11 15:17:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : 프로그래밍
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 일급함수(First-Class Function)
Created: 2025년 5월 11일 오후 3:17
Tags: 프로그래밍
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

### **📚 일급 함수 (First-Class Function) 개념 정리**

---

### **📝 일급 함수란?**

프로그래밍에서 **일급 함수 (First-Class Function)**는 다른 변수처럼 자유롭게 다룰 수 있는 함수를 의미합니다. 즉, 함수가 **일급 객체 (First-Class Citizen)**로 취급된다는 것입니다.

---

### **✅ 일급 함수의 특징**

1. **변수에 할당 가능**
2. **함수의 인자로 전달 가능**
3. **함수의 반환값으로 사용 가능**
4. **데이터 구조 (맵, 슬라이스 등)에 저장 가능**

---

### **🛠️ Golang에서 일급 함수 활용 예시**

### **1. 변수에 할당하기**

```go
package main
import "fmt"

// 간단한 함수 정의
func greet(name string) string {
    return "Hello, " + name
}

func main() {
    // 함수를 변수에 할당
    sayHello := greet
    fmt.Println(sayHello("Golang")) // Hello, Golang
}
```

---

### **2. 인자로 전달하기**

```go
package main
import "fmt"

// 고차 함수
func printMessage(msg string, fn func(string) string) {
    fmt.Println(fn(msg))
}

func shout(msg string) string {
    return msg + "!"
}

func main() {
    printMessage("Go is awesome", shout) // Go is awesome!
}
```

---

### **3. 함수의 반환값으로 사용하기**

```go
package main
import "fmt"

// 함수를 반환하는 함수
func makeGreeting(greeting string) func(string) string {
    return func(name string) string {
        return greeting + ", " + name
    }
}

func main() {
    hello := makeGreeting("Hello")
    fmt.Println(hello("Golang")) // Hello, Golang
}
```

---

### **4. 데이터 구조에 저장하기**

```go
package main
import "fmt"

func add(a, b int) int { return a + b }
func subtract(a, b int) int { return a - b }

func main() {
    // 맵에 함수 저장
    operations := map[string]func(int, int) int{
        "add": add,
        "subtract": subtract,
    }

    fmt.Println(operations["add"](3, 4))       // 7
    fmt.Println(operations["subtract"](10, 4)) // 6
}
```

---

### **💡 일급 함수의 장점**

- **유연성:** 다양한 패턴 (예: 콜백, 클로저, 커링) 구현 가능
- **간결성:** 코드 구조 단순화
- **재사용성:** 같은 로직을 반복하지 않고 함수로 분리하여 재사용 가능

---

### **🚫 일급 함수가 아닌 경우**

- 함수를 변수처럼 다룰 수 없는 언어에서는 일급 함수가 아닙니다.
- 예를 들어, **C 언어**는 함수 포인터가 있지만 함수 자체를 반환하거나 변수에 직접 할당할 수 없습니다.

---

태그: #프로그래밍 #golang #일급함수 #함수 #고차함수 #클로저
