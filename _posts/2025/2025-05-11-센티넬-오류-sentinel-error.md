---
layout  : post
title   : 센티넬 오류 (Sentinel Error)
summary : 'import ( "errors" "fmt" )'
date    : 2025-05-11 15:38:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 센티넬 오류 (Sentinel Error)
Created: 2025년 5월 11일 오후 3:38
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# 🚫 센티넬 오류 (Sentinel Error) 개념과 예시

---

## 📚 센티넬 오류란?

- *센티넬 오류 (Sentinel Error)**는 **고정된 형태의 명시적인 에러 값**을 의미합니다. Go에서 흔히 사용하는 **`errors.New()`*나 **`fmt.Errorf()`*를 통해 생성된 **미리 정의된 에러**를 **센티넬 오류**라고 합니다.

---

### ✅ 센티넬 오류의 특징

1. **고정된 에러 값**
    - 특정한 상황에서 **명시적으로 반환**하는 **상수형 에러**
    - 예를 들어, **`io.EOF`**, **`sql.ErrNoRows`** 등
2. **직접 비교 가능**
    - *`errors.Is()`*나 **`==`*를 사용하여 비교할 수 있음
3. **단순하지만 제한적**
    - 에러의 **맥락**이나 **세부 정보**가 부족할 수 있음

---

### 📝 센티넬 오류 예시

### **1. 기본적인 센티넬 오류**

```go
package main

import (
    "errors"
    "fmt"
)

var ErrNotFound = errors.New("item not found")

func findItem(id int) (string, error) {
    if id != 1 {
        return "", ErrNotFound
    }
    return "Item 1", nil
}

func main() {
    _, err := findItem(2)
    if errors.Is(err, ErrNotFound) {
        fmt.Println("Item not found")
    } else if err != nil {
        fmt.Println("Unknown error:", err)
    }
}

```

### **💡 실행 결과**

```
Item not found

```

---

### **2. `errors.Is()`를 사용한 비교**

```go
package main

import (
    "errors"
    "fmt"
)

var ErrInvalidID = errors.New("invalid ID")

func validateID(id int) error {
    if id <= 0 {
        return ErrInvalidID
    }
    return nil
}

func main() {
    err := validateID(-1)
    if errors.Is(err, ErrInvalidID) {
        fmt.Println("Invalid ID error")
    }
}

```

### **💡 실행 결과**

```
Invalid ID error

```

---

### ❌ 센티넬 오류의 단점

1. **에러의 맥락 부족**
    - 에러 메시지가 고정되어 있어 **추가적인 정보**를 제공하기 어려움
2. **테스트의 어려움**
    - 에러가 **상수**이기 때문에 특정 상황에 대한 세부 테스트가 어려울 수 있음
3. **에러 확장성 제한**
    - 동일한 오류를 확장하거나 추가적인 정보와 함께 반환하는 것이 어려움

---

### 📝 일반적인 에러와의 비교

| **특징** | **센티넬 오류** | **일반적인 에러** |
| --- | --- | --- |
| **에러 메시지** | 고정적 | 동적 (포맷팅 가능) |
| **비교 방법** | `==`, `errors.Is()` | `errors.As()`, `errors.Unwrap()` |
| **맥락 정보** | 부족 | 충분히 포함 가능 |
| **테스트 용이성** | 낮음 | 높음 |

---

### ✅ 센티넬 오류가 유용한 경우

- 단순한 조건에서 빠르게 실패를 처리할 때
- **"파일 없음"**, **"데이터 없음"** 같은 단순한 상태 표현
- **패키지 내에서만 사용**될 때

---

### 📝 결론

- **센티넬 오류**는 **명시적인 에러 반환**을 위해 유용하지만, **맥락**과 **추적성**이 필요한 경우 **랩핑 (Wrapping)**을 통한 에러 처리가 더 나은 선택일 수 있습니다.
- **대규모 서버**나 **복잡한 서비스**에서는 **에러 체계**를 더 명확하게 정의하는 것이 좋습니다. 😊

---

태그: #센티넬오류 #SentinelError #Go #에러처리 #명시적에러 #ErrorHandling
