---
layout  : post
title   : Kotlinx - 14. Anko 확장 활용
summary : 'Last Edited Time: 2022년 10월 26일 오후 10:34 Type: Kotlin, android Created By: HAE JEONG YU'
date    : 2021-01-14 16:32:00 +0900
updated : 2021-01-14 16:32:00 +0900
tag     : notion import
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Kotlinx - 14. Anko 확장 활용
Created: 2021년 1월 14일 오후 4:32
Last Edited Time: 2022년 10월 26일 오후 10:34
Type: Kotlin, android
Created By: HAE JEONG YU

<aside>
💡 제목 : Anko SQLite, Anko Coroutines 사용하여 기존 방법보다 더 쉽게 접근하기

</aside>

---

### 키워드

- Anko

### 필기

### Anko 라이브러리

- DSL 제공 : xml 레이아웃 구성하지 않아도 코드상에서 더 빠르게 표현 가능함
- Anko Commons : Dialog와 Toast 등의 공통 유틸리티 클래스 제공
    - Toast 메시지를 띄우거나 다이얼로그를 간단하게 작성할 수 있도록 도움을 줌
- Anko Coroutines : Kotlinx.corutines 라이브러리를 기반으로 코루틴을 좀 더 편리하게 사용할 수 있도록 함
- Anko SQLite : 안드로이드의 데이터베이스인 SQLite에 쿼리나 DSL, 파서 등의 기능을 제공함
- Anko Layouts : 레이아웃에 사용되는 xml 코드를 코틀린 메인 코드에서 작성할 수 있게 해줌 - 뷰가 복잡해질수록 Anko Layout 사용 시 성능 향상
- 샘플 안드로이드 프로젝트에 추가

---

<aside>
💡 요약 : 거지같은 anko 새끼들... 근데 이거 안 쓸거같음 ui랑 비즈니스 로직이랑 분리가 안됨

</aside>
