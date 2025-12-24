#!/usr/bin/env python3
"""
Image Generation Skill - Main Generation Script

支持文生图、图生图、多图融合，默认使用流式响应。
"""

import argparse
import base64
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

from config import Config


def get_client() -> OpenAI:
    """获取 OpenAI 客户端"""
    return OpenAI(
        base_url=Config.API_BASE,
        api_key=Config.API_KEY,
    )


def encode_image(image_path: str) -> str:
    """将图片文件编码为 base64"""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # 检测 MIME 类型
    suffix = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(suffix, "image/png")
    
    with open(path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode()
    
    return f"data:{mime_type};base64,{b64_data}"


def text_to_image(prompt: str, model: str = None, stream: bool = None) -> str:
    """
    文生图：根据文字描述生成图片
    
    Args:
        prompt: 图片描述
        model: 模型名称（可选）
        stream: 是否流式输出（可选）
    
    Returns:
        包含 Markdown 图片的响应文本
    """
    client = get_client()
    model = model or Config.DEFAULT_MODEL
    stream = stream if stream is not None else Config.STREAM
    
    messages = [{"role": "user", "content": prompt}]
    
    if stream:
        return _stream_response(client, model, messages)
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content


def image_to_image(prompt: str, image_path: str, model: str = None, stream: bool = None) -> str:
    """
    图生图：基于现有图片进行风格转换或场景修改
    
    Args:
        prompt: 转换指令
        image_path: 输入图片路径
        model: 模型名称（可选）
        stream: 是否流式输出（可选）
    
    Returns:
        包含 Markdown 图片的响应文本
    """
    client = get_client()
    model = model or Config.DEFAULT_MODEL
    stream = stream if stream is not None else Config.STREAM
    
    image_url = encode_image(image_path)
    
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
    }]
    
    if stream:
        return _stream_response(client, model, messages)
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content


def multi_image_gen(prompt: str, image_paths: list[str], model: str = None, stream: bool = None) -> str:
    """
    多图融合：结合多张图片生成新图片
    
    Args:
        prompt: 融合指令
        image_paths: 输入图片路径列表
        model: 模型名称（可选）
        stream: 是否流式输出（可选）
    
    Returns:
        包含 Markdown 图片的响应文本
    """
    client = get_client()
    model = model or Config.DEFAULT_MODEL
    stream = stream if stream is not None else Config.STREAM
    
    content = [{"type": "text", "text": prompt}]
    for path in image_paths:
        image_url = encode_image(path)
        content.append({"type": "image_url", "image_url": {"url": image_url}})
    
    messages = [{"role": "user", "content": content}]
    
    if stream:
        return _stream_response(client, model, messages)
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content


def _stream_response(client: OpenAI, model: str, messages: list) -> str:
    """
    处理流式响应
    
    Args:
        client: OpenAI 客户端
        model: 模型名称
        messages: 消息列表
    
    Returns:
        完整的响应文本
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    full_content = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_content += content
    
    print()  # 换行
    return full_content


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Image Generation Skill - 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文生图
  python generate.py --mode text --prompt "一只戴帽子的猫"
  
  # 图生图
  python generate.py --mode i2i --prompt "转为卡通风格" --image photo.jpg
  
  # 多图融合
  python generate.py --mode multi --prompt "融合风格" --images style.jpg,content.jpg
        """
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["text", "i2i", "multi"],
        required=True,
        help="生成模式: text=文生图, i2i=图生图, multi=多图融合"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="图片描述或转换指令"
    )
    parser.add_argument(
        "--image", "-i",
        help="输入图片路径（图生图模式）"
    )
    parser.add_argument(
        "--images",
        help="多张图片路径，逗号分隔（多图融合模式）"
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"模型名称（默认: {Config.DEFAULT_MODEL}）"
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="禁用流式输出"
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="打印当前配置"
    )
    
    args = parser.parse_args()
    
    if args.config:
        Config.print_config()
        return
    
    stream = not args.no_stream
    
    try:
        if args.mode == "text":
            result = text_to_image(args.prompt, model=args.model, stream=stream)
        
        elif args.mode == "i2i":
            if not args.image:
                parser.error("图生图模式需要 --image 参数")
            result = image_to_image(args.prompt, args.image, model=args.model, stream=stream)
        
        elif args.mode == "multi":
            if not args.images:
                parser.error("多图融合模式需要 --images 参数")
            image_list = [p.strip() for p in args.images.split(",")]
            result = multi_image_gen(args.prompt, image_list, model=args.model, stream=stream)
        
        if not stream:
            print(result)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
