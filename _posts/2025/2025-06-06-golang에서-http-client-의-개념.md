---
layout  : post
title   : Golang에서 http.Client 의 개념
summary : 'Go에서 “client”라는 용어는 일반적으로 무언가에 요청(Request)을 보내는 역할을 하는 객체 또는 구조체를 의미합니다. 특히 http.Client는 HTTP 프로토콜을 사용하여 외부 서버에 요청을 보내고 '
date    : 2025-06-06 18:32:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Golang에서 http.Client 의 개념
Created: 2025년 6월 6일 오후 6:32
Tags: golang
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

Go에서 “client”라는 용어는 일반적으로 **무언가에 요청(Request)을 보내는 역할을 하는 객체 또는 구조체**를 의미합니다. 특히 http.Client는 HTTP 프로토콜을 사용하여 **외부 서버에 요청을 보내고 응답을 받는 기능을 담당하는 구조체**입니다.

---

## **✅ Golang에서 http.Client 의 개념**

### **📌 정의**

> http.Client는
> 
> 
> **HTTP 요청을 생성하고 전송한 뒤, 응답을 받는 기능을 제공하는 표준 라이브러리의 구조체**
> 

> 내부적으로
> 
> 
> **TCP 연결, Keep-Alive, 타임아웃, 리다이렉션 처리 등**
> 

---

## **✅ 기본 사용 예시**

```
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	client := http.Client{}

	resp, err := client.Get("https://example.com")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Println(string(body))
}
```

- client.Get(...) → GET 요청을 보내고 응답을 받음
- resp.Body → 응답 바디 (body)를 읽기

---

## **✅ http.Client의 주요 필드**

| **필드** | **설명** |
| --- | --- |
| Transport | 요청을 어떻게 보낼지 정의 (기본은 http.DefaultTransport) |
| Timeout | 전체 요청-응답 시간 제한 (이게 없으면 영원히 기다릴 수 있음!) |
| CheckRedirect | 리다이렉션 허용 여부 설정 |
| Jar | 쿠키 저장소 (세션 유지에 필요 시 사용) |

---

## **✅ 실무에서 중요한 포인트**

### **✔️ 재사용**

- http.Client는 **재사용이 권장됩니다.**
- 매 요청마다 새로 만들면 **Keep-Alive가 비활성화되어 성능 저하** 및 **포트 exhaustion** 위험

```
var client = &http.Client{
	Timeout: 10 * time.Second,
}
```

### **✔️ 커스텀 설정**

```
client := &http.Client{
	Transport: &http.Transport{
		MaxIdleConns:    100,
		IdleConnTimeout: 90 * time.Second,
	},
	Timeout: 10 * time.Second,
}
```

- 커넥션 풀, 타임아웃 등을 조절해 고성능 API 호출 가능

---

## **✅ 요약**

| **항목** | **설명** |
| --- | --- |
| 역할 | HTTP 요청을 보내고 응답을 받는 역할 |
| 핵심 구조체 | http.Client |
| 재사용 | 가능하면 재사용해야 성능과 안정성 확보 |
| 타임아웃 | 설정하지 않으면 요청이 무한 대기할 수 있음 |

---
