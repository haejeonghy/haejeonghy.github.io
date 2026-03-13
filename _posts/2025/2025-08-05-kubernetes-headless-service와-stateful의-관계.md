---
layout  : post
title   : Kubernetes Headless Service와 Stateful의 관계
summary : 'Kubernetes Headless Service와 Stateful의 관계의 핵심 개념과 실무 포인트를 정리합니다.'
date    : 2025-08-05 23:10:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : k8s
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Kubernetes Headless Service와 Stateful의 관계
Created: 2025년 8월 5일 오후 11:10
Tags: k8s
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

## 1. Headless Service란?

- Kubernetes에서 **`clusterIP: None`** 으로 설정된 서비스
- 일반적인 ClusterIP 서비스와 달리, **중앙의 가상 IP(ClusterIP)가 생성되지 않음**
- 서비스 이름으로 DNS 질의 시, **각 Pod의 실제 IP가 전부 반환됨**
- 클라이언트는 반환된 Pod IP들 중에서 **직접 선택하여 연결 가능**

## 2. 일반 서비스와의 비교

| 항목 | 일반 Service (ClusterIP) | Headless Service |
| --- | --- | --- |
| ClusterIP 존재 여부 | 있음 | 없음 (`clusterIP: None`) |
| DNS 질의 결과 | 단일 ClusterIP 반환 | 각 Pod의 IP 전부 반환 |
| 라우팅 방식 | kube-proxy가 로드밸런싱 처리 | 클라이언트가 직접 Pod 선택 |
| 활용 사례 | 일반 API 서버 등 | StatefulSet, Kafka, Redis 등 |

## 3. 왜 Headless가 필요한가?

### 3.1 Pod 개별 접근 (Stateful 애플리케이션)

- Kafka, Cassandra, Redis Sentinel 등은 **각 노드(Pod)가 고유한 역할**을 가짐
- Headless Service를 사용하면 **Pod별 고정 DNS 주소로 직접 접근 가능**
    - 예: `my-app-0.my-app.default.svc.cluster.local`

### 3.2 클라이언트 측 커스텀 로드밸런싱

- 일반 서비스는 round-robin 등 고정된 방식
- Headless는 클라이언트가 **latency, 부하, 해시 등 기준으로 직접 선택 가능**

### 3.3 서비스 디스커버리 목적

- 외부 애플리케이션이 DNS 질의를 통해 **전체 Pod 목록을 조회**하고 직접 연결
- 예: Kafka 클라이언트가 브로커 목록을 알아내기 위해 사용

## 4. Headless + StatefulSet 조합

- StatefulSet은 Pod 이름, 볼륨, DNS가 **재시작되어도 고정**
- Headless 서비스는 이를 가능하게 하는 **DNS 인프라 역할**
- 필수 조건: **Pod 간 고정 통신이 필요한 경우**

## 5. 요약

- Headless는 ClusterIP가 없는 서비스로, Pod IP를 그대로 DNS로 노출
- 클라이언트가 직접 Pod에 연결하는 구조로, stateful한 구조에 적합
- 로드밸런싱 제어, 고정된 Pod 접근, 서비스 디스커버리 등에 유리
- 대표적으로 StatefulSet과 함께 사용됨

## 6. 참고 링크

- Kubernetes 공식 문서: [https://kubernetes.io/docs/concepts/services-networking/service/#headless-services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)
- IBM Cloud 설명글: [https://www.ibm.com/cloud/blog/stateful-vs-stateless](https://www.ibm.com/cloud/blog/stateful-vs-stateless)
