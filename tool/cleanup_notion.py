#!/usr/bin/env python3
"""
블로그 포스트 Notion 유산 정리 스크립트

처리 내용:
1. frontmatter summary의 Notion 메타데이터 제거
2. 본문의 Notion 메타데이터 라인 제거 (Created:, Last Edited Time: 등)
3. 'notion import' 태그를 파일명 기반으로 실제 태그로 교체
"""

import os
import re
import sys

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', '_posts')

# Notion 메타데이터 라인 패턴
NOTION_LINE_PATTERNS = [
    re.compile(r'^Created:\s+\d{4}년.*$'),
    re.compile(r'^Last Edited Time:\s+.*$'),
    re.compile(r'^Type:\s+.*$'),
    re.compile(r'^Created By:\s+.*$'),
    re.compile(r'^Tags:\s+.*$'),
    re.compile(r'^보관소:\s+.*$'),
    re.compile(r'^최종 편집 일시:\s+.*$'),
]

# Notion summary 패턴
NOTION_SUMMARY_PATTERN = re.compile(
    r"'?(Last Edited Time:|Created:).*'"
)

# 파일명 → 태그 매핑 (우선순위 순서로 체크)
FILENAME_TAG_MAP = [
    ('streaming-systems', 'streaming book'),
    ('러닝-고', 'golang book'),
    ('켄트-벡', 'book'),
    ('tidy-first', 'book'),
    ('command-패턴', 'pattern'),
    ('프록시', 'pattern'),
    ('kotlin-스터디', 'kotlin study'),
    ('안드로이드-스터디', 'android study'),
    ('kotlinx', 'kotlin android'),
    ('kotlin', 'kotlin'),
    ('안드로이드', 'android'),
    ('unable-to-locate-adb', 'android'),
    ('jdbcsession', 'spring'),
    ('jpa', 'jpa spring'),
    ('aws', 'aws'),
    ('gradle', 'gradle'),
    ('grpc', 'grpc'),
    ('osi', 'network'),
    ('네트워크', 'network'),
    ('cloudevents', 'cloudevents'),
    ('cmd', 'command'),
    ('copybara', 'copybara'),
    ('intellij', 'intellij'),
    ('architecture', 'architecture'),
    ('project-kickoff', 'template'),
    ('technical-spec', 'template'),
    ('코넬', 'template'),
    ('org-gradle', 'gradle'),
]


def is_notion_summary(summary: str) -> bool:
    return bool(NOTION_SUMMARY_PATTERN.search(summary))


def infer_tags_from_filename(filename: str):
    name = filename.lower()
    for keyword, tags in FILENAME_TAG_MAP:
        if keyword.lower() in name:
            return tags
    return None


def is_notion_line(line: str) -> bool:
    stripped = line.rstrip()
    return any(p.match(stripped) for p in NOTION_LINE_PATTERNS)


def parse_frontmatter(content: str):  # type: ignore
    """frontmatter와 본문을 분리"""
    if not content.startswith('---'):
        return None, None, content
    end = content.find('\n---', 3)
    if end == -1:
        return None, None, content
    fm_raw = content[3:end]
    body = content[end + 4:]
    return content[:3], fm_raw, body


def clean_body(body: str) -> tuple[str, int]:
    """본문에서 Notion 메타데이터 라인 제거"""
    lines = body.split('\n')
    cleaned = []
    removed = 0
    for line in lines:
        if is_notion_line(line):
            removed += 1
        else:
            cleaned.append(line)
    # 연속된 빈 줄 2개 이상 → 1개로 축소
    result_lines = []
    prev_blank = False
    for line in cleaned:
        if line.strip() == '':
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False
        result_lines.append(line)
    return '\n'.join(result_lines), removed


def clean_frontmatter(fm_raw: str, filename: str) -> tuple[str, list[str]]:
    """frontmatter 수정: summary 정리, notion import 태그 교체"""
    changes = []
    lines = fm_raw.split('\n')
    new_lines = []

    for line in lines:
        # summary 정리
        if line.strip().startswith('summary') and is_notion_summary(line):
            new_lines.append("summary : ''")
            changes.append('summary 정리')
            continue

        # notion import 태그 교체
        if re.match(r'^tag\s*:\s*notion\s+import\s*$', line.strip()):
            inferred = infer_tags_from_filename(filename)
            if inferred:
                new_lines.append(f'tag     : {inferred}')
                changes.append(f'태그 변경: notion import → {inferred}')
            else:
                new_lines.append('tag     :')
                changes.append('태그 변경: notion import → (빈 태그)')
            continue

        new_lines.append(line)

    return '\n'.join(new_lines), changes


def process_file(filepath: str, dry_run: bool = True) -> dict:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    _, fm_raw, body = parse_frontmatter(content)
    if fm_raw is None:
        return {'file': filename, 'skipped': True}

    new_fm, fm_changes = clean_frontmatter(fm_raw, filename)
    new_body, removed_lines = clean_body(body)

    all_changes = fm_changes.copy()
    if removed_lines > 0:
        all_changes.append(f'본문 Notion 메타데이터 {removed_lines}줄 제거')

    if not all_changes:
        return {'file': filename, 'changes': []}

    if not dry_run:
        new_content = f'---{new_fm}\n---{new_body}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return {'file': filename, 'changes': all_changes}


def main():
    dry_run = '--apply' not in sys.argv
    if dry_run:
        print('=== DRY RUN 모드 (실제 변경 없음) ===')
        print('실제 적용하려면: python3 tool/cleanup_notion.py --apply\n')
    else:
        print('=== 실제 적용 모드 ===\n')

    results = []
    for root, _, files in os.walk(POSTS_DIR):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            result = process_file(fpath, dry_run=dry_run)
            results.append(result)

    changed = [r for r in results if r.get('changes')]
    skipped = [r for r in results if r.get('skipped')]

    print(f'총 포스트: {len(results)}개')
    print(f'변경 대상: {len(changed)}개')
    print(f'건너뜀: {len(skipped)}개\n')

    for r in changed:
        print(f'  [{r["file"]}]')
        for c in r['changes']:
            print(f'    - {c}')

    if dry_run and changed:
        print(f'\n위 {len(changed)}개 파일에 변경사항이 있습니다.')
        print('적용하려면: python3 tool/cleanup_notion.py --apply')


if __name__ == '__main__':
    main()
