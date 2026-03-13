---
layout  : post
title   : MySQL Collation 때문에 발생한 Duplicate Entry 이슈
summary : 값이 같아 보이는데도 unique key 중복이 발생한 원인과 collation 동작 차이를 정리합니다.
date    : 2026-03-14 10:00:00 +0900
updated : 2026-03-14 10:00:00 +0900
tag     : mysql collation mydata
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

## 배경

마이데이터 sync 시 기관에서 받아온 `string` 필드와 `varchar` 컬럼에 적재된 필드가 분명히 같은 값처럼 보였는데, DB에서는 동일하다고 판단하여 insert 시 unique key에 걸리고 `duplicate entry` 응답이 발생했습니다.

## 원인

핵심 원인은 MySQL의 **collation(정렬/비교 규칙)** 입니다.

```sql
SELECT 'a' = 'a ' COLLATE utf8mb4_unicode_ci;   -- PAD SPACE 콜레이션 예시
SELECT 'a' = 'a ' COLLATE utf8mb4_0900_ai_ci;   -- NO PAD 콜레이션 예시
```

- 테이블과 컬럼의 `collation`이 다르면, 비교 시에는 **컬럼의 collation이 우선 적용**됩니다.
- 따라서 애플리케이션에서 보기에는 값이 달라도(예: trailing space 포함 여부), 특정 collation에서는 동일 값으로 평가될 수 있습니다.

## Collation이 중요한 이유

Collation은 문자 데이터의 비교 및 정렬 방식을 규정하는 규칙 집합입니다. 즉, 아래 동작에 직접 영향을 줍니다.

- 검색 결과 정렬 순서
- 문자열 동등 비교(=`=`) 및 조건 필터링
- unique key 중복 판단

또한 collation은 문자 집합(character set)과 밀접하게 연결됩니다. 선택한 문자 집합과 호환되는 collation을 사용하지 않으면 정렬/비교 결과가 기대와 달라질 수 있고, 데이터베이스 동작이나 애플리케이션 기능에 문제를 유발할 수 있습니다.
