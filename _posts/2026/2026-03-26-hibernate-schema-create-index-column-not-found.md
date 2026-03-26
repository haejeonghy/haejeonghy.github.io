---
layout  : post
title   : Hibernate 스키마 생성 중 Column not found가 나는 이유
summary : JPA 테스트에서 Hibernate가 create index 실행 중 Column not found로 실패하는 원인과 확인 포인트를 정리합니다.
date    : 2026-03-26 16:10:00 +0900
updated : 2026-03-26 16:10:00 +0900
tag     : jpa hibernate database test
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

## 배경

테스트를 실행하다 보면 비즈니스 로직에 진입하기도 전에 애플리케이션이 뜨는 과정에서 예외가 발생하는 경우가 있다. 이번에 본 로그도 그런 종류였다. 서비스 코드가 실패한 것이 아니라, Hibernate가 테스트용 데이터베이스 스키마를 자동 생성하는 과정에서 실패한 케이스였다.

흐름은 대략 다음과 같다.

1. 엔티티 매핑 정보를 읽는다.
2. `create table` SQL을 만든다.
3. `create index` SQL을 만든다.
4. 테스트 DB에 실행한다.
5. 실행 중 특정 DDL이 실패한다.

즉 이번 에러는 애플리케이션 로직 에러가 아니라 스키마 생성 에러로 보는 것이 맞다.

## 실제로 실패한 작업

로그에서 실패한 SQL은 다음과 같은 형태였다.

```sql
create index idx_sample_token_m1
on sample_token
(client_id, expired_at, scheduled_at, is_active)
```

여기서 Hibernate는 `sample_token` 테이블에 대해 복합 인덱스를 만들려고 했다.

복합 인덱스는 여러 컬럼을 묶어서 만드는 인덱스다. 예를 들어 아래 조건으로 자주 조회한다면 DB는 해당 조합으로 빠르게 찾기 위한 색인을 만들 수 있다.

- `client_id`: 어느 고객인지
- `expired_at`: 만료 시각
- `scheduled_at`: 예약 시각
- `is_active`: 활성 여부

## 직접적인 실패 원인

로그의 핵심은 아래 한 줄이다.

```text
Column "scheduled_at" not found
```

이 메시지로부터 확실하게 말할 수 있는 것은 하나다.

인덱스가 참조한 컬럼이 실제 생성된 테이블에 존재하지 않는다.

여기서 주의할 점은 "엔티티에 필드가 없다"라고 단정할 수는 없다는 것이다. 자바 필드가 존재하더라도 실제 테이블 컬럼이 생성되지 않았을 수 있기 때문이다. 문제의 핵심은 엔티티 필드 존재 여부가 아니라, 실제 테이블 컬럼 존재 여부다.

## 왜 이런 일이 생기나

가장 흔한 원인은 인덱스 정의와 실제 컬럼 매핑이 어긋난 경우다.

예를 들어 인덱스 정의는 아래처럼 되어 있다고 가정해보자.

```java
@Table(
    indexes = {
        @Index(
            name = "idx_sample_token_m1",
            columnList = "client_id, expired_at, scheduled_at, is_active"
        )
    }
)
```

그런데 실제 컬럼 매핑이나 생성 결과가 다음과 같이 다르면 문제가 생긴다.

- 인덱스 정의에는 `scheduled_at`를 적어 둠
- 실제 테이블에는 `schedule_at`로 생성됨

그러면 DB 입장에서는 `scheduled_at`라는 컬럼을 찾을 수 없으므로 `create index`를 실행할 수 없다.

## `@Table(indexes = ...)`에서 중요한 점

JPA에서는 `@Table(indexes = ...)`로 테이블 인덱스를 선언할 수 있다. 이때 `@Index`의 `columnList`는 자바 필드명이 아니라 DB 컬럼명 기준으로 작성해야 한다.

즉 다음처럼 이해해야 한다.

- `scheduledAt`: 자바 필드명
- `scheduled_at`: DB 컬럼명

`columnList`에는 `scheduledAt`가 아니라 `scheduled_at`가 들어가야 한다. 이 부분이 어긋나면 Hibernate는 인덱스 생성 SQL을 만들더라도 DB에서 거절당하게 된다.

## 이 에러를 읽는 올바른 관점

이번 예외는 다음처럼 정리할 수 있다.

Hibernate가 엔티티 메타데이터를 바탕으로 스키마를 생성하던 중, 실제 테이블에 존재하지 않는 컬럼을 포함한 인덱스를 만들려고 해서 실패했다.

즉 이 에러의 성격은 다음과 같다.

- DDL 문제
- 스키마 생성 문제
- 인덱스 정의와 실제 컬럼 불일치 문제

여기서 DDL은 데이터베이스 구조를 정의하는 SQL을 뜻한다. 대표적으로 아래 명령들이 DDL이다.

- `create table`
- `create index`
- `alter table`

이번 에러는 그중에서도 `create index` 단계에서 발생했다.

## `CommandAcceptanceException`은 무슨 의미인가

`CommandAcceptanceException`은 Hibernate가 DB에 전달한 명령을 DB가 받아들이지 않았다는 뜻이다. 여기서는 Hibernate가 생성한 DDL을 실행했는데, H2가 그 SQL을 거절한 상황이다.

이번 경우 DB가 거절한 이유는 명확하다.

- 인덱스 생성 SQL 안에 있는 컬럼명이
- 실제 테이블 컬럼과 맞지 않았다

즉 예외의 본질은 Hibernate 내부 동작 자체보다는, 생성된 SQL과 실제 스키마의 불일치에 있다.

## H2의 역할

H2는 여기서 테스트용 데이터베이스 역할을 한다. Hibernate가 만든 `create table`, `create index` 같은 SQL을 실제로 실행하는 대상이다.

역할을 나누면 다음과 같다.

- JPA: 자바 객체와 DB를 연결하는 표준
- Hibernate: JPA 구현체, 실제 SQL 생성 담당
- H2: 테스트 DB, 생성된 SQL 실행 담당

즉 Hibernate가 SQL을 만들고, H2가 그 SQL을 실행하다가 문제를 발견한 것이다.

## 먼저 확인할 것

이런 로그를 보면 아래 세 가지를 먼저 확인하는 것이 좋다.

### 1. 엔티티의 `@Table(indexes = ...)`

`columnList`에 적은 이름이 실제 DB 컬럼명과 일치하는지 확인한다.

### 2. 각 필드의 `@Column(name = "...")`

필드가 실제 어떤 컬럼명으로 생성되는지 확인한다. 명시적으로 이름을 지정했다면 인덱스 정의와 정확히 같은 문자열이어야 한다.

### 3. 생성된 `create table ...` 로그

이 부분이 가장 중요하다. `create index` 로그만 보면 어떤 컬럼명이 없다고 말하는지는 알 수 있지만, 왜 없어진 것인지는 `create table`을 봐야 알 수 있다.

정리하면 다음과 같다.

- `create index`: 증상
- `create table`: 원인 확인 자료

## `@Transient`가 중요한 이유

`@Transient`는 해당 필드를 DB 컬럼으로 저장하지 않겠다는 의미다.

예를 들어 엔티티에 이런 필드가 있다고 하자.

```java
private LocalDateTime scheduledAt;
```

여기에 `@Transient`가 붙으면 자바 객체에는 필드가 존재하더라도 DB 테이블에는 컬럼이 생성되지 않는다.

그런데 인덱스 정의에는 여전히 `scheduled_at`를 적어 두면 다음 상황이 발생할 수 있다.

- 자바 객체에는 필드가 있다
- DB 테이블에는 컬럼이 없다
- 인덱스를 만들 때 해당 컬럼을 찾을 수 없다
- 결국 스키마 생성이 실패한다

즉 "필드는 있는데 컬럼은 없는" 상태가 가능하다.

## `@DynamicUpdate`와의 관계

`@DynamicUpdate`는 Hibernate 전용 기능으로, `UPDATE` SQL을 만들 때 실제로 변경된 컬럼만 포함하도록 해 준다.

예를 들어 기본 방식은 다음처럼 전체 컬럼을 포함한 `UPDATE`를 만들 수 있다.

```sql
update customer
set name = ?, email = ?, phone = ?
where id = ?
```

반면 `@DynamicUpdate`를 사용하면 변경된 컬럼만 포함해서 아래처럼 생성될 수 있다.

```sql
update customer
set name = ?
where id = ?
```

하지만 이 기능은 이번 에러와 직접적인 관련이 없다.

- 이번 에러: 스키마 생성 단계의 DDL 문제
- `@DynamicUpdate`: 데이터 수정 단계의 DML 문제

즉 둘은 다루는 영역이 다르다.

## 정리

이번 에러에서 기억할 핵심은 다음과 같다.

- 애플리케이션 로직 에러가 아니라 스키마 생성 에러다.
- Hibernate가 인덱스를 생성하려다가 실패한 것이다.
- 직접 원인은 인덱스가 참조한 컬럼이 실제 테이블에 없기 때문이다.
- `@Table(indexes = ...)`의 `columnList`는 자바 필드명이 아니라 DB 컬럼명 기준이다.
- 문제를 분석할 때는 `create index`뿐 아니라 `create table` 로그도 함께 봐야 한다.
- `@DynamicUpdate`는 이번 문제와 별개로 `UPDATE` SQL 생성 방식에 관한 기능이다.

## 한 줄 요약

Hibernate가 테스트용 H2 DB에 스키마를 생성하던 중, 실제 테이블에 존재하지 않는 컬럼을 포함한 인덱스를 만들려고 해서 실패한 에러다.
