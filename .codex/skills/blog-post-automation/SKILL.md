---
name: blog-post-automation
description: Transform pasted markdown into a blog post that matches this repository's existing style, then create the post file under _posts and, by default, run data generation, git commit, and git push.
---

# Blog Post Automation

이 스킬은 이 저장소에서 새 블로그 글을 만들 때 사용한다. 입력은 사용자가 붙여넣은 초안 마크다운이다.

## 언제 사용할지

- 사용자가 초안 마크다운을 이 블로그 스타일에 맞춰 포스팅으로 바꾸고 싶을 때
- 사용자가 새 포스트 파일 생성까지 원할 때
- 사용자가 커밋과 푸시까지 한 번에 처리하길 원할 때

## 먼저 확인할 것

1. 이 저장소의 규칙은 [references/blog-style.md](references/blog-style.md)를 따른다.
2. 최근 포스트 3~5개를 직접 읽고 말투, 헤더 구조, 강조 방식, 코드 블록 유지 방식을 확인한다.
3. 임의 스타일을 만들지 말고 기존 스타일에 맞춘다.

추천 확인 명령:

```bash
find _posts -type f -name '*.md' | sort | tail -n 5
```

## 작업 절차

1. 최근 포스트를 읽고 스타일을 요약한다.
2. 입력 마크다운을 같은 톤과 구조로 다시 정리한다.
3. 프론트매터를 이 저장소 규칙에 맞게 작성한다.
4. 파일 경로를 `_posts/YYYY/YYYY-MM-DD-slug.md` 형식으로 정한다.
5. 아래 출력 형식으로 결과를 만든다.
6. 기본 실행은 파일 생성, 데이터 갱신, git commit, git push까지 한 번에 진행한다.
7. 자동 푸시를 원하지 않을 때만 `--no-push`를 사용한다.

## 변환 규칙

- 본문 의미는 유지하고 표현과 구조만 다듬는다.
- 코드 블록 내용과 backtick 개수는 바꾸지 않는다.
- 클릭 유도형 제목은 피하고 기술 블로그 톤을 유지한다.
- 태그는 `tags` 배열이 아니라 `tag` 문자열로 쓴다.
- `categories`는 사용하지 않는다.
- `summary`, `date`, `updated`, `public`을 포함한다.
- `toc: true`, `comment: false`는 최근 글 패턴에 맞을 때 우선 사용한다.
- 날짜와 시간은 `Asia/Seoul` 기준 현재 시각을 사용한다.
- 커밋 메시지는 반드시 한국어로 작성한다.
- 기본 워크플로우는 커밋과 푸시까지 자동으로 진행한다.

## 출력 형식

반드시 아래 3개 섹션을 순서대로 출력한다.

```text
===FILEPATH===
_posts/YYYY/YYYY-MM-DD-slug.md

===FILE===
---
layout: post
title: ...
summary: ...
date: YYYY-MM-DD HH:MM:SS +0900
updated: YYYY-MM-DD HH:MM:SS +0900
tag: tag1 tag2 tag3
toc: true
comment: false
public: true
---

(본문)

===COMMIT===
블로그 글 추가: {제목}
```

## 실행 절차

기본 실행은 붙여넣은 내용을 한 번에 포스팅, 커밋, 푸시까지 진행한다:

```bash
./post.sh <<'EOF'
(붙여넣을 초안 마크다운)
EOF
```

자동 푸시만 막고 커밋까지만 할 때:

```bash
./post.sh --no-push <<'EOF'
(붙여넣을 초안 마크다운)
EOF
```

저수준 스크립트를 직접 쓸 때도 보통은 커밋 메시지 파일을 함께 넘겨 커밋까지 진행한다:

```bash
.codex/skills/blog-post-automation/scripts/create_post.sh \
  --filepath "_posts/2026/2026-04-01-example.md" \
  --content-file /tmp/post.md \
  --commit-message-file /tmp/commit.txt
```

직접 스크립트에서 자동 푸시까지 진행할 때:

```bash
.codex/skills/blog-post-automation/scripts/create_post.sh \
  --filepath "_posts/2026/2026-04-01-example.md" \
  --content-file /tmp/post.md \
  --commit-message-file /tmp/commit.txt \
  --push
```

## 실행 시 주의

- 새 포스트나 태그가 생기면 반드시 `node generateData.js`를 실행한다.
- 스크립트는 위 작업을 포함한다.
- 기본값은 커밋과 푸시까지 자동 진행이다.
- 푸시를 막아야 할 때만 `./post.sh --no-push`를 사용한다.
