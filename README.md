# SenseNova U1 WebUI

一个简洁、高效的 SenseNova U1 Fast 生图模型 WebUI，支持本地单文件运行，零依赖部署。

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-red.svg)](http://www.wtfpl.net/)

## 特性

- **单文件运行** — 纯 HTML + JavaScript，双击即用，无需构建
- **毛玻璃深色主题** — 现代简洁的视觉风格
- **完整参数支持** — 11 种 2K 分辨率预设尺寸
- **自动本地保存** — 使用 File System Access API，一键选择目录后自动保存
- **API 调用日志** — 实时追踪每次调用，精准可控
- **响应式布局** — 桌面端/移动端自适应

## 快速开始

1. 获取 [SenseNova API Key](https://platform.sensenova.cn/console/keys)
2. 下载 `index.html`，双击在浏览器中打开
3. 填入 API Key，输入提示词，点击生成

或者在线体验（需要自建后端）：

```bash
git clone https://github.com/yourusername/sensenova-u1-webui.git
cd sensenova-u1-webui
# 直接用浏览器打开 index.html
```

## API 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `model` | string | ✅ | — | 固定 `sensenova-u1-fast` |
| `prompt` | string | ✅ | — | 生成提示词，最长 4096 tokens |
| `size` | string | — | `2752x1536` | 2K 固定分辨率，11 种宽高比 |
| `n` | integer | — | `1` | 生成数量，1-4 |
| `response_format` | string | — | `url` | `url` 或 `b64_json` |

### 支持的尺寸（2K 固定分辨率）

| 宽高比 | 像素值 | 适用场景 |
|--------|--------|----------|
| 1:1 | 2048×2048 | 社交媒体头像、正方形海报 |
| 4:3 | 2048×1536 | PPT 配图、文档插图 |
| 3:4 | 1536×2048 | 竖版文档、小红书封面 |
| 3:2 | 2048×1365 | 横版摄影风格 |
| 2:3 | 1365×2048 | 竖版摄影风格 |
| **16:9** | **2752×1536** | **默认，横幅、视频封面** |
| 9:16 | 1536×2752 | 竖屏视频、抖音封面 |
| 21:9 | 2752×1179 | 超宽屏、电影感画面 |
| 9:21 | 1179×2752 | 超窄竖屏、长图 |
| 4:5 | 2048×2560 | Instagram 竖版 |
| 5:4 | 2560×2048 | Instagram 横版 |

## 官方文档

- [SenseNova 官方文档](https://platform.sensenova.cn/docs)
- [SenseNova U1 Fast API 参考](https://platform.sensenova.cn/en/docs)（英文）
- [SenseNova GitHub](https://github.com/OpenSenseNova)

API 端点：`https://token.sensenova.cn/v1/images/generations`

认证方式：Bearer Token（OpenAI 兼容格式）

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Enter` | 生成图片 |
| `Esc` | 关闭大图预览 |

## 浏览器兼容性

- ✅ Chrome / Edge（推荐，完整支持 File System Access API）
- ✅ Firefox（不支持自动保存到指定目录，回退到下载）
- ✅ Safari（不支持自动保存到指定目录，回退到下载）

## 技术细节

- 使用原生 Fetch API 调用 SenseNova 接口
- 响应格式默认 `b64_json`，图片数据直接写入本地
- 目录选择使用 [File System Access API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API)
- 状态持久化使用 localStorage

## Python 脚本

项目同时提供一个 Python 命令行脚本 `generate.py`，支持 Agent 自动化调用：

```bash
python generate.py --prompt "一只金色凤凰在日出时飞翔" --size 16:9 --n 1
```

详见 [AGENT_README.md](./AGENT_README.md)

## 注意事项

- **API 额度**：SenseNova U1 Fast 提供 1,500 次 / 5 小时的免费额度
- **分辨率锁定**：API 版本固定 2K 分辨率，无法自定义像素值
- **临时链接**：`url` 格式返回的图片链接有过期时间，建议使用 `b64_json` 格式

## 许可证

**WTFPL** — Do What The Fuck You Want To Public License

详见 [LICENSE](./LICENSE)。简单说：你想干嘛就干嘛，没有任何限制。

## 致谢

- [SenseNova](https://platform.sensenova.cn/) — 商汤日日新大模型平台
- [SenseNova U1](https://github.com/OpenSenseNova/SenseNova-U1) — 开源原生多模态统一模型

---

**免责声明**：本项目为第三方社区工具，非商汤官方出品。API 调用产生的费用和额度消耗由用户自行承担。