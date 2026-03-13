---
layout  : post
title   : golang exit code
summary : 'Go 프로그램이 종료될 때 > > > 외부 프로세스에 실행 결과 상태를 전달하는 숫자 값 >'
date    : 2025-06-06 18:28:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# golang exit code
Created: 2025년 6월 6일 오후 6:28
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## **📌 Golang에서 Exit Code 사용 및 활용 사례 정리**

### **1. Golang에서 Exit Code란?**

> Go 프로그램이 종료될 때
> 
> 
> **외부 프로세스에 실행 결과 상태를 전달하는 숫자 값**
> 

> 표준 패키지 os.Exit(code)를 통해 명시적으로 지정할 수 있으며, code == 0이면 정상 종료, 0이 아니면 실패를 의미합니다.
> 

---

### **2. 기본 사용 예시**

```
package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "인자가 부족합니다.")
		os.Exit(1) // ❌ 비정상 종료
	}

	fmt.Println("정상 실행")
	os.Exit(0) // ✅ 정상 종료
}
```

---

### **3. Exit Code를 사용하는 주요 상황**

| **사용 상황** | **설명** |
| --- | --- |
| CLI 도구 | 잘못된 입력을 받은 경우 os.Exit(1) 등으로 종료 |
| CI/CD | exit code를 통해 Job 성공/실패 판단 |
| Kubernetes | 컨테이너가 어떤 이유로 종료되었는지 판단하는 기준 |
| CronJob | 작업 성공/실패 결과를 시스템에 전달할 때 사용 |

---

### **4. panic vs os.Exit(1) 비교**

| **항목** | panic | os.Exit(1) |
| --- | --- | --- |
| 목적 | 예기치 않은 오류, 논리 오류 | 예상된 실패, 외부에 실패 상태 전달 |
| 로그 출력 | 스택 트레이스 포함 (과도함) | stderr만 출력 가능 |
| 종료 코드 | 기본적으로 2 이상 | 원하는 숫자로 명시 가능 |
| 외부 처리 | 다루기 어려움 (쿠버네티스, CI 등) | **명확하게 실패 신호 전달 가능** |

---

### **5. 실제 적용 예: CronJob 파라미터 누락 시 종료**

```
package main

import (
	"fmt"
	"os"
)

func main() {
	mode := os.Getenv("RUN_MODE")
	if mode == "" {
		fmt.Fprintln(os.Stderr, "RUN_MODE 환경 변수가 필요합니다.")
		os.Exit(1) // ❗ 실패 상태 코드 전달
	}

	fmt.Println("크론잡 실행 중...")
}
```

> 이처럼 파라미터 오류, 파일 누락, 환경 설정 오류 등
> 
> 
> **예상 가능한 실패 상황**
> 
> **깔끔하게 종료하고, 외부 시스템에 상태를 전달**
> 

---

## **✅ 요약**

- Go에서는 os.Exit(code)를 사용하여 명시적인 종료 코드를 반환할 수 있음
- panic은 개발 중 디버깅용, os.Exit은 **운영 환경에서의 명확한 실패 처리**에 사용
- 특히 **CronJob, CLI, Kubernetes 환경에서는 exit code가 필수적인 신호 역할**

---
