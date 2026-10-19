#!/usr/bin/env python3
"""LLM judge 代理评分（0–5）。注意：这是代理，不是人类专家。

用法：python3 llm_judge.py
输出：../results/interpret_llm_judge.json
"""
import json
import os
import re
import ssl
import urllib.request

import certifi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "..", "metrics", "shuowen_interpret.json")
OUT = os.path.join(ROOT, "results", "interpret_llm_judge.json")

SYSTEM = """你是文字学专家。下面给出一个字、模型的训释、以及《说文解字》原文。
请按 0–5 分评分：
5 = 本义与构形理据都与《说文》一致
4 = 本义对，理据部分对
3 = 只对了一部分（如只对部首、只对义类）
2 = 方向对但细节错
1 = 基本不对，但沾边
0 = 完全无关
只输出一个数字，不要解释。"""


def load_key():
    if os.environ.get("DEEPSEEK_API_KEY"):
        return os.environ["DEEPSEEK_API_KEY"]
    for line in open(os.path.expanduser("~/.reasonix/.env"), encoding="utf-8"):
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("DEEPSEEK_API_KEY not found")


def chat(prompt, key):
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 10,
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    ctx = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
        j = json.loads(r.read())
    return j["choices"][0]["message"]["content"].strip()


def main():
    key = load_key()
    m = json.load(open(SRC, encoding="utf-8"))
    rows = []
    for r in m["rows"]:
        prompt = f"字：{r['char']}\n模型训释：{r['model']}\n《说文》原文：{r['gold']}"
        try:
            out = chat(prompt, key)
            score = int(re.search(r"[0-5]", out).group()) if re.search(r"[0-5]", out) else None
        except Exception as e:
            print(r["char"], "失败", e)
            score = None
        rows.append({"char": r["char"], "model": r["model"], "gold": r["gold"], "score": score})
        print(r["char"], "->", score)

    valid = [r["score"] for r in rows if r["score"] is not None]
    out = {
        "judge": "deepseek-chat (LLM judge, 非人类专家)",
        "n": len(rows),
        "valid": len(valid),
        "mean": sum(valid) / len(valid) if valid else None,
        "distribution": {i: valid.count(i) for i in range(6)},
        "rows": rows,
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nLLM judge 均值 {out['mean']:.2f} / 5，有效 {out['valid']}/{out['n']}")
    print("分布", out["distribution"])


if __name__ == "__main__":
    main()
