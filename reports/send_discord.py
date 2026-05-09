#!/usr/bin/env python3
import os, json, urllib.request, time

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL", "")

messages = [
    """📊 美股盤前快報 — 2026年5月9日

🔥 頭條新聞

1️⃣ **美伊停火再度搖晃**：伊朗指控美國及盟友違反停火協議，霍爾木茲海峽再度爆發交火，WTI本週劇震。川普堅稱停火仍有效，談判繼續中。

2️⃣ **四月非農就業超預期**：+11.5萬人（高於預期），帶動S&P 500（+0.84%）與那斯達克（+1.71%）週五雙創歷史新高。S&P 500收7,398，那斯達克收26,247。

3️⃣ **消費者信心跌至歷史新低**：密西根大學5月初步讀值48.2，月減3.2%，汽油突破$4.50/加侖是主因。強就業與低信心形成罕見背離。

4️⃣ **Micron（MU）本週暴漲25%**：AI記憶體超級週期加速，市值突破7,000億美元，進入美國科技市值前十。HBM完售至2026年底，DA Davidson目標價上看$1,000。""",

    """📈 盤前主要動向（2026/5/9 約8:00 AM ET）

🟢 **MU**  ▲ +3.84%  $671.30｜AI HBM需求爆炸，分析師喊$1,000
🟢 **TSLA**  ▲ +2%  $405.97｜跟隨科技強勢，反彈動能延續
🟢 **MSFT**  ▲ 小漲  $414.36｜AI雲端業務持續受益
🟢 **S&P 500期貨**  ▲ +0.33%  7,387.50
🟢 **那斯達克期貨**  ▲ +0.51%  28,827.50
🔴 **WTI原油**  ▼ -2.2%  $93.02｜伊朗談判進展降低供應風險
🔴 **Brent**  ▼ -2.0%  $99.21
🟡 **黃金**  ▲ 走高｜地緣風險 + 通膨擔憂雙重支撐

🏭 板塊觀察

✅ 強勢：科技/半導體（MU領漲，AI記憶體生態圈全面受益）、通訊服務、醫療保健（防禦輪動）
❌ 弱勢：能源（油價下跌壓制XOM/CVX）、非必需消費品（消費信心48.2 + 汽油貴壓縮可支配收入）""",

    """🐦 X/推特熱門話題

🔥 **$MU** — 本週最熱cashtag，「AI記憶體超級週期」已成主流敘事，+25%週漲
💬 **$TSLA** — 反彈能否持續是核心爭議，多空激烈
⚠️ **#IranCeasefire / #Hormuz** — 最大地緣尾部風險，一則新聞就能讓市場跳空
🛢️ **$OIL / $USO** — 能源交易者緊盯霍爾木茲，二元事件賭注大
🤖 **$NVDA / $AMD** — AI基礎設施股熱度不退，輝達供應鏈全面受益
📊 市場情緒：整體偏樂觀，但「經濟數據的hopium vs. 消費信心現實」形成分歧

⚡ 波段交易關注點

1️⃣ **MU/半導體族群**：HBM需求強力支撐，回調-5%~-8%可考慮波段進場。$683為短期高點，留意獲利了結。建議分批進場，不追高。

2️⃣ **能源股雙向機會**：談判破局→油價反彈，XOM/CVX/OXY短線急漲；達成協議→反向做空ERY。霍爾木茲是本週最大二元事件，倉位控管要嚴。

3️⃣ **防禦輪動信號**：消費信心48.2為異常低值，若下週出現從成長股流向XLU/XLP/XLV的資金輪動，可能是市場見頂前兆，需留意。""",

    """📌 今日關鍵事件

🔴 **5月9日（週六）**：美股休市，無盤中交易

⚠️ **週一（5/11）開盤注意事項**：
• 密切留意週末美伊最新動態
• 若霍爾木茲局勢升級，週一跳空風險大
• 油價動向將主導開盤情緒

📊 **下週重要數據**：
• **CPI**（消費者物價指數）— 將影響聯準會利率路徑
• 密西根大學消費者信心最終值
• 多位聯準會官員公開講話

📋 **財報季尾聲回顧**：
Q1 EPS年增率15.1% ✅
84%企業超預期 ✅
平均超出幅度12.3% ✅
→ 本季為FactSet有史以來追蹤到的最強財報季

---
🤖 由 Claude Code 自動生成｜資料來源：CNBC、TheStreet、CoinCentral、Schwab""",
]

if not WEBHOOK:
    print("ERROR: DISCORD_WEBHOOK_URL not set")
    for i, msg in enumerate(messages, 1):
        print(f"\n--- Message {i} ({len(msg)} chars) ---\n{msg}")
else:
    for i, msg in enumerate(messages, 1):
        payload = json.dumps({"content": msg}).encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            print(f"Message {i}/{len(messages)} sent — HTTP {resp.status}")
        if i < len(messages):
            time.sleep(1)
