"""
店小秘店铺业绩统计 - 30天店铺分析（最终版）
关闭页面重新打开确保数据准确
"""

import subprocess
import time
import json


def run_js(js_code):
    result = subprocess.run(
        ["osascript", "-e", 'tell application "Google Chrome" to execute active tab of window 1 javascript "' + js_code.replace('"', '\\"') + '"'],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout.strip()


def analyze_stores():
    print("="*60)
    print("店小秘 30天店铺业绩分析")
    print("="*60)
    
    # 先获取店铺列表
    subprocess.run(
        ["osascript", "-e", 'tell application "Google Chrome" to open location "https://www.dianxiaomi.com/web/stat/storePerformance"'],
        capture_output=True
    )
    time.sleep(18)
    
    # 点击30天内
    run_js('''var btns=document.querySelectorAll(".ant-radio-button-wrapper");for(var i=0;i<btns.length;i++){if(btns[i].textContent.includes("30天内")){btns[i].click();break;}}''')
    time.sleep(8)
    
    # 获取店铺列表
    stores_str = run_js('''var c=document.querySelectorAll(".d-checkbox-group-wrapper")[1];var l=c.querySelectorAll("label");var s=[];for(var i=1;i<l.length;i++){s.push(l[i].textContent.trim());}JSON.stringify(s)''')
    
    try:
        stores = json.loads(stores_str)
    except:
        stores = []
    
    print(f"发现 {len(stores)} 个店铺")
    
    if not stores:
        return "未找到店铺"
    
    all_data = []
    
    # 分析前10个店铺（减少数量加快速度）
    for idx, store in enumerate(stores[:10]):
        store_key = store.split("（")[0].split("（")[0].strip()
        print(f"\n[{idx+1}/{len(stores)}] 分析: {store_key}...")
        
        # 关闭当前标签页
        run_js("window.close()")
        time.sleep(2)
        
        # 重新打开页面
        subprocess.run(
            ["osascript", "-e", 'tell application "Google Chrome" to open location "https://www.dianxiaomi.com/web/stat/storePerformance"'],
            capture_output=True
        )
        time.sleep(20)
        
        # 点击30天内
        run_js('''var btns=document.querySelectorAll(".ant-radio-button-wrapper");for(var i=0;i<btns.length;i++){if(btns[i].textContent.includes("30天内")){btns[i].click();break;}}''')
        time.sleep(8)
        
        # 取消全选
        run_js('''var c=document.querySelectorAll(".d-checkbox-group-wrapper")[1];var l=c.querySelectorAll("label");if(l[0].querySelector("input").checked){l[0].click();}''')
        time.sleep(3)
        
        # 选择指定店铺
        run_js(f'''var c=document.querySelectorAll(".d-checkbox-group-wrapper")[1];var l=c.querySelectorAll("label");for(var i=0;i<l.length;i++){{if(l[i].textContent.includes("{store_key}")){{l[i].click();break;}}}}''')
        time.sleep(8)
        
        # 获取数据
        data_str = run_js('''var rows=document.querySelectorAll("tr.vxe-body--row");var r=rows[0];var cells=r.querySelectorAll("td");cells[0].textContent+"|"+cells[2].textContent+"|"+cells[4].textContent+"|"+cells[7].textContent''')
        
        try:
            parts = data_str.split("|")
            if len(parts) >= 4:
                orders = parts[1].strip()
                payment = parts[2].strip()
                refund = parts[3].strip()
                
                payment_num = float(payment.replace("$", "").replace(",", ""))
                
                all_data.append({
                    "store": store,
                    "orders": orders,
                    "payment": payment,
                    "refund": refund,
                    "payment_num": payment_num
                })
                print(f"  -> 订单:{orders}, 付款:{payment}, 退款:{refund}")
        except Exception as e:
            print(f"  -> 错误: {e}")
    
    if not all_data:
        return "未获取到数据"
    
    # 按付款金额排序
    all_data.sort(key=lambda x: x["payment_num"], reverse=True)
    
    best = all_data[0]
    worst = all_data[-1]
    
    total_orders = sum(int(d["orders"].replace(",", "")) for d in all_data)
    total_payment = sum(d["payment_num"] for d in all_data)
    total_refund = sum(float(d["refund"].replace("$", "").replace(",", "")) for d in all_data)
    
    output = f"""
📊 30天店铺业绩分析 (2026-02-01 ~ 03-02)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 业绩最佳店铺: {best['store']}
   📦 订单量: {best['orders']}
   💰 付款: {best['payment']}
   💸 退款: {best['refund']}

⚠️ 业绩最差店铺: {worst['store']}
   📦 订单量: {worst['orders']}
   💰 付款: {worst['payment']}
   💸 退款: {worst['refund']}

📋 店铺排名 (按付款金额):
"""
    
    for i, d in enumerate(all_data[:15]):
        output += f"{i+1}. {d['store']}: {d['payment']} (订单 {d['orders']})\n"
    
    output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 总计:
   📦 订单量: {total_orders:,}
   💰 付款: ${total_payment:,.2f}
   💸 退款: ${total_refund:,.2f}
   💵 净收入: ${total_payment - total_refund:,.2f}
"""
    
    return output


if __name__ == "__main__":
    print(analyze_stores())
