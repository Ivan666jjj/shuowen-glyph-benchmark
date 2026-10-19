#!/usr/bin/env python3
"""导出人类专家评分表（CSV）：模型训释 + 《说文》原文 + 0–5 评分列。

用法：python3 make_rating_sheet.py
输出：../results/interpret_rating_sheet.csv
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "..", "metrics", "shuowen_interpret.json")
OUT = os.path.join(ROOT, "results", "interpret_rating_sheet.csv")

RUBRIC = """\
评分标准（0–5）：
5 = 本义与构形理据都与《说文》一致
4 = 本义对，理据部分对
3 = 只对了一部分（如只对部首、只对义类）
2 = 方向对但细节错
1 = 基本不对，但沾边
0 = 完全无关
"""


def main():
    m = json.load(open(SRC, encoding="utf-8"))
    rows = m["rows"]
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["序号", "字", "模型训释", "《说文》原文", "评分(0-5)", "备注"])
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["char"], r["model"].replace("\n", " "), r["gold"], "", ""])
    print("written", OUT, "rows:", len(rows))
    print(RUBRIC)


if __name__ == "__main__":
    main()
