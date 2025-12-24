---
name: Image Generation
description: 通过 OpenAI 兼容的 API 生成图片，支持文生图、图生图、多图融合。适用于原型图设计、SVG 设计、Logo 设计等场景。
---

# Image Generation Skill

通过 OpenAI 兼容格式的 API 进行智能图片生成与编辑。

## 功能概述

| 功能 | 描述 |
|------|------|
| 文生图 | 根据文字描述生成图片 |
| 图生图 | 基于现有图片进行风格转换或场景修改 |
| 多图融合 | 结合多张图片生成新图片 |

## 使用场景

- **原型图设计**：快速生成移动端/Web 界面原型
- **SVG 图标**：生成扁平化、单色图标
- **Logo 设计**：为品牌创建极简 Logo
- **风格转换**：油画、水彩、卡通、像素风格
- **场景修改**：替换背景、添加/移除元素

## 执行流程

### 1. 识别用户意图

根据用户输入判断生成模式：

| 输入类型 | 模式 |
|----------|------|
| 仅文字描述 | 文生图 (text-to-image) |
| 文字 + 1张图片 | 图生图 (image-to-image) |
| 文字 + 多张图片 | 多图融合 (multi-image) |

### 2. 构建请求

使用 OpenAI 兼容格式构建请求体：

**文生图：**
```json
{
  "model": "gemini-3-pro-preview",
  "messages": [{"role": "user", "content": "用户的描述"}],
  "stream": true
}
```

**图生图：**
```json
{
  "model": "gemini-3-pro-preview",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "转换指令"},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
    ]
  }],
  "stream": true
}
```

### 3. 调用脚本

执行 `scripts/generate.py` 发送请求：

```bash
# 文生图
python scripts/generate.py --mode text --prompt "描述内容"

# 图生图
python scripts/generate.py --mode i2i --prompt "转换指令" --image path/to/image.jpg

# 多图融合
python scripts/generate.py --mode multi --prompt "融合指令" --images style.jpg,content.jpg
```

### 4. 返回结果

解析响应并返回 Markdown 格式图片：
- **URL 模式**：`![image](http://...)`
- **Base64 模式**：`![image](data:image/png;base64,...)`

## 性能最佳实践

> [!TIP]
> AI 在使用本 Skill 时应优先采用**并发流式执行**以保证速度。

### 并发执行

当需要生成多张图片时，应**并行发起请求**而非串行等待：

```python
# ✅ 推荐：并发执行
import asyncio

async def generate_batch(prompts):
    tasks = [generate_image(p) for p in prompts]
    return await asyncio.gather(*tasks)

# ❌ 避免：串行执行
for prompt in prompts:
    result = generate_image(prompt)  # 阻塞等待
```

### 流式输出

始终启用 `stream: true` 以实时获取生成进度：

- 用户可以更早看到部分结果
- 减少感知的等待时间
- 支持中途取消长时间任务

```bash
# 流式调用（推荐）
python scripts/generate.py --mode text --prompt "..." --stream

# 非流式调用（仅在需要完整结果时使用）
python scripts/generate.py --mode text --prompt "..." --no-stream
```

---

## 配置参数

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `IMAGE_API_BASE` | API 端点 | `http://127.0.0.1:8000/v1` |
| `IMAGE_API_KEY` | API 密钥 | `default-key` |
| `IMAGE_MODEL` | 模型名称 | `gemini-3-pro-preview` |
| `IMAGE_OUTPUT_MODE` | 输出模式 (url/base64) | `url` |
| `IMAGE_STREAM` | 启用流式 | `true` |

## 快速示例

### 生成一只猫的图片
```
请帮我生成一只戴帽子的可爱猫咪
```

### 将照片转为卡通风格
```
将这张图片转换成卡通风格
[附上图片]
```

### 融合两张图片
```
使用第一张图片的风格，重新绘制第二张图片的内容
[附上风格图] [附上内容图]
```

## 提示词模板

详见 `assets/prompt-templates.md` 获取更多预设模板。

## 参考资料

- API 详细示例：`references/api-examples.md`
- 配置管理：`scripts/config.py`
