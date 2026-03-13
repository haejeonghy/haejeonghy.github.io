---
layout  : post
title   : Kubernetes Service 라벨 충돌로 인한 502 이슈 정리
summary : 'Label → Pod을 부르는 명칭'
date    : 2025-11-28 16:37:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : k8s
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Kubernetes Service 라벨 충돌로 인한 502 이슈 정리
Created: 2025년 11월 28일 오후 4:37
Tags: k8s
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

Label → Pod을 부르는 명칭

Selector → Service에서 pod으로 트래픽을 넘기는 연결 규칙

---

## **1. 문제 상황**

- /v1/bankaccount/* 및 /v1/card/* API에서 **ingress 502 Bad Gateway**가 주기적으로 발생.
- 애플리케이션(pod) 레벨에서는 에러 증가 없음 → **ingress → service → pod** 사이에서 문제가 발생한 케이스.

---

## **2. 원인 분석 (Root Cause)**

### **✔ 내부 원인**

**배치 파드(batch job pod)가 bankaccount/card 서비스의 Deployment와 동일한 라벨(app=bankaccount)을 사용하고 있었음.**

Jenkins Pipeline에 다음 라벨이 정의되어 있었음:

```yaml
labels:
  app: bankaccount
  accountName: bankaccount
```

### **✔ Kubernetes 동작 원리와의 충돌**

- Service는 selector로 pod를 선택해 엔드포인트로 등록함.
- bankaccount Service는 다음과 같은 selector를 가짐:

```yaml
selector:
  app: bankaccount
```

- 따라서 동일한 라벨을 가진 **모든 pod**가 bankaccount의 endpoint 리스트에 포함됨.

### **✔ 잘못된 라우팅 발생**

- 배치 파드는 HTTP 서버가 아님.
- cronjob 종료 직전에는 **Terminating 상태**로 들어감.
- 이 상태의 배치 파드가 endpoint로 포함되면
    
    → ingress가 해당 파드로 요청을 전달
    
    → 파드는 응답 불가
    
    → ingress에서 502 발생
    

---

## **3. 왜 특정 시간대(18시 이후)에 더 많이 발생했는가?**

- 배치 파드 실행·종료가 집중적으로 발생하는 시간대였을 가능성이 큼.
- 배치 파드가 endpoint list에 잠깐 포함되면서 **확률적으로 API 요청이 배치 파드로 분배됨**.
- ingress 레벨에서만 502가 증가한 이유가 여기에 있음.

---

## **4. 해결 방향**

### **✔ 단기 해결 (즉시 적용 가능)**

### **1) 배치 파드의 라벨을 분리**

배치 job에 서비스 라벨(app=bankaccount)을 사용하지 않도록 수정.

예:

```
labels:
  app: bankaccount-batch
  jobType: batch
```

### **2) Service selector 강화**

Deployment만 식별하도록 selector를 다중 라벨로 구성.

Service:

```
selector:
  app: bankaccount
  type: deployment
```

Deployment:

```
labels:
  app: bankaccount
  type: deployment
```

Batch pod:

```
labels:
  app: bankaccount-batch
  type: batch
```

---

## **5. 장기 개선 방향**

- Jenkins batch job 스펙이 코드(IaC)로 관리되지 않고 pipeline 내부에만 존재 → **가시성/관리성 문제**
- batch job이 어떤 라벨을 사용할지에 대한 **팀 단위 라벨 표준화 필요**
- bankaccount/card 서비스는 구조가 동일하므로 **두 서비스 모두 수정 필요**
- 서비스 selector 설계 시 “Deployment만 대상으로 삼는 라벨 체계” 확립 필요

---

## **6. 이번 이슈에서 배운 점**

- Kubernetes Service는 selector에 매칭되는 모든 pod로 트래픽을 보낸다.
- 라벨 충돌은 API 장애로 즉시 이어지는 주요 원인이다.
- 배치 파드·테스트 파드·기타 임시 파드는 절대 서비스 라벨을 공유하면 안 된다.
- ingress 레벨의 502는 애플리케이션 레벨에서 보이지 않기 때문에
    
    **nginx ingress 로그, upstream pod 정보가 중요하다.**
