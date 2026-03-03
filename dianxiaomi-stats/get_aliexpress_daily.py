import subprocess
import time
import json
import sys
from datetime import datetime, timedelta


def open_url_in_chrome(url):
    """使用 AppleScript 在 Chrome 中打开 URL"""
    cmd = ['osascript', '-e', 
           'tell application "Google Chrome" to open location "' + url + '"']
    subprocess.run(cmd)


def get_aliexpress_stats(wait_seconds=15):
    """获取速卖通昨日业绩数据"""
    print("正在打开店小秘...")
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    target_url = "https://www.dianxiaomi.com/web/stat/storePerformance"
    open_url_in_chrome(target_url)

    print(f"已在 Chrome 中打开: {target_url}")
    print(f"等待 {wait_seconds} 秒让页面加载...")

    time.sleep(wait_seconds)
    print("正在获取数据...")

    # 获取数据
    js_code = '''JSON.stringify(Array.from(document.querySelectorAll('tr.vxe-body--row')).map(function(row) {
    var store = row.querySelector('td[colid="col_1"] .vxe-cell--label');
    var date = row.querySelector('td[colid="col_6"] .vxe-cell--label');
    var orderCount = row.querySelector('td[colid="col_8"] .vxe-cell--label');
    var paymentAmount = row.querySelector('td[colid="col_10"] .vxe-cell--label');
    return {
        "店铺": store ? store.textContent.trim() : "",
        "日期": date ? date.textContent.trim() : "",
        "订单量": orderCount ? orderCount.textContent.trim() : "",
        "付款金额": paymentAmount ? paymentAmount.textContent.trim() : ""
    };
}).filter(function(item) { return item.日期 || item.订单量 || item.付款金额; }));'''

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
        return f"解析数据失败: {result.stdout}"

    if not data:
        return "未找到数据，请确保 Chrome 已开启 AppleScript JavaScript 权限（菜单: 查看 > 开发者 > 允许 Apple 事件中的 JavaScript）"

    print(f"共获取 {len(data)} 条数据")
    
    # 查找昨日数据
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_data = None
    
    for item in data:
        date = item.get("日期", "")
        if date == yesterday:
            yesterday_data = item
            break
    
    if not yesterday_data:
        # 找合计
        for item in data:
            if item.get("日期") == "合计":
                yesterday_data = item
                break

    if yesterday_data:
        orders = yesterday_data.get("订单量", "0")
        amount = yesterday_data.get("付款金额", "$0")
        
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y年%m月%d日")
        
        output = f"""📊 速卖通昨日业绩 ({yesterday_str})
━━━━━━━━━━━━━━━━━━━
📦 订单量: {orders}
💰 付款金额: {amount}
━━━━━━━━━━━━━━━━━━━"""
        
        return output
    else:
        return "未找到昨日数据"


if __name__ == "__main__":
    print("="*50)
    print("速卖通昨日业绩统计")
    print("="*50)
    
    result = get_aliexpress_stats()
    print(result)
