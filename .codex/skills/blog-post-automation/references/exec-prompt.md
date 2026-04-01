Use the local skill `blog-post-automation` in this repository.

The user's pasted markdown will be provided in a `<stdin>` block. Transform it into a post that matches this repository's existing blog style.

Requirements:

- Read recent posts under `_posts` before writing.
- Follow this repository's actual rules, not generic blog conventions.
- Use `_posts/YYYY/YYYY-MM-DD-slug.md` as the filepath.
- Use frontmatter keys compatible with this repo: `layout`, `title`, `summary`, `date`, `updated`, `tag`, `toc`, `comment`, `public`.
- Do not use `tags` or `categories`.
- Preserve code blocks exactly.
- Write the commit message in Korean.
- Use this exact timestamp for both `date` and `updated`: `__CURRENT_TIMESTAMP__`
- This output will be consumed by an automation script that commits and pushes by default, so always provide a usable filepath and commit message.

Return only the following format with no extra commentary:

===FILEPATH===
_posts/YYYY/YYYY-MM-DD-slug.md

===FILE===
---
layout: post
title: ...
summary: ...
date: __CURRENT_TIMESTAMP__
updated: __CURRENT_TIMESTAMP__
tag: tag1 tag2 tag3
toc: true
comment: false
public: true
---

(body)

===COMMIT===
블로그 글 추가: {제목}
