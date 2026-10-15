# -*- coding: utf-8 -*-
"""Temporary script: reconstruct the lost stu_agent/.env from PyCharm caches,
Claude Code transcripts, and sibling projects' .env files."""
import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

TARGET = 'E:/ai_code/stu_agent/.env'
PYCHARM_DIR = 'C:/Users/16072/AppData/Local/JetBrains/PyCharm2025.3'
TRANSCRIPT_ROOT = 'C:/Users/16072/.claude/projects'
SIBLINGS = [
    ('my_rag', 'E:/ai_code/my_rag_project/.env'),
    ('my_rag_copy', 'E:/ai_code/my_rag_project_copy/.env'),
    ('stu_fastapi', 'E:/ai_code/stu_fastapi/.env'),
]
EXTRA = ['OPEN_API_KEY', 'LLM_NAME', 'LLM_BASE_URL', 'OLLAMA_BASE_URL',
         'OLLAMA_MODEL_NAME', 'CHROMA_DATA_PATH', 'MYSQL_DATABASE']

# -------- 1. discover which env keys stu_agent code actually reads --------
need = set()
for fp in glob.glob('E:/ai_code/stu_agent/**/*.py', recursive=True):
    try:
        text = open(fp, encoding='utf-8', errors='ignore').read()
    except OSError:
        continue
    for m in re.finditer(r'os\.getenv\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)', text):
        need.add(m.group(1))
ALL_KEYS = sorted(need) + EXTRA

def clean(v, key):
    """normalize a raw candidate value; return None if junk"""
    v = v.strip()
    v = re.split(r'[\x00-\x20\x7f]', v)[0]      # cut at any whitespace/control
    v = re.split(r'[\\\\`]', v)[0]              # cut at backslash / backtick
    v = v.rstrip('.,!?').strip()
    low = v.lower()
    if low in ('none', 'null', 'undefined', 'true', 'false', 'nan', 'your_key',
               'your-api-key', 'xxx', '缺省', '默认'):
        return None
    if (low.startswith('not') and len(v) < 20) or any(
            s in low for s in ('你的', '替换', '填写', '示例', '例子')):
        return None
    if len(v) < 2 or len(v) > 300:
        return None
    if key.endswith('_PORT') and not re.fullmatch(r'\d{2,6}', v):
        return None
    return v

def mask(v):
    v = str(v)
    if len(v) <= 8:
        return v[:2] + '***'
    return v[:4] + '***' + v[-2:]

cand_src = {}   # (key, value) -> (count, source)

def add(key, v, weight, src):
    v = clean(v, key)
    if v is None:
        return
    prev = cand_src.get((key, v), (0, ''))
    cand_src[(key, v)] = (prev[0] + weight, src)

# -------- 2. PyCharm cache scan: KEY=value near key occurrences --------
# value chars: printable, excluding quotes, whitespace, comma, braces, $, backslash, controls
VAL = '[^"\'\\s,{}$\\\\' + '\\x00-\\x1f\\x7f]'

def scan_binary(fp, weight):
    try:
        data = open(fp, 'rb').read()
    except OSError:
        return
    for key in ALL_KEYS:
        for m in re.finditer(re.escape(key.encode()), data):
            start, end = max(0, m.start() - 5), min(len(data), m.end() + 300)
            win = data[start:end].decode('latin-1')
            mm = re.search(re.escape(key) + '=' + VAL + '{2,300}', win)
            if mm:
                v = clean(mm.group(1), key)
                if v is not None and len(v) >= (6 if key.endswith(('_KEY', '_CODE', '_PASSWORD', '_TOKEN', '_SECRET')) else 2):
                    prev = cand_src.get((key, v), (0, ''))
                    cand_src[(key, v)] = (prev[0] + weight, fp)

files = glob.glob(PYCHARM_DIR + '/caches/content.dat*') + \
        glob.glob(PYCHARM_DIR + '/index/ru.adelf.idea.php.dotenv.keyvalues/*')
for fp in files:
    scan_binary(fp, weight=2)

# -------- 3. Claude Code transcripts: KEY=value votes --------
pat = re.compile(r'\b(' + '|'.join(re.escape(k) for k in ALL_KEYS) + ')=' + VAL + '{2,300}')
for fp in glob.glob(TRANSCRIPT_ROOT + '/**/*.jsonl', recursive=True):
    try:
        text = open(fp, encoding='utf-8', errors='ignore').read()
    except OSError:
        continue
    seen = set()
    for m in pat.finditer(text):
        k, v = m.group(1), m.group(2)
        if (k, v) not in seen:
            seen.add((k, v))
            add(k, v, 1, 'transcripts')

# -------- 4. decide best value per key (votes desc, then length desc) --------
def best_value(key):
    cands = [(v, c, s) for (k, v), (c, s) in cand_src.items() if k == key]
    cands.sort(key=lambda t: (-t[1], -len(t[0])))
    if not cands:
        return None, None, 0, []
    top, cnt, src = cands[0]
    alt = [t for t in cands[1:] if t[0] != top and t[1] >= max(1, cnt / 2)]
    return top, src, cnt, alt

# -------- 5. sibling .env fallback mapping --------
def parse_env(path):
    d = {}
    try:
        for line in open(path, encoding='utf-8', errors='ignore'):
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.split(' #')[0].split('\t#')[0].strip().strip('"').strip("'")
            if v:
                d[k.strip()] = v
    except OSError:
        pass
    return d

sibs = {n: parse_env(p) for n, p in SIBLINGS}
MAPPING = {
    'MYSQL_HOST': 'MYSQL_HOST', 'MYSQL_PORT': 'MYSQL_PORT',
    'MYSQL_USER': 'MYSQL_USER', 'MYSQL_PASSWORD': 'MYSQL_PASSWORD',
    'MYSQL_NAME': 'MYSQL_DATABASE', 'SMTP_SERVER': 'SMTP_SERVER',
    'SMTP_PORT': 'SMTP_PORT', 'AUTH_CODE': 'AUTH_CODE', 'SEND_EMAIL': 'SEND_EMAIL',
    'LINE_API_KEY': 'OPEN_API_KEY', 'LINE_BASE_URL': 'LLM_BASE_URL',
    'MODEL_LINE_NAME': 'LLM_NAME', 'MODEL_LOCAL_NAME': 'OLLAMA_MODEL_NAME',
    'LOCAL_BASE_URL': 'OLLAMA_BASE_URL',
}

final, missing = {}, []
for k in sorted(need):
    v, src, cnt, alt = best_value(k)
    if v is not None:
        final[k] = (v, '%s(%d票)' % (os.path.basename(src), cnt), alt)
    elif k in MAPPING:
        for name, env in sibs.items():
            if MAPPING[k] in env:
                final[k] = (env[MAPPING[k]], 'sibling:%s[%s]' % (name, MAPPING[k]), [])
                break
    if k not in final and k == 'CHROMA_DB_URL' and os.path.isdir('E:/ai_code/stu_agent/chromadb_data'):
        final[k] = ('E:/ai_code/stu_agent/chromadb_data', '本地chromadb_data目录', [])
    if k not in final:
        missing.append(k)

# -------- 6. write .env --------
lines = ['# 2026-10-15 重建。原 .env 丢失，内容来自本机 PyCharm 缓存 / Claude 会话记录 / 同类项目。', '']
for k in sorted(need):
    if k in final:
        lines.append('%s=%s' % (k, final[k][0]))
    else:
        lines.append('# %s=  <缺失，请手动补充>' % k)
with open(TARGET, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

# -------- report (values masked) --------
print('== 写入 %s' % TARGET)
for k in sorted(need):
    if k in final:
        print('  OK   %-16s -> %-16s 来源:%s' % (k, mask(final[k][0]), final[k][1]))
        for av, ac, asrc in final[k][2][:2]:
            print('         备选: %s (%s, %d票)' % (mask(av), os.path.basename(asrc), ac))
    else:
        print('  MISS %-16s  <未找到任何线索>' % k)
print('扫描的PyCharm缓存文件: %d 个, 有效键值证据: %d 条' % (len(files), len(cand_src)))