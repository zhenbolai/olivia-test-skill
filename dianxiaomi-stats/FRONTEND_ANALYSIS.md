# 店小秘前端代码分析

## 页面 URL
https://www.dianxiaomi.com/web/stat/storePerformance

## 关键元素

### 1. 数据表格 (table)
```javascript
// 选择器
document.querySelectorAll('tr.vxe-body--row')
// 或
document.querySelectorAll('.vxe-table--body-wrapper tbody tr')

// 表格列对应关系
{
  "日期": 'td[colid="col_1"]',
  "客户数": 'td[colid="col_2"]',
  "订单量": 'td[colid="col_3"]',
  "下单总金额": 'td[colid="col_4"]',
  "付款总金额": 'td[colid="col_5"]',
  "付款订单数": 'td[colid="col_6"]',
  "付款客户数": 'td[colid="col_7"]',
  "退款金额": 'td[colid="col_8"]',
  "退款订单数": 'td[colid="col_9"]',
  "退款客户数": 'td[colid="col_10"]',
  "客单价": 'td[colid="col_11"]'
}
```

### 2. 筛选条件

#### 平台渠道 (Platform)
```javascript
// 选择器
document.querySelectorAll('.d-checkbox-group-wrapper label')

// 选项
- 全部 (checkbox)
- 速卖通 (checkbox)
- 其它 (checkbox)

// 获取选中状态
document.querySelector('label:has(input[checked])')
```

#### 店铺账号 (Store) - 已验证可用
```javascript
// 店铺区域容器
var container = document.querySelectorAll(".d-checkbox-group-wrapper")[1];

// 获取所有店铺label
var labels = container.querySelectorAll("label");

// 取消全选
if(labels[0].querySelector("input").checked) {
    labels[0].click();
}

// 选择指定店铺 (例如 27店)
for(var i=0; i<labels.length; i++) {
    if(labels[i].textContent.includes("27店")) {
        labels[i].click();
        break;
    }
}

// 获取当前选中的店铺
var selected = [];
for(var i=0; i<labels.length; i++) {
    if(labels[i].querySelector("input").checked) {
        selected.push(labels[i].textContent.trim());
    }
}
selected.join(", ");
- 6店（速卖通）
- 9店（速卖通）
- 12店（速卖通）
- 27店（速卖通）
- 17店（速卖通）
- 19 店（速卖通）
- 28（速卖通）
- 14（速卖通）
- 29店（速卖通）
- 1店（速卖通）
- 11（速卖通）
- 13（速卖通）
- 20（速卖通）
- 23（速卖通）
- 24（速卖通）
- 25（速卖通）
- 26（速卖通）
- 2（速卖通）
- 3（速卖通）
- 4（速卖通）
- 5（速卖通）
- 7（速卖通）
- 8（速卖通）
- 10（速卖通）
- 16（速卖通）
- 18（速卖通）
- 21（速卖通）
- 22（速卖通）
- 30（速卖通）
- 31（速卖通）
- 32（速卖通）
- 35（速卖通）
- 33（速卖通）
- 34（速卖通）
- 36（速卖通）
- 37（速卖通）
- 38（速卖通）
- 手工订单（其它）
```

### 3. 时间筛选
```javascript
// 时间快捷选项
- 昨天 (cursor: pointer)
- 7天内 (cursor: pointer)
- 30天内 (cursor: pointer)

// 日期输入框
开始日期: input[placeholder="开始日期"]
结束日期: input[placeholder="结束日期"]
```

### 4. 功能按钮
```javascript
// 导出报表
button:contains("导出报表")

// 币种选择
combobox (USD)
```

### 5. 分页
```javascript
// 每页显示
30条/页

// 分页信息
第1-30条，共30条记录
```

## 获取数据的 JavaScript 代码

```javascript
// 获取表格数据
const data = JSON.stringify(Array.from(document.querySelectorAll('tr.vxe-body--row')).map(function(row) {
    return {
        "日期": row.querySelector('td[colid="col_1"] .vxe-cell--label')?.textContent.trim(),
        "客户数": row.querySelector('td[colid="col_2"] .vxe-cell--label')?.textContent.trim(),
        "订单量": row.querySelector('td[colid="col_3"] .vxe-cell--label')?.textContent.trim(),
        "下单总金额": row.querySelector('td[colid="col_4"] .vxe-cell--label')?.textContent.trim(),
        "付款总金额": row.querySelector('td[colid="col_5"] .vxe-cell--label')?.textContent.trim(),
        "付款订单数": row.querySelector('td[colid="col_6"] .vxe-cell--label')?.textContent.trim(),
        "付款客户数": row.querySelector('td[colid="col_7"] .vxe-cell--label')?.textContent.trim(),
        "退款金额": row.querySelector('td[colid="col_8"] .vxe-cell--label')?.textContent.trim(),
        "退款订单数": row.querySelector('td[colid="col_9"] .vxe-cell--label')?.textContent.trim(),
        "退款客户数": row.querySelector('td[colid="col_10"] .vxe-cell--label')?.textContent.trim(),
        "客单价": row.querySelector('td[colid="col_11"] .vxe-cell--label')?.textContent.trim()
    };
}));
```

## 常用操作

### 1. 点击"昨天"按钮
```javascript
document.querySelector('div:has-text("昨天")').click()
```

### 2. 筛选特定店铺
```javascript
// 点击速卖通checkbox
document.querySelector('label:has-text("速卖通") input').click()
```

### 3. 获取汇总数据
```javascript
// 页面顶部汇总
{
    "客户数": document.querySelector('.ant-card .ant-statistic-content-value')?.textContent,
    "订单量": ...
    "付款总金额": ...
}
```
