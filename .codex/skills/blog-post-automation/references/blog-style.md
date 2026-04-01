# Blog Style Reference

이 저장소의 블로그 포스트는 아래 규칙을 우선한다.

## 파일 경로

- 위치: `_posts/YYYY/YYYY-MM-DD-slug.md`
- 연도별 디렉터리를 사용한다.

## 프론트매터

기본 키:

```yaml
layout: post
title: ...
summary: ...
date: 2026-04-01 09:10:00 +0900
updated: 2026-04-01 09:10:00 +0900
tag: spring http client
toc: true
comment: false
public: true
```

중요:

- `tags`가 아니라 `tag`를 사용한다.
- `tag`는 배열이 아니라 공백 구분 문자열이다.
- `categories`는 쓰지 않는다.

## 본문 스타일

- 설명형 기술 블로그 톤을 유지한다.
- 보통 `## 1.`, `## 2.` 형태의 섹션 구조를 사용한다.
- 서두에서 왜 헷갈리는지, 무엇을 비교하는지 짧게 잡아준다.
- 표, bullet, 코드 블록을 섞어서 이해를 돕는다.
- 코드 식별자와 핵심 용어는 백틱으로 강조한다.
- 과장된 마케팅 표현은 피한다.

## 최근 포스트에서 보이는 패턴

- 제목은 주제를 직접 드러낸다.
- `summary`는 한 문장으로 글의 핵심을 요약한다.
- 문체는 설명형 평서문 중심이다.
- 비유를 쓰더라도 기술 개념 설명이 중심이다.

## 데이터 동기화

포스트 생성 또는 태그 변경 후 반드시 아래를 실행한다.

```bash
node generateData.js
```

이 스크립트는 다음 경로를 갱신한다.

- `data/tag_count.json`
- `data/total-document-url-list.json`
- `data/tag/*`
- `data/metadata/*`
