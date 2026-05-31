---
layout: post
title: DataSource와 Connection Pool이 왜 헷갈릴까
summary: DataSource와 connection pool이 왜 같은 뜻처럼 들리는지, DataSource의 실제 역할과 용도를 중심으로 차이와 관계를 자세히 정리합니다.
date: 2026-05-31 15:24:00 +0900
updated: 2026-05-31 15:24:00 +0900
tag: datasource jdbc database spring connection-pool hikari
toc: true
comment: false
public: true
---
- TOC
  {:toc}

## 1. 왜 `DataSource`와 `connection pool`이 자꾸 같은 말처럼 들릴까

Spring이나 JDBC를 공부하다 보면 아래 같은 표현을 자주 본다.

- `DataSource`를 등록한다
- `HikariDataSource`를 쓴다
- connection pool 설정을 조정한다
- `DataSource`에서 커넥션을 가져온다

이쯤 되면 자연스럽게 이런 생각이 든다.

> 그래서 `DataSource`가 곧 connection pool 아닌가?

이 오해는 꽤 자연스럽다.

왜냐하면 실무에서 가장 자주 만나는 `DataSource` 구현체가 실제로는 풀링 기능을 함께 제공하는 경우가 많기 때문이다.

대표적으로 Spring Boot에서 기본으로 많이 보게 되는 `HikariDataSource`가 그렇다.

하지만 개념적으로 보면 둘은 같은 것이 아니다.

- `DataSource`
  애플리케이션이 데이터베이스 연결을 얻기 위한 표준 인터페이스이자 진입점
- `connection pool`
  데이터베이스 연결을 미리 만들어두고 재사용해서 성능을 높이는 기법 또는 구성요소

즉, `DataSource`는 역할이고, `connection pool`은 구현 전략 또는 내부 메커니즘에 가깝다.

## 2. 가장 짧게 요약하면

먼저 한 줄씩 요약하면 아래와 같다.

- `DataSource`
  "DB 연결을 어떻게 얻을지"를 애플리케이션에 제공하는 추상화
- `connection pool`
  "DB 연결을 새로 만들지 말고 재사용하자"는 자원 관리 방식

이 둘은 자주 함께 등장하지만 질문의 방향이 다르다.

- `DataSource`는 인터페이스와 책임의 관점
- `connection pool`은 성능과 자원 관리의 관점

## 3. `DataSource`의 핵심 역할은 무엇인가

`DataSource`를 단순히 "커넥션을 주는 객체" 정도로만 이해하면 반만 이해한 것이다.

실제로는 아래 역할을 함께 가진다.

### 3.1 애플리케이션의 DB 연결 진입점

애플리케이션 코드는 보통 `DriverManager.getConnection(...)`을 직접 매번 호출하지 않는다.

대신 `DataSource`를 통해 연결을 얻는다.

```java
Connection connection = dataSource.getConnection();
```

즉, 애플리케이션 입장에서는 "DB 연결이 필요하면 `DataSource`에게 요청한다"가 기본 모델이다.

이것이 첫 번째 역할이다.

### 3.2 연결 생성 방법을 숨기는 추상화

호출하는 쪽은 보통 이런 것을 몰라도 된다.

- 실제 JDBC URL이 무엇인지
- 사용자명과 비밀번호가 무엇인지
- 매번 새 연결을 만드는지
- 풀에서 꺼내는지
- 프록시 커넥션을 반환하는지

즉, `DataSource`는 **연결 획득 방식의 구현 세부사항을 감춘다**.

애플리케이션은 그저 `getConnection()`만 호출하면 된다.

### 3.3 프레임워크 통합 지점

Spring, JPA, MyBatis, `JdbcTemplate`, 트랜잭션 매니저 같은 것들은 대체로 `DataSource`를 기준으로 동작한다.

예를 들면:

- `JdbcTemplate`는 `DataSource`에서 커넥션을 얻는다
- `DataSourceTransactionManager`는 `DataSource` 기준으로 트랜잭션을 묶는다
- JPA도 내부적으로 JDBC 연결이 필요할 때 `DataSource`를 참조할 수 있다

즉, `DataSource`는 단순 유틸리티 객체가 아니라 프레임워크가 DB 접근을 조직하는 핵심 접점이다.

여기서 말하는 영속성(persistence)도 결국 데이터가 메모리를 넘어 DB에 저장되고 다시 조회되는 흐름을 뜻하는데, 이 영속성 계층이 실제 DB와 통신하려면 최종적으로는 `DataSource`를 통한 JDBC 연결이 필요하다.

참고로 `JdbcTemplate`의 용도는 JDBC 반복 코드를 줄이는 데 있다.

- 커넥션 획득
- `PreparedStatement` 생성
- 파라미터 바인딩
- `ResultSet` 순회
- 예외 변환
- 커넥션 반납

같은 작업을 템플릿화해서, 개발자는 SQL과 매핑 코드에 더 집중하게 만든다.

반면 MyBatis는 단순 JDBC 보조 유틸리티라기보다 SQL 매퍼 프레임워크에 가깝다.

- `JdbcTemplate`
  JDBC 위에서 비교적 얇게 동작하며 SQL 실행을 편하게 해주는 도구
- MyBatis
  SQL을 매퍼 XML이나 인터페이스에 선언하고 객체 매핑까지 조직해주는 프레임워크

즉, 둘 다 결국 내부적으로는 `DataSource`를 통해 커넥션을 얻지만, `JdbcTemplate`는 JDBC 작업 단순화에 더 가깝고 MyBatis는 SQL 매핑 구조화에 더 가깝다.

### 3.4 운영 설정의 캡슐화

보통 운영 환경에서는 아래 정보가 함께 붙는다.

- JDBC URL
- 계정 정보
- 커넥션 타임아웃
- 최대 풀 크기
- idle connection 관리
- validation query
- leak detection

이런 설정들이 보통 `DataSource` 수준에서 캡슐화된다.

즉, `DataSource`는 단지 커넥션 하나를 반환하는 객체라기보다, **DB 연결 정책 전체를 들고 있는 구성 요소**로 보는 편이 맞다.

## 4. connection pool은 정확히 무엇인가

반대로 `connection pool`은 역할보다 메커니즘에 더 가깝다.

DB 연결은 비싼 자원이다.

매 요청마다 아래 과정을 반복하면 비용이 크다.

- 소켓 연결
- 인증
- 세션 생성
- 드라이버 초기화

그래서 보통은 연결을 미리 몇 개 만들어 두고 재사용한다.

이것이 connection pool이다.

즉, connection pool의 관심사는 아래와 같다.

- 연결을 몇 개 유지할까
- 최대 몇 개까지 열 수 있을까
- 놀고 있는 연결은 언제 정리할까
- 죽은 연결은 어떻게 감지할까
- 동시에 연결 요청이 많으면 어떻게 대기시킬까

이건 전형적으로 자원 관리 문제이다.

## 5. 왜 실무에서는 둘이 거의 붙어 다닐까

이제 헷갈리는 이유가 나온다.

실무에서 많이 쓰는 `DataSource` 구현체가 connection pool 기능을 내부에 같이 담고 있기 때문이다.

예를 들면:

- `HikariDataSource`
- Apache DBCP 기반 `DataSource`
- C3P0 기반 `DataSource`

이 구현체들은 바깥으로는 `DataSource`처럼 보이지만, 내부적으로는 connection pool을 운영한다.

즉, 애플리케이션은 `DataSource`를 사용하지만 실제 동작은 "풀에서 커넥션을 빌려주고 반납받는 방식"일 수 있다.

그래서 실무에서는 아래 문장이 자연스럽게 섞인다.

- "`DataSource` 설정을 조정한다"
- "풀 크기를 늘린다"

둘 다 같은 객체 주변에서 일어나는 일이기 때문이다.

## 6. 같은 코드로 보면 더 분명하다

### 6.1 `DriverManager` 직접 사용

가장 원시적인 방식은 아래와 같다.

```java
Connection connection = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/app",
    "user",
    "password"
);
```

이 방식은 작동은 하지만, 애플리케이션 코드가 연결 생성 세부사항에 직접 묶인다.

문제는 아래와 같다.

- 설정이 코드에 노출된다
- 테스트가 불편하다
- 프레임워크 통합이 약하다
- 풀링을 붙이기 어렵다

### 6.2 `DataSource` 사용

```java
Connection connection = dataSource.getConnection();
```

이 코드만 보면 단순하지만, 사실 이 안에는 많은 것이 숨겨질 수 있다.

- 직접 새 연결 생성
- 풀에서 기존 연결 반환
- 프록시 객체 반환
- 트랜잭션 컨텍스트와 연결

즉, `DataSource`의 장점은 호출 코드가 단순해지는 것보다도 **연결 획득 정책을 교체 가능하게 만든다**는 데 있다.

## 7. `DataSource`의 용도를 더 자세히 보면

이 글에서 가장 중요한 부분은 여기다.

`DataSource`는 왜 필요한가?

단순히 "커넥션을 얻기 쉽게 하려고"만은 아니다.

### 7.1 애플리케이션 코드와 연결 생성 코드를 분리하기 위해

비즈니스 코드가 매번 아래를 알 필요는 없다.

- URL
- 계정
- 드라이버 종류
- 풀링 정책

이것을 `DataSource`가 대신 가진다.

즉, 서비스 코드는 "연결이 필요하다"만 표현하고, "어떻게 연결되는가"는 `DataSource`가 책임진다.

### 7.2 구현체 교체를 쉽게 하기 위해

예를 들어 아래는 모두 가능하다.

- 개발 환경에서는 간단한 `DataSource`
- 운영 환경에서는 `HikariDataSource`
- 테스트에서는 임베디드 DB용 `DataSource`

호출 코드는 같고, 구현체만 바뀐다.

이 점이 추상화의 가장 큰 힘이다.

### 7.3 풀링, 모니터링, 설정을 붙이기 위해

`DataSource`는 보통 connection pool과 결합되면서 아래 기능을 자연스럽게 수용한다.

- 최대 연결 수 제어
- idle timeout
- connection validation
- metrics 수집
- leak 탐지

즉, `DataSource`는 단순 추상화에 그치지 않고 운영 편의성의 중심점이 되기도 한다.

### 7.4 트랜잭션 관리와 연동하기 위해

Spring에서 트랜잭션은 보통 `DataSource`를 기준으로 연결을 묶는다.

즉 한 요청 안에서:

- 같은 트랜잭션이면 같은 연결을 재사용하고
- 트랜잭션이 끝나면 적절히 반환하고
- auto-commit과 rollback을 통제한다

이런 흐름의 중심에 `DataSource`가 놓인다.

이건 단순한 풀링과는 또 다른 역할이다.

### 7.5 프레임워크의 공통 계약이 되기 위해

라이브러리와 프레임워크는 "DB에 연결이 필요하다"는 공통 요구를 가진다.

이때 모두가 `DriverManager`를 제각각 사용하면 통합이 어렵다.

그래서 `DataSource`라는 공통 계약을 기준으로 생태계가 맞춰진다.

즉, `DataSource`는 단지 객체 하나가 아니라 JDBC 생태계의 표준 접점이다.

## 8. `DataSource`가 꼭 풀이어야 할까

아니다.

이 점이 매우 중요하다.

`DataSource`는 인터페이스이고, connection pool은 선택 가능한 구현 전략이다.

즉:

- 풀링 없는 `DataSource`도 가능하다
- 풀링 있는 `DataSource`도 가능하다

실무에서는 풀링 있는 구현체가 거의 기본값처럼 쓰여서 잘 안 느껴질 뿐이다.

그래서 아래 문장은 정확하다.

> 모든 connection pool 기반 DB 접근은 보통 `DataSource`를 통해 노출되지만, 모든 `DataSource`가 곧 connection pool인 것은 아니다.

## 9. 왜 `HikariDataSource`가 특히 더 헷갈리게 만들까

Spring Boot에서는 `HikariCP`를 많이 사용한다.

그런데 클래스 이름이 `HikariDataSource`다.

이 이름만 보면 이런 인상이 생긴다.

- `DataSource`구나
- 동시에 풀 설정도 있네
- 결국 둘이 같은 말 아닌가?

실제로는 이렇게 이해하는 편이 정확하다.

- `DataSource`
  외부에 보여주는 역할
- Hikari pool
  내부에서 연결을 관리하는 방식

즉, `HikariDataSource`는 `DataSource` 인터페이스를 구현한 객체이면서, 내부적으로는 Hikari connection pool을 운영하는 구현체라고 보면 된다.

## 10. `HikariCP`와 `HikariDataSource`의 관계를 정확히 보면

여기서 한 번 더 정리해보자.

이 둘은 같은 단어가 아니다.

- `HikariCP`
  connection pool 라이브러리 또는 풀링 기술 이름
- `HikariDataSource`
  그 풀링 기능을 품고 있으면서 `DataSource` 인터페이스를 구현한 구체 클래스

즉, `HikariCP`는 "풀 엔진"에 가깝고, `HikariDataSource`는 애플리케이션이 실제로 주입받아 사용하는 `DataSource` 구현체에 가깝다.

이 관계를 코드로 보면 느낌이 더 온다.

```java
HikariDataSource dataSource = new HikariDataSource();
dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/app");
dataSource.setUsername("user");
dataSource.setPassword("password");
dataSource.setMaximumPoolSize(10);
```

이 코드에서 보이는 것이 핵심이다.

- 애플리케이션은 `dataSource` 객체를 사용한다
- 그런데 그 객체에는 풀 크기 같은 Hikari 설정도 같이 들어간다

즉, 하나의 객체 안에:

- `DataSource`로서의 역할
- Hikari connection pool 설정과 운영 기능

이 함께 들어 있다.

바로 이 점 때문에 `DataSource`와 pool이 머릿속에서 하나처럼 붙는다.

### 10.1 Spring Boot에서는 왜 더 헷갈릴까

Spring Boot에서는 보통 개발자가 직접 풀을 조립하지 않아도 된다.

예를 들어 설정 파일에 이런 값을 넣으면:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/app
    username: user
    password: password
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
```

애플리케이션 입장에서는 그냥 `DataSource` 빈 하나가 생긴 것처럼 보인다.

하지만 내부적으로는:

- Spring Boot가 `DataSource`를 구성하고
- 그 구현체로 `HikariDataSource`를 쓰고
- Hikari 설정을 함께 주입하고
- 결국 Hikari pool이 연결을 관리한다

는 구조가 된다.

즉, 코드에서 보는 것은 `DataSource`인데 실제 운영 메커니즘은 `HikariCP`인 셈이다.

### 10.2 그래서 정확한 문장은 이렇게 된다

- Spring Boot는 보통 `DataSource` 빈을 제공한다
- 그 빈의 실제 구현체가 `HikariDataSource`일 수 있다
- `HikariDataSource`는 내부적으로 HikariCP connection pool을 사용한다

이렇게 이해하면 세 층이 분리된다.

- 추상화: `DataSource`
- 구현체: `HikariDataSource`
- 내부 메커니즘: HikariCP

## 11. 카페 비유로 보면

비유로 보면 더 쉽다.

### 11.1 `DataSource`

`DataSource`는 카페의 "주문 창구"에 가깝다.

손님 입장에서는:

- 주문이 필요하면 창구로 간다
- 내부 주방 구조는 몰라도 된다
- 누가 커피를 만드는지 몰라도 된다

즉, 외부에 노출된 공식 진입점이다.

### 11.2 connection pool

connection pool은 주방 안쪽의 "미리 준비된 컵과 도구를 재사용하는 운영 방식"에 가깝다.

손님은 보통 이것을 직접 보지 못한다.

중요한 것은:

- 내부 자원을 미리 준비해둔다
- 새로 만들지 않고 재사용한다
- 너무 많이 쓰면 대기시킨다

즉, 내부 효율화 전략이다.

이 비유로 보면 둘의 차이가 자연스럽다.

- `DataSource`는 외부 진입점
- connection pool은 내부 운영 방식

### 11.3 Hikari는 이 비유에서 어디인가

Hikari는 주문 창구 자체라기보다, 주방 안에서 컵과 머신과 작업 순서를 매우 빠르게 관리하는 운영 팀에 가깝다.

즉:

- 손님은 창구인 `DataSource`를 본다
- 내부에서는 Hikari가 자원 재사용을 최적화한다

그래서 손님 입장에서는 둘이 하나처럼 보이지만, 내부 책임은 다르다.

## 12. 실무에서 어떻게 구분해서 말하면 좋을까

아래처럼 말하면 비교적 정확하다.

### 12.1 이런 말은 정확하다

- "`DataSource`를 통해 DB 연결을 얻는다"
- "`DataSource` 구현체로 `HikariDataSource`를 사용한다"
- "connection pool의 최대 크기를 조정한다"
- "현재 `DataSource`는 내부적으로 풀링을 사용한다"
- "Spring Boot의 `DataSource`가 내부적으로 HikariCP를 사용한다"

### 12.2 이런 말은 문맥에 따라 부정확할 수 있다

- "`DataSource`는 그냥 풀이다"
- "`DataSource`와 pool은 같은 말이다"
- "`Hikari`가 곧 `DataSource` 그 자체다"

실무 대화에서는 대충 통할 수 있어도, 개념 설명으로는 좋지 않다.

## 13. 정리하면

혼동의 원인은 간단하다.

- 많이 쓰는 `DataSource` 구현체가 풀링을 내장한다
- Spring Boot에서 그 구현체를 기본처럼 만난다
- 그래서 추상화와 구현 전략이 머릿속에서 섞인다
- 그리고 그 대표 구현체가 바로 `HikariDataSource`라서 이름 차원에서도 더 헷갈린다

하지만 개념적으로는 아래처럼 정리하는 것이 맞다.

- `DataSource`
  애플리케이션이 DB 연결을 얻기 위한 표준 추상화이자 프레임워크 통합 지점
- connection pool
  DB 연결을 재사용하기 위한 자원 관리 메커니즘
- `HikariCP`
  그 connection pool 메커니즘을 제공하는 대표 구현체
- `HikariDataSource`
  `DataSource` 인터페이스를 구현하면서 내부적으로 HikariCP를 사용하는 구체 클래스

이 글에서 가장 중요한 한 줄만 남기면 이것이다.

> `DataSource`는 "연결을 어떻게 제공할 것인가"의 인터페이스이고, connection pool은 "그 연결을 얼마나 효율적으로 관리할 것인가"의 구현 전략이며, `HikariCP`는 그 구현 전략의 대표 사례이다.
