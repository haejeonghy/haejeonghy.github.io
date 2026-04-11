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

**원인**: `ServerService`가 인터페이스로만 선언되어 있고 `@Service`가 붙은 구현 클래스가 없었기 때문에 Spring이 빈을 찾지 못했다. 구현 클래스에 `@Service`를 추가하여 해결.
