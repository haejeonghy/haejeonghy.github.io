---
layout  : post
title   : mustache 이용한 html 템플릿
summary : 'ex) JSP 의 경우는 안에 있는 JAVA 문법은 서버단에서, Javascirpt 는 클라이언트단에서 동작하기 때문에 하나의 JSP 파일 안에서'
date    : 2021-12-27 23:32:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : html
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# mustache 이용한 html 템플릿
Created: 2021년 12월 27일 오후 11:32
Tags: HTML
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

**1) 개요**

- Mustache 는 Springboot 에서 공식으로 지원하는 템플릿 엔진이다. 매우 심플한 문법으로 배워서 그 즉시 적용할 수 있을 정도로 심플하다.

- Mustache 는 JAVA 뿐만 아니라 현존하는 대부분의 언어를 지원하고 있다. 예를들어 JAVA 에서 사용될 때는 서버 템플릿 엔진으로, Javascript 에서 사용될 때는 클라이언트 템플릿 엔진으로 사용할 수 있는 장점이 있다.

- 로직 코드가 없어서(Logic-less templates) 뷰(View)의 역할에 충실하여, 서버와 역할을 분리할 수 있다.

ex) JSP 의 경우는 <% %> 안에 있는 JAVA 문법은 서버단에서, Javascirpt 는 클라이언트단에서 동작하기 때문에 하나의 JSP 파일 안에서

서버와 클라이언트 코드가 뒤섞이는 등의 문제가 있어 유지보수를 하기에 어려움이 있다.

---

등록 뷰를 만들었는데 뭔지 모르겠지만 서버에서 mustache 파일을 못 찾아오고 있음

이거 원인 파악해야됨

인덱스는 읽어오면서? 생리통 오진다... 개졸림
