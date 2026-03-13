---
layout  : post
title   : Kubernetes NetworkPolicy
summary : 'Kubernetes 클러스터 내에서 > > > Pod 간 네트워크 통신을 제어 >'
date    : 2025-06-09 14:37:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : k8s
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Kubernetes NetworkPolicy
Created: 2025년 6월 9일 오후 2:37
Tags: k8s
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## **📘 Kubernetes NetworkPolicy 정리**

### **✅ NetworkPolicy란?**

> Kubernetes 클러스터 내에서
> 
> 
> **Pod 간 네트워크 통신을 제어**
> 
- 기본적으로는 모든 Pod 간 통신이 허용됨
- NetworkPolicy를 사용하면 **서비스 간 접근을 세밀하게 제어** 가능
- 보안을 강화하고 의도하지 않은 내부 접근을 막는 데 사용

---

### **🔧 구성 요소**

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: <정책 이름>
spec:
  podSelector:
    matchLabels:
      <대상 라벨>
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from: ...
  egress:
    - to: ...
```

| **필드** | **설명** |
| --- | --- |
| podSelector | 이 정책이 **적용될 대상 Pod** (라벨로 지정) |
| policyTypes | Ingress (수신), Egress (발신) 중 선택 |
| ingress.from | **어떤 Pod가 접근할 수 있는지** 조건 지정 |
| egress.to | **어디로 나가는 것을 허용할지** 지정 |

---

### **⚠️ 작동 조건**

- 적용된 Pod는 명시된 트래픽 외에는 **모두 차단**
- 아무 정책도 없으면 **기본적으로 모든 통신 허용**
- CNI(네트워크 플러그인)가 NetworkPolicy를 **지원해야 동작함**
    - 예: ✅ Calico, Cilium, Weave
    - 예: ❌ Flannel (기본 상태에서는 지원 안 함)

---

### **✅ 예시 1: 특정 Pod만 접근 허용 (Ingress)**

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-nginx-to-api
spec:
  podSelector:
    matchLabels:
      role: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: nginx
```

→ role=api Pod는 role=nginx인 Pod만 접근 가능

---

### **✅ 예시 2: 외부로 나가는 트래픽 차단 (Egress)**

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/8
```

→ app=backend Pod는 10.0.0.0/8 대역 IP로만 통신 가능

→ 외부 인터넷 접근 차단

---

### **🧪 사용 시 확인 명령어**

```
kubectl get networkpolicy -n <namespace>
kubectl describe networkpolicy <정책 이름> -n <namespace>
```

---

### **🚨 주의 사항 요약**

- 정책이 적용되면 **정책에 명시된 트래픽 외엔 모두 차단**
- **DNS가 막히는 경우도 있으므로, 필요 시 kube-dns 접근도 열어야 함**
- CNI가 NetworkPolicy를 **지원하지 않으면 적용해도 무효**

---

### **📌 요약**

| **항목** | **설명** |
| --- | --- |
| 목적 | Pod 간 통신 제어 (보안 강화) |
| 기본 동작 | 아무 정책 없으면 전체 허용 |
| 정책 적용 시 | 명시된 트래픽만 허용, 나머지 차단 |
| 방향 | Ingress, Egress 또는 둘 다 |
| 주의사항 | CNI 플러그인 반드시 확인 필요 |

---
