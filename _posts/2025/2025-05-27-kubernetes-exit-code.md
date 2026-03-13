---
layout  : post
title   : kubernetes exit code
summary : 'Kubernetes에서 컨테이너의 종료 상태를 나타내는 Exit Code는 애플리케이션의 실행 결과를 진단하고 문제를 해결하는 데 중요한 정보를 제공합니다. 이러한 코드들은 주로 Unix/Linux 시스템의 종료 코'
date    : 2025-05-27 11:47:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : k8s
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# kubernetes exit code
Created: 2025년 5월 27일 오전 11:47
Tags: k8s
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

Kubernetes에서 컨테이너의 종료 상태를 나타내는 **Exit Code**는 애플리케이션의 실행 결과를 진단하고 문제를 해결하는 데 중요한 정보를 제공합니다. 이러한 코드들은 주로 Unix/Linux 시스템의 종료 코드 규칙을 따르며, Kubernetes 자체에서 정의한 것은 아닙니다. 아래는 자주 발생하는 Exit Code와 그 의미를 정리한 것입니다.

---

### **🧾 Kubernetes Exit Code 정리**

| **Exit Code** | **설명** |
| --- | --- |
| **0** | 정상 종료 (성공적으로 작업을 마침) |
| **1** | 일반적인 애플리케이션 오류 (예: 예외 처리 실패, 잘못된 명령어 등) |
| **2** | 셸 내장 명령어의 잘못된 사용 (예: 문법 오류) |
| **125** | 컨테이너 실행 명령 실패 (예: 잘못된 명령어 실행 시도) |
| **126** | 명령어는 존재하지만 실행 권한 없음 |
| **127** | 명령어나 파일을 찾을 수 없음 |
| **128** | 잘못된 종료 코드 사용 (0~255 범위를 벗어남) |
| **130** | 사용자가 Ctrl+C로 프로세스 종료 (SIGINT) |
| **134** | 비정상 종료 (SIGABRT, 예: abort() 호출) |
| **137** | 강제 종료 (SIGKILL, 예: OOMKilled) |
| **139** | 세그멘테이션 오류 (SIGSEGV, 잘못된 메모리 접근) |
| **143** | 우아한 종료 요청 (SIGTERM, 예: 스케일 다운, 롤링 업데이트 등) |
| **255** | 알 수 없는 오류 또는 종료 코드 범위 초과 |

---

### **🔍 주요 Exit Code 상세 설명**

### **Exit Code 0**

### **: 정상 종료**

- **의미**: 프로세스가 성공적으로 작업을 마치고 종료됨을 나타냅니다.
- **조치**: 특별한 조치 필요 없음.

### **Exit Code 1**

### **: 일반적인 애플리케이션 오류**

- **의미**: 애플리케이션 내부 오류로 인해 종료됨을 나타냅니다.
- **원인 예시**:
    - 잘못된 환경 변수 설정
    - 필수 파일 또는 디렉토리 누락
    - 애플리케이션의 예외 처리 실패
- **조치**: 컨테이너 로그를 확인하여 오류 원인을 파악하고 수정합니다.

### **Exit Code 137**

### **: 강제 종료 (SIGKILL)**

- **의미**: 컨테이너가 시스템에 의해 강제로 종료되었음을 나타냅니다.
- **주요 원인**:
    - 메모리 초과로 인한 OOMKilled
    - 사용자 또는 시스템에 의한 강제 종료
- **조치**:
    - kubectl describe pod <pod-name> 명령어로 이벤트 로그를 확인하여 OOMKilled 여부를 확인합니다.
    - 메모리 리소스 제한을 조정하거나 애플리케이션의 메모리 사용을 최적화합니다.

### **Exit Code 143**

### **: 우아한 종료 요청 (SIGTERM)**

- **의미**: Kubernetes가 컨테이너에 종료 요청을 보냈음을 나타냅니다.
- **주요 발생 시점**:
    - Pod 스케일 다운
    - 롤링 업데이트
    - 수동 Pod 삭제
- **조치**:
    - 애플리케이션이 SIGTERM 신호를 처리하여 종료 전에 필요한 정리 작업을 수행하도록 구현합니다.
    - terminationGracePeriodSeconds 값을 조정하여 애플리케이션이 충분한 시간 내에 종료 작업을 완료할 수 있도록 합니다.

---

### **🛠️ Exit Code 확인 방법**

- **Pod 상태 확인**:

```
  kubectl get pod <pod-name>
```

- **Pod 상세 정보 확인**:

```
  kubectl describe pod <pod-name>
```

- **컨테이너 종료 코드 확인**:

```
  kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].state.terminated.exitCode}'
```

- **컨테이너 로그 확인**:

```
  kubectl logs <pod-name> -c <container-name>
```

---

### **📚 참고 자료**

- [Komodor: Exit Codes in Docker and Kubernetes: The Complete Guide](https://komodor.com/learn/exit-codes-in-containers-and-kubernetes-the-complete-guide/)
- [Ananta Cloud: Understanding Kubernetes Exit Codes](https://www.anantacloud.com/post/kubernetes-exit-codes-decoded-common-problems-and-solutions)
- [Lumigo: Kubernetes Exit Code 143: A Practical Guide](https://lumigo.io/kubernetes-troubleshooting/kubernetes-exit-code-143-a-practical-guide/)

---
