"""
店小秘店铺业绩统计 - 支持指定店铺和指定日期查询
"""

import subprocess
import time
import json
from datetime import datetime, timedelta


def open_url_in_chrome(url):
    """使用 AppleScript 在 Chrome 中打开 URL"""
    cmd = ['osascript', '-e', 
           'tell application "Google Chrome" to open location "' + url + '"']
    subprocess.run(cmd)


def get_store_stats(store_name=None, date_str=None, wait_seconds=20):
    """获取指定店铺和指定日期的业绩数据"""
    print("正在打开店小秘...")
    
    target_url = "https://www.dianxiaomi.com/web/stat/storePerformance"
    open_url_in_chrome(target_url)

    print(f"已在 Chrome 中打开: {target_url}")
    print(f"等待 {wait_seconds} 秒让页面加载...")

    time.sleep(wait_seconds)
    
    # 如果指定了店铺，先筛选
    if store_name and store_name != "全部":
        print(f"正在筛选店铺: {store_name}...")
        
        # 第一步：取消全选
        js_uncheck = '''(function() {
            var containers = document.querySelectorAll(".d-checkbox-group-wrapper");
            var container = containers[1];
            if(!container) return "container not found";
            
            var labels = container.querySelectorAll("label");
            var allLabel = labels[0];
            
            var checkbox = allLabel.querySelector("input");
            if(checkbox && checkbox.checked) {
                allLabel.click();
                return "unchecked all";
            }
            return "already unchecked";
        })();'''
        
        js_escaped = js_uncheck.replace('"', '\\"')
        
        result = subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"取消全选: {result.stdout.strip()}")
        time.sleep(2)
        
        # 第二步：选择指定店铺
        js_check = f'''(function() {{
            var containers = document.querySelectorAll(".d-checkbox-group-wrapper");
            var container = containers[1];
            if(!container) return "container not found";
            
            var labels = container.querySelectorAll("label");
            
            for(var i=0; i<labels.length; i++) {{
                var text = labels[i].textContent.trim();
                if(text.includes("{store_name}")) {{
                    labels[i].click();
                    return "selected: " + text;
                }}
            }}
            return "not found: {store_name}";
        }})();'''
        
        js_escaped = js_check.replace('"', '\\"')
        
        result = subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"选择店铺: {result.stdout.strip()}")
        
        # 等待数据刷新
        print("等待数据刷新...")
        time.sleep(15)
    
    # 如果指定了日期，设置日期筛选
    if date_str:
        print(f"正在设置日期: {date_str}...")
        # 日期格式: 2026-02-28
        js_date = f'''(function() {{
            // 找到日期输入框
            var startInput = document.querySelector('input[placeholder="开始日期"]');
            var endInput = document.querySelector('input[placeholder="结束日期"]');
            
            if(startInput && endInput) {{
                // 设置开始日期
                startInput.value = "{date_str}";
                startInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                startInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                
                // 设置结束日期
                endInput.value = "{date_str}";
                endInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                endInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                
                return "date set: {date_str}";
            }}
            return "date input not found";
        }})();'''
        
        js_escaped = js_date.replace('"', '\\"')
        
        result = subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"设置日期: {result.stdout.strip()}")
        
        # 等待数据刷新
        print("等待数据刷新...")
        time.sleep(10)
    
    print("正在获取数据...")

    # 获取数据
    js_code = '''(function() {
        var rows = document.querySelectorAll('tr.vxe-body--row');
        var result = [];
        for(var i=0; i<Math.min(rows.length, 10); i++) {
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

    js_escaped = js_code.replace('"', '\\"')

    result = subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        return f"获取数据失败: {result.stderr}"

    try:
        data = json.loads(result.stdout.strip())
    except:
        return f"解析数据失败: {result.stdout[:200]}"

    if not data:
        return "未找到数据"

    print(f"共获取 {len(data)} 条数据")
    
    # 打印数据
    for i, item in enumerate(data):
        print(f"  行{i}: {item}")
    
    # 查找指定日期的数据
    target_date = date_str if date_str else (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    target_data = None
    
    for item in data:
        date = item.get("日期", "")
        if date == target_date:
            target_data = item
            break
    
    # 如果没找到，尝试第一行
    if not target_data and len(data) >= 1:
        target_data = data[0]

    if target_data:
        orders = target_data.get("订单量", "0")
        payment = target_data.get("付款总金额", "$0")
        refund = target_data.get("退款金额", "$0")
        
        date_display = target_data.get("日期", "")
        
        store_display = store_name if store_name else "全部店铺"
        
        output = f"""📊 {store_display} 业绩 ({date_display})
━━━━━━━━━━━━━━━━━━━
📦 订单量: {orders}
💰 付款金额: {payment}
💸 退款金额: {refund}
━━━━━━━━━━━━━━━━━━━"""
        
        return output
    else:
        return "未找到数据"


if __name__ == "__main__":
    import sys
    
    print("="*50)
    print("店小秘店铺业绩统计")
    print("="*50)
    print("用法:")
    print("  python3 get_store_stats.py                    # 查询全部店铺昨日")
    print("  python3 get_store_stats.py 20               # 查询20店昨日")
    print("  python3 get_store_stats.py 20 2026-02-28      # 查询20店 2月28日")
    print("="*50)
    
    store_name = None
    date_str = None
    
    if len(sys.argv) > 1:
        store_name = sys.argv[1]
    if len(sys.argv) > 2:
        date_str = sys.argv[2]
    
    if store_name and date_str:
        print(f"查询店铺: {store_name}, 日期: {date_str}")
    elif store_name:
        print(f"查询店铺: {store_name}")
    else:
        print("查询全部店铺昨日数据")
    
    result = get_store_stats(store_name, date_str)
    print(result)
