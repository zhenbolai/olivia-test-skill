"""
店小秘店铺业绩统计 - 支持环比变化分析
"""

import subprocess
import time
import json
import re
from datetime import datetime, timedelta


def open_url_in_chrome(url):
    """使用 AppleScript 在 Chrome 中打开 URL"""
    cmd = ['osascript', '-e', 
           'tell application "Google Chrome" to open location "' + url + '"']
    subprocess.run(cmd)


def parse_money(money_str):
    """解析金额字符串为数字"""
    if not money_str:
        return 0
    # 移除 $ 和 , 
    money_str = money_str.replace('$', '').replace(',', '').strip()
    try:
        return float(money_str)
    except:
        return 0


def calculate_change(current, previous):
    """计算变化值和百分比"""
    if previous == 0:
        return 0, "N/A"
    
    diff = current - previous
    percent = (diff / previous) * 100
    
    return diff, percent


def format_money(amount):
    """格式化金额显示"""
    if amount >= 0:
        return f"${amount:,.2f}"
    else:
        return f"-${abs(amount):,.2f}"


def get_store_data(store_name=None, date_str=None, wait_seconds=15):
    """获取指定店铺和日期的数据"""
    
    target_url = "https://www.dianxiaomi.com/web/stat/storePerformance"
    open_url_in_chrome(target_url)

    print(f"等待 {wait_seconds} 秒让页面加载...")
    time.sleep(wait_seconds)
    
    # 如果指定了店铺，先筛选
    if store_name and store_name != "全部":
        print(f"正在筛选店铺: {store_name}...")
        
        # 取消全选
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
        
        subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        time.sleep(2)
        
        # 选择指定店铺
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
        
        subprocess.run(
            ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        time.sleep(10)
    
    # 获取数据
    js_code = '''(function() {
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

    js_escaped = js_code.replace('"', '\\"')

    result = subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        return None, f"获取数据失败: {result.stderr}"

    try:
        data = json.loads(result.stdout.strip())
    except:
        return None, f"解析数据失败: {result.stdout[:200]}"

    if not data:
        return None, "未找到数据"
    
    return data, None


def get_store_stats(store_name=None, date_str=None, show_change=True):
    """获取指定店铺和日期的业绩数据（含环比变化）"""
    
    print("="*60)
    print("店小秘店铺业绩统计 (含环比变化)")
    print("="*60)
    
    # 解析日期
    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        prev_date = target_date - timedelta(days=1)
        prev_date_str = prev_date.strftime("%Y-%m-%d")
    else:
        # 默认昨天
        target_date = datetime.now() - timedelta(days=1)
        target_date_str = target_date.strftime("%Y-%m-%d")
        prev_date = target_date - timedelta(days=1)
        prev_date_str = prev_date.strftime("%Y-%m-%d")
    
    print(f"查询日期: {target_date_str} (前一日: {prev_date_str})")
    
    # 获取当日数据
    print(f"\n正在获取 {target_date_str} 数据...")
    data, error = get_store_data(store_name, target_date_str)
    
    if error:
        return error
    
    # 解析当日数据
    current_data = None
    for item in data:
        if item.get("日期") == target_date_str:
            current_data = item
            break
    
    if not current_data and len(data) >= 2:
        current_data = data[1]  # 第二行是最新一天
    
    if not current_data:
        return f"未找到 {target_date_str} 的数据"
    
    # 解析前一日数据
    prev_data = None
    for item in data:
        if item.get("日期") == prev_date_str:
            prev_data = item
            break
    
    # 计算变化
    if current_data:
        current_orders = int(current_data.get("订单量", "0").replace(',', ''))
        current_payment = parse_money(current_data.get("付款总金额", "$0"))
        current_refund = parse_money(current_data.get("退款金额", "$0"))
        
        if prev_data:
            prev_orders = int(prev_data.get("订单量", "0").replace(',', ''))
            prev_payment = parse_money(prev_data.get("付款总金额", "$0"))
            prev_refund = parse_money(prev_data.get("退款金额", "$0"))
            
            # 计算变化
            orders_diff, orders_pct = calculate_change(current_orders, prev_orders)
            payment_diff, payment_pct = calculate_change(current_payment, prev_payment)
            refund_diff, refund_pct = calculate_change(current_refund, prev_refund)
        else:
            prev_orders = 0
            prev_payment = 0
            prev_refund = 0
            orders_diff, orders_pct = 0, 0
            payment_diff, payment_pct = 0, 0
            refund_diff, refund_pct = 0, 0
        
        # 格式化输出
        store_display = store_name if store_name else "全部店铺"
        
        # 确定符号和颜色
        def get_change_symbol(value):
            if value > 0:
                return "📈"
            elif value < 0:
                return "📉"
            else:
                return "➡️"
        
        orders_symbol = get_change_symbol(orders_diff)
        payment_symbol = get_change_symbol(payment_diff)
        refund_symbol = get_change_symbol(refund_diff)
        
        # 格式化百分比
        orders_pct_str = f"{orders_pct:+.2f}%" if isinstance(orders_pct, (int, float)) else orders_pct
        payment_pct_str = f"{payment_pct:+.2f}%" if isinstance(payment_pct, (int, float)) else payment_pct
        refund_pct_str = f"{refund_pct:+.2f}%" if isinstance(refund_pct, (int, float)) else refund_pct
        
        output = f"""
📊 {store_display} 业绩 ({target_date_str})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 订单量: {current_orders:,}
   {orders_symbol} {orders_diff:+,.0f} ({orders_pct_str})

💰 付款金额: {format_money(current_payment)}
   {payment_symbol} {format_money(payment_diff)} ({payment_pct_str})

💸 退款金额: {format_money(current_refund)}
   {refund_symbol} {format_money(refund_diff)} ({refund_pct_str})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 对比日期: {prev_date_str}
   (前一日: 订单量 {prev_orders:,}, 金额 {format_money(prev_payment)}, 退款 {format_money(prev_refund)})
"""
        
        return output
    
    return "未找到数据"


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("店小秘店铺业绩统计 (含环比变化)")
    print("="*60)
    print("用法:")
    print("  python3 get_store_stats.py                           # 昨日数据+环比")
    print("  python3 get_store_stats.py 20                        # 20店昨日+环比")
    print("  python3 get_store_stats.py 20 2026-02-28             # 20店2月28日+环比")
    print("  python3 get_store_stats.py 20 2026-02-28 --no-change  # 不显示环比")
    print("="*60)
    
    store_name = None
    date_str = None
    show_change = True
    
    for arg in sys.argv[1:]:
        if arg.startswith("20"):
            store_name = arg
        elif "-" in arg and len(arg) == 10:
            date_str = arg
        elif arg == "--no-change":
            show_change = False
    
    if not store_name:
        print("查询全部店铺昨日数据（含环比变化）")
    else:
        if date_str:
            print(f"查询店铺: {store_name}, 日期: {date_str}")
        else:
            print(f"查询店铺: {store_name} 昨日数据（含环比变化）")
    
    result = get_store_stats(store_name, date_str, show_change)
    print(result)
