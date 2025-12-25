# 🛠️ Nano Skills

> 一个轻量级的 AI Agent 技能库，为 AI 助手提供可扩展的专业能力。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-v2.0.12+-blueviolet)](https://claude.ai)

## 📖 简介

**Nano Skills** 是一套专为 AI Agent（如 Claude、Cursor、Gemini CLI 等）设计的技能模块集合。每个技能都是一个独立的、可插拔的功能单元，让 AI 助手能够快速获得某个领域的专业能力。

### 设计理念

- **🎯 专注**：每个技能只做一件事，并把它做好
- **📦 独立**：技能之间相互独立，按需加载
- **🔧 可扩展**：标准化的结构，易于添加新技能
- **📚 自文档化**：每个技能包含完整的使用说明

## 🚀 快速安装

### 方式一：Claude Plugins CLI（推荐）

使用 `claude-plugins` CLI 工具一键安装：

```bash
npx claude-plugins install @Odd-skills/nano-skills
```

管理已安装的插件：

```bash
# 列出已安装插件
npx claude-plugins list

# 启用/禁用
npx claude-plugins enable nano-skills
npx claude-plugins disable nano-skills
```

### 方式二：手动安装 Skills

将技能目录复制到 Claude 的 skills 目录：

```bash
# 克隆仓库
git clone https://github.com/Odd-skills/nano-skills.git
cd nano-skills

# 安装单个技能（个人使用）
cp -r skills/image-gen-skill ~/.claude/skills/

# 或安装到项目（团队共享）
cp -r skills/image-gen-skill .claude/skills/
```

### 方式三：作为完整插件安装

```bash
# 克隆到 Claude 插件目录
git clone https://github.com/Odd-skills/nano-skills.git ~/.claude/plugins/nano-skills
```

## 📁 项目结构

```
nano-skills/
├── .claude-plugin/
│   └── plugin.json           # Claude Plugin 清单
├── skills/                    # 技能目录
│   └── image-gen-skill/       # 图片生成技能
│       ├── SKILL.md           # 技能定义文件
│       ├── scripts/           # 执行脚本
│       │   ├── generate.py    # 主生成脚本
│       │   └── config.py      # 配置管理
│       ├── assets/            # 静态资源
│       │   └── prompt-templates.md
│       └── references/        # 参考文档
│           └── api-examples.md
├── AGENTS.md                  # AI Agent 配置
├── LICENSE                    # MIT 许可证
└── README.md                  # 本文件
```

## 📦 可用技能

### 🖼️ image-generation

**描述**：通过 OpenAI 兼容的 API 生成图片，支持文生图、图生图、多图融合。

**触发条件**：当用户请求生成图片、设计 Logo、创建原型图、进行风格转换时自动激活。

**功能矩阵**：

| 模式 | 输入 | 输出 |
|------|------|------|
| 文生图 | 文字描述 | 生成图片 |
| 图生图 | 文字 + 1张图片 | 转换后图片 |
| 多图融合 | 文字 + 多张图片 | 融合图片 |

**适用场景**：
- 原型图设计（移动端/Web 界面）
- SVG 图标生成
- Logo 设计
- 照片风格转换
- 场景修改与合成

详细文档：[skills/image-gen-skill/SKILL.md](./skills/image-gen-skill/SKILL.md)

## ⚙️ 配置

### 环境变量

```bash
export IMAGE_API_BASE="http://your-api-endpoint/v1"
export IMAGE_API_KEY="your-api-key"
export IMAGE_MODEL="gemini-3-pro-preview"  # 可选
```

### 使用示例

```bash
# 文生图
python skills/image-gen-skill/scripts/generate.py --mode text --prompt "一只戴帽子的可爱猫咪"

# 图生图
python skills/image-gen-skill/scripts/generate.py --mode i2i --prompt "转为卡通风格" --image photo.jpg

# 多图融合
python skills/image-gen-skill/scripts/generate.py --mode multi --prompt "融合风格" --images style.jpg,content.jpg
```

## 🤖 AI Agent 集成

### Claude Code

本项目完全兼容 Claude Code 的插件和技能规范：

- **Plugin 格式**：包含 `.claude-plugin/plugin.json` 清单
- **Skills 格式**：每个技能遵循 `SKILL.md` 规范
- **自动发现**：Claude 会根据任务上下文自动决定是否使用技能

### 其他平台

| 平台 | 支持方式 |
|------|----------|
| ✅ Claude Code | 完整插件支持 |
| ✅ Cursor | 通过 AGENTS.md |
| ✅ Gemini CLI | 通过 AGENTS.md |
| ✅ GitHub Copilot | 通过 AGENTS.md |

## 🔧 开发指南

### 添加新技能

1. 创建技能目录：
```bash
mkdir -p skills/my-new-skill/{scripts,assets,references}
```

2. 创建 `SKILL.md` 文件：
```markdown
---
name: my-new-skill
description: 技能描述，说明何时应该使用此技能。
allowed-tools:
  - Bash
  - Read
  - Write
---

# My New Skill

详细的使用说明...

## Instructions

1. 步骤一
2. 步骤二

## Examples

示例使用场景...
```

3. 更新 `AGENTS.md` 注册新技能

### SKILL.md 规范

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | ✅ | 唯一标识符，小写 + 连字符，最长 64 字符 |
| `description` | ✅ | 技能描述和触发条件，最长 1024 字符 |
| `allowed-tools` | ⬜ | 限制可使用的工具列表 |

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
