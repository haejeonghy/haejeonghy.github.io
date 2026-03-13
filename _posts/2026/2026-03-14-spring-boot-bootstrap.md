---
layout  : post
title   : Spring Boot Bootstrap이란 무엇인가
summary : Spring Boot의 bootstrap 개념과 실행 흐름, bootstrap.yml 변화, 현재 확장 포인트를 정리합니다.
date    : 2026-03-14 09:00:00 +0900
updated : 2026-03-14 09:00:00 +0900
tag     : spring boot bootstrap config
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

## 1. Bootstrap이란 무엇인가

Spring에서 말하는 **bootstrap**이란,

> 애플리케이션이 완전히 시작되기 전에, 설정과 실행 환경을 먼저 준비하는 초기화 단계

를 의미합니다.

Spring Boot 기준으로 보면,

- `ApplicationContext`(스프링 컨테이너)가 생성되기 **이전**에
- 어떤 설정을 사용할지
- 설정을 어디서 가져올지
- 실행 프로파일과 환경 변수를 어떻게 적용할지

를 결정하는 단계입니다.

즉, bootstrap은 **비즈니스 로직이나 Bean 초기화 이전의 준비 단계**입니다.

```text
Spring Boot
 ├─ 애플리케이션 기동 전체를 담당
 │
 ├─ 그 안에
 │    └─ bootstrap 단계가 포함됨
 │
 └─ 이후
      ├─ ApplicationContext 생성
      └─ Bean 초기화 및 실행


[ Application Code Layer ]
  - Spring
  - Spring Boot
  - Spring Cloud

---------------------------------

[ Platform / Infra Layer ]
  - Kubernetes
  - Container Runtime
  - Network / Service
```

## 2. Bootstrap 단계가 필요한 이유

Spring 애플리케이션은 설정이 없으면 시작 자체가 불가능합니다.

예를 들면 다음과 같은 값들이 있습니다.

- DB 접속 정보 (URL, username, password)
- 서버 포트
- 외부 API 엔드포인트
- 시크릿 키
- 실행 프로파일 (dev / stage / prod)

이 값들은 **Bean이 생성되기 전부터 필요**합니다.

따라서 Spring 내부 흐름은 구조적으로 다음과 같이 나뉩니다.

```text
[ Bootstrap 단계 ]
- Environment 생성
- PropertySource 로딩
- 외부 설정 결정

        ↓

[ ApplicationContext 생성 ]
- BeanDefinition 로딩
- @Configuration 처리
- @ComponentScan 실행

        ↓

[ Bean 초기화 및 실행 ]
- @PostConstruct
- ApplicationRunner / CommandLineRunner
```

bootstrap은 이 중 **가장 처음 실행되는 단계**입니다.

## 3. Spring Boot 실행 시 Bootstrap 동작 흐름

Spring Boot 애플리케이션은 다음 순서로 시작됩니다.

### 3.1 SpringApplication.run()

```java
SpringApplication.run(MyApplication.class, args);
```

이 한 줄이 애플리케이션 전체 부트스트랩 과정을 시작합니다.

### 3.2 Environment 준비 (Bootstrap의 핵심)

이 단계에서 Spring은 `Environment` 객체를 생성합니다.

여기에 포함되는 정보는 다음과 같습니다.

- JVM 시스템 프로퍼티 (`-D` 옵션)
- OS 환경 변수
- 커맨드라인 인자
- `application.yml` / `application.properties`
- 외부 설정(Config Server 등)

이 시점에는 **아직 ApplicationContext도, Bean도 존재하지 않습니다.**

### 3.3 PropertySource 로딩 및 우선순위

설정 값들은 정해진 우선순위에 따라 로딩됩니다.

일반적인 우선순위는 다음과 같습니다.

1. 커맨드라인 인자
2. OS 환경 변수
3. JVM 시스템 프로퍼티
4. `application-{profile}.yml`
5. `application.yml`

이 과정이 바로 **bootstrap 단계의 실질적인 역할**입니다.

### 3.4 ApplicationContext 생성

Environment와 설정이 확정된 이후에야 다음 작업이 진행됩니다.

- `ApplicationContext` 생성
- BeanDefinition 로딩
- `@Configuration` 클래스 처리
- `@ComponentScan` 실행

즉, **bootstrap 단계에서는 Bean을 사용할 수 없습니다.**

## 4. 과거의 bootstrap.yml과 현재 방식

### 4.1 bootstrap.yml의 역할 (과거)

Spring Boot 2.3 이전, Spring Cloud Config를 사용할 경우 `bootstrap.yml`이 사용되었습니다.

```yaml
spring:
  application:
    name: my-service
  cloud:
    config:
      uri: http://config-server
```

의미는 다음과 같습니다.

- Config Server에 접속하기 위한 설정을
- `application.yml`보다 **먼저 로딩**

즉,

> "설정을 가져오기 위한 설정"

을 담는 파일이었습니다.

### 4.2 현재(Spring Boot 2.4 이후)의 변경 사항

Spring Boot 2.4부터는 `bootstrap.yml` 방식이 deprecated 되었습니다.

대신 **Config Data API**가 도입되었습니다.

```yaml
spring:
  config:
    import: "optional:configserver:http://config-server"
```

bootstrap 개념 자체가 사라진 것은 아니며, **구현 방식만 통합되고 변경**되었습니다.

## 5. 현재 기준에서의 Bootstrap 확장 지점

현재 bootstrap 단계는 파일이 아니라 **확장 포인트(Extension Point)**로 다뤄집니다.

### 5.1 EnvironmentPostProcessor

```java
public class CustomEnvProcessor implements EnvironmentPostProcessor {
    @Override
    public void postProcessEnvironment(
        ConfigurableEnvironment environment,
        SpringApplication application
    ) {
        // Bean 생성 이전, 설정 조작 가능
    }
}
```

특징:

- Bean 생성 이전 실행
- PropertySource 수정 가능
- bootstrap 단계에서 설정을 바꿀 수 있는 핵심 수단

### 5.2 ApplicationContextInitializer

```java
public class CustomInitializer
        implements ApplicationContextInitializer<ConfigurableApplicationContext> {

    @Override
    public void initialize(ConfigurableApplicationContext context) {
        // ApplicationContext 생성 직후, Bean 초기화 전
    }
}
```

`EnvironmentPostProcessor` 이후, `ApplicationContext`가 만들어진 직후에 실행됩니다.

## 6. 실무에서 Bootstrap이 사용되는 대표적인 사례

Spring Boot 기반 MSA 환경에서 bootstrap 단계는 주로 다음 용도로 사용됩니다.

- Spring Cloud Config
- Vault
- AWS Parameter Store / Secrets Manager
- DB 비밀번호 복호화
- KMS 키 로딩
- 환경별 Feature Toggle 초기 결정

공통점은 모두 **Bean 이전에 반드시 결정되어야 하는 설정**이라는 점입니다.

## 7. 카페 운영으로 비유한 Bootstrap 개념

카페를 연다고 가정하면:

- Bootstrap 단계: 오늘 영업 여부 결정, 메뉴판 로딩 위치 결정, 원두 공급처 확인, 결제 수단 사용 가능 여부 확인
- Spring Context 단계: 바리스타 배치, POS 기동
- 비즈니스 로직 단계: 주문 접수, 음료 제조

즉, **가게 문을 열기 전에 준비하는 모든 과정이 bootstrap**에 해당합니다.

## 8. 핵심 요약

- Bootstrap은 파일명이 아니라 **애플리케이션 초기화 단계 개념**이다.
- Spring 컨테이너(`ApplicationContext`) 생성 **이전에 실행**된다.
- 목적은 하나다.

> 어떤 설정과 환경으로 이 애플리케이션을 실행할지 결정하는 것

- 현재는 `bootstrap.yml` 대신 Config Data API와 Environment 확장 방식을 사용한다.

## 9. 공식 문서 참고 링크

- Spring Boot Externalized Configuration
  - https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config
- Spring Boot Config Data API
  - https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config.files.configtree
- Spring Cloud Config Reference
  - https://docs.spring.io/spring-cloud-config/docs/current/reference/html/
