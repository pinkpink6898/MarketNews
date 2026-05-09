---
name: market-news-digest
description: >
  Daily US stock market news digest for swing traders in Traditional Chinese, sent to Discord.
  Two modes: (1) pre-market briefing (~9AM ET) with overnight news, movers, and setups;
  (2) post-market review (~10PM ET) analyzing why the market moved and reviewing trades.
  Trigger on: "morning report", "market digest", "pre-market news", "post-market review",
  "market recap", "盤前新聞", "今日新聞", "盤前整理", "盤後回顧", "收盤分析", "今日覆盤",
  "what's moving today", "send me the market update", "how did the market do today",
  "any big news today", or any request for a daily financial news roundup or market summary.
  Uses web search, NewsAPI, and Polygon.io for data, tracks X/Twitter sentiment and cashtags.
  Do NOT trigger for backtesting, charting, or trade execution.
---

# Market News Digest

A skill that gathers US stock market news and trending topics from X (Twitter), compiles them
into structured reports in Traditional Chinese, and delivers them to Discord via webhook.

## Two Report Modes

This skill produces two distinct report types. Determine which one the user wants based on
context (time of day, keywords used, or explicit request). If unclear, ask the user.

### Mode 1: 盤前快報 (Pre-Market Briefing)
- **Purpose**: Prepare the trader for the upcoming session
- **Timing**: ~9:00 AM ET, before market open at 9:30 AM ET
- **Tone**: Forward-looking, actionable, "what to watch"
- **Focus**: Overnight developments, pre-market movers, earnings from previous evening,
  economic data releases scheduled for today, geopolitical developments, X/Twitter sentiment

### Mode 2: 盤後回顧 (Post-Market Review)
- **Purpose**: Review what happened during the session and analyze why
- **Timing**: ~10:00 PM ET, after all after-hours activity settles
- **Tone**: Analytical, backward-looking, "what happened and why"
- **Focus**: Intraday price action, sector rotation, volume analysis, key earnings released
  after the bell, how the market reacted to economic data, what narratives drove buying/selling,
  after-hours movers, and implications for the next session

## Workflow

1. **Determine report mode** (pre-market or post-market) based on user request
2. **Gather news** from multiple sources (web search, NewsAPI, Polygon.io)
3. **Gather X/Twitter sentiment** (trending tickers, cashtags, market sentiment)
4. **Synthesize** into the appropriate report format
5. **Write entirely in Traditional Chinese** (繁體中文), keeping tickers in English ($AAPL)
6. **Send to Discord** via webhook

## Step 1: Gather Market News

Use all three sources for broad coverage:

### Web Search
Tailor queries to the report mode:

**Pre-market queries:**
- `US stock market news today`
- `pre-market movers today`
- `stock market breaking news overnight`
- `economic calendar today`

**Post-market queries:**
- `stock market today close`
- `stock market recap today`
- `after hours earnings movers today`
- `sector performance today stock market`

Focus on: Fed/FOMC decisions, earnings surprises, geopolitical events, sector rotations,
major analyst upgrades/downgrades, IPOs, economic data releases, and any black swan events.

### NewsAPI
Run the script to fetch top financial headlines.
Requires `NEWSAPI_KEY` environment variable.

```bash
python3 /path/to/skill/scripts/fetch_news.py
```

### Polygon.io
Run the script to pull market-moving news and top gainers/losers.
Requires `POLYGON_API_KEY` environment variable.

```bash
python3 /path/to/skill/scripts/fetch_polygon.py
```

## Step 2: Gather X/Twitter Hot Topics

Use web search to find trending finance topics on X/Twitter:
- `site:x.com stock market trending today`
- `fintwit trending tickers today`
- `cashtag trending stocks twitter today`
- `stock market sentiment twitter today`

Look for: heavily discussed cashtags, viral finance posts, contrarian sentiment signals,
meme-stock momentum, and notable calls from prominent traders.

## Step 3: Compile the Report

### Pre-Market Report Format (盤前快報)

```
📊 美股盤前快報 — {YYYY/MM/DD}

🔥 頭條新聞
• [Top 3-4 most impactful news items with brief context]

📈 盤前主要動向
• [Pre-market movers: ticker, direction, catalyst — 5-8 items]

🏭 板塊觀察
• [Sector breakdown: which sectors are hot/cold and why]

🐦 X/推特熱門話題
• [Trending cashtags and what people are saying]
• [Notable sentiment shifts or viral finance posts]

⚡ 波段交易關注點
• [2-3 actionable items specifically relevant to swing trading setups]

📌 今日關鍵事件
• [Earnings releases, economic data, Fed speakers with times in ET]
```

### Post-Market Report Format (盤後回顧)

```
📊 美股盤後回顧 — {YYYY/MM/DD}

📉 今日行情總結
• S&P 500: [close, change %, key level commentary]
• Nasdaq: [close, change %, key level commentary]
• Dow: [close, change %, key level commentary]
• VIX: [level, change]
• Oil/Gold/BTC: [key commodity and crypto moves]

🔍 行情分析：今天為什麼這樣走？
• [2-3 paragraphs analyzing the day's narrative: what drove buying/selling,
  how sentiment shifted intraday, which catalysts mattered most]

📈 主要個股表現
• 🟢 漲幅領先: [Top 5 gainers with catalysts]
• 🔴 跌幅領先: [Top 5 losers with catalysts]
• 🌙 盤後重點: [Key after-hours movers from earnings/news]

🏭 板塊輪動分析
• [Which sectors led/lagged, fund flows, rotation patterns]

🐦 X/推特盤後情緒
• [What fintwit is saying about today's action]
• [Sentiment shift: more bullish or bearish vs morning?]

⚡ 波段交易覆盤
• [How did pre-market setups play out?]
• [New setups forming for tomorrow]
• [Key levels to watch on major indices]

📌 明日預告
• [Tomorrow's earnings, economic data, events to watch]
```

### Writing Guidelines (both modes)
- Keep it concise and scannable — this is a Discord message, not an essay
- Use Traditional Chinese (繁體中文) throughout, but keep ticker symbols in English ($AAPL)
- Bold key tickers and numbers for quick scanning
- Include relevant emojis for visual scanning in Discord
- Prioritize actionable information for swing traders
- If a piece of news has direct trading implications, say so briefly
- Total length should be readable in ~2 minutes per report

## Step 4: Send to Discord

The Discord webhook URL is stored in the `DISCORD_WEBHOOK_URL` environment variable.

Run the send script, which automatically splits long messages:

```bash
echo "<report_content>" | python3 /path/to/skill/scripts/send_discord.py
```

Or pass as argument:
```bash
python3 /path/to/skill/scripts/send_discord.py "<report_content>"
```

Discord has a 2000-character limit per message. The script handles splitting automatically,
breaking at section boundaries (double newlines) so each chunk is self-contained.

Alternatively, send directly via curl:
```bash
curl -H "Content-Type: application/json" \
  -d "{\"content\": \"<report_content>\"}" \
  "$DISCORD_WEBHOOK_URL"
```

## Step 5: Confirm Delivery

After sending, confirm to the user:
- Which report was sent (盤前快報 or 盤後回顧)
- Whether all sections were delivered successfully
- If any news source failed, mention it and note the report was compiled from remaining sources

## Environment Variables

| Variable | Purpose |
|---|---|
| `NEWSAPI_KEY` | NewsAPI.org API key |
| `POLYGON_API_KEY` | Polygon.io API key |
| `DISCORD_WEBHOOK_URL` | Discord channel webhook URL |

If any are missing, tell the user which ones need to be set:
```bash
export NEWSAPI_KEY="your-key-here"
export POLYGON_API_KEY="your-key-here"
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

## Error Handling

- If NewsAPI fails → proceed with web search + Polygon
- If Polygon fails → proceed with web search + NewsAPI
- If Discord webhook fails → save the report to a local file and tell the user
- If all news sources fail → tell the user and suggest checking API keys
- Always produce the best report possible with whatever sources are available
