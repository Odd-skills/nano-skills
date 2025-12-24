# API 使用示例

详细的 API 调用示例，涵盖所有支持的图片生成场景。

## 文生图 (Text-to-Image)

### curl 示例

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-enterprise",
    "messages": [
      {"role": "user", "content": "生成一张日落时分的海滩图片，有椰子树和沙滩"}
    ],
    "stream": true
  }'
```

### Python 示例

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="your-key"
)

response = client.chat.completions.create(
    model="gemini-enterprise",
    messages=[{"role": "user", "content": "一只戴帽子的可爱猫咪"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## 图生图 (Image-to-Image)

### curl 示例

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-enterprise",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "将这张图片转换成卡通风格"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
      ]
    }],
    "stream": true
  }'
```

### Python 示例

```python
import base64
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="your-key"
)

# 读取图片
with open("photo.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gemini-enterprise",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "将这张图片转换成油画风格"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]
    }],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## 多图融合 (Multi-Image Fusion)

### Python 示例

```python
import base64
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="your-key"
)

# 读取风格图和内容图
with open("style.jpg", "rb") as f:
    style_b64 = base64.b64encode(f.read()).decode()
with open("content.jpg", "rb") as f:
    content_b64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gemini-enterprise",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "使用第一张图片的风格，重新绘制第二张图片的内容"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{style_b64}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{content_b64}"}}
        ]
    }],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## 常见转换场景

| 场景 | Prompt 示例 |
|------|-------------|
| 风格转换 | "将图片转换成油画/水彩/卡通/素描风格" |
| 场景修改 | "将背景改为海滩/森林/城市夜景" |
| 添加元素 | "在图片中添加一只猫/彩虹/雪花效果" |
| 移除元素 | "移除图片中的人物/背景/水印" |
| 颜色调整 | "将图片改为黑白/复古色调/高对比度" |
| 扩展画面 | "扩展图片的右侧区域，保持风格一致" |

---

## 响应格式

### URL 模式（默认）

```
我已经为您生成了这张图片。

http://127.0.0.1:8000/image/gemini_20241216_180000_a1b2c3d4.png
```

### Base64 模式

```
我已经为您生成了这张图片。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...)
```
