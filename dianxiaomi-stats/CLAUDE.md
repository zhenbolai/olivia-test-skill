# 店小秘业绩统计 Skill

## 概述

这个 skill 用于获取店小秘 ERP 的店铺业绩统计数据。

## 使用方法

### 运行脚本获取数据

```bash
# 获取全部店铺数据
python3 /Users/lzb/.openclaw/skills/skills/lzb/dianxiaomi-stats/get_dianxiaomi_stats.py

# 获取指定店铺数据
python3 /Users/lzb/.openclaw/skills/skills/lzb/dianxiaomi-stats/get_dianxiaomi_stats.py "27店"
```

脚本会自动：
1. 启动 Chrome 浏览器
2. 打开店小秘店铺业绩页面
3. 获取数据并输出

## 首次使用

1. 首次运行时，Chrome 会提示登录店小秘
2. 登录一次后，登录状态会保存在 Chrome 用户数据中
3. 后续运行无需再次登录

## 可用店铺列表

部分店铺：
- 6店（速卖通）
- 9店（速卖通）
- 12店（速卖通）
- 27店（速卖通）
- 1店（速卖通）
- 等等...

## 输出示例

```json
[
  {
    "店铺账号": "全部",
    "日期": "合计",
    "订单量": "2416",
    "付款金额": "$160289.65"
  },
  {
    "店铺账号": "全部",
    "日期": "2026-03-01",
    "订单量": "81",
    "付款金额": "$5042.83"
  }
]
```

## 注意事项

- 使用现有的 Chrome 用户数据目录保持登录状态
- 数据来源于店小秘 ERP 的"店铺业绩"页面
