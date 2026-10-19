#!/usr/bin/env bash
# 一键跑 benchmark 的评分部分（人类评分表 + LLM judge）
set -euo pipefail
cd "$(dirname "$0")"

echo "== 1/2 生成人类评分表 =="
python3 scripts/make_rating_sheet.py

echo "== 2/2 LLM judge 代理评分 =="
python3 scripts/llm_judge.py

echo
echo "完成。结果在 results/ 下。"
echo "下一步：打开 results/interpret_rating_sheet.csv，把 评分(0-5) 一列填上人类评分。"
