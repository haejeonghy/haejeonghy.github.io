---
layout  : post
title   : CSP (Communicating Sequential Processes)와 동시성 모델 비교 정리
summary : 'CSP(Communicating Sequential Processes)는 > > > 1978년 C.A.R. Hoare가 제안한 동시성 프로그래밍 모델로, > > 프로세스들이 공유 메모리 없이 채널을 통해 메시지를 주'
date    : 2025-05-17 20:55:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : csp 동시성모델
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# CSP (Communicating Sequential Processes)와 동시성 모델 비교 정리
Created: 2025년 5월 17일 오후 8:55
Tags: CSP, 동시성모델
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# ⚙️ CSP (Communicating Sequential Processes)와 동시성 모델 비교 정리

---

## 1. CSP란 무엇인가?

> **CSP(Communicating Sequential Processes)**는
> 
> 
> 1978년 C.A.R. Hoare가 제안한 **동시성 프로그래밍 모델**로,
> 
> 프로세스들이 **공유 메모리 없이 채널을 통해 메시지를 주고받으며 통신**하는 방식이다.
> 

### ✅ 특징

- 프로세스는 **서로 직접 데이터를 주고받음**
- **공유 메모리 없이** 통신만으로 협력
- **동기화는 채널을 통해 자연스럽게** 이루어짐

---

## 2. CSP 실생활 비유

> “전하와 나인”
> 
- 전하: “차를 가져오너라!”
- 나인: “예” 하고 찻잔을 들고 와 직접 전달

→ 전하는 주방을 알 필요 없이 **채널(명령과 찻잔)**만으로 소통

→ 이는 **goroutine + channel** 구조와 같음

---

## 3. Go 코드 예시 (CSP 구조)

```go
func main() {
    ch := make(chan string)

    go func() {
        ch <- "아메리카노"
    }()

    order := <-ch
    fmt.Println("전하께 내온 음료:", order)
}

```

---

## 4. CSP 외 다른 동시성 모델은 무엇이 있는가?

| 모델명 | 개념 핵심 | 대표 언어/사례 |
| --- | --- | --- |
| **CSP** | 프로세스는 채널을 통해 통신 | Go |
| **Actor Model** | 각 Actor가 메시지를 받고 자체 상태를 변경하며 통신 | Erlang, Akka (Scala), Elixir |
| **Shared Memory** | 여러 스레드가 메모리를 공유, 락으로 제어 | C, C++, Java |
| **Dataflow Model** | 데이터가 준비되면 작업 자동 실행 | TensorFlow, DAG 기반 시스템 |
| **Fork/Join** | 병렬로 나눠 처리하고 결과 병합 | Java ParallelStream, OpenMP |

---

## 5. “나인과 찻잔” 비유로 본 동시성 모델 비교

| 동시성 모델 | 설명 | 비유 |
| --- | --- | --- |
| **CSP (Go)** | 채널을 통한 직접 통신 | 전하: “차를 가져오너라” → 나인이 직접 찻잔을 건넴 |
| **Actor Model** | 메시지 기반 비동기 처리 | 전하가 쪽지를 보냄, 나인이 자기 방식으로 처리하고 쪽지로 회신 |
| **Shared Memory** | 공유 자원에 접근, 락 필요 | 전하와 나인이 같은 찻장에서 동시에 찻잔을 꺼내려 함 → 충돌 방지 위해 락 |
| **Dataflow Model** | 선언형 흐름 기반 자동 처리 | “찻잎 → 물 → 잔”이 준비되면 자동 실행, 전하는 흐름에 관여 안 함 |
| **Fork/Join** | 병렬 작업 후 결과 병합 | 여러 나인이 각각 찻잔·찻잎·물을 준비 후 함께 전달 |

---

## 6. Shared Memory와 DBMS의 유사성

| 항목 | Shared Memory | DBMS |
| --- | --- | --- |
| 공유 방식 | 메모리 직접 공유 | 디스크/메모리 상 데이터 공유 |
| 충돌 방지 | Mutex, RWLock | 트랜잭션, Lock, MVCC |
| 경쟁 상태 | Race Condition 발생 | 격리 수준, 복구 메커니즘 있음 |
| 비유 | 나인이 같은 찻장을 동시에 열어 충돌 가능 | 사서가 순서를 정해 찻장 사용을 통제 |

> ✅ DBMS는 실전에서 Shared Memory 구조를 안정적으로 운용하기 위한 고차 구조라 볼 수 있음
> 

---

## ✅ 결론 요약

- **CSP는 Go 언어의 핵심 동시성 모델**이며, 명확하고 안전한 통신 방식
- **다양한 동시성 모델**이 존재하며, 용도에 따라 알맞은 구조 선택이 중요
- **Shared Memory**는 강력하지만 위험하며, **DBMS는 이를 제어하는 고급 시스템**
- 실전 개발에선 **CSP 기반 설계**가 유지보수성과 예측 가능성 측면에서 우수함

---

## 🗂️ 태그 추천

`#Go` `#CSP` `#동시성모델` `#ActorModel` `#SharedMemory` `#DBMS` `#Concurrency` `#채널` `#goroutine`
