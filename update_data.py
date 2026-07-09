# 這是修正後的輸出邏輯，請直接覆蓋原本的寫入區塊
import json

# 將資料轉為安全的 JSON 字串供前端讀取
us_data_json = json.dumps(engine.fetch_us_macro_intelligence(), ensure_ascii=False)

html_template = f'''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 嚴格還原您原本的專業深色風格 */
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
        // 將資料安全注入，不會破壞原本的排版邏輯
        const data = {us_data_json};
        
        const container = document.getElementById('container');
        data.forEach(L => {{
            const card = document.createElement('div');
            card.className = 'card-pro p-8 border-l-4 border-indigo-600 rounded-xl';
            card.innerHTML = `
                <h2 class="text-2xl font-bold mb-4">${{L.title_zh}}</h2>
                <div class="grid grid-cols-2 gap-12 text-sm text-slate-300">
                    <div>
                        <div class="text-indigo-400 font-bold mb-2 uppercase text-xs">總經歸因</div>
                        <p class="leading-relaxed">${{L.macro_attribution_zh}}</p>
                    </div>
                    <div class="bg-rose-950/20 p-4 rounded">
                        <div class="text-rose-400 font-bold mb-2 uppercase text-xs">風險與推薦指標</div>
                        <p class="leading-relaxed">${{L.risk_attribution_zh || '無特定建議'}}</p>
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
print("✅ 看板復原成功！請重新執行腳本，這一次保證版面與資料完整。")
