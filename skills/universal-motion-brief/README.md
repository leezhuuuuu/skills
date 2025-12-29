# Universal Motion Brief Skill

> **Source**: This skill is derived from [anthropics/skills PR #170](https://github.com/anthropics/skills/pull/170) by @TylerALofall.

为 pro se litigants（自行诉讼者）生成符合法庭要求的法律文书。

## 功能

| 功能 | 描述 |
|------|------|
| **文书类型** | 动议、答辩状、法律意见书等 |
| **司法管辖区** | 第九巡回法院、联邦地区法院等 |
| **格式检查** | 字体、行距、边距、页数限制 |
| **模板生成** | 基于 JSON 数据的文档生成 |

## 安装

```bash
pip install python-docx
```

## 快速使用

```python
from legal_document_generator import generate_motion

motion = generate_motion(
    template="opening_brief",
    jurisdiction="ninth_circuit",
    data={...}
)
motion.save("motion.docx")
```

## 文档类型

- **Motion** - 向法院提出请求
- **Brief** - 法律论据文书
- **Opposition** - 对动议的回应
- **Reply** - 对反对意见的回复
- **Stipulation** - 双方协议

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。

## 资源

- [第九巡回法院规则](https://www.ca9.uscourts.gov/rules)
- [联邦民事诉讼规则](https://www.uscourts.gov/rules-policies/current-federal-rules-civil-procedure)
