---
name: dianxiaomi-stats
description: >
  店小秘店铺业绩统计工具。通过 Chrome 浏览器获取店小秘 ERP 的店铺业绩数据。
  用于：(1) 查询店铺销售数据，(2) 获取订单量和付款金额，(3) 追踪每日业绩趋势。
  支持获取全部店铺或指定单个店铺的数据。
  注意：需要 Chrome 已登录店小秘。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "bins": ["python3"],
            "pip": ["playwright"],
          },
        "install":
          [
            {
              "kind": "pip",
              "package": "playwright",
              "label": "pip install playwright && playwright install chromium",
            },
          ],
      },
  }
---

# 店小秘店铺业绩统计

通过 Chrome 浏览器获取店小秘 ERP 的店铺业绩数据。

## 前置要求

1. 安装 Playwright：
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. 在 Chrome 中登录店小秘（只需要登录一次，后续会自动保持登录状态）

## 使用方法

### 获取全部店铺数据

```bash
python3 /path/to/dianxiaomi_stats.py
```

### 获取指定店铺数据

```bash
python3 /path/to/dianxiaomi_stats.py "27店"
python3 /path/to/dianxiaomi_stats.py "6店"
```

## 输出字段

- **店铺账号**: 店铺名称
- **日期**: 统计数据日期
- **订单量**: 订单数量
- **付款金额**: 付款金额（美元）

## 注意事项

- 使用现有的 Chrome 用户数据目录以保持登录状态
- 脚本会自动启动 Chrome 并打开店小秘页面
- 数据来源于店小秘 ERP 的"店铺业绩"页面
