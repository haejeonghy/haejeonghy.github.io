---
layout: post
title: Spring Data, JPA, Hibernate, JDBC의 관계를 한 번에 정리하기
summary: Repository, CrudRepository, PagingAndSortingRepository, JpaRepository부터 JPA, Hibernate, ORM, JDBC, JDK 인터페이스까지 서로 어떤 층위에서 연결되는지 체계적으로 정리합니다.
date: 2026-06-03 22:05:00 +0900
updated: 2026-06-03 22:05:00 +0900
tag: spring data jpa hibernate jdbc orm repository
toc: true
comment: false
public: true
---
- TOC
  {:toc}

## 1. 왜 이 개념들이 자꾸 한 덩어리처럼 들릴까

Spring으로 데이터 접근을 공부하다 보면 아래 용어가 거의 항상 같이 나온다.

- `Repository`
- `CrudRepository`
- `PagingAndSortingRepository`
- `JpaRepository`
- `Spring Data JPA`
- `JPA`
- `Hibernate`
- `ORM`
- `JDBC`
- `JDK 인터페이스`

문제는 이 용어들이 모두 같은 층위의 개념이 아니라는 점이다.

어떤 것은 자바 언어 차원의 추상화이고, 어떤 것은 표준 API이며, 어떤 것은 ORM 명세이고, 어떤 것은 구현체이고, 어떤 것은 Spring이 제공하는 상위 추상화다.

그래서 이들을 정확히 이해하려면 "누가 누구 위에서 동작하는가"를 먼저 잡아야 한다.

가장 단순화하면 아래 구조로 보면 된다.

```text
애플리케이션 코드
  -> Spring Data Repository
  -> JPA
  -> Hibernate
  -> JDBC
  -> DB
```

그리고 이 구조를 이루는 각 API 상당수는 자바의 인터페이스 개념 위에 서 있다.

## 2. 가장 먼저 `ORM`과 `JPA`, `Hibernate`를 구분해야 한다

이 셋이 가장 자주 섞여서 말해진다.

### 2.1 `ORM`은 제품명이 아니라 개념이다

`ORM(Object-Relational Mapping)`은 객체와 관계형 데이터베이스 테이블을 매핑하는 방식 또는 기술 범주를 뜻한다.

즉, 아래 같은 문제를 객체 중심으로 풀게 해 주는 접근이다.

- 테이블의 row를 객체로 다루기
- 외래 키 관계를 객체 참조로 다루기
- SQL 결과를 수동으로 매핑하지 않기

따라서 `ORM` 자체는 "무엇을 구현할 것인가"에 가까운 개념이다.

### 2.2 `JPA`는 자바 ORM 표준 명세다

`JPA(Java Persistence API)`는 자바 진영에서 ORM을 어떻게 다룰지 정한 표준이다.

예를 들면 아래 같은 개념이 JPA에 속한다.

- `@Entity`
- `@Id`
- `EntityManager`
- 영속성 컨텍스트
- JPQL

중요한 점은 `JPA`가 직접 동작하는 프로그램이 아니라는 점이다.

`JPA`는 표준이므로 실제 실행을 위해서는 구현체가 필요하다.

### 2.3 `JPQL`은 JPA가 사용하는 객체 중심 질의 언어다

`JPQL(Java Persistence Query Language)`은 JPA에서 사용하는 질의 언어다.

겉보기에는 SQL과 비슷하지만, 중요한 차이는 **테이블과 컬럼이 아니라 엔티티와 엔티티 필드 기준으로 쿼리를 쓴다**는 점이다.

예를 들어 SQL은 보통 이렇게 쓴다.

```sql
select *
from users
where name = 'kim'
```

반면 JPQL은 이런 식이다.

```java
select u
from User u
where u.name = :name
```

여기서 `User`는 테이블명이 아니라 엔티티 클래스이고, `name`도 컬럼명이 아니라 엔티티 필드다.

즉, JPQL은 "DB 스키마 중심"이라기보다 "객체 모델 중심" 질의 언어다.

JPA 구현체인 Hibernate는 이 JPQL을 해석해서 실제 DB에 맞는 SQL로 변환한다.

그래서 관계를 쓰면 아래와 같다.

```text
JPQL 작성
  -> JPA가 질의 모델로 해석
  -> Hibernate가 SQL 생성
  -> JDBC 실행
```

실무에서는 JPQL이 주로 아래 지점에서 등장한다.

- `EntityManager.createQuery(...)`
- `@Query` 어노테이션
- named query

즉, `@Query`를 쓸 때 기본적으로는 SQL이 아니라 JPQL을 쓰는 경우가 많다.

### 2.4 `Hibernate`는 JPA의 대표 구현체다

`Hibernate`는 ORM 프레임워크이며, 오늘날에는 보통 JPA 구현체로 이해하는 것이 가장 실용적이다.

즉, 애플리케이션이 JPA API를 통해 요청하면 실제로는 Hibernate가 아래 일을 수행한다.

- 엔티티 매핑 해석
- SQL 생성
- 변경 감지
- 지연 로딩 처리
- 1차 캐시 관리

정리하면 다음과 같다.

- `ORM`
  객체-관계 매핑이라는 기술 개념
- `JPA`
  자바 ORM 표준 명세
- `JPQL`
  JPA가 제공하는 객체 중심 질의 언어
- `Hibernate`
  JPA를 구현하는 대표 프레임워크

## 3. `JDBC`는 어디에 위치하는가

`JDBC`는 자바에서 데이터베이스와 직접 통신하기 위한 저수준 표준 API다.

대표적으로 아래 타입이 여기에 속한다.

- `Connection`
- `PreparedStatement`
- `ResultSet`

JDBC를 직접 쓰면 개발자가 아래 작업을 더 많이 책임져야 한다.

- SQL 작성
- 파라미터 바인딩
- 실행
- `ResultSet` 순회
- 객체 매핑
- 자원 반납

예를 들면 이런 식이다.

```java
Connection connection = dataSource.getConnection();
PreparedStatement ps = connection.prepareStatement(
    "select id, name from users where id = ?"
);
ps.setLong(1, 1L);
ResultSet rs = ps.executeQuery();
```

반면 Hibernate는 이 JDBC 위에서 동작한다.

즉, 아래처럼 이해하면 된다.

```text
객체 조작
  -> Hibernate가 SQL 생성
  -> JDBC로 SQL 실행
  -> 결과를 다시 객체로 매핑
```

따라서 `JDBC`는 ORM의 경쟁 상대라기보다, ORM이 최종적으로 내려가서 사용하는 실행 수단이다.

## 4. `JDK 인터페이스`는 왜 같이 언급되는가

`JDK 인터페이스`는 앞의 기술들과 범주가 다르다.

이것은 자바 언어와 표준 라이브러리 차원의 추상화 방식이다.

예를 들면 아래가 모두 인터페이스다.

- `List`
- `Map`
- `AutoCloseable`
- `Connection`
- `PreparedStatement`
- `ResultSet`

즉, JDBC API도 사실 많은 부분이 인터페이스로 정의되어 있다.

예를 들어 `Connection`은 인터페이스이고, 실제 구현은 데이터베이스 드라이버가 제공한다.

이 관점은 Spring Data Repository를 이해할 때도 중요하다.

왜냐하면 Spring Data 역시 개발자가 인터페이스만 선언하면, 런타임에 그 구현체를 만들어 쓰는 구조이기 때문이다.

## 5. `Repository`는 먼저 패턴이고, 그 다음에 Spring 인터페이스다

여기서부터 Spring Data 계층으로 올라온다.

### 5.1 `Repository`는 저장소 패턴 개념이다

원래 `Repository`는 DDD에서 나온 저장소 패턴 개념이다.

핵심 아이디어는 아래와 같다.

- 도메인 객체를 저장하고 조회하는 기능을 한곳에 모은다
- 호출하는 쪽은 저장 방식의 세부사항을 몰라도 된다

예를 들면 이런 인터페이스가 있을 수 있다.

```java
public interface UserRepository {
    User save(User user);
    Optional<User> findById(Long id);
}
```

이 시점의 `Repository`는 아직 Spring Data 전용 타입이 아니라, 저장소 역할 자체를 가리키는 개념에 가깝다.

### 5.2 Spring Data의 `Repository`는 인터페이스 기반 진입점이다

Spring Data는 이 저장소 패턴을 프레임워크 차원에서 일반화했다.

개발자는 구현 클래스를 직접 만들지 않고, 인터페이스를 선언하는 쪽에 집중한다.

즉, 아래 구조가 만들어진다.

- 개발자는 repository 인터페이스만 작성
- Spring Data가 런타임에 구현체 생성
- 구현체는 JPA를 통해 데이터 접근 수행

## 6. `CrudRepository`, `PagingAndSortingRepository`, `JpaRepository`는 어떻게 이어지는가

이 셋은 Spring Data가 제공하는 구체 인터페이스다.

개념 관계를 먼저 보면 아래처럼 이해하면 된다.

```text
Repository
  -> CrudRepository
  -> PagingAndSortingRepository
  -> JpaRepository
```

즉, 점점 더 많은 기능을 추가한 확장 구조다.

여기서 `Repository` 자체도 같이 봐야 그림이 더 정확해진다.

- `Repository`
  가장 일반적인 저장소 추상화이자 최상위 마커 인터페이스
- `CrudRepository`
  저장, 조회, 삭제 같은 기본 CRUD 기능 추가
- `PagingAndSortingRepository`
  목록 조회에 필요한 정렬과 페이징 기능 추가
- `JpaRepository`
  JPA 친화 기능을 더한 실무 중심 인터페이스

즉, 앞에서 말한 "저장소 패턴으로서의 repository"가 Spring Data 안에서는 계층적 인터페이스 체계로 구체화된다고 보면 된다.

### 6.1 `CrudRepository`

`CrudRepository<T, ID>`는 기본 CRUD 기능을 제공한다.

대표 메서드는 아래와 같다.

- `save`
- `findById`
- `findAll`
- `deleteById`
- `existsById`

즉, 가장 기본적인 저장/조회/삭제를 공통화한 인터페이스다.

중요한 점은 이 인터페이스가 단지 메서드 시그니처 모음이 아니라는 점이다.

Spring Data는 이 시그니처를 보고 런타임에 실제 동작을 연결한다. 따라서 개발자는 구현 클래스를 만들지 않아도 `save`, `findById` 같은 동작을 바로 사용할 수 있다.

### 6.2 `PagingAndSortingRepository`

`PagingAndSortingRepository<T, ID>`는 `CrudRepository` 기능에 페이징과 정렬을 더한다.

대표 메서드는 아래와 같다.

- `findAll(Sort sort)`
- `findAll(Pageable pageable)`

즉, 목록 조회가 중요해지는 순간 더 자주 의미를 가지는 계층이다.

예를 들어 "회원 목록을 이름순으로 가져온다"거나 "주문 내역을 20개씩 페이지로 끊어 본다" 같은 요구가 생기면 이 계층의 의미가 커진다.

### 6.3 `JpaRepository`

`JpaRepository<T, ID>`는 `PagingAndSortingRepository`를 확장하면서 JPA 친화적인 기능을 더 제공한다.

실무에서는 대개 이것을 가장 많이 직접 상속한다.

예를 들면 아래처럼 사용한다.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByName(String name);
}
```

Spring Data는 이 인터페이스를 보고 구현체를 자동으로 생성한다.

즉, 개발자는 "어떤 엔티티를 어떤 키로 다룰지"와 "어떤 조회 메서드가 필요한지"에 집중하고, 실제 구현은 프레임워크가 맡는다.

`JpaRepository`가 자주 선택되는 이유는 아래 같은 JPA 친화 기능도 함께 주기 때문이다.

- flush 관련 메서드
- batch 성격의 저장 메서드
- 예시(Example) 기반 조회 확장점

즉, 실무에서는 `CrudRepository`와 `PagingAndSortingRepository`를 개념적으로 이해하되, 실제 선언은 `JpaRepository`를 바로 상속하는 경우가 많다.

## 7. 여기서 `Spring Data JPA`는 정확히 무엇인가

`Spring Data JPA`는 JPA를 더 편하게 쓰게 해 주는 Spring의 모듈이다.

중요한 점은 이것이 ORM 구현체가 아니라는 점이다.

`Spring Data JPA`의 역할은 주로 아래와 같다.

- repository 인터페이스 기반 개발 지원
- 메서드 이름 기반 쿼리 생성
- 페이징, 정렬, 공통 CRUD 추상화
- JPA 사용 보일러플레이트 감소

즉, `Spring Data JPA`는 JPA 위에 놓인 상위 추상화다.

따라서 정확한 관계는 이렇게 봐야 한다.

- `Spring Data JPA`
  JPA 사용을 편하게 해 주는 Spring 계층
- `JPA`
  자바 ORM 표준
- `Hibernate`
  JPA 구현체

## 8. Spring Data는 `findBy...` 같은 이름을 보고 어떻게 쿼리 의도를 아는가

Spring Data를 처음 보면 가장 신기한 부분이 여기다.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByName(String name);
}
```

개발자는 구현을 쓰지 않았는데도, Spring Data는 이 메서드를 보고 "이건 조회 쿼리"라고 해석한다.

이것은 단순 추측이 아니라 **메서드 이름 파싱 규칙**에 기반한다.

### 8.1 먼저 repository 인터페이스 메타데이터를 수집한다

애플리케이션 시작 시 Spring Data는 repository 인터페이스를 스캔한다.

그 과정에서 아래 정보를 모은다.

- 어떤 인터페이스가 repository인지
- 도메인 타입이 무엇인지
- ID 타입이 무엇인지
- 선언된 메서드 이름이 무엇인지
- 그 메서드가 기본 제공 메서드인지, 파생 쿼리 메서드인지

즉, `UserRepository extends JpaRepository<User, Long>`를 보면 Spring Data는 이 저장소가 `User` 엔티티를 대상으로 한다는 것을 먼저 안다.

### 8.2 메서드 이름의 접두어로 동작 종류를 해석한다

Spring Data는 메서드 이름에서 특정 패턴을 읽는다.

예를 들어 아래 접두어는 보통 조회 계열로 해석된다.

- `find...By`
- `read...By`
- `get...By`
- `query...By`
- `search...By`

반대로 아래 접두어는 존재 여부나 개수처럼 다른 의도를 나타낸다.

- `exists...By`
- `count...By`
- `delete...By`
- `remove...By`

즉, `findByName`이라는 이름을 보면 Spring Data는 먼저 `find`를 보고 "조회 계열 메서드"라고 판단한다.

### 8.3 `By` 뒤를 조건으로 해석한다

접두어 다음의 `By`는 조건절이 시작된다는 신호다.

예를 들어:

- `findByName`
  `name = ?`
- `findByNameAndAge`
  `name = ? and age = ?`
- `findByStatusOrType`
  `status = ? or type = ?`

즉, `By` 뒤에 오는 프로퍼티 이름을 엔티티 필드와 매칭해서 조건식을 만든다.

### 8.4 프로퍼티 경로와 키워드도 함께 해석한다

Spring Data는 단순 필드명만 보는 것이 아니라 비교 방식도 읽는다.

예를 들면:

- `findByNameContaining`
- `findByAgeGreaterThan`
- `findByCreatedAtBetween`
- `findByOrderByIdDesc`

이런 이름에서 `Containing`, `GreaterThan`, `Between`, `OrderBy` 같은 예약 키워드를 파싱해 JPQL 또는 Criteria 기반 질의를 구성한다.

즉, 메서드 이름은 그냥 사람이 읽기 좋은 이름이 아니라, Spring Data 입장에서는 일종의 작은 DSL처럼 취급된다.

### 8.5 그 다음에 JPA 질의로 바꾸고, 구현체가 실행한다

Spring Data는 이렇게 해석한 메서드 정보를 바탕으로 내부 질의 모델을 만든다.

그리고 실제 실행 시에는 JPA 계층으로 내려보낸다.

흐름을 단순화하면 아래와 같다.

```text
findByName(...)
  -> Spring Data가 이름 파싱
  -> 조회 쿼리라는 점과 조건 필드 식별
  -> JPA 질의 생성
  -> Hibernate가 실제 SQL 생성
  -> JDBC 실행
```

즉, `find`라는 단어 자체에 마법이 있는 것이 아니라, Spring Data가 미리 정의한 메서드명 규칙을 런타임에 해석하는 것이다.

### 8.6 모든 메서드를 이름만으로 처리하는 것은 아니다

물론 Spring Data가 모든 질의를 메서드명만으로 해결하는 것은 아니다.

복잡한 경우에는 아래 방식도 쓴다.

- `@Query`로 JPQL 또는 native query 직접 작성
- `Specification`
- Querydsl
- 커스텀 repository 구현

즉, 메서드명 기반 질의 생성은 Spring Data의 강력한 기본값이지만, 복잡한 조건을 모두 그 방식으로 풀어야 한다는 뜻은 아니다.

### 8.7 `@Query`를 직접 쓰는 편이 더 좋은 경우도 많다

메서드명 기반 쿼리는 간단한 조회에는 매우 편하지만, 항상 최선은 아니다.

특히 아래 같은 경우에는 `@Query`가 더 명확하거나 안전할 수 있다.

#### 첫째, 메서드 이름이 지나치게 길어질 때

예를 들어 아래 같은 이름은 읽는 순간 피로해진다.

```java
findByStatusAndCreatedAtBetweenAndTypeOrderByPriorityDesc(...)
```

이런 경우는 동작은 가능해도 의도가 빠르게 읽히지 않는다.

차라리 `@Query`로 질의를 직접 드러내는 편이 유지보수성이 더 좋다.

```java
@Query("""
    select o
    from Order o
    where o.status = :status
      and o.createdAt between :from and :to
      and o.type = :type
    order by o.priority desc
""")
List<Order> findImportantOrders(
    @Param("status") OrderStatus status,
    @Param("from") LocalDateTime from,
    @Param("to") LocalDateTime to,
    @Param("type") OrderType type
);
```

즉, 메서드 이름으로 규칙을 맞추는 것보다 쿼리 자체를 드러내는 편이 읽기 쉬운 시점이 있다.

#### 둘째, 조인 의도를 명확히 보여주고 싶을 때

연관 엔티티를 조회할 때 조인 조건이 중요한 경우가 있다.

예를 들면:

- 특정 회원의 최근 주문 조회
- 특정 게시글과 작성자를 함께 조회
- `fetch join`으로 N+1 문제를 피하고 싶은 조회

이런 경우 메서드명만으로는 조인 전략이 드러나지 않는다.

반면 `@Query`를 쓰면 어떤 조인을 하는지 바로 보인다.

```java
@Query("""
    select p
    from Post p
    join fetch p.author
    where p.id = :id
""")
Optional<Post> findPostWithAuthor(@Param("id") Long id);
```

즉, 조회 결과뿐 아니라 **어떤 방식으로 가져올지**가 중요한 쿼리라면 `@Query`가 더 적합하다.

#### 셋째, JPQL로 비즈니스 의도를 더 선명하게 표현하고 싶을 때

메서드명 파생 방식은 규칙 기반이라 단순 조건 나열에는 좋지만, 질의의 의미를 풍부하게 설명하지는 못한다.

예를 들어:

- 활성 사용자만 조회
- 만료 예정 구독만 조회
- 재고 부족 상품만 조회

이런 경우는 메서드명을 길게 늘이기보다, 의미 있는 메서드명과 함께 `@Query`를 쓰는 편이 더 낫다.

```java
@Query("""
    select s
    from Subscription s
    where s.status = 'ACTIVE'
      and s.expireAt <= :deadline
""")
List<Subscription> findExpiringSubscriptions(@Param("deadline") LocalDateTime deadline);
```

즉, API 이름은 비즈니스 의미를 드러내고, 실제 조건은 `@Query`가 맡게 할 수 있다.

여기서 쓰는 `@Query`는 보통 JPQL 기준이라고 이해하면 된다.

즉, 아래 예시의 `Subscription`은 테이블명이 아니라 엔티티 이름이고, `expireAt`도 컬럼명이 아니라 엔티티 속성이다.

#### 넷째, 집계나 projection이 들어갈 때

단순 엔티티 조회가 아니라 아래처럼 집계가 들어가면 메서드명만으로는 한계가 빨리 온다.

- `count`
- `sum`
- `avg`
- DTO projection
- 그룹화

예를 들면:

```java
@Query("""
    select new com.example.sales.SalesSummary(p.id, p.name, sum(oi.quantity))
    from OrderItem oi
    join oi.product p
    group by p.id, p.name
""")
List<SalesSummary> findSalesSummaries();
```

이런 질의는 `@Query`가 훨씬 직접적이다.

#### 다섯째, 성능 최적화를 위해 쿼리를 더 정밀하게 통제하고 싶을 때

실무에서는 "결과가 맞느냐"만큼 "어떤 SQL이 나가느냐"도 중요하다.

메서드명 기반 쿼리는 빠르고 편리하지만, 복잡한 조회에서는 생성되는 질의를 세밀하게 통제하기 어렵다.

예를 들면:

- 꼭 필요한 컬럼만 조회하고 싶을 때
- 조인 순서나 fetch 전략이 중요할 때
- count query를 별도로 제어하고 싶을 때
- 페이지 조회 성능을 따로 조정하고 싶을 때

이런 경우 `@Query`는 의도를 더 직접적으로 고정하는 수단이 된다.

#### 여섯째, native query가 필요한 경우

JPA와 JPQL로는 표현이 번거롭거나 DB 고유 기능을 써야 하는 경우가 있다.

예를 들면:

- DB 전용 함수 사용
- 복잡한 윈도 함수 사용
- CTE 사용
- 성능상 native SQL이 더 적합한 경우

이때는 `@Query(nativeQuery = true)`가 필요할 수 있다.

즉, 이 단계는 "Spring Data 파생 쿼리"보다 더 아래 레벨로 내려가서 SQL을 직접 제어하는 경우다.

### 8.8 그렇다고 항상 `@Query`가 더 좋은 것은 아니다

반대로 아래 같은 경우는 메서드명 기반 파생 쿼리가 더 낫다.

- 조건이 단순할 때
- 메서드 이름이 짧고 명확할 때
- 표준 CRUD성 조회일 때
- 빠르게 작성하고 읽기 쉬운 것이 중요할 때

예를 들어 아래 정도는 파생 쿼리가 오히려 가장 자연스럽다.

```java
findByEmail(String email)
existsByNickname(String nickname)
findByStatus(OrderStatus status)
```

이런 쿼리까지 모두 `@Query`로 바꾸면 오히려 보일러플레이트가 늘어난다.

### 8.9 실무 기준으로 정리하면

실무에서는 보통 아래 기준이 가장 현실적이다.

- 단순 조회는 메서드명 파생 쿼리로 시작
- 이름이 길어지거나 조인, 집계, projection, fetch 전략이 중요해지면 `@Query` 고려
- 더 복잡한 동적 조건은 Querydsl이나 커스텀 repository로 이동

즉, `@Query`는 "Spring Data가 만들어 주는 쿼리를 못 믿어서 쓰는 것"이 아니라, **질의 의도와 실행 방식을 더 명시적으로 통제하고 싶을 때 쓰는 도구**라고 이해하는 편이 맞다.

참고로 `@Query`에는 두 층위가 있다.

- JPQL 기반 `@Query`
  엔티티와 필드 기준으로 작성
- native SQL 기반 `@Query`
  실제 테이블과 컬럼 기준으로 작성

기본값은 보통 JPQL이라고 보면 된다. 실제 SQL을 그대로 쓰려면 `nativeQuery = true`를 지정해야 한다.

## 9. 한 요청이 실제로 실행될 때 내부에서는 무슨 일이 일어나는가

아래 코드 한 줄을 예로 들어 보자.

```java
userRepository.findById(1L);
```

겉으로는 단순하지만 내부 흐름은 대략 아래와 같다.

1. 애플리케이션이 `UserRepository`를 호출한다.
2. 실제 구현체는 Spring Data JPA가 만든 프록시 또는 런타임 구현체다.
3. 이 구현체는 JPA의 `EntityManager`를 사용한다.
4. `EntityManager` 동작은 Hibernate가 구현한다.
5. Hibernate가 필요한 SQL을 만든다.
6. Hibernate가 JDBC를 통해 DB에 SQL을 보낸다.
7. 결과를 엔티티 객체로 다시 매핑해서 반환한다.

즉, 한 줄로 압축하면 아래와 같다.

```text
Repository 호출
  -> Spring Data JPA
  -> EntityManager(JPA)
  -> Hibernate
  -> JDBC
  -> DB
```

여기에 앞 절의 내용을 합치면 아래처럼 이해할 수 있다.

```text
findByName(...)
  -> Spring Data가 메서드명 규칙 해석
  -> JPA EntityManager 호출
  -> Hibernate가 SQL 생성
  -> JDBC 실행
  -> 결과를 엔티티로 반환
```

## 10. 각 용어를 같은 문장에 놓았을 때 어떻게 읽어야 하는가

이제 각 개념을 같은 좌표계 위에 놓고 보면 헷갈림이 많이 줄어든다.

| 용어 | 성격 | 역할 |
| --- | --- | --- |
| `JDK 인터페이스` | 자바 언어/표준 라이브러리 개념 | 계약을 인터페이스로 추상화 |
| `JDBC` | 저수준 표준 API | DB 연결과 SQL 실행 |
| `ORM` | 기술 개념 | 객체와 테이블 매핑 |
| `JPA` | 자바 ORM 표준 | ORM 사용 방식 정의 |
| `JPQL` | JPA 질의 언어 | 엔티티 기준 질의 작성 |
| `Hibernate` | 프레임워크, 구현체 | JPA 실제 동작 수행 |
| `Repository` | 패턴, 추상 개념 | 저장소 역할 추상화 |
| `CrudRepository` | Spring Data 인터페이스 | 기본 CRUD 제공 |
| `PagingAndSortingRepository` | Spring Data 인터페이스 | CRUD + 정렬/페이징 |
| `JpaRepository` | Spring Data 인터페이스 | JPA 친화 기능 추가 |
| `Spring Data JPA` | Spring 모듈 | repository 개발 단순화 |

핵심은 "이것들이 경쟁 관계"가 아니라 "층이 다른 협력 구조"라는 점이다.

## 11. 자주 하는 오해를 정리하면

### 11.1 `JPA`와 `Hibernate`는 같은가

아니다.

- `JPA`는 표준
- `Hibernate`는 구현체

### 11.2 `Spring Data JPA`가 곧 Hibernate인가

아니다.

`Spring Data JPA`는 JPA를 편하게 쓰게 해 주는 상위 계층이고, 실제 ORM 동작은 보통 Hibernate가 수행한다.

### 11.3 `Repository`와 `JpaRepository`는 같은 말인가

아니다.

- `Repository`는 저장소 패턴이라는 더 넓은 개념
- `JpaRepository`는 Spring Data JPA가 제공하는 구체 인터페이스

### 11.4 `findBy...`는 자바 문법이 이해하는 것인가

아니다.

이것은 자바 언어 기능이 아니라 Spring Data 프레임워크 규칙이다.

자바 컴파일러가 `findByName`을 보고 SQL 의미를 아는 것이 아니라, Spring Data가 런타임에 repository 메서드명을 파싱해서 질의 의도를 해석한다.

### 11.5 ORM을 쓰면 JDBC를 안 쓰는 것인가

아니다.

개발자가 JDBC를 직접 덜 다룰 뿐, ORM 구현체는 내부적으로 결국 JDBC를 사용해 DB와 통신한다.

### 11.6 `@Query`에 쓰는 것은 항상 SQL인가

아니다.

대부분의 `@Query` 예시는 기본적으로 JPQL이다.

- JPQL
  엔티티와 필드 기준
- native SQL
  실제 테이블과 컬럼 기준

즉, `@Query`를 쓴다고 해서 바로 SQL을 직접 쓰는 것은 아니다.

## 12. 실무에서는 어떻게 기억하면 좋은가

실무 관점에서는 아래 순서로 기억하는 것이 가장 편하다.

1. DB와 직접 대화하는 가장 아래 API는 `JDBC`다.
2. 객체와 테이블 매핑이라는 개념이 `ORM`이다.
3. 자바에서 ORM 표준으로 정한 것이 `JPA`다.
4. JPA의 객체 중심 질의 언어가 `JPQL`이다.
5. 그 JPA를 실제로 구현하는 대표 프레임워크가 `Hibernate`다.
6. Spring에서는 `Spring Data JPA`가 repository 인터페이스 기반 개발을 더 쉽게 만든다.
7. `CrudRepository`, `PagingAndSortingRepository`, `JpaRepository`는 그 위에서 제공되는 저장소 인터페이스들이다.

즉, 아래처럼 외우면 된다.

```text
Spring Data JPA Repository
  -> JPA
  -> Hibernate
  -> JDBC
  -> DB
```

그리고 이 전체 구조는 자바의 인터페이스 중심 설계 위에서 유연하게 결합된다.

여기에 repository 계층을 더 풀어 쓰면 아래처럼 기억해도 좋다.

```text
Repository
  -> CrudRepository
  -> PagingAndSortingRepository
  -> JpaRepository
  -> Spring Data JPA
  -> JPA
  -> Hibernate
  -> JDBC
  -> DB
```

그리고 `findByName`, `countByStatus`, `existsByEmail` 같은 메서드는 Spring Data가 이름 규칙을 해석해 질의 의도를 결정한다.

## 13. 마무리

이 주제를 이해할 때 가장 중요한 것은 용어를 평면적으로 외우지 않는 것이다.

`JPA`, `Hibernate`, `Spring Data`, `Repository`, `JDBC`는 서로 대체하는 말이 아니라 서로 다른 책임을 가진 계층이다.

이 관계를 정확히 잡아두면 아래 같은 표현도 자연스럽게 읽힌다.

- "Spring Data JPA에서 `JpaRepository`를 사용한다"
- "실제 ORM 구현체는 Hibernate다"
- "Hibernate는 결국 JDBC로 SQL을 실행한다"
- "JDBC API는 인터페이스 중심으로 정의되어 있다"

즉, Spring 애플리케이션의 데이터 접근 계층은 높은 수준의 repository 추상화에서 시작해, 가장 아래에서는 JDBC를 통해 실제 데이터베이스와 연결된다.
