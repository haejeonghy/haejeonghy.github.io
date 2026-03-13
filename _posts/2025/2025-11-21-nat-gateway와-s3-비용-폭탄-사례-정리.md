---
layout  : post
title   : NAT Gateway와 S3 비용 폭탄 사례 정리
summary : 'URL: https://news.hada.io/topic?id=24504'
date    : 2025-11-21 12:36:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : aws 인프라
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# NAT Gateway와 S3 비용 폭탄 사례 정리
Created: 2025년 11월 21일 오후 12:36
Tags: AWS, 인프라
URL: https://news.hada.io/topic?id=24504
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

1. 핵심 이해

EC2 → S3 업로드 자체는 무료

하지만 EC2가 S3에 접근할 때 NAT Gateway를 통해 나가면 비용이 발생

이유: NAT Gateway는

시간당 비용

처리한 데이터(GB) 단위 비용
을 별도로 부과함

---

1. 구조 비유 (VPC = 감옥)

VPC: 보안이 유지되는 감옥 내부

프라이빗 서브넷 EC2: 감옥 내부 직원

NAT Gateway: 감옥 밖으로 나갈 수 있는 공식 검문소

프라이빗 EC2가 외부로 나갈 때는 반드시 NAT Gateway를 지나게 됨

이 검문소를 통해 대량의 트래픽이 지나가면 비용 폭증

---

1. 문제의 원인 (사건 이해)

EC2가 S3에 접근할 때 직접 S3 Endpoint로 가지 않음

대신 NAT Gateway → 인터넷 → S3로 우회함

AWS는 이를

“EC2 → NAT Gateway → 외부로 나가는 트래픽”
으로 인식

결과적으로 NAT 처리 비용 폭탄 발생

---

1. 해결 방법

S3 Gateway VPC Endpoint 사용

프라이빗 서브넷에서 S3를 NAT 없이 바로 접근할 수 있는 별도 통로

비용: 무료

NAT를 우회하므로 트래픽 비용 절감 효과 매우 큼

---

1. 결론

EC2 → S3 업로드는 무료가 맞음

하지만 NAT Gateway를 경유하면 유료

원인은 S3 VPC Endpoint 미구현

대량 데이터 전송 시 반드시

S3 VPC Endpoint

혹은 PrivateLink
등을 사용해 NAT를 우회해야 함

---
