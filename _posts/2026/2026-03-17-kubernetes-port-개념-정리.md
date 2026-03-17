---
layout  : post
title   : Kubernetes 포트 개념 정리
summary : Kubernetes에서 containerPort, targetPort, Service port, nodePort가 각각 어떤 역할을 하는지 네트워크 흐름과 함께 정리합니다.
date    : 2026-03-17 09:30:00 +0900
updated : 2026-03-17 09:30:00 +0900
tag     : k8s kubernetes network
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

## 들어가며

Kubernetes를 사용하다 보면 `containerPort`, `targetPort`, `port`, `nodePort`가 함께 등장한다. 이름이 비슷해서 헷갈리기 쉽지만, 각 포트는 **서로 다른 계층에서 역할이 다르다**.

특히 Service와 Pod 사이의 트래픽 흐름을 이해하려면 다음 네 가지를 같이 봐야 한다.

- `containerPort`
- `targetPort`
- `port`
- `nodePort`

이 글에서는 각 포트가 무엇을 의미하는지, 실제 요청이 어떤 경로로 흘러가는지, 실무에서 자주 헷갈리는 포인트는 무엇인지 정리한다.

## 1. `containerPort`

`containerPort`는 **컨테이너가 실제로 listen 하고 있는 포트**를 의미한다.

예를 들어 애플리케이션이 `8080` 포트에서 HTTP 서버를 실행하고 있다면 다음과 같이 볼 수 있다.

```go
http.ListenAndServe(":8080", nil)
```

Pod spec에서는 다음처럼 표현한다.

```yaml
containers:
  - name: app
    image: myapp
    ports:
      - containerPort: 8080
```

여기서 중요한 점은 `containerPort`가 **트래픽 라우팅 자체에 반드시 필요한 값은 아니라는 것**이다.

- 주로 문서화 목적에 가깝다.
- `kubectl describe` 같은 도구에서 확인하기 좋다.
- 포트 이름 기반 Service 연결 시 메타데이터 역할을 한다.

즉, `containerPort`는 "이 컨테이너가 보통 이 포트로 통신합니다"라고 명시하는 선언에 가깝다.

## 2. `port` (Service Port)

`port`는 **Service가 요청을 받는 포트**다.

클라이언트는 직접 Pod에 붙는 것이 아니라 보통 Service를 통해 접근하므로, 먼저 Service의 `port`로 요청을 보낸다.

```yaml
apiVersion: v1
kind: Service
spec:
  ports:
    - port: 80
```

이 경우 클라이언트 입장에서는 다음처럼 보인다.

```text
client -> service:80
```

즉 `port`는 **Service의 입구 포트**라고 이해하면 된다.

## 3. `targetPort`

`targetPort`는 **Service가 받은 요청을 Pod의 어느 포트로 전달할지 결정하는 값**이다.

```yaml
ports:
  - port: 80
    targetPort: 8080
```

흐름은 다음과 같다.

```text
client -> service:80 -> pod:8080
```

정리하면:

| 구성 | 의미 |
| --- | --- |
| `port` | Service가 받는 포트 |
| `targetPort` | Service가 Pod로 전달하는 포트 |

실무에서는 `port: 80`, `targetPort: 8080` 조합을 자주 본다. 외부나 내부 클라이언트는 `80`으로 접근하고, 실제 애플리케이션은 컨테이너 안에서 `8080`으로 떠 있는 구조다.

## 4. `nodePort`

`nodePort`는 **외부에서 Node IP와 특정 포트로 접근할 수 있게 하는 포트**다.

```yaml
type: NodePort
ports:
  - port: 80
    targetPort: 8080
    nodePort: 30007
```

이 경우 전체 흐름은 다음과 같다.

```text
external client
  -> NodeIP:30007
  -> Service:80
  -> Pod:8080
```

즉 `nodePort`는 **클러스터 외부에서 노드로 들어오는 진입 포트**라고 보면 된다.

다만 실무에서는 `NodePort`를 직접 쓰기보다 보통 다음 구조를 더 많이 사용한다.

```text
Ingress -> Service -> Pod
```

## 전체 네트워크 흐름

위 개념을 한 줄로 연결하면 다음과 같다.

```text
외부 클라이언트
     |
     v
NodePort (30007)   <- optional
     |
     v
Service port (80)
     |
     v
targetPort (8080)
     |
     v
containerPort (8080)
```

여기서 `nodePort`는 선택 사항이고, `containerPort`는 메타데이터 성격이 강하다. 그래서 실제로 라우팅 관점에서 핵심은 보통 **Service의 `port`와 `targetPort`** 다.

## 카페 비유로 이해하기

이 개념은 카페 구조로 생각하면 조금 더 직관적이다.

| Kubernetes 개념 | 카페 비유 |
| --- | --- |
| `nodePort` | 건물 입구 |
| `port` | 주문 카운터 |
| `targetPort` | 바리스타 작업대 |
| `containerPort` | 커피 머신 |

손님 흐름은 다음과 같다.

```text
건물 입구(nodePort)
  -> 주문 카운터(service port)
  -> 바리스타 작업대(targetPort)
  -> 커피 머신(containerPort)
```

즉 손님은 주문 카운터로 요청하고, 내부적으로는 작업대와 머신이 실제 일을 처리하는 구조다.

## 실무에서 자주 헷갈리는 포인트

### `containerPort`와 `targetPort`는 꼭 같을 필요가 없다

많이 쓰는 형태는 다음과 같다.

```yaml
containerPort: 8080
targetPort: 8080
```

하지만 반드시 같아야 하는 것은 아니다.

```yaml
containerPort: 8080
targetPort: 9000
```

중요한 것은 **Service가 실제로 전달해야 할 Pod 포트가 무엇인가**다. 단, `targetPort`가 실제 애플리케이션이 listen 하는 포트와 다르면 당연히 연결이 실패한다.

즉 개념적으로는 다를 수 있지만, 실제 구성은 애플리케이션 포트와 일치해야 한다.

### `containerPort`가 없어도 Service는 동작할 수 있다

다음처럼 Service를 정의했다고 가정하자.

```yaml
ports:
  - port: 80
    targetPort: 8080
```

Pod spec에 `containerPort: 8080`이 없어도, 애플리케이션이 실제로 `8080`에서 listen 하고 있다면 Service 연결은 가능하다.

그래서 `containerPort`는 **필수 라우팅 설정이라기보다 명시적인 메타데이터**에 가깝다.

### `targetPort`는 숫자 대신 이름을 사용할 수도 있다

Pod에서 포트 이름을 정의하면:

```yaml
containers:
  - ports:
      - name: http
        containerPort: 8080
```

Service에서는 숫자 대신 이름으로 연결할 수 있다.

```yaml
ports:
  - port: 80
    targetPort: http
```

이 방식은 포트 번호가 바뀌더라도 이름 기준으로 연결할 수 있어 조금 더 읽기 쉬운 설정이 된다.

## 실무에서 많이 사용하는 구조

### 내부 서비스

내부 통신에서는 다음처럼 구성하는 경우가 많다.

```yaml
port: 80
targetPort: 8080
```

### 외부 서비스

외부 노출은 보통 `NodePort`를 직접 열기보다 다음 구조를 많이 사용한다.

```text
Ingress -> Service -> Pod
```

즉 외부 요청은 Ingress가 받고, Service는 내부 라우팅을 담당하며, Pod가 실제 애플리케이션을 처리하는 구조다.

## 요약

| 개념 | 역할 |
| --- | --- |
| `containerPort` | 컨테이너가 실제로 listen 하는 포트 |
| `targetPort` | Service가 Pod로 전달할 포트 |
| `port` | Service가 노출하는 포트 |
| `nodePort` | 외부에서 Node로 접근하는 포트 |

핵심만 다시 정리하면, 클라이언트는 보통 **Service의 `port`** 로 접근하고, Service는 그 요청을 **`targetPort`** 로 전달한다. `containerPort`는 컨테이너가 어떤 포트를 사용하는지 나타내는 선언이고, `nodePort`는 필요할 때만 외부 진입점으로 사용한다.

## 참고 자료

- Kubernetes 공식 문서 Service: https://kubernetes.io/docs/concepts/services-networking/service/
