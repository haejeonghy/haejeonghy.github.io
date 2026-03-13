---
layout  : post
title   : Golang 제네릭(Generic) 정리
summary : 'func PrintIntSlice(s []int) { ... } func PrintStringSlice(s []string) { ... }'
date    : 2025-06-08 15:44:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Golang 제네릭(Generic) 정리
Created: 2025년 6월 8일 오후 3:44
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## **📘 Golang 제네릭(Generic) 정리**

### **✅ 개념 요약**

- *제네릭(Generic)**은 함수나 타입에서 **타입을 고정하지 않고**, 유연하게 다양한 타입을 처리할 수 있도록 하는 문법.
- **Go 1.18** 버전부터 정식 지원됨.
- 목적: **코드 재사용성** 향상 + **타입 안정성 유지**

---

### **📌 왜 제네릭이 필요한가?**

### **❌ 제네릭이 없던 시절**

```
func PrintIntSlice(s []int) { ... }
func PrintStringSlice(s []string) { ... }
```

- 타입마다 함수를 중복 작성해야 했음

### **✅ 제네릭 도입 후**

```
func PrintSlice[T any](s []T) {
	for _, v := range s {
		fmt.Println(v)
	}
}
```

- 한 번 작성으로 어떤 타입이든 처리 가능

---

### **🧱 기본 문법**

### **📍 함수에서 제네릭 사용**

```
func Identity[T any](input T) T {
	return input
}
```

- T: 타입 파라미터
- any: 모든 타입 허용 (alias of interface{})

### **📍 호출 예시**

```
val1 := Identity(42)             // int
val2 := Identity[string]("hi")   // string
```

---

### **📍 구조체에서 제네릭 사용**

```
type Pair[K, V any] struct {
	Key   K
	Value V
}

p := Pair[string, int]{Key: "age", Value: 30}
```

---

### **📍 타입 제약 (constraint) 사용**

```
type Number interface {
	~int | ~float64
}

func Sum[T Number](a, b T) T {
	return a + b
}
```

- ~int: int와 int 기반 사용자 정의 타입 포함

---

### **🧪 실전 예제: 필터 함수**

```
func Filter[T any](s []T, fn func(T) bool) []T {
	var result []T
	for _, v := range s {
		if fn(v) {
			result = append(result, v)
		}
	}
	return result
}

// 사용 예시
nums := []int{1, 2, 3, 4}
even := Filter(nums, func(n int) bool { return n%2 == 0 })
// 결과: [2, 4]
```

---

### **⚠️ 사용 시 주의사항**

| **항목** | **설명** |
| --- | --- |
| 성능 | 제네릭은 컴파일 타임에 타입별 코드로 변환되어 성능 저하 거의 없음 |
| 타입 추론 | 대부분의 경우 Go가 타입을 자동 추론해줌 |
| 남용 금지 | 과한 사용은 코드 가독성과 유지보수성 저하시킬 수 있음 |

---

### **🧠 요약**

| **구분** | **내용** |
| --- | --- |
| 도입 시점 | Go 1.18 |
| 키워드 | T, any, constraint, ~ |
| 장점 | 타입 안전 + 코드 재사용 |
| 주요 활용 | 공통 로직 함수(filter/map/reduce), 자료구조(map/slice 등) |

---
