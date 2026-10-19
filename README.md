# 字形表义性 Benchmark（Glyph Meaningfulness Benchmark）

![License](https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY%204.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-v0.1.0-green)


一套可复用的评测流程，用来检验“AI 造出来的字形是否承载意义”。
本目录是从《说文》部首造字实验中抽出来的最小可复现版本。

## 任务

| 任务 | 输入 | 输出 | 指标 |
|---|---|---|---|
| `form`（造字） | 概念 + 部首表 | 字形（部首组合） | 猜义正确率、字形稳定率 |
| `interpret`（释字） | 单字 | 本义 + 构形理据 | 关键词命中率、人类评分（0–5）、LLM judge（0–5） |
| `learn`（可学性） | 使用示例 / 码表 | 猜义 | 三条件正确率 |
| `metrics`（结构） | 字形表 | — | RSA、CKA、互信息、整字表义一致性 |

## 数据

| 文件 | 内容 |
|---|---|
| `dataset/concepts.json` | 105 个现代概念（造字的目标） |
| `dataset/radicals.json` | 468 个《说文》部首（形符池） |
| `dataset/shuowen_sample.json` | 100 个《说文》原字（释字任务） |
| `dataset/schema.md` | 字段说明 |

## 安装

```bash
pip install -r requirements.txt
```

主实验脚本（造字 / 释字）依赖 Node.js 与 API key，见主仓库说明；本目录的评分脚本只需 Python。

## 目录结构

```
benchmark/
├── README.md
├── LICENSE                  # 代码 MIT，数据 CC BY 4.0
├── requirements.txt
├── run_all.sh               # 一键跑评分部分
├── dataset/                 # 104 概念 / 468 部首 / 100 释字样本
├── scripts/                 # 评分表生成、LLM judge
└── results/                 # 评分表、judge 结果、leaderboard
```

## 跑法

```bash
# 1) 造字 + 猜义（40 轮，同源）
node ../shuowen_lifecycle.js --stage form --rounds 40 --seed 101 --label bench_form

# 2) 释字 + 关键词命中
node ../shuowen_interpret.js

# 3) 结构指标（RSA / CKA / 互信息）
python3 ../measures_enhanced.py

# 4) 人类评分表（导出 CSV，人工打分）
python3 scripts/make_rating_sheet.py

# 5) LLM judge（代理评分，非人类）
python3 scripts/llm_judge.py
```

## 评分标准（0–5）

| 分 | 标准 |
|---|---|
| 5 | 本义与构形理据都与《说文》一致 |
| 4 | 本义对，理据部分对 |
| 3 | 只对了一部分（如只对部首、只对义类） |
| 2 | 方向对但细节错 |
| 1 | 基本不对，但沾边 |
| 0 | 完全无关 |

## 已跑结果（2026-10-19）

| 实验 | 结果 |
|---|---|
| 1000 轮造字 | 猜义 0.619；带提示词优化 0.805 |
| 5 seeds（40 轮） | 0.575 ± 0.053 |
| 跨模型（3 对 × 5 seeds） | DS→千问 0.600±0.025；千问→DS 0.635±0.049；DS→GLM 0.500±0.043 |
| 释字（100 字） | 关键词命中 0.970；LLM judge #1 3.95/5、#2 4.40/5（相关 0.755）；**人类评分待填** |
| RSA / CKA | 0.313 / 0.108 |
| 互信息（初/中/终） | 0.62 / 0.58 / 0.42 |
| 整字表义一致性 | 0.896 |

## 引用

如果用到这套流程，请引用：

> 严毓焕. 《说文》部首驱动的机器造字：468 部、1000 轮与可学性检验[J]. 数字人文研究（审稿中）.

## 许可

- 代码：MIT
- 数据：CC BY 4.0

## 局限

1. 数据集只覆盖 468/540 部，缺 72 部；
2. 释字任务的“关键词命中”是宽松指标，接近饱和，需配合人类评分；
3. LLM judge 是代理，不是真正的人类专家；
4. 主要结果来自 DeepSeek，跨模型只做了 3 对。
