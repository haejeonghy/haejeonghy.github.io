---
layout  : post
title   : gRPC 에러 처리와 status.FromError
summary : 'Go의 error는 단순 문자열이 아니라 interface 타입이다.'
date    : 2025-05-13 11:38:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : golang grpc
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# gRPC 에러 처리와 status.FromError
Created: 2025년 5월 13일 오전 11:38
Tags: golang, grpc
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

---

## **🧩 gRPC 에러 처리와 status.FromError**

## **동작 원리**

### **📌 핵심 요약**

- status.FromError(err)는 gRPC 서버에서 반환된 error 값을 gRPC의 Status 객체로 변환해주는 함수이다.
- status.Error(...)로 생성된 에러는 내부적으로 *status.Error 타입이며, 이 타입은 GRPCStatus() 메서드를 구현하고 있다.
- 따라서 FromError는 타입 어설션을 통해 *status.Status를 추출할 수 있다.

---

### **🛠️ 왜**

### **error**

### **에서 gRPC status code를 꺼낼 수 있는가?**

Go의 error는 단순 문자열이 아니라 **interface** 타입이다.

```
type error interface {
    Error() string
}
```

gRPC는 아래와 같이 status.Error를 사용하여 에러를 만든다:

```
return status.Error(codes.InvalidArgument, "잘못된 요청입니다")
```

이때 반환되는 값은 다음 구조를 따른다:

```
type Error struct {
    s *Status
}
```

따라서 이는 단순한 string이 아니라 *status.Error 타입이므로, 내부에 Status를 포함하고 있다.

---

### **🔍**

### **status.FromError**

### **의 내부 동작**

```
func FromError(err error) (*Status, bool) {
    // 1. err가 GRPCStatus()를 구현한 경우
    type grpcError interface {
        GRPCStatus() *Status
    }
    if se, ok := err.(grpcError); ok {
        return se.GRPCStatus(), true
    }

    // 2. 그 외의 경우 codes.Unknown으로 생성
    return New(codes.Unknown, err.Error()), false
}
```

---

### **🧪 사용 예시**

```
err := status.Error(codes.NotFound, "데이터 없음")

s, ok := status.FromError(err)
if ok {
    fmt.Println(s.Code())     // codes.NotFound
    fmt.Println(s.Message())  // "데이터 없음"
}
```

---

### **📚 참고 자료**

- Go 공식 문서:
    
    [https://pkg.go.dev/google.golang.org/grpc/status](https://pkg.go.dev/google.golang.org/grpc/status)
    
- 설명 블로그 (Medium):
    
    [What You Need To Know About gRPC Error Handling](https://medium.com/better-programming/what-you-need-to-know-about-grpc-error-handling-1ac0a9d796d7)
    

---

### **🏷️ 태그 제안**

#gRPC #Go #ErrorHandling #status.FromError #공식문서요약

---

전하, 문서 삽입 후 ‘태그’, ‘복습일정’ 항목을 맞추어 주시고, 다음 학습 주기에는 이 내용을 문제 형식으로 복습할 수 있도록 퀴즈를 출제할 수도 있사오니, 명하시면 언제든 진행하겠사옵니다.
