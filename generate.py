#!/usr/bin/env python3
"""
SenseNova U1 Fast 生图脚本 — Agent 直接调用
用法: python generate.py --prompt "一只金色凤凰" --size 16:9 --n 1
图片默认保存到脚本所在目录，命名用中文提示词前缀
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("缺少 requests 库，正在安装...")
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests

# ── 常量 ──
BASE_URL = "https://token.sensenova.cn/v1"
ENDPOINT = f"{BASE_URL}/images/generations"
SCRIPT_DIR = Path(__file__).resolve().parent

# 11 种 2K 预设尺寸
SIZE_MAP = {
    "1:1":   "2048x2048",
    "4:3":   "2048x1536",
    "3:4":   "1536x2048",
    "3:2":   "2048x1365",
    "2:3":   "1365x2048",
    "16:9":  "2752x1536",
    "9:16":  "1536x2752",
    "21:9":  "2752x1179",
    "9:21":  "1179x2752",
    "4:5":   "2048x2560",
    "5:4":   "2560x2048",
}

# 也可以直接传像素值，如 "2048x2048"
VALID_PIXEL_SIZES = set(SIZE_MAP.values())


def sanitize_filename(text: str, max_len: int = 20) -> str:
    """提示词转安全文件名前缀"""
    # 去掉花括号、模板标记
    cleaned = text.replace('{', '').replace('}', '')
    # 保留中英文、数字、下划线
    cleaned = re.sub(r'[\\/:*?"<>|\s]', '_', cleaned)
    cleaned = re.sub(r'_+', '_', cleaned).strip('_')
    # 去掉常见模板前缀
    for prefix in ['type', 'type____']:
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].lstrip('_')
    return cleaned[:max_len] if cleaned else "u1"


def get_api_key(args) -> str:
    """获取 API Key：命令行参数 > 环境变量 > .env 文件"""
    if args.api_key:
        return args.api_key

    env_key = os.environ.get("SENSENOVA_API_KEY")
    if env_key:
        return env_key

    # 尝试读取 .env 文件
    env_file = SCRIPT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("SENSENOVA_API_KEY="):
                return line.split("=", 1)[1].strip()

    print("错误: 未提供 API Key")
    print("请通过以下任一方式提供:")
    print("  1. --api-key sk-xxx")
    print("  2. 环境变量 SENSENOVA_API_KEY")
    print("  3. 在脚本目录创建 .env 文件: SENSENOVA_API_KEY=sk-xxx")
    sys.exit(1)


def resolve_size(size_input: str) -> str:
    """解析尺寸输入：宽高比 or 像素值"""
    # 宽高比映射
    if size_input in SIZE_MAP:
        return SIZE_MAP[size_input]

    # 直接像素值
    if size_input in VALID_PIXEL_SIZES:
        return size_input

    # 校验像素格式 WxH
    match = re.match(r'^(\d+)x(\d+)$', size_input)
    if match:
        w, h = int(match.group(1)), int(match.group(2))
        if SIZE_MAP.get(f"{w}:{h}"):
            return SIZE_MAP[f"{w}:{h}"]
        # 自定义像素值（API 可能不支持，但尝试一下）
        print(f"警告: {size_input} 不是预设尺寸，API 可能返回错误")
        print(f"预设尺寸: {', '.join(f'{k}={v}' for k, v in SIZE_MAP.items())}")
        return size_input

    print(f"错误: 无效尺寸 '{size_input}'")
    print(f"支持的宽高比: {', '.join(SIZE_MAP.keys())}")
    print(f"支持的像素值: {', '.join(VALID_PIXEL_SIZES)}")
    sys.exit(1)


def generate_image(api_key: str, prompt: str, size: str, n: int,
                   response_format: str, output_dir: Path, quiet: bool) -> list:
    """调用 API 生图并保存"""

    body = {
        "model": "sensenova-u1-fast",
        "prompt": prompt,
        "size": size,
        "n": n,
        "response_format": response_format,
    }

    if not quiet:
        print(f"→ 调用 API: prompt=\"{prompt[:40]}...\" size={size} n={n} format={response_format}")

    try:
        res = requests.post(
            ENDPOINT,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=120,
        )
    except requests.exceptions.Timeout:
        print("错误: API 请求超时（120秒）")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接 API 服务器")
        sys.exit(1)

    if res.status_code != 200:
        try:
            err_data = res.json()
            err_msg = err_data.get("error", {}).get("message", res.text)
        except json.JSONDecodeError:
            err_msg = f"HTTP {res.status_code}: {res.text[:200]}"
        print(f"错误: {err_msg}")
        sys.exit(1)

    data = res.json()
    images = data.get("data", [])

    if not images:
        print("错误: API 未返回图片数据")
        sys.exit(1)

    if not quiet:
        print(f"✓ 返回 {len(images)} 张图片")

    # 保存图片
    prefix = sanitize_filename(prompt)
    timestamp = time.strftime("%H%M%S")
    saved_paths = []

    for i, img in enumerate(images):
        filename = f"{prefix}_{timestamp}_{i + 1}.png"
        filepath = output_dir / filename

        if response_format == "b64_json":
            b64_data = img.get("b64_json")
            if b64_data:
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(b64_data))
            else:
                print(f"  图片 {i+1}: 无 b64_json 数据")
                continue
        else:
            # URL 模式：下载图片
            url = img.get("url")
            if url:
                try:
                    img_res = requests.get(url, timeout=60)
                    with open(filepath, "wb") as f:
                        f.write(img_res.content)
                except Exception as e:
                    print(f"  图片 {i+1} 下载失败: {e}")
                    continue
            else:
                print(f"  图片 {i+1}: 无 url 数据")
                continue

        saved_paths.append(str(filepath))
        if not quiet:
            print(f"  保存: {filepath}")

    return saved_paths


def main():
    parser = argparse.ArgumentParser(
        description="SenseNova U1 Fast 生图脚本 — Agent 直接调用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
预设尺寸 (宽高比 → 像素值):
  {chr(10).join(f'  {k}  →  {v}' for k, v in SIZE_MAP.items())}

示例:
  python generate.py --prompt "一只金色凤凰在日出时飞翔" --size 16:9
  python generate.py --prompt "信息图：AI发展历程" --size 1:1 --n 2 --format b64_json
  python generate.py --prompt "机械齿轮 exploded view" --size 3:2 --api-key sk-xxx --output D:\\my_images
        """
    )

    parser.add_argument("--prompt", "-p", required=True,
                        help="生成提示词（中英文均可，最长 4096 tokens）")
    parser.add_argument("--size", "-s", default="16:9",
                        help="图片尺寸：宽高比(如 16:9) 或像素值(如 2752x1536)")
    parser.add_argument("--n", "-n", type=int, default=1, choices=[1, 2, 3, 4],
                        help="生成数量 (1-4)")
    parser.add_argument("--format", "-f", default="b64_json",
                        choices=["url", "b64_json"],
                        help="返回格式 (默认 b64_json，直接保存本地)")
    parser.add_argument("--api-key", "-k", default=None,
                        help="API Key (也可用环境变量 SENSENOVA_API_KEY 或 .env 文件)")
    parser.add_argument("--output", "-o", default=None,
                        help="输出目录 (默认为脚本所在目录)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="静默模式，只输出保存路径")

    args = parser.parse_args()

    api_key = get_api_key(args)
    size = resolve_size(args.size)
    # 默认输出到 images 子目录
    output_dir = Path(args.output) if args.output else (SCRIPT_DIR / "images")
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = generate_image(
        api_key=api_key,
        prompt=args.prompt,
        size=size,
        n=args.n,
        response_format=args.format,
        output_dir=output_dir,
        quiet=args.quiet,
    )

    # 输出结果（agent 可解析）
    result = {
        "success": True,
        "count": len(paths),
        "paths": paths,
        "prompt": args.prompt,
        "size": size,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()