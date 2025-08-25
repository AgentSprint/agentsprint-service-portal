import os
import re
import sys
import string

BODY = sys.stdin.read()

# Find sections that start with "### <Header>" and capture everything until the next "###" or end of text
SECTION_RE = re.compile(r"^###\s+(.+?)\s*\n([\s\S]*?)(?=^###\s+|\Z)", re.MULTILINE)

def sanitize_key(header: str) -> str:
    # Lowercase, replace non-alnum with underscores, collapse repeats, strip ends
    key = header.strip().lower()
    key = re.sub(r"[^a-z0-9]+", "_", key)
    key = re.sub(r"_+", "_", key).strip("_")
    # Env var must not be empty or start with a digit
    if not key:
        key = "field"
    if key[0] in string.digits:
        key = f"f_{key}"
    return key

def first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""

pairs = {}
for header, block in SECTION_RE.findall(BODY):
    key = sanitize_key(header)
    value = first_non_empty_line(block)
    pairs[key] = value

# Write to $GITHUB_ENV so later steps can use them as $key
env_path = os.environ.get("GITHUB_ENV")
if not env_path:
    print("GITHUB_ENV not set", file=sys.stderr)
    sys.exit(1)

with open(env_path, "a", encoding="utf-8") as f:
    for k, v in pairs.items():
        f.write(f"{k}={v}\n")

# Optional: echo what we parsed for logs
for k, v in pairs.items():
    print(f"{k}={v}")
