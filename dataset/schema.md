# 数据集字段说明

## `concepts.json`

104 个现代概念（造字任务的目标所指）。

```json
["电灯", "手机", "电脑", ...]
```

## `radicals.json`

468 个《说文》部首。字段：

| 字段 | 说明 |
|---|---|
| `form` | 部首写法（如「火」「目」） |
| `pinyin` | 现代读音 |
| `meaning` | 释义（截取） |
| `category` | 义类：器物 / 自然 / 抽象 / 人体 / 动物 |

## `shuowen_sample.json`

100 个《说文》原字（释字任务）。字段：

| 字段 | 说明 |
|---|---|
| `char` | 单字 |
| `radical` | 所属部首（如「一部」） |
| `pinyin` | 现代读音 |
| `content` | 《说文》原文（训释） |

## 评分表 `results/interpret_rating_sheet.csv`

| 列 | 说明 |
|---|---|
| 序号 | 1–100 |
| 字 | 单字 |
| 模型训释 | 模型输出的本义 + 理据 |
| 《说文》原文 | 对照原文 |
| 评分(0-5) | **留空，待人类专家填写** |
| 备注 | 可选 |

## LLM judge `results/interpret_llm_judge.json`

| 字段 | 说明 |
|---|---|
| `judge` | 判分模型（deepseek-chat） |
| `n` / `valid` | 总数 / 有效评分 |
| `mean` | 均值（0–5） |
| `distribution` | 各分数的人数 |
| `rows` | 逐字结果 |
