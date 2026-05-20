# SenseNova U1 WebUI

一个简洁、高效的 SenseNova U1 Fast 生图模型 WebUI，纯前端单文件运行，零依赖部署。

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-red.svg)](http://www.wtfpl.net/)

---

## 特性

- **单文件架构** — 纯 HTML + JavaScript，无需构建工具、无需 Node.js
- **毛玻璃深色主题** — 支持一键切换深色/浅色模式，圆形扩散动画平滑过渡
- **11 种 2K 分辨率预设** — 覆盖 16:9、1:1、4:3、9:16 等常见宽高比
- **自动本地保存** — 使用 File System Access API，选定目录后自动写入
- **目录记忆持久化** — 通过本地服务器运行时，目录权限跨会话保留，无需重复选择
- **实时调用日志** — 追踪每次 API 请求状态
- **响应式布局** — 桌面端/移动端自适应

## 快速开始

### 方式一：本地服务器（推荐）

目录权限可跨会话保持，选一次永久记住。

```bash
git clone https://github.com/yourusername/sensenova-u1-webui.git
cd sensenova-u1-webui
```

双击 `start.bat`，浏览器自动打开 `http://localhost:8080`。

### 方式二：直接打开（零依赖）

双击 `index.html` 在浏览器中打开即可使用。但注意：以 `file://` 协议打开时，Chrome 不持久化文件系统权限，每次需要重新选择保存目录。

### 使用步骤

1. 获取 [SenseNova API Key](https://platform.sensenova.cn/console/keys)
2. 打开页面，填入 API Key
3. （可选）点击「选择目录」设定自动保存路径
4. 输入提示词，点击生成或按 `Ctrl + Enter`

## 主题切换

支持深色/浅色两种主题，点击顶栏右侧的太阳/月亮图标切换。

切换时使用 CSS `mask-image` 径向渐变从按钮位置向外扩散，扩散区域内直接展示目标主题的完整 UI，无中间闪烁。

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

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Enter` | 生成图片 |
| `Esc` | 关闭大图预览 |

## 目录结构

```
sensenova-u1-webui/
├── index.html              # WebUI 主界面（单文件）
├── start.bat               # Windows 本地服务器启动脚本
├── generate.py             # Python 命令行生图脚本
├── .env.example            # API Key 配置文件模板
├── images/                 # Python 脚本的默认输出目录
├── AGENT_README.md         # Python 脚本调用指南
└── LICENSE                 # WTFPL 许可证
```

## 浏览器兼容性

| 功能 | Chrome / Edge | Firefox | Safari |
|------|:---:|:---:|:---:|
| 核心功能（API 调用、展示） | ✅ | ✅ | ✅ |
| 自动保存到选定目录 | ✅ | ❌ 回退到下载 | ❌ 回退到下载 |
| 目录权限跨会话记忆 | ✅ 需本地服务器 | — | — |

## 技术细节

- 使用原生 Fetch API 调用 SenseNova 接口
- 响应格式默认 `b64_json`，图片数据直接写入本地
- 目录选择使用 [File System Access API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API)
- 目录句柄经由 IndexedDB 持久化，配合 `showDirectoryPicker({ id })` 实现跨会话恢复
- 主题切换使用 CSS `mask-image` + `requestAnimationFrame` 驱动的径向渐变展开
- 状态持久化使用 localStorage（API Key、提示词、参数选择、主题偏好）

## Python 脚本

项目附带 `generate.py`，支持命令行和 Agent 自动化调用：

```bash
python generate.py --prompt "一只金色凤凰在日出时飞翔" --size 16:9 --n 1
```

详细参数见 [AGENT_README.md](./AGENT_README.md)。

## 注意事项

- **API 额度**：SenseNova U1 Fast 提供 1,500 次 / 5 小时的免费额度
- **分辨率锁定**：API 版本固定 2K 分辨率，无法自定义像素值
- **临时链接**：`url` 格式返回的图片链接有过期时间，建议使用 `b64_json` 格式
- **目录权限**：`file://` 协议下 Chrome 不持久化文件系统权限，推荐使用 `start.bat` 以本地服务器方式运行

## 许可证

**WTFPL** — Do What The Fuck You Want To Public License

详见 [LICENSE](./LICENSE)。

## 致谢

- [SenseNova](https://platform.sensenova.cn/) — 商汤日日新大模型平台
- [SenseNova U1](https://github.com/OpenSenseNova/SenseNova-U1) — 开源原生多模态统一模型

---

**免责声明**：本项目为第三方社区工具，非商汤官方出品。API 调用产生的费用和额度消耗由用户自行承担。
