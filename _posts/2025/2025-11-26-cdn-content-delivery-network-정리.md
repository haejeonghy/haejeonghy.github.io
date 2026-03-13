---
layout  : post
title   : CDN(Content Delivery Network) 정리
summary : 'TTL 관리, Cache-Control 정책, 캐시 무효화 전략이 중요'
date    : 2025-11-26 23:02:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : network
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# CDN(Content Delivery Network) 정리
Created: 2025년 11월 26일 오후 11:02
Tags: Network
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

## **1. 개념**

- CDN은 **지리적으로 분산된 서버 네트워크**로, 사용자와 가장 가까운 위치에서 콘텐츠를 전달하는 시스템입니다.
- 웹사이트·앱의 정적 콘텐츠(이미지, CSS, JS, 동영상 등)를 **엣지 서버(Edge Server)**에 캐시해 빠르게 제공합니다.
- 참고:
    - Wikipedia – https://en.wikipedia.org/wiki/Content_delivery_network
    - IBM – https://www.ibm.com/think/topics/content-delivery-networks

---

## **2. 왜 중요한가**

- **로딩 속도 개선** → 사용자 경험(UX) 향상
- **원본 서버(Origin)의 부하 감소** → 트래픽 폭증 시 안정성 증가
- **글로벌 최적화** → 해외 사용자도 가까운 서버에서 콘텐츠 수신
- **보안 및 가용성 강화** → 일부 CDN 제공자는 DDoS 방어·WAF를 함께 제공
- 참고:
    - NetApp – https://www.netapp.com/data-services/what-is-content-delivery-network/

---

## **3. CDN 동작 흐름**

1. 사용자가 특정 도메인을 요청
2. DNS가 해당 요청을 **가장 가까운 CDN 엣지 서버로 라우팅**
3. 엣지 서버에 콘텐츠가 **캐시되어 있으면 즉시 응답**
4. 캐시가 없으면(origin miss) 원본 서버에서 가져와 캐시에 저장 후 응답
5. 이후 동일 콘텐츠 요청은 모두 엣지 서버에서 빠르게 처리
- 참고:
    - Cloudflare – https://www.cloudflare.com/learning/cdn/what-is-a-cdn/

---

## **4. 주요 용어 정리**

| **용어** | **설명** |
| --- | --- |
| **Origin Server** | 실제 원본 콘텐츠가 저장된 서버 |
| **Edge Server** | 사용자 위치와 가까운 CDN 캐시 서버 |
| **PoP(Point of Presence)** | CDN 제공업체가 구축한 물리 서버 지점 |
| **Cache** | 자주 요청되는 콘텐츠를 저장해 빠르게 제공하는 메커니즘 |
| **Pull CDN** | 요청이 있을 때 엣지가 원본에서 콘텐츠를 가져와 캐시 |
| **Push CDN** | 원본 서버가 콘텐츠를 미리 엣지로 전송해 배포 |

---

## **5. MSA/실무 운영 관점에서 CDN 사용 시 고려사항**

- 정적 리소스(이미지, 스크립트 등)를 CDN에 캐싱하면 **원본 API 서버 부하를 크게 줄일 수 있음**
- 동적 콘텐츠(사용자별 개인정보, 금융정보 등)는 캐시 위험이 있으므로
    
    **TTL 관리, Cache-Control 정책, 캐시 무효화 전략**이 중요
    
- 사내망/내부 네트워크 환경에서 프록시·방화벽을 거치면
    
    **엣지 선택이 비최적화될 수 있어 성능 저하**가 발생할 수 있음
    
- 원본 장애 시 CDN의 fallback 정책과 캐시 만료 시점이 중요
- 참고:
    - TechTarget – https://www.techtarget.com/searchnetworking/definition/CDN-content-delivery-network

---

## **6. 요약**

> CDN은 콘텐츠를 사용자에게
> 
> 
> **가장 가까운 서버에서 전달**
> 

> 속도를 크게 개선하고, 원본 서버의 부담을 줄이며,
> 

> 글로벌 환경에서도 안정적으로 서비스할 수 있게 해 주는 핵심 인프라입니다.
>
