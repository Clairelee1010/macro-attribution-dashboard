# 這是您程式碼最底部，寫入 HTML 的部分
# 請確保您的數據擷取函數已經跑完，並賦值給這些變數

# 確保這兩個變數包含了您最新的資料列表
us_data = engine.fetch_us_macro_intelligence()
# ... (其他數據源)

# 關鍵點：在這裡直接把最新的資料塞進去
# 我們使用 json.dumps 將 Python 的 list 轉成 JS 可以讀取的格式
html_template = f'''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #090d16; color: #e2e8f0; }}
        .card-pro {{ background: #1e293b; border: 1px solid #334155; }}
    </style>
</head>
<body class="p-8">
    <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-8">🎯 每日總經與台美股跨市場連動歸因看板</h1>
        <div id="container" class="space-y-6"></div>
    </div>
    <script>
        // 【核心修正】這裡直接寫入最新的資料
        const data = {json.dumps(us_data, ensure_ascii=False)};
        
        const container = document.getElementById('container');
        data.forEach(L => {{
            const card = document.createElement('div');
            card.className = 'card-pro p-8 border-l-4 border-indigo-600 rounded-xl';
            card.innerHTML = `
                <h2 class="text-2xl font-bold mb-4">${{L.title_zh}}</h2>
                <div class="grid grid-cols-2 gap-12 text-sm text-slate-300">
                    <div>
                        <div class="text-indigo-400 font-bold mb-2 uppercase text-xs">總經歸因</div>
                        <p>${{L.macro_attribution_zh}}</p>
                    </div>
                    <div class="bg-rose-950/20 p-4 rounded">
                        <div class="text-rose-400 font-bold mb-2 uppercase text-xs">風險/推薦標的</div>
                        <p>${{L.risk_attribution_zh || '無特定建議'}}</p>
                    </div>
                </div>
            `;
            container.appendChild(card);
        }});
    </script>
</body>
</html>
'''

with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)
print("✅ 看板已完美重繪，指標與數據皆已更新！")
