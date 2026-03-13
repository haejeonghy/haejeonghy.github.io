---
layout  : post
title   : API 문서 자동 생성기 (API Documentation Generator)
summary : '❗ > > > 함수 내부의 코드를 해석해서 문서를 작성하는 것은 아님 >'
date    : 2025-05-17 20:40:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : documentation 문서화
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# API 문서 자동 생성기 (API Documentation Generator)
Created: 2025년 5월 17일 오후 8:40
Tags: Documentation, 문서화
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# **📘 godoc vs javadoc 문서화 도구 비교 정리**

## **📌 1. godoc과 javadoc은 어떤 도구인가?**

| **항목** | godoc | javadoc |
| --- | --- | --- |
| 사용 언어 | Go | Java |
| 주석 형식 | // 단일 줄 주석 | /** ... */ 자바독 스타일 주석 |
| 사용 목적 | 코드에 작성한 주석을 바탕으로 API 문서를 자동 생성 |  |
| 출력 형식 | HTML 웹 페이지, CLI | HTML 웹 페이지 |
| 문서 위치 | 코드 상단 주석 기반 | 코드 상단 주석 기반, 패키지 설명 포함 가능 |

---

## **🧾 2. “자동 생성”이란 어떤 의미인가?**

> ❗
> 
> 
> **함수 내부의 코드를 해석해서 문서를 작성하는 것은 아님**
> 

> ✅ 오직
> 
> 
> **개발자가 작성한 주석(comment)을 수집해서 보기 좋게 정리**
> 

### **예시 (Go 코드)**

```
// Add는 두 수를 더합니다.
func Add(a, b int) int {
    return a + b
}
```

➡ 위 주석을 godoc이 읽어서 HTML로 출력함.

---

## **🌐 3. godoc HTML 문서 예시 (카페 시스템)**

```
// Package cafe는 커피숍 시스템의 핵심 로직을 다룹니다.
package cafe

// MenuItem은 커피 메뉴 항목을 나타냅니다.
type MenuItem struct {
    Name  string // 메뉴 이름
    Price int    // 가격
}

// Order는 고객의 주문을 나타냅니다.
type Order struct {
    Items []MenuItem
    Paid  bool
}

// AddItem은 주문에 항목을 추가합니다.
func (o *Order) AddItem(item MenuItem) { ... }

// Total은 주문 총액을 반환합니다.
func (o *Order) Total() int { ... }
```

### **godoc HTML 출력 결과 요약**

- Package cafe 설명 표시
- 구조체 MenuItem, Order 문서화
- 메서드 AddItem, Total에 주석이 있으면 설명 포함됨

---

## **⚖️ 4. godoc의 장단점**

### **✅ 장점**

- Go 표준 도구로 별도 설치 없이 사용 가능
- 주석 기반이라 코드와 문서가 분리되지 않음
- 브라우저에서 바로 확인 가능 (godoc -http=:6060)
- 문서 관리가 간편 (주석만 잘 달면 됨)

### **❌ 단점**

- 기능이 단순하고 예시/다이어그램 등은 표현 불가
- Markdown 지원이 미약
- 커스터마이징 불가 (디자인, 테마 등)
- CI/CD 통합 어려움
- 팀 문화상 문서화를 Notion, Swagger로 대체하는 경우가 많음
- 주석 작성 문화 부족 → 실제 현장에서는 문서 품질이 낮음

---

## **🧭 5. 왜 godoc을 잘 안 쓰게 되는가?**

- 현업에서는 Swagger, Notion, Markdown 기반 문서 등 **표현력이 풍부하고 공유가 쉬운 도구**로 이동
- godoc은 정적 설명 위주이므로 **예제, 인증 흐름, API 규칙, JSON 응답 예시 등은 정리 불가능**
- 팀 내 문서화 요구 수준이 높아짐에 따라 godoc은 보조적 수단으로 밀려남

---

## **📛 6. godoc, javadoc은 어떤 도구인가?**

> 📌 명칭:
> 
> 
> **API 문서 자동 생성기 (API Documentation Generator)**
> 

### **관련 용어**

| **분류** | **설명** | **예시** |
| --- | --- | --- |
| 문서 생성기 | 주석 기반으로 API 문서를 생성 | godoc, javadoc, rustdoc, doxygen |
| 명세 기반 문서화 | OpenAPI 등으로 명세서 → 문서화 | Swagger UI, Redoc, Stoplight |
| 정적 문서 생성기 | Markdown으로 문서 → 정적 사이트 | mkdocs, Docusaurus, Sphinx |
| IDE 문서 기능 | 코드에 마우스 올릴 때 설명 표시 | GoLand, VSCode hover docs |

---
