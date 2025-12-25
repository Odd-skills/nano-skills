# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: Bash("openskills read <skill-name>")
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<skill>
<name>image-generation</name>
<description>通过 OpenAI 兼容的 API 生成图片，支持文生图、图生图、多图融合。适用于原型图设计、SVG 设计、Logo 设计等场景。当用户请求生成图片、设计 Logo、创建原型图、进行风格转换时使用此技能。</description>
<location>skills/image-gen-skill</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
