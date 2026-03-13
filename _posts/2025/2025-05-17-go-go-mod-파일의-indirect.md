---
layout  : post
title   : Go go.mod 파일의 // indirect
summary : 'go.mod 파일에서 require 항목 옆에 붙는 // indirect는'
date    : 2025-05-17 20:48:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Go go.mod 파일의 // indirect
Created: 2025년 5월 17일 오후 8:48
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# 📦 Go `go.mod` 파일의 `// indirect` 코멘트 설명

## 📌 `// indirect`란?

`go.mod` 파일에서 `require` 항목 옆에 붙는 `// indirect`는

해당 모듈이 **직접적으로는 사용하지 않지만, 간접적으로(import chain 상)** 필요한 의존성임을 의미함.

```go
require (
    github.com/sirupsen/logrus v1.8.1 // indirect
)

```

---

## 📚 발생 배경

- `go get`, `go mod tidy` 등을 실행할 때,**직접 import하지 않은 모듈**이지만 **다른 패키지가 사용 중이면 자동으로 추가**됨
- 이때 Go는 해당 의존성을 `// indirect`로 표시하여 **직접 쓴 것이 아님을 명시**

---

## 🧾 예시

### 구조

```
main.go → mylib → logrus

```

`main.go`에서는 `logrus`를 직접 import하지 않지만,

`mylib` 내부에서 사용하고 있을 경우:

```go
require (
    github.com/yourname/mylib v1.2.3
    github.com/sirupsen/logrus v1.8.1 // indirect
)

```

---

## ❓ 언제 없어지거나 사라지나?

- 프로젝트에서 해당 모듈이 **더 이상 어떤 경로로도 사용되지 않으면**,`go mod tidy` 실행 시 `go.mod`에서 자동으로 삭제됨
- 반대로 직접 import하면 **`// indirect`는 사라짐**

---

## ⚠️ 주의사항

| 항목 | 설명 |
| --- | --- |
| 자동 관리 | `// indirect`는 수동으로 추가하거나 제거할 필요 없음 |
| 버전 고정 주의 | 간접 의존성이지만 버전 충돌을 피하려면 명시적으로 고정할 수도 있음 |
| git conflict 주의 | 팀 작업 중 `go.mod` 충돌 시 `// indirect` 라인도 정확히 병합해야 함 |

---

## 🎯 결론

- `// indirect`는 Go가 **간접적으로 필요한 의존성을 추적**하기 위한 표시
- 수동으로 관리하지 않아도 되고, `go mod tidy`로 정리 가능
- 실제 import 경로 분석 시, 간접 의존성 여부를 파악할 수 있는 중요한 단서가 됨

---

## 🗂️ 태그 추천

`#Go` `#gomod` `#의존성관리` `#indirect` `#go모듈`
