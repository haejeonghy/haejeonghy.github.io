#!/usr/bin/env python3
"""
AI 티 제거 스크립트

처리 내용 (코드 블록 내부는 건드리지 않음):
1. 이모지 제거 (본문 + summary 필드)
2. 헤더의 **굵게** 마크업 제거 (## **Title** → ## Title)
3. 장식용 --- 수평선 제거
4. AI 고백 라인 제거
5. 소셜 미디어 해시태그 블록 제거 (#Tag1 #Tag2 형태)
6. *text** 오타 수정 → **text**
7. summary의 > > > 패턴 정리
8. 연속 빈 줄 정리
"""

import os
import re
import sys

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', '_posts')

# 이모지 유니코드 범위 (코드 블록 밖에서만 적용)
# 주의: → (U+2192) 같은 텍스트용 화살표는 포함하지 않음
EMOJI_RE = re.compile(
    '['
    '\U0001F000-\U0001F9FF'   # 이모지 메인 블록 (📝, 🔧, 🐘 등)
    '\U0001FA00-\U0001FAFF'   # 추가 이모지 심볼
    '\u2600-\u26FF'           # 기타 기호 (☀, ★, ✅, ⚙, ⚡ 등)
    '\u2700-\u27BF'           # 딩벳 (✅, ❌, ❓, 💬 등)
    '\uFE0E\uFE0F'            # variation selectors (이모지 뒤에 남는 ️)
    ']+',
    flags=re.UNICODE
)

# AI 고백 라인 패턴
AI_DISCLAIMER_RE = re.compile(
    r'^>?\s*이 게시글은 AI에게.*작성된 글입니다\.?\s*$'
)

# 헤더의 **굵게** 제거: ## **Title** → ## Title
BOLD_HEADER_RE = re.compile(
    r'^(#{1,6}\s+)\*\*(.+?)\*\*\s*$'
)

# 오타 수정: *text** → **text** (앞에 * 하나, 뒤에 ** 두 개)
MALFORMED_BOLD_RE = re.compile(r'(?<!\*)\*([^*\n]+?)\*\*(?!\*)')

# 소셜 미디어 해시태그 라인 (줄 전체가 #태그들로만 구성)
HASHTAG_LINE_RE = re.compile(r'^(#\w[\w가-힣]*(\s+|$))+$')
BACKTICK_HASHTAG_LINE_RE = re.compile(r'^(`#\w[\w가-힣]*`\s*)+$')


def clean_emojis(text):
    """이모지 제거 (공백은 그대로 유지)"""
    return EMOJI_RE.sub('', text)


def clean_summary(line):
    """frontmatter summary 필드 정리"""
    cleaned = clean_emojis(line)
    # 따옴표 안의 내용 추출하여 > > > 패턴 제거 (Notion 블록쿼트 아티팩트)
    def clean_summary_value(m):
        prefix = m.group(1)
        value = m.group(2)
        # 값 안의 > > > 패턴 제거 (앞/중간/뒤 모두)
        value = re.sub(r'\s*(>\s*)+', ' ', value).strip()
        # 빈 값이면 빈 summary로
        if not value:
            return "summary : ''"
        return f"{prefix}'{value}'"
    cleaned = re.sub(r"(summary\s*:\s*)'(.*)'", clean_summary_value, cleaned)
    # 따옴표 안이 비거나 공백/> 만 있으면 빈 summary로
    cleaned = re.sub(r"summary\s*:\s*'[\s>]*'", "summary : ''", cleaned)
    return cleaned.rstrip()


def is_hashtag_line(line):
    stripped = line.strip()
    if not stripped:
        return False
    return bool(HASHTAG_LINE_RE.match(stripped)) or bool(BACKTICK_HASHTAG_LINE_RE.match(stripped))


def clean_body(body):
    """본문 정리 (코드 블록 내부 보존)"""
    lines = body.split('\n')
    result = []
    in_code_block = False
    prev_blank = False  # 코드 블록 밖에서만 연속 빈 줄 제거에 사용

    for line in lines:
        # 코드 블록 진입/탈출 감지
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            prev_blank = False
            continue

        # 코드 블록 내부: 손대지 않음 (연속 빈 줄도 보존)
        if in_code_block:
            result.append(line)
            continue

        # AI 고백 라인 제거
        if AI_DISCLAIMER_RE.match(line):
            continue

        # 소셜 미디어 해시태그 라인 제거
        if is_hashtag_line(line):
            continue

        # 장식용 --- 제거 (본문 내 --- 는 모두 장식용으로 간주)
        if line.strip() == '---':
            continue

        # 이모지 제거
        cleaned = clean_emojis(line)

        # 이모지 제거 후 남는 연속 공백 정리 (단, 인덴트는 보존)
        leading_spaces = len(cleaned) - len(cleaned.lstrip(' '))
        cleaned = cleaned[:leading_spaces] + re.sub(r' {2,}', ' ', cleaned[leading_spaces:])

        # 헤더의 **굵게** 제거
        m = BOLD_HEADER_RE.match(cleaned)
        if m:
            cleaned = m.group(1) + m.group(2).strip()

        # *text** 오타 수정 → **text**
        cleaned = MALFORMED_BOLD_RE.sub(r'**\1**', cleaned)

        # 이모지만 있던 헤더가 빈 헤더로 남은 경우 제거
        if re.match(r'^#{1,6}\s*$', cleaned.rstrip()):
            continue

        # 이모지 제거 후 **만 남은 헤더 제거 (예: ### **** )
        if re.match(r'^#{1,6}\s+\*+\s*$', cleaned.rstrip()):
            continue

        # AI 생성 태그 제안 섹션 헤더 제거
        if re.match(r'^#{1,6}\s*태그\s*제안', cleaned.rstrip()):
            continue

        # 코드 블록 밖에서 연속 빈 줄 2개 이상 → 1개로
        if cleaned.strip() == '':
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False

        result.append(cleaned)

    # 원본의 trailing newline 상태 유지
    result_str = '\n'.join(result)
    if body.endswith('\n') and not result_str.endswith('\n'):
        result_str += '\n'
    return result_str


def clean_frontmatter(fm_raw):
    """frontmatter 정리"""
    lines = fm_raw.split('\n')
    result = []
    for line in lines:
        if re.match(r'^summary\s*:', line):
            result.append(clean_summary(line))
        else:
            result.append(line)
    return '\n'.join(result)


def parse_frontmatter(content):
    if not content.startswith('---'):
        return None, None, content
    end = content.find('\n---', 3)
    if end == -1:
        return None, None, content
    fm_raw = content[3:end]
    body = content[end + 4:]
    return content[:3], fm_raw, body


def process_file(filepath, dry_run=True):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    _, fm_raw, body = parse_frontmatter(content)
    if fm_raw is None:
        return {'file': filename, 'skipped': True}

    new_fm = clean_frontmatter(fm_raw)
    new_body = clean_body(body)

    changed = (new_fm != fm_raw) or (new_body != body)

    if changed and not dry_run:
        new_content = f'---{new_fm}\n---{new_body}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return {'file': filename, 'changed': changed}


def main():
    dry_run = '--apply' not in sys.argv
    if dry_run:
        print('=== DRY RUN 모드 (실제 변경 없음) ===')
        print('실제 적용하려면: python3 tool/remove_ai_style.py --apply\n')
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

    changed = [r for r in results if r.get('changed')]
    skipped = [r for r in results if r.get('skipped')]

    print(f'총 포스트: {len(results)}개')
    print(f'변경 대상: {len(changed)}개')
    print(f'건너뜀: {len(skipped)}개\n')

    for r in changed:
        print(f'  {r["file"]}')

    if dry_run and changed:
        print(f'\n위 {len(changed)}개 파일에 변경사항이 있습니다.')
        print('적용하려면: python3 tool/remove_ai_style.py --apply')


if __name__ == '__main__':
    main()
