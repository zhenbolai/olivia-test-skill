"""
店小秘店铺业绩统计 - 30天店铺分析（修复版）
"""

import subprocess
import time
import json
from datetime import datetime, timedelta


def open_url_in_chrome(url):
    cmd = ['osascript', '-e', 
           'tell application "Google Chrome" to open location "' + url + '"']
    subprocess.run(cmd)


def parse_money(money_str):
    if not money_str:
        return 0
    money_str = money_str.replace('$', '').replace(',', '').strip()
    try:
        return float(money_str)
    except:
        return 0


def analyze_stores():
    """分析30天所有店铺业绩"""
    
    print("="*60)
    print("店小秘 30天店铺业绩分析")
    print("="*60)
    
    target_url = "https://www.dianxiaomi.com/web/stat/storePerformance"
    open_url_in_chrome(target_url)
    
    print("等待页面加载...")
    time.sleep(25)
    
    # 先获取所有店铺列表
    print("获取店铺列表...")
    
    js_stores = '''(function() {
        var container = document.querySelectorAll(".d-checkbox-group-wrapper")[1];
        if(!container) return "[]";
        
        var labels = container.querySelectorAll("label");
        var stores = [];
        
        for(var i=1; i<labels.length; i++) {
            var text = labels[i].textContent.trim();
            if(text) stores.push(text);
        }
        
        return JSON.stringify(stores);
    })();'''
    
    js_escaped = js_stores.replace('"', '\\"')
    
    result = subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    try:
        stores = json.loads(result.stdout.strip())
    except:
        stores = []
    
    print(f"发现 {len(stores)} 个店铺")
    
    if not stores:
        return "未找到店铺"
    
    # 收集所有店铺的数据
    all_stores_data = []
    
    # 分析所有店铺
    # 先点击"30天内"按钮
    print("点击 30天内 按钮...")
    js_30days = '''(function() {
        var btns = document.querySelectorAll(".ant-radio-button-wrapper");
        for(var i=0; i<btns.length; i++) {
            if(btns[i].textContent.includes("30天内")) {
                btns[i].click();
                return "clicked 30天内";
            }
        }
        return "30天内 not found";
    })();'''
    
    js_escaped = js_30days.replace('"', '\\"')
    subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
        capture_output=True, text=True, timeout=30
    )
    time.sleep(15)
    
    for i, store in enumerate(stores[:5]):
        print(f"\n正在分析: {store} ({i+1}/{len(stores)})...")
        
        # 筛选店铺 - 分步执行确保成功
        # 第一步：取消全选
        js_uncheck = '''(function() {
            var containers = document.querySelectorAll(".d-checkbox-group-wrapper");
            var container = containers[1];
            if(!container) return "no container";
            
            var labels = container.querySelectorAll("label");
            if(labels[0].querySelector("input").checked) {
                labels[0].click();
            }
            return "unchecked";
        })();'''
        
        js_escaped = js_uncheck.replace('"', '\\"')
        subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True, text=True, timeout=30
        )
        
        time.sleep(2)
        
        # 第二步：选择指定店铺
        # 提取店铺名称的主要部分（如 "20" 从 "20（速卖通）"）
        store_key = store.split("（")[0].split("（")[0].strip()
        
        js_check = f'''(function() {{
            var containers = document.querySelectorAll(".d-checkbox-group-wrapper");
            var container = containers[1];
            if(!container) return "no container";
            
            var labels = container.querySelectorAll("label");
            var found = false;
            
            for(var j=0; j<labels.length; j++) {{
                var text = labels[j].textContent.trim();
                if(text.includes("{store_key}")) {{
                    labels[j].click();
                    found = true;
                    return "selected: " + text;
                }}
            }}
            return "not found: {store_key}";
        }})();'''
        
        js_escaped = js_check.replace('"', '\\"')
        
        result = subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True, text=True, timeout=30
        )
        
        print(f"  选择结果: {result.stdout.strip()}")
        
        # 等待数据刷新 - 增加等待时间确保数据加载完成
        time.sleep(25)
        
        # 第三步：获取数据
        js_data = '''(function() {
            var rows = document.querySelectorAll('tr.vxe-body--row');
            var result = [];
            for(var i=0; i<Math.min(rows.length, 35); i++) {
                var cells = rows[i].querySelectorAll('td');
                if(cells.length >= 11) {
                    result.push({
                        "日期": cells[0].textContent.trim(),
                        "订单量": cells[2].textContent.trim(),
                        "付款总金额": cells[4].textContent.trim(),
                        "退款金额": cells[7].textContent.trim()
                    });
                }
            }
            return JSON.stringify(result);
        })();'''
        
        js_escaped = js_data.replace('"', '\\"')
        
        result = subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True, text=True, timeout=30
        )
        
        try:
            data = json.loads(result.stdout.strip())
        except:
            data = []
        
        # 汇总30天数据
        total_orders = 0
        total_payment = 0
        total_refund = 0
        
        for item in data:
            if item.get("日期") == "合计":
                continue
            try:
                total_orders += int(item.get("订单量", "0").replace(',', ''))
            except:
                pass
            total_payment += parse_money(item.get("付款总金额", "$0"))
            total_refund += parse_money(item.get("退款金额", "$0"))
        
        print(f"  数据: 订单={total_orders}, 付款=${total_payment:.2f}, 退款=${total_refund:.2f}")
        
        if total_orders > 0 or total_payment > 0:
            all_stores_data.append({
                "store": store,
                "orders": total_orders,
                "payment": total_payment,
                "refund": total_refund,
                "net": total_payment - total_refund
            })
    
    if not all_stores_data:
        return "未获取到数据"
    
    # 按付款金额排序
    all_stores_data.sort(key=lambda x: x["payment"], reverse=True)
    
    # 输出结果
    best_store = all_stores_data[0]
    worst_store = all_stores_data[-1]
    
    output = f"""
📊 30天店铺业绩分析 (约 2026-02-01 ~ 03-02)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 业绩最佳店铺: {best_store['store']}
   📦 订单量: {best_store['orders']:,}
   💰 付款: ${best_store['payment']:,.2f}
   💸 退款: ${best_store['refund']:,.2f}
   💵 净收入: ${best_store['net']:,.2f}

⚠️ 业绩最差店铺: {worst_store['store']}
   📦 订单量: {worst_store['orders']:,}
   💰 付款: ${worst_store['payment']:,.2f}
   💸 退款: ${worst_store['refund']:,.2f}
   💵 净收入: ${worst_store['net']:,.2f}

📋 店铺排名 (按付款金额):
"""
    
    for i, s in enumerate(all_stores_data[:10]):
        output += f"{i+1}. {s['store']}: ${s['payment']:,.2f} (订单 {s['orders']:,})\n"
    
    # 计算总计
    total_orders_all = sum(s["orders"] for s in all_stores_data)
    total_payment_all = sum(s["payment"] for s in all_stores_data)
    total_refund_all = sum(s["refund"] for s in all_stores_data)
    
    output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 总计:
   📦 订单量: {total_orders_all:,}
   💰 付款: ${total_payment_all:,.2f}
   💸 退款: ${total_refund_all:,.2f}
   💵 净收入: ${total_payment_all - total_refund_all:,.2f}
"""
    
    return output


if __name__ == "__main__":
    import sys
    result = analyze_stores()
    print(result)
