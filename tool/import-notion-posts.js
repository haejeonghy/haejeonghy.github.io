#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const DEFAULT_SRC_ROOT = '/Users/yuhaejeong/Downloads/개인 페이지 & 공유된 페이지/자원 - Resources';
const DEFAULT_POSTS_ROOT = path.join(REPO_ROOT, '_posts');
const DEFAULT_RESOURCE_ROOT = path.join(REPO_ROOT, 'resource', 'post-format');
const DEFAULT_REPORT = path.join(REPO_ROOT, 'data', 'notion-import-failures.json');

function usage() {
  console.log(
    [
      'Usage:',
      '  node tool/import-notion-posts.js [--src <path>] [--report <path>] [--year-dir <year>] [--run-generate-data]',
      '',
      'Options:',
      '  --src <path>             Notion export root path',
      '  --report <path>          Failure report output json path',
      '  --year-dir <year>        Force output under _posts/<year> (default: from Created date)',
      '  --run-generate-data      Run `node generateData.js` after import',
    ].join('\n')
  );
}

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {
    srcRoot: DEFAULT_SRC_ROOT,
    reportPath: DEFAULT_REPORT,
    fixedYear: '',
    runGenerateData: false,
    dryRun: false,
  };

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--help' || a === '-h') {
      usage();
      process.exit(0);
    }
    if (a === '--src') {
      out.srcRoot = args[++i];
      continue;
    }
    if (a === '--report') {
      out.reportPath = args[++i];
      continue;
    }
    if (a === '--year-dir') {
      out.fixedYear = args[++i];
      continue;
    }
    if (a === '--run-generate-data') {
      out.runGenerateData = true;
      continue;
    }
    if (a === '--dry-run') {
      out.dryRun = true;
      continue;
    }
    throw new Error(`Unknown argument: ${a}`);
  }
  return out;
}

function walkMd(dir, out = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walkMd(p, out);
    else if (ent.isFile() && p.toLowerCase().endsWith('.md')) out.push(p);
  }
  return out;
}

function stripNotionId(name) {
  return name.replace(/\s+[0-9a-f]{32}$/i, '').replace(/\s+/g, ' ').trim();
}

function slugify(input) {
  const s = input
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s-]/gu, ' ')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+|-+$/g, '');
  return s || 'untitled';
}

function parseKoreanDate(text) {
  if (!text) return '';
  const m = text.match(/(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일\s*(오전|오후)\s*(\d{1,2}):(\d{2})/);
  if (!m) return '';
  const year = Number(m[1]);
  const month = Number(m[2]);
  const day = Number(m[3]);
  const ampm = m[4];
  let hour = Number(m[5]);
  const minute = Number(m[6]);
  if (ampm === '오후' && hour < 12) hour += 12;
  if (ampm === '오전' && hour === 12) hour = 0;
  return `${year.toString().padStart(4, '0')}-${month.toString().padStart(2, '0')}-${day
    .toString()
    .padStart(2, '0')} ${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}:00 +0900`;
}

function removeNotionMeta(lines) {
  let i = 0;
  while (i < lines.length && lines[i].trim() === '') i++;
  if (i < lines.length && /^#\s+/.test(lines[i])) i++;

  let j = i;
  while (j < lines.length) {
    const line = lines[j].trim();
    if (line === '') {
      j++;
      break;
    }
    if (/^(Created|Tags|보관소|최종 편집 일시)\s*:/i.test(line)) {
      j++;
      continue;
    }
    break;
  }
  if (j > i) return [...lines.slice(0, i), ...lines.slice(j)];
  return lines;
}

function extractTags(lines) {
  for (const l of lines.slice(0, 30)) {
    const m = l.match(/^Tags\s*:\s*(.+)$/i);
    if (!m) continue;
    const tags = m[1]
      .split(/[;,]/)
      .map((v) => slugify(v.trim()))
      .filter(Boolean);
    if (tags.length) return tags.join(' ');
  }
  return 'notion import';
}

function pickSummary(body, title) {
  const lines = body.split(/\r?\n/);
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    if (/^#/.test(line)) continue;
    if (/^[-*]\s+/.test(line)) continue;
    if (/^>/.test(line)) continue;
    if (/^!?\[[^\]]*]\([^)]+\)$/.test(line)) continue;
    if (/^(```|\* TOC|\{:toc\})/.test(line)) continue;
    const cleaned = line.replace(/[*_`~]/g, '').trim();
    if (cleaned.length >= 8) return cleaned.slice(0, 120);
  }
  return `${title}의 핵심 내용을 정리합니다.`.slice(0, 120);
}

function uniquePath(dir, filename) {
  const ext = path.extname(filename);
  const stem = path.basename(filename, ext);
  let n = 0;
  while (true) {
    const cand = n === 0 ? `${stem}${ext}` : `${stem}-${n}${ext}`;
    const full = path.join(dir, cand);
    if (!fs.existsSync(full)) return { full, name: cand };
    n++;
  }
}

function inInlineCode(line, index) {
  const before = line.slice(0, index);
  const ticks = (before.match(/`/g) || []).length;
  return ticks % 2 === 1;
}

function hasFileLikeShape(linkPath) {
  if (!linkPath) return false;
  if (/^(https?:\/\/|mailto:|#)/i.test(linkPath)) return false;
  if (linkPath.startsWith('/')) return false;
  if (/[<>]/.test(linkPath)) return false;
  // Require either nested path or explicit extension to reduce false positives from code tokens.
  if (linkPath.includes('/')) return true;
  return /\.[a-z0-9]{1,8}$/i.test(linkPath);
}

function normalizeLinkTarget(rawTarget) {
  let t = rawTarget.trim();
  if (t.startsWith('<') && t.endsWith('>')) t = t.slice(1, -1).trim();
  // markdown link title support: (path "title")
  // Keep quoted paths intact, otherwise use first token.
  if ((t.startsWith('"') && t.includes('" ')) || (t.startsWith("'") && t.includes("' "))) {
    const quote = t[0];
    const end = t.indexOf(quote, 1);
    if (end > 1) t = t.slice(1, end);
  } else {
    t = t.split(/\s+/)[0];
  }
  return t;
}

function rewriteLinksAndCopyAssets({ body, srcFile, assetDir, failures, dryRun }) {
  const lines = body.split(/\r?\n/);
  let inFence = false;
  let copiedAssets = 0;

  const outLines = lines.map((line) => {
    const trimmed = line.trim();
    if (/^```/.test(trimmed)) {
      inFence = !inFence;
      return line;
    }
    if (inFence) return line;

    return line.replace(/(!?)\[([^\]]*)\]\(([^)\n]+)\)/g, (full, bang, label, rawTarget, offset) => {
      if (inInlineCode(line, offset)) return full;

      const target = normalizeLinkTarget(rawTarget);
      if (!hasFileLikeShape(target)) return full;

      let decoded = '';
      try {
        decoded = decodeURIComponent(target);
      } catch {
        decoded = target;
      }

      const sourcePath = path.resolve(path.dirname(srcFile), decoded);
      if (!fs.existsSync(sourcePath) || !fs.statSync(sourcePath).isFile()) {
        failures.push({ file: srcFile, reason: 'missing_asset', asset: decoded });
        return full;
      }

      const targetInfo = uniquePath(assetDir, path.basename(sourcePath));
      if (!dryRun) {
        fs.copyFileSync(sourcePath, targetInfo.full);
      }
      copiedAssets++;
      const urlPath = encodeURI(`/resource/post-format/${path.basename(assetDir)}/${targetInfo.name}`);
      return `${bang}[${label}](${urlPath})`;
    });
  });

  return { body: outLines.join('\n'), copiedAssets };
}

function main() {
  const args = parseArgs();
  const srcRoot = args.srcRoot;
  const reportPath = path.resolve(args.reportPath);

  if (!fs.existsSync(srcRoot)) throw new Error(`Source root not found: ${srcRoot}`);

  const posts = walkMd(srcRoot);
  const failures = [];
  let createdPosts = 0;
  let copiedAssets = 0;

  for (const src of posts) {
    try {
      const raw = fs.readFileSync(src, 'utf8');
      const lines = raw.split(/\r?\n/);
      const baseName = stripNotionId(path.basename(src, '.md'));
      const firstTitle = lines.find((l) => /^#\s+/.test(l.trim())) || '';
      const title = stripNotionId(firstTitle.replace(/^#\s+/, '').trim() || baseName);

      const createdLine = lines.find((l) => /^Created\s*:/i.test(l.trim())) || '';
      const updatedLine = lines.find((l) => /^최종 편집 일시\s*:/i.test(l.trim())) || '';
      const date = parseKoreanDate(createdLine) || '2026-03-14 12:00:00 +0900';
      const updated = parseKoreanDate(updatedLine) || date;
      const year = args.fixedYear || date.slice(0, 4);
      const day = date.slice(0, 10);
      const slug = slugify(title);

      const yearDir = path.join(DEFAULT_POSTS_ROOT, year);
      fs.mkdirSync(yearDir, { recursive: true });

      const postPath = uniquePath(yearDir, `${day}-${slug}.md`);
      const postSlug = path.basename(postPath.name, '.md').replace(/^\d{4}-\d{2}-\d{2}-/, '');
      const assetDir = path.join(DEFAULT_RESOURCE_ROOT, postSlug);
      if (!args.dryRun) {
        fs.mkdirSync(assetDir, { recursive: true });
      }

      const stripped = removeNotionMeta(lines).join('\n').trim();
      if (!stripped) {
        failures.push({ file: src, reason: 'empty_body' });
        continue;
      }

      const rewritten = rewriteLinksAndCopyAssets({
        body: stripped,
        srcFile: src,
        assetDir,
        failures,
        dryRun: args.dryRun,
      });
      copiedAssets += rewritten.copiedAssets;

      const summary = pickSummary(rewritten.body, title);
      const tag = extractTags(lines);

      const frontmatter = [
        '---',
        'layout  : post',
        `title   : ${title}`,
        `summary : '${summary.replace(/'/g, "''")}'`,
        `date    : ${date}`,
        `updated : ${updated}`,
        `tag     : ${tag}`,
        'toc     : true',
        'comment : false',
        'public  : true',
        '---',
        '* TOC',
        '{:toc}',
        '',
      ].join('\n');

      if (!args.dryRun) {
        fs.writeFileSync(postPath.full, `${frontmatter}${rewritten.body.trim()}\n`);
      }
      createdPosts++;
    } catch (e) {
      failures.push({ file: src, reason: 'exception', message: e.message });
    }
  }

  fs.mkdirSync(path.dirname(reportPath), { recursive: true });
  fs.writeFileSync(
    reportPath,
    JSON.stringify(
      {
        source_root: srcRoot,
        total_markdown: posts.length,
        created_posts: createdPosts,
        copied_assets: copiedAssets,
        failure_count: failures.length,
        failures,
      },
      null,
      2
    )
  );

  if (args.runGenerateData) {
    execSync('node generateData.js', { cwd: REPO_ROOT, stdio: 'inherit' });
  }

  console.log(
    JSON.stringify(
      {
        source_root: srcRoot,
        total_markdown: posts.length,
        created_posts: createdPosts,
        copied_assets: copiedAssets,
        failure_count: failures.length,
        report: reportPath,
      },
      null,
      2
    )
  );
}

main();
