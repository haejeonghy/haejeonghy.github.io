---
layout  : post
title   : Apache Kafka란 무엇인가?
summary : 'Apache Kafka > > > 분산 메시지 큐 >'
date    : 2025-05-13 17:08:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : kafka
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Apache Kafka란 무엇인가?
Created: 2025년 5월 13일 오후 5:08
Tags: kafka
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

## **🐘 Apache Kafka란 무엇인가?**

### **📌 정의**

> Apache Kafka
> 
> 
> **분산 메시지 큐**
> 

> 고속/고내구성의
> 
> 
> **로그 기반 데이터 파이프라인 시스템**
> 

---

## **⚙️ 기본 구성 요소**

| **구성 요소** | **설명** |
| --- | --- |
| **Producer** | 메시지를 Kafka로 전송하는 주체 (예: 앱, 서버 등) |
| **Broker** | Kafka 서버. 메시지를 저장하고 전달 |
| **Topic** | 메시지를 분류하는 단위 |
| **Partition** | Topic을 물리적으로 나눈 단위. 병렬 처리 가능 |
| **Consumer** | 메시지를 읽는 주체 |
| **Consumer Group** | 여러 Consumer가 Topic을 나눠서 병렬 소비 |
| **Zookeeper (또는 KRaft)** | 클러스터 메타데이터 관리 (v3 이상부터 KRaft 도입) |

---

## **🧠 전하의 질문과 도승지의 충언 정리**

---

### **❓**

### **“Kafka도 결국에는 DB라고 하는 의견이 있다 한다. 왜 그렇느냐?”**

### **💬 답변:**

Kafka는 다음과 같은 이유로 **“DB와 유사한 점이 있다”고 평가**됩니다.

| **유사점** | **설명** |
| --- | --- |
| ✅ **데이터 저장** | Kafka는 메시지를 디스크에 저장하고, 삭제 정책을 지정하지 않으면 유지됩니다. |
| ✅ **조회 가능** | 메시지를 오프셋(offset) 또는 timestamp 기준으로 조회할 수 있습니다. |
| ✅ **내구성 보장** | 복제(replication), ack, commit log로 고가용성 유지 |
| ✅ **불변 로그 구조** | append-only 방식으로, 일부 타임시리즈 DB와 유사 |

그러나…

| **한계점** | **설명** |
| --- | --- |
| ❌ **임의 조건 조회 불가** | userId = 123 같은 조건으로 조회 불가능 (인덱스 없음) |
| ❌ **인덱스 없음** | 필드 기반 조회, 정렬, 조인 등 불가 |
| ❌ **CRUD 미지원** | Create(Read)만 가능, Update/Delete 불가 |

### **📚 참고:**

- [Confluent 블로그: Is Kafka a Database?](https://www.confluent.io/blog/apache-kafka-is-not-a-database/)
- [Martin Kleppmann 발표](https://www.confluent.io/kafka-summit-ny-2019/kafka-the-log-structured-database-inside/)

---

### **❓**

### **“Kafka에 인덱싱이 없으면 풀스캔으로 조회해야 하는 것이냐?”**

### **💬 답변:**

예, 전하.

Kafka는 **RDB처럼 key나 특정 필드에 대한 인덱스가 없기 때문에**,

조건 검색을 하려면 **Consumer가 메시지를 처음부터 끝까지 순차 조회**해야 하옵니다.

즉, **풀스캔(full scan)**이 이루어지옵니다.

> 단, 다음과 같은 “예외적 전략”은 존재하옵니다:
> 

### **✅ 예외적 최적화 방법**

| **전략** | **설명** |
| --- | --- |
| **Log Compaction 사용** | 특정 키의 마지막 값만 유지하는 토픽 설정 (cleanup.policy = compact) |
| **Kafka Streams로 materialized view 구성** | 로컬 RocksDB 등을 이용해 key-value 형태로 캐싱 |
| **Kafka → 외부 검색 엔진 연동** | Elasticsearch 등과 연계하여 인덱싱 가능하게 구성 |

---

## **🧪 Kafka는 언제 쓰는가?**

- 마이크로서비스 간 이벤트 기반 비동기 통신
- 실시간 로그 수집, 모니터링
- 스트리밍 분석 파이프라인 구축
- Kafka Streams + KSQL로 실시간 데이터 처리

---

## **🏷️ 태그 제안**

#Kafka #분산시스템 #메시지큐 #데이터베이스철학

#Consumer전략 #CompactedTopic #이벤트드리븐 #로그데이터베이스

---
