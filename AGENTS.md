# AGENTS.md

## 1) 콘텐츠 규칙

- 블로그 글 위치: `_posts/YYYY/YYYY-MM-DD-slug.md`
- 프론트매터 기본 키: `layout: post`, `title`, `summary`, `date`, `updated`, `tag`, `public`
- 태그는 `tags`가 아니라 `tag`(문자열) 사용.

## 2) 데이터 동기화

- 문서/태그 변경 후 반드시 `node generateData.js` 실행.
- 이 스크립트는 `data/tag_count.json`, `data/total-document-url-list.json`, `data/tag/*`, `data/metadata/*`를 갱신함.

## 3) 커밋 메시지 규칙

- 사용자가 커밋을 요청한 경우, 커밋 메시지는 반드시 한글로 작성.

## 4) 금지사항

- 사용자 요청 없이 파괴적 명령(`git reset --hard` 등) 실행 금지.
