"""
Image Generation Skill - Configuration Module

统一管理 API 配置，支持环境变量覆盖。
"""

import os


class Config:
    """图片生成 API 配置"""
    
    # API 端点
    API_BASE: str = os.getenv("IMAGE_API_BASE", "https://nano.shunleite.com/v1")
    
    # API 密钥
    API_KEY: str = os.getenv("IMAGE_API_KEY", "default-key")
    
    # 默认模型
    DEFAULT_MODEL: str = os.getenv("IMAGE_MODEL", "gemini-3-pro-preview")
    
    # 输出模式: url | base64
    OUTPUT_MODE: str = os.getenv("IMAGE_OUTPUT_MODE", "base64")
    
    # 是否启用流式响应
    STREAM: bool = os.getenv("IMAGE_STREAM", "true").lower() == "true"
    
    @classmethod
    def to_dict(cls) -> dict:
        """返回配置字典"""
        return {
            "api_base": cls.API_BASE,
            "api_key": cls.API_KEY[:8] + "..." if len(cls.API_KEY) > 8 else "***",
            "model": cls.DEFAULT_MODEL,
            "output_mode": cls.OUTPUT_MODE,
            "stream": cls.STREAM,
        }
    
    @classmethod
    def print_config(cls):
        """打印当前配置"""
        print("=== Image Generation Config ===")
        for k, v in cls.to_dict().items():
            print(f"  {k}: {v}")
        print("=" * 32)


if __name__ == "__main__":
    Config.print_config()
