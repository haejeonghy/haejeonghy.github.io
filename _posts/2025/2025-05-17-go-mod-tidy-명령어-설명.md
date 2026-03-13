---
layout  : post
title   : go mod tidy 명령어 설명
summary : 'go mod tidy는 Go 프로젝트에서 go.mod와 go.sum 파일을 정리하고,'
date    : 2025-05-17 20:49:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# go mod tidy 명령어 설명
Created: 2025년 5월 17일 오후 8:49
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# 🧹 `go mod tidy` 명령어 설명

## 📌 개요

`go mod tidy`는 Go 프로젝트에서 **`go.mod`와 `go.sum` 파일을 정리**하고,

필요한 모듈만 남기고 불필요한 의존성을 제거하는 명령어.

---

## 🛠️ 주요 기능

| 기능 | 설명 |
| --- | --- |
| ✅ 사용하지 않는 모듈 제거 | 코드에서 import하지 않는 모듈은 `go.mod`에서 제거 |
| ✅ 누락된 모듈 추가 | 코드에서 import했지만 `go.mod`에 없는 모듈을 자동 추가 |
| ✅ `go.sum` 정리 | 체크섬 파일인 `go.sum`도 정리 및 최신화 |
| ✅ 간접 의존성 처리 | 사용 중인 패키지가 내부적으로 사용하는 모듈도 `// indirect`로 표시하여 관리 |

---

## 🧾 예시

```bash
go mod tidy

```

이 명령을 실행하면 다음과 같은 변화가 생길 수 있음:

- `go.mod`에서 쓰지 않는 `require` 항목 삭제
- 필요하지만 누락된 모듈 자동 추가
- `// indirect` 항목 자동 정리
- `go.sum`의 해시 값 갱신

---

## 🎯 언제 사용하나?

- 새로운 의존성을 추가/삭제한 후
- 오래된 `go.mod`를 정리할 때
- 팀 작업 후 충돌 병합 이후 정리 시
- CI/CD 파이프라인에서 모듈 상태 검증 시

---

## 🧼 팁

- `go mod tidy`는 **수동으로 의존성을 관리할 필요 없이 자동 정리**해 줌
- 모듈 충돌 문제나 의존성 누락 문제가 생기면 가장 먼저 실행해볼 것

---

## 🗂️ 태그 추천

`#Go` `#gomod` `#gobuild` `#모듈정리` `#go모듈` `#tidy`
