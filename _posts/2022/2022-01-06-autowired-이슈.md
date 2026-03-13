---
layout  : post
title   : Autowired 이슈
summary : 'Error starting ApplicationContext. To display the conditions report re-run your application with ''debug'' enabled. 2022-0'
date    : 2022-01-06 22:28:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : spring
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Autowired 이슈
Created: 2022년 1월 6일 오후 10:28
Tags: spring
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

```jsx
Error starting ApplicationContext. To display the conditions report re-run your application with 'debug' enabled.
2022-01-06 22:27:50.791 ERROR 7180 --- [           main] o.s.b.d.LoggingFailureAnalysisReporter   : 

***************************
APPLICATION FAILED TO START
***************************

Description:

Field service in kr.co.shelter.web.server.controller.ServerController required a bean of type 'kr.co.shelter.web.server.service.ServerService' that could not be found.

The injection point has the following annotations:
	- @org.springframework.beans.factory.annotation.Autowired(required=true)

Action:

Consider defining a bean of type 'kr.co.shelter.web.server.service.ServerService' in your configuration.

Process finished with exit code 1
```

```
@Autowired
ServerService service;
```

@Autowired로 자동 주입 설정한 service 빈을 찾지 못하는 이슈 발생. 

- @Service 어노테이션 빠뜨렸을 경우에 발생하는 케이스 있음
    - Service 인터페이스에서 클래스로 변경, 메소드에 바디 추가해서 테스트 → 성공!

Review: 너무 쉽게 해결됨. 아마 서비스 클래스가 인터페이스로 선언되서 구현을 해 실제 서비스가 필요했는데 그걸 놓친 거 같음.
