# 請將這整塊 html_template 覆蓋您程式碼中原本的模板區塊
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
        const data = {json.dumps(engine.fetch_us_macro_intelligence(), ensure_ascii=False)};
        const container = document.getElementById('container');
        
        data.forEach(L => {{
            // 處理雙語與指標的渲染
            const recUsHtml = L.rec_attribution_us || 'N/A';
            const riskTwHtml = L.risk_attribution_tw || 'N/A';
            const riskUsHtml = L.risk_attribution_us || 'N/A';

            const card = document.createElement('div');
            card.className = 'card-pro p-8 border-l-4 border-indigo-600 rounded-xl';
            card.innerHTML = `
                <h2 class="text-2xl font-bold mb-4">${{L.title_zh}}</h2>
                <div class="grid grid-cols-2 gap-12 text-sm text-slate-300">
                    <div>
                        <div class="text-indigo-400 font-bold mb-2 uppercase text-xs">總經歸因 (Macro Attribution)</div>
                        <p class="leading-relaxed">${{L.macro_attribution_zh}}</p>
                    </div>
                    <div class="space-y-4">
                        <div class="bg-emerald-950/20 border border-emerald-900/30 rounded-xl p-4">
                            <div class="text-[11px] font-bold text-emerald-400 uppercase mb-2">${{L.rec_title_us}}</div>
                            <div class="leading-relaxed">${{recUsHtml}}</div>
                        </div>
                        <div class="bg-rose-950/20 border border-rose-900/30 rounded-xl p-4">
                            <div class="text-[11px] font-bold text-rose-400 uppercase mb-2">${{L.risk_title_tw}}</div>
                            <div class="leading-relaxed">${{riskTwHtml}}</div>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        }});
    </script>
</body>
</html>
'''

# 確保寫入檔案的路徑正確
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)
print("🎯 原始版本已恢復，請執行您的 Python 腳本。")
