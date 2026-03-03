import subprocess
import time
import json
import sys


def open_url_in_chrome(url):
    """使用 AppleScript 在 Chrome 中打开 URL（激活已存在的窗口或创建新窗口）"""
    # 使用更简单的 AppleScript 语法
    cmd = ['osascript', '-e', 
           'tell application "Google Chrome" to open location "' + url + '"']
    subprocess.run(cmd)


def get_dianxiaomi_stats(store_name=None, wait_seconds=8):
    """通过 Chrome 获取店小秘店铺数据。"""
    print("正在打开店小秘...")

    target_url = "https://www.dianxiaomi.com/web/stat/storePerformance"
    open_url_in_chrome(target_url)

    print(f"已在 Chrome 中打开: {target_url}")
    print(f"等待 {wait_seconds} 秒让页面加载...")

    time.sleep(wait_seconds)
    print("正在获取数据...")

    # 获取数据
    js_code = '''JSON.stringify(Array.from(document.querySelectorAll('tr.vxe-body--row')).map(function(row) {
    var date = row.querySelector('td[colid="col_6"] .vxe-cell--label');
    var orderCount = row.querySelector('td[colid="col_8"] .vxe-cell--label');
    var paymentAmount = row.querySelector('td[colid="col_10"] .vxe-cell--label');
    return {
        "日期": date ? date.textContent.trim() : "",
        "订单量": orderCount ? orderCount.textContent.trim() : "",
        "付款金额": paymentAmount ? paymentAmount.textContent.trim() : ""
    };
}).filter(function(item) { return item.日期 || item.订单量 || item.付款金额; }));'''

    # 转义引号
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
        return "未找到数据，请确认页面已加载完成并显示数据"

    # 获取选中的店铺
    js_shop = '''(function() {
        var labels = document.querySelectorAll('.d-checkbox-group-wrapper label.ant-checkbox-wrapper-checked');
        var texts = [];
        for (var i = 0; i < labels.length; i++) {
            var text = labels[i].textContent.trim();
            if (text && text !== '全部') {
                texts.push(text);
            }
        }
        return texts.join(', ') || '全部';
    })();'''

    js_shop_escaped = js_shop.replace('"', '\\"')

    result_shop = subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_shop_escaped}"'],
        capture_output=True,
        text=True,
        timeout=30
    )

    shop_account = result_shop.stdout.strip() if result_shop.returncode == 0 else "全部"

    # 添加店铺账号
    for item in data:
        item["店铺账号"] = shop_account

    # 重新排列字段顺序
    data = [{"店铺账号": item["店铺账号"], "日期": item["日期"], "订单量": item["订单量"], "付款金额": item["付款金额"]} for item in data]

    print("数据获取完成")
    return json.dumps(data, ensure_ascii=False, indent=2)


def get_shop_list():
    """获取所有可用的店铺列表"""
    print("正在打开店小秘...")

    target_url = "https://www.dianxiaomi.com/web/stat/storePerformance"
    open_url_in_chrome(target_url)

    print(f"已在 Chrome 中打开: {target_url}")
    print("等待 5 秒让页面加载...")

    time.sleep(5)
    print("正在获取店铺列表...")

    js_code = '''JSON.stringify(Array.from(document.querySelectorAll('.d-checkbox-group-wrapper label'))
.map(function(l) { return l.textContent.trim(); })
.filter(function(t) { return t && t !== '全部'; }));'''

    js_escaped = js_code.replace('"', '\\"')

    result = subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to execute active tab of window 1 javascript "{js_escaped}"'],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        return f"获取店铺列表失败: {result.stderr}"

    try:
        shops = json.loads(result.stdout.strip())
    except:
        return f"解析数据失败: {result.stdout}"

    return json.dumps(shops, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("="*50)
    print("店小秘业绩统计")
    print("="*50)
    print("脚本会在 Chrome 中打开店小秘页面并自动获取数据")
    print("浏览器将保持打开状态")
    print("="*50)

    if len(sys.argv) > 1:
        store_name = sys.argv[1]
        result = get_dianxiaomi_stats(store_name)
    else:
        result = get_dianxiaomi_stats()

    print(result)
