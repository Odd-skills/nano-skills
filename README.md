# 🛠️ Nano Skills

> 一个轻量级的 AI Agent 技能库，为 AI 助手提供可扩展的专业能力。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 简介

**Nano Skills** 是一套专为 AI Agent（如 Claude、Cursor、Gemini CLI 等）设计的技能模块集合。每个技能都是一个独立的、可插拔的功能单元，让 AI 助手能够快速获得某个领域的专业能力。

### 设计理念

- **🎯 专注**：每个技能只做一件事，并把它做好
- **📦 独立**：技能之间相互独立，按需加载
- **🔧 可扩展**：标准化的结构，易于添加新技能
- **📚 自文档化**：每个技能包含完整的使用说明

## 📁 项目结构

```
nano-skills/
├── AGENTS.md                 # AI Agent 配置文件
├── LICENSE                   # MIT 许可证
├── README.md                 # 本文件
└── image-gen-skill/          # 图片生成技能
    ├── SKILL.md              # 技能说明文档
    ├── scripts/              # 执行脚本
    │   ├── generate.py       # 主生成脚本
    │   └── config.py         # 配置管理
    ├── assets/               # 静态资源
    │   └── prompt-templates.md
    └── references/           # 参考文档
        └── api-examples.md
```

## 🚀 快速开始

### 前置要求

- Python 3.8+
- 一个支持 OpenAI 兼容格式的图片生成 API

### 安装

```bash
# 克隆仓库
git clone https://github.com/Odd-skills/nano-skills.git
cd nano-skills

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install httpx -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 配置

设置环境变量：

```bash
export IMAGE_API_BASE="http://your-api-endpoint/v1"
export IMAGE_API_KEY="your-api-key"
export IMAGE_MODEL="gemini-3-pro-preview"  # 可选
```

### 使用示例

```bash
# 文生图
python image-gen-skill/scripts/generate.py --mode text --prompt "一只戴帽子的可爱猫咪"

# 图生图
python image-gen-skill/scripts/generate.py --mode i2i --prompt "转为卡通风格" --image photo.jpg

# 多图融合
python image-gen-skill/scripts/generate.py --mode multi --prompt "融合风格" --images style.jpg,content.jpg
```

## 📦 可用技能

### 🖼️ Image Generation Skill

**描述**：通过 OpenAI 兼容的 API 生成图片，支持文生图、图生图、多图融合。

**适用场景**：
- 原型图设计（移动端/Web 界面）
- SVG 图标生成
- Logo 设计
- 照片风格转换
- 场景修改与合成

**功能矩阵**：

| 模式 | 输入 | 输出 |
|------|------|------|
| 文生图 | 文字描述 | 生成图片 |
| 图生图 | 文字 + 1张图片 | 转换后图片 |
| 多图融合 | 文字 + 多张图片 | 融合图片 |

详细文档：[image-gen-skill/SKILL.md](./image-gen-skill/SKILL.md)

## 🤖 AI Agent 集成

### 在 AI Agent 中使用

本技能库支持多种 AI Agent 系统自动加载。AI 助手可以通过读取 `AGENTS.md` 文件了解可用技能，并按需调用。

**调用方式**：
```bash
# AI 助手内部调用
openskills read image-gen-skill
```

### 支持的 AI 平台

- ✅ Claude (via MCP)
- ✅ Cursor
- ✅ Gemini CLI / Canvas
- ✅ 其他支持 Agent Protocol 的平台

## 🔧 开发指南

### 添加新技能

1. 创建技能目录：
```bash
mkdir -p my-new-skill/{scripts,assets,references}
```

2. 创建 `SKILL.md` 文件，遵循以下格式：
```markdown
---
name: 技能名称
description: 技能简要描述
---

# 技能名称

详细的使用说明...
```

3. 在 `AGENTS.md` 中注册新技能

### 技能结构规范

每个技能应包含：

| 文件/目录 | 必需 | 说明 |
|-----------|------|------|
| `SKILL.md` | ✅ | 技能说明文档 |
| `scripts/` | ✅ | 可执行脚本 |
| `assets/` | ⬜ | 静态资源（模板、配置等） |
| `references/` | ⬜ | 参考文档和示例 |

## 📄 许可证

本项目采用 [MIT 许可证](./LICENSE)。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Odd-skills">Odd-skills</a>
</p>
