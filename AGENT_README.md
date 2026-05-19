# SenseNova U1 生图脚本 — Agent 调用指南

## 快速调用

```bash
cd D:/Agent/SenseNova-U1
E:/Conda/envs_dirs/Agent/python.exe generate.py --prompt "提示词内容" --size 16:9 --n 1
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` / `-p` | ✅ | — | 生成提示词（中英文均可，最长4096 tokens） |
| `--size` / `-s` | — | `16:9` | 图片尺寸：宽高比或像素值 |
| `--n` / `-n` | — | `1` | 生成数量（1-4） |
| `--format` / `-f` | — | `b64_json` | 返回格式：`b64_json`（默认）或 `url` |
| `--api-key` / `-k` | — | 从 .env 读取 | API Key，也可放 .env 文件或环境变量 |
| `--output` / `-o` | — | `./images` | 输出目录，默认脚本所在目录下的 images 子目录 |
| `--quiet` / `-q` | — | — | 静默模式，只输出 JSON 结果 |

## 支持的尺寸

| 宽高比 | 像素值 |
|--------|--------|
| 1:1 | 2048x2048 |
| 4:3 | 2048x1536 |
| 3:4 | 1536x2048 |
| 3:2 | 2048x1365 |
| 2:3 | 1365x2048 |
| 16:9 | 2752x1536 |
| 9:16 | 1536x2752 |
| 21:9 | 2752x1179 |
| 9:21 | 1179x2752 |
| 4:5 | 2048x2560 |
| 5:4 | 2560x2048 |

## Agent 调用示例

### 单张图片
```bash
cd D:/Agent/SenseNova-U1 && E:/Conda/envs_dirs/Agent/python.exe generate.py --prompt "一只金色凤凰在日出时飞翔，中国水墨画风格" --size 16:9
```

### 多张图片（n=4）
```bash
cd D:/Agent/SenseNova-U1 && E:/Conda/envs_dirs/Agent/python.exe generate.py --prompt "机械齿轮爆炸视图，工业设计风格" --size 3:2 --n 4
```

### 指定输出目录
```bash
cd D:/Agent/SenseNova-U1 && E:/Conda/envs_dirs/Agent/python.exe generate.py --prompt "信息图：AI发展历程" --size 1:1 --output D:/Agent/Academic_Figures
```

### 静默模式（返回 JSON）
```bash
cd D:/Agent/SenseNova-U1 && E:/Conda/envs_dirs/Agent/python.exe generate.py --prompt "产品精修工作流信息图" --size 4:3 --quiet
```

输出格式：
```json
{"success": true, "count": 1, "paths": ["D:/Agent/SenseNova-U1/images/产品精修工作流信息图_143052_1.png"], "prompt": "产品精修工作流信息图", "size": "2048x1536"}
```

## API Key 配置

三种方式（优先级从高到低）：

1. **命令行参数**：`--api-key sk-xxxxx`
2. **环境变量**：`SENSENOVA_API_KEY=sk-xxxxx`
3. **.env 文件**：在脚本目录创建 `.env` 文件，内容为 `SENSENOVA_API_KEY=sk-xxxxx`

推荐用第 3 种，已经创建了 `.env` 模板，填入你的 Key 即可。

## 目录结构

```
D:\Agent\SenseNova-U1\
├── generate.py              # 主脚本
├── SenseNova-U1生图工作台.html # WebUI
├── .env                      # API Key 配置文件
├── images/                   # 默认图片输出目录
└── AGENT_README.md           # 本文件
```

## 给其他 Agent 的指令模板

当需要让其他 agent 生图时，直接复制以下内容：

```
请使用 D:/Agent/SenseNova-U1/generate.py 脚本生成图片。

参数：
- prompt: [填入提示词]
- size: [填入宽高比，如 16:9, 1:1, 3:4 等]
- n: [填入数量 1-4，默认 1]

调用命令示例：
cd D:/Agent/SenseNova-U1 && E:/Conda/envs_dirs/Agent/python.exe generate.py --prompt "[提示词]" --size [尺寸]

图片将保存在 D:/Agent/SenseNova-U1/images/ 目录下。
```