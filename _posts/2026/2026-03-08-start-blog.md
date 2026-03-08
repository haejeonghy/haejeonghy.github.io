---
layout  : post
title   : 블로그 시작 글
summary : 블로그 초기 세팅과 스켈레톤 정리, 홈/아이콘 개선 작업을 진행했습니다.
date    : 2026-03-08 09:00:00 +0900
updated : 2026-03-08 16:10:00 +0900
tag     : blog start github-pages jekyll
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

이 글은 블로그 동작 확인을 위한 첫 글이며, 오늘 작업 내역을 함께 기록합니다.

## 무엇을 했나

- Jekyll 기반 사이트 설정 확인
- 데이터 생성 스크립트 실행
- 로컬 서버 실행 준비

## 오늘 업데이트한 내용

- 스켈레톤에서 넘어온 불필요 포스트(`_posts/2017/*`) 삭제
- 스켈레톤 위키 문서 정리 및 `root-index` 단순화
- `/wiki/how-to/` 에러 원인 수정
  - 샘플 값(`SAMPLE-VALUE`)일 때 댓글/분석/광고 스크립트가 로드되지 않도록 조건 강화
- 홈 화면을 위키 목록 중심에서 블로그 글 목록 중심으로 변경
- 파비콘/앱 아이콘 세트를 새 이미지로 전면 교체
- Codex 시작 지침 문서(`AGENTS.md`) 추가 및 간소화

## 다음 단계

- 새 글을 `_posts/YYYY/YYYY-MM-DD-slug.md` 형식으로 추가
- 변경 사항 커밋 후 `master` 브랜치에 push
- `https://haejeonghy.github.io`에서 반영 확인
