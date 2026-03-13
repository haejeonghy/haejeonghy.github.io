---
layout  : post
title   : 네임스페이스 (Namespace)와 라이브러리 (Library)의 차이
summary : '// utils/math.go package utils'
date    : 2025-05-11 15:43:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang 프로그래밍
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# 네임스페이스 (Namespace)와 라이브러리 (Library)의 차이
Created: 2025년 5월 11일 오후 3:43
Tags: golang, 프로그래밍
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## 📚 네임스페이스 (Namespace)란?

- *네임스페이스 (Namespace)**는 **이름 충돌**을 방지하고, 코드를 **논리적으로 그룹화**하는 단위입니다. 주로 **패키지, 모듈, 클래스**의 이름을 관리하는 데 사용됩니다.

### ✅ 네임스페이스의 특징

- **목적:** 이름 충돌 방지
- **범위:** 주로 패키지, 모듈, 클래스
- **역할:** 동일한 이름의 함수나 변수가 여러 곳에서 사용될 때 충돌을 피하도록 구분

---

### 🛠️ 네임스페이스 예시 (Golang)

```go
// utils/math.go
package utils

func Add(a, b int) int {
    return a + b
}

```

```go
// main.go
package main

import (
    "fmt"
    "myapp/utils"
)

func main() {
    result := utils.Add(2, 3)
    fmt.Println(result) // 5
}

```

- 여기서 **`utils`*가 네임스페이스 역할을 합니다.
- 동일한 **`Add()`** 함수가 다른 패키지에 있어도 충돌 없이 사용할 수 있습니다.

---

### 🛠️ 네임스페이스 예시 (Python)

```python
# math_utils.py
def add(a, b):
    return a + b

# main.py
import math_utils

print(math_utils.add(2, 3)) # 5

```

- *`math_utils`*가 네임스페이스 역할을 합니다.

---

## 📦 라이브러리 (Library)란?

- *라이브러리 (Library)**는 자주 사용되는 **코드, 함수, 데이터 구조** 등을 모아둔 **재사용 가능한 코드 모음**입니다.

### ✅ 라이브러리의 특징

- **목적:** 재사용성 높은 코드 집합 제공
- **범위:** 하나의 독립적인 코드 집합
- **역할:** 특정 기능을 쉽게 구현할 수 있도록 미리 작성된 코드 제공

---

### 🛠️ 라이브러리 예시 (Golang 표준 라이브러리)

```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    fmt.Println(strings.ToUpper("hello")) // HELLO
}

```

- **`strings`** 패키지는 **문자열 조작**을 위한 라이브러리입니다.

---

### 🛠️ 라이브러리 예시 (Python 표준 라이브러리)

```python
import math

print(math.sqrt(16)) # 4.0

```

- *`math`*는 **수학 함수**들을 포함하는 표준 라이브러리입니다.

---

## 📝 네임스페이스와 라이브러리의 주요 차이점

| **특징** | **네임스페이스 (Namespace)** | **라이브러리 (Library)** |
| --- | --- | --- |
| **역할** | 이름 충돌 방지, 코드 그룹화 | 재사용 가능한 코드 집합 |
| **구성 요소** | 패키지, 모듈, 클래스 | 함수, 데이터 구조, 알고리즘 |
| **범위** | 파일, 패키지, 클래스 | 독립적인 코드 집합 |
| **재사용성** | 중간 수준 | 높은 수준 |
| **예시** | utils, math_utils | fmt, strings (Go) / math, datetime (Python) |

---

## 📝 결론

- **네임스페이스**는 코드를 **구조화**하고 **이름 충돌**을 방지하는 데 중점을 둡니다.
- **라이브러리**는 특정 기능을 **재사용**하기 위해 미리 작성된 코드 집합입니다.
- 대부분의 최신 프로그래밍 언어는 네임스페이스와 라이브러리를 함께 사용하여 **코드의 유지보수성**과 **가독성**을 높입니다. 😊

---

태그: #네임스페이스 #라이브러리 #Namespace #Library #프로그래밍 #Go #Python #코드구성
