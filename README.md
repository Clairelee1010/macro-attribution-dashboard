# Macro & Web3 Risk Intelligence Engine 🌸

> **P01 v1.0 — Macro Attribution & Cross-Market Intelligence**
>
> An evidence-driven, bilingual market intelligence dashboard connecting
> **U.S. macro conditions, cross-asset market signals, Web3/RWA context,
> and Taiwan market indicators**.

🌐 Live Demo: https://clairelee1010.github.io/macro-attribution-dashboard/

---

## Overview

The Macro & Web3 Risk Intelligence Engine is a portfolio project exploring how
market data, deterministic signal processing, evidence confidence, and
source-aware news intelligence can be combined into an explainable
cross-market decision-support product.

Instead of presenting a single AI-generated market opinion, the system separates:

- live market observations,
- deterministic intelligence outputs,
- evidence confidence,
- source provenance,
- and prototype-only concepts.

The objective is to answer three questions:

1. **What is happening in the market?**
2. **What evidence supports the current interpretation?**
3. **How confident should we be in that interpretation?**

This repository represents **P01 — UNDERSTAND**, the first phase of a broader
three-stage product roadmap.

---

# Product Architecture

```text
External Market Sources
        │
        ▼
┌─────────────────────────┐
│ Multi-Source Data Layer │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Normalization & Quality │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Signal Engine           │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Market Regime           │
│ Market Risk             │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Attribution Engine      │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Evidence Confidence     │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ News Intelligence       │
│ Source + Ranking + i18n │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Bilingual Dashboard     │
│ 中文 / English           │
└─────────────────────────┘
Core Capabilities
1. Multi-Source Market Data Pipeline

The dashboard currently monitors core cross-market indicators including:

U.S. 10-Year Treasury Yield
U.S. Dollar Index (DXY)
VIX
Bitcoin (BTC)
Ethereum (ETH)

The production pipeline supports primary and fallback data routes and exposes
data freshness and availability to downstream intelligence modules.

2. Data Quality Layer

Before market observations are used downstream, the system evaluates:

data availability,
freshness,
source route,
and overall data quality.

The dashboard explicitly distinguishes incomplete evidence from usable evidence.

3. Deterministic Market Signals

Normalized observations are transformed into explainable signals such as:

US10Y → VERY_HIGH_YIELD → RISK_OFF
DXY   → FIRM_DOLLAR     → RISK_OFF
VIX   → NORMAL_VOLATILITY → NEUTRAL

Signal generation is deterministic rather than based on an opaque AI-generated
market conclusion.

4. Market Regime & Risk Assessment

Signals are aggregated into higher-level intelligence including:

Market Regime
Market Risk
Risk Score
Assessment Confidence

Example:

MARKET REGIME
RISK_OFF

MARKET RISK
HIGH · 100/100

Risk and confidence are intentionally treated as different concepts.

High assessed market risk does not automatically imply high evidence confidence.

5. Cross-Market Attribution

The Attribution Engine identifies which eligible signals contribute most strongly
to the current market regime.

Example:

US10Y · VERY_HIGH_YIELD   61.8%
DXY   · FIRM_DOLLAR       38.2%

Attribution represents evidence alignment, not causal proof.

6. Evidence Confidence

The system separately evaluates the reliability of the evidence supporting
the current intelligence output.

The dashboard exposes:

Evidence Confidence
Evidence Coverage
Data Quality
Excluded Signals
Fallback Source Usage
Attribution Support

This prevents market risk, model output, and evidence reliability from being
presented as the same concept.

Market & Web3 Intelligence Feed

P01 includes a source-aware market intelligence pipeline.

The pipeline follows:

Sources
   ↓
Fetch
   ↓
Normalize
   ↓
Deduplicate
   ↓
Freshness Evaluation
   ↓
Relevance Scoring
   ↓
Priority Classification
   ↓
Context Linking
   ↓
Bilingual Intelligence Layer
   ↓
Dashboard
Source Intelligence

The intelligence layer can collect information associated with sources such as:

U.S. Macro / Regulation
Federal Reserve
U.S. Securities and Exchange Commission
U.S. Treasury
Web3 / Digital Assets
Coinbase
Binance
OKX
Circle
Bybit
Bitget
Gate
MEXC
Taiwan Market
Taiwan Stock Exchange
TSMC

Additional news sources may appear through the news aggregation layer.

Source availability varies by update cycle.

Intelligence Ranking

P01-NEWS-004 introduced deterministic relevance ranking.

Each eligible intelligence item can contain:

{
  "relevance_score": 85,
  "priority": "HIGH",
  "ranking_reasons": [
    "NEWS_SOURCE",
    "FRESH",
    "STRONG_P01_CONTEXT_MATCH",
    "CORE_TOPIC",
    "HIGH_MARKET_IMPACT"
  ]
}

Ranking considers factors including:

source authority,
freshness,
P01 context relevance,
core topic relevance,
and market-impact keywords.

Priority is classified as:

HIGH
MEDIUM
LOW

The ranking system is designed to be explainable rather than dependent on
opaque LLM ranking.

Bilingual Intelligence Layer

P01-NEWS-005 introduced bilingual intelligence presentation.

The dashboard supports:

🇹🇼 Traditional Chinese
🇺🇸 English

Each intelligence item may contain:

Original Source Title
Source
Freshness
Priority
Relevance Score
Intelligence Summary
Why It Matters
Linked P01 Context
Ranking Reasons
Evidence
Limitations

Original source titles are preserved to maintain provenance.

The bilingual layer applies to the intelligence interpretation rather than
rewriting the original source headline.

Data Semantics

The dashboard explicitly labels three data types.

LIVE

Automatically retrieved market observations.

Examples:

U.S. Treasury Yield
DXY
VIX
BTC
ETH
GENERATED

Deterministic intelligence produced by the system.

Examples:

Market Regime
Market Risk
Attribution
Evidence Confidence
News Relevance Score
PROTOTYPE

Illustrative concepts that are not current production market evidence.

Prototype values are visually labeled and should not be interpreted as live data.

This separation is a deliberate product design decision to prevent prototype
concepts from being confused with production intelligence.

Bilingual Dashboard

The production interface supports real-time switching between:

繁體中文
English

Localization covers:

market intelligence labels,
market status,
risk and confidence descriptions,
news metadata,
intelligence summaries,
ranking explanations,
evidence descriptions,
and limitations.
Automation

The project uses GitHub Actions to automate the intelligence pipeline.

A typical update cycle includes:

Market Data Update
        ↓
Normalization
        ↓
Data Quality
        ↓
Signals
        ↓
Market Regime
        ↓
Market Risk
        ↓
Attribution
        ↓
Evidence Confidence
        ↓
News Intelligence
        ↓
Validation
        ↓
Generated Artifacts
        ↓
GitHub Pages

Generated artifacts are validated before being committed back to the repository.

Technology Stack
Data / Intelligence
Python
Requests
yfinance
CoinGecko Public API
Intelligence Architecture
Deterministic Signal Engine
Market Regime Engine
Market Risk Engine
Attribution Engine
Evidence Confidence Layer
News Intelligence Ranking
Frontend
HTML
CSS
JavaScript
Bilingual UI
DevOps
GitHub
GitHub Actions
GitHub Pages
Product Design Principles

P01 was built around several product principles:

Explainability over black-box conclusions

Market conclusions should expose their supporting evidence.

Risk ≠ Confidence

A high-risk environment does not necessarily mean the evidence supporting the
assessment is highly reliable.

Provenance matters

Original sources and headlines are preserved whenever possible.

Graceful degradation

Individual provider failures should not automatically break the complete
intelligence pipeline.

Prototype ≠ Production

Illustrative concepts are explicitly separated from live market evidence.

No causal overclaiming

Attribution represents evidence alignment and should not be interpreted as
proof of market causality.

Project Roadmap

This project is designed as a three-phase product portfolio.

P01 — UNDERSTAND ✅
Macro & Web3 Risk Intelligence Engine
Market Data
    ↓
Signals
    ↓
Regime / Risk
    ↓
Attribution
    ↓
Evidence Confidence
    ↓
News Intelligence

Status: P01 v1.0

P02 — PREDICT / COMPARE 🔜
Tokenized Market & Prediction Intelligence

Planned exploration areas include:

Tokenized U.S. equities
24/7 market structure
Prediction markets
Polymarket / Kalshi intelligence
Implied probability
Liquidity analysis
Cross-market discrepancies
Crypto / stablecoin yield intelligence

The objective is to explore how always-on markets may change price discovery
and cross-market intelligence.

P03 — ACT 🔜
AI Agent Wallet + x402

Planned product concepts include:

AI Agent execution
Wallet authorization
Account Abstraction
x402 payments
Spending policies
Spending limits
Whitelists
Human-in-the-loop approval
Multi-signature controls
Risk checks
Audit trails
On-chain execution

Conceptual flow:

Intelligence Signal
        ↓
AI Agent
        ↓
Risk Check
        ↓
Policy Check
        ↓
Human Approval
        ↓
Wallet Authorization
        ↓
x402 / Payment / Execution
        ↓
Audit Trail
Current Limitations

P01 is an experimental portfolio product and not a production trading system.

Known limitations include:

some data sources may rely on fallback routes,
news provider availability can vary,
not every market signal has sufficient historical context,
evidence coverage may be incomplete,
attribution does not establish causality,
prototype metrics are not live market evidence,
intelligence ranking is deterministic and rule-based,
and the system does not execute trades or manage user funds.
Disclaimer

This project is provided for research, product exploration, and portfolio
demonstration purposes only.

Nothing presented by the dashboard constitutes investment, financial, legal,
or trading advice.

Market risk assessments, attribution results, relevance scores, intelligence
summaries, and evidence-confidence outputs should not be interpreted as
predictions of future market performance.

Users should independently verify source information and perform their own
due diligence before making financial decisions.

Author

Claire Lee

Technical Project Manager focused on:

Web3
RWA
AI / Agentic Systems
Cross-Market Intelligence
Product Strategy

Medium: https://medium.com/@claireli_79034


### 這版有三個重要修正

第一，**拿掉「RAG-powered」作為目前核心技術宣稱**。你現在真正有完成、而且 recruiter 可以從 repo 驗證的是 deterministic intelligence pipeline，這比硬寫 RAG 更可信。

第二，把 **`Agentic RWA Net Flows +$52.4M` 定義成 PROTOTYPE**。你 Dashboard 本來就已經這樣標示，所以 README 現在和產品畫面一致。

第三，P02 / P03 我故意寫成 **Planned**，不會讓 recruiter 誤以為你已經完成 Prediction Market、tokenized equities 或 x402。

我建議你現在直接把 GitHub 的 `README.md` **Ctrl+A 全部覆蓋成這版**。

Commit message：

```text
Freeze P01 v1.0 documentation and roadmap

Commit 完成後，不要再新增 P01 功能。

接下來我會帶你做最後一個很短的 Freeze Checklist；如果全部 PASS，就正式標記 🧊 P01 v1.0 FROZEN，然後我們開始 P02。

所以你要我修正: README.md 是那些?  

對，這一步你只需要改 GitHub repo 根目錄的 README.md 一個檔案，其他程式先不要動。

你現在的 README 是舊版，所以要做的是：

GitHub → README.md → Edit → Ctrl+A 全選 → 刪除 → 貼上新版 README → Commit changes

不是只修改其中幾行。我建議整份替換，因為舊版有幾個描述已經和現在 P01 不一致：

舊 README	現在應改成
RAG powered	evidence-driven / deterministic intelligence
RAG-based AI Engine	Signal / Risk / Attribution / Evidence / News Intelligence
RWA net flow 看起來像 real-time	明確標示為 PROTOTYPE
所有 attribution 是 AI generated	改成 deterministic attribution / evidence alignment
沒有 NEWS 系統介紹	加 NEWS-003/004/005 架構
沒有 Ranking	加 Priority / Relevance Score / Ranking Reasons
雙語只有簡單描述	加 NEWS-005 bilingual intelligence
沒有 LIVE / GENERATED / PROTOTYPE 定義	補上 Data Semantics
沒有完整 Architecture	補上 pipeline architecture
沒有 P02/P03	加 roadmap，但標記 Planned
沒有 x402 roadmap	放在 P03 Planned，不是宣稱已完成
你現在要貼哪一份？

就是我上一則訊息裡從這行開始：

# Macro & Web3 Risk Intelligence Engine 🌸

一直複製到：

Medium: https://medium.com/@claireli_79034

整段取代你現在 README.md 的全部內容。

不要把我後面的「這版有三個重要修正」那些說明貼進 README。

Commit message 用：

Freeze P01 v1.0 documentation and roadmap
其他檔案現在不要碰

index.html 不要改，你剛剛 NEWS-005 production 畫面已經正常。

market_intelligence.py 不要改，NEWS-005 backend 已 PASS。

GitHub Actions workflow 先不要改；那個還顯示 Run P01-NEWS-001... 只是名稱問題，不影響 P01 Freeze。

所以現在真的非常單純：

只更新 README.md → Commit → 給我看 README 畫面 → Final Freeze Check 🧊

如果你希望更方便，我也可以直接幫你做成一個完整 README.md 檔案讓你下載，你就不用從聊天內容複製。

完整 README.md 謝謝

完成，我已經幫你整理成可以直接使用的完整 README.md。

下載完整 README.md

你現在到 GitHub repo：

README.md → Edit / Upload → 用這份完整取代原內容 → Commit

Commit message：

Freeze P01 v1.0 documentation and roadmap

這份已經包含 P01 Architecture、NEWS-004 Ranking、NEWS-005 雙語 Intelligence、LIVE/GENERATED/PROTOTYPE 定義、GitHub Actions pipeline、Limitations，以及 P02 / P03（含 x402）Roadmap。

更新完成後給我看一下 GitHub README 畫面，我們就做最後的 P01 Freeze Checklist 🧊。 

README.md
文件

檔案庫
/
README.md
Macro & Web3 Risk Intelligence Engine 🌸

P01 v1.0 — Macro Attribution & Cross-Market Intelligence

An evidence-driven, bilingual market intelligence dashboard connecting U.S. macro conditions, cross-asset market signals, Web3/RWA context, and Taiwan market indicators.

🌐 Live Demo: https://clairelee1010.github.io/macro-attribution-dashboard/

Overview

The Macro & Web3 Risk Intelligence Engine explores how market data, deterministic signal processing, evidence confidence, and source-aware news intelligence can be combined into an explainable cross-market decision-support product.

Instead of presenting a single AI-generated market opinion, the system separates:

live market observations,
deterministic intelligence outputs,
evidence confidence,
source provenance,
and prototype-only concepts.

The product is designed to answer:

What is happening in the market?
What evidence supports the current interpretation?
How confident should we be in that interpretation?

This repository represents P01 — UNDERSTAND, the first phase of a three-stage product roadmap.

Product Architecture
External Market Sources
        │
        ▼
Multi-Source Data Layer
        │
        ▼
Normalization & Data Quality
        │
        ▼
Signal Engine
        │
        ▼
Market Regime & Market Risk
        │
        ▼
Attribution Engine
        │
        ▼
Evidence Confidence
        │
        ▼
News Intelligence
(Source + Ranking + i18n)
        │
        ▼
Bilingual Dashboard
(中文 / English)
Core Capabilities
1. Multi-Source Market Data Pipeline

The dashboard monitors core cross-market indicators including:

U.S. 10-Year Treasury Yield
U.S. Dollar Index (DXY)
VIX
Bitcoin (BTC)
Ethereum (ETH)

The production pipeline supports primary and fallback data routes and exposes data freshness and availability to downstream intelligence modules.

2. Data Quality Layer

Before observations are used downstream, the system evaluates:

data availability,
freshness,
source route,
and overall data quality.

The dashboard explicitly distinguishes incomplete evidence from usable evidence.

3. Deterministic Market Signals

Normalized observations are transformed into explainable signals such as:

US10Y → VERY_HIGH_YIELD → RISK_OFF
DXY   → FIRM_DOLLAR → RISK_OFF
VIX   → NORMAL_VOLATILITY → NEUTRAL

Signal generation is deterministic rather than based on an opaque AI-generated market conclusion.

4. Market Regime & Risk Assessment

Signals are aggregated into higher-level intelligence including:

Market Regime
Market Risk
Risk Score
Assessment Confidence

Risk and confidence are intentionally treated as different concepts.

High assessed market risk does not automatically imply high evidence confidence.

5. Cross-Market Attribution

The Attribution Engine identifies which eligible signals contribute most strongly to the current market regime.

Example:

US10Y · VERY_HIGH_YIELD   61.8%
DXY   · FIRM_DOLLAR       38.2%

Attribution represents evidence alignment, not causal proof.

6. Evidence Confidence

The system separately evaluates the reliability of the evidence supporting the current intelligence output.

The dashboard exposes:

Evidence Confidence
Evidence Coverage
Data Quality
Excluded Signals
Fallback Source Usage
Attribution Support

This prevents market risk, model output, and evidence reliability from being presented as the same concept.

Market & Web3 Intelligence Feed

P01 includes a source-aware market intelligence pipeline:

Sources
   ↓
Fetch
   ↓
Normalize
   ↓
Deduplicate
   ↓
Freshness Evaluation
   ↓
Relevance Scoring
   ↓
Priority Classification
   ↓
Context Linking
   ↓
Bilingual Intelligence Layer
   ↓
Dashboard
Source Intelligence

The intelligence layer can collect information associated with sources such as:

U.S. Macro / Regulation

Federal Reserve
U.S. Securities and Exchange Commission
U.S. Treasury

Web3 / Digital Assets

Coinbase
Binance
OKX
Circle
Bybit
Bitget
Gate
MEXC

Taiwan Market

Taiwan Stock Exchange
TSMC

Additional news sources may appear through the news aggregation layer. Source availability varies by update cycle.

Intelligence Ranking

P01-NEWS-004 introduced deterministic relevance ranking.

Each eligible intelligence item can contain:

{
  "relevance_score": 85,
  "priority": "HIGH",
  "ranking_reasons": [
    "NEWS_SOURCE",
    "FRESH",
    "STRONG_P01_CONTEXT_MATCH",
    "CORE_TOPIC",
    "HIGH_MARKET_IMPACT"
  ]
}

Ranking considers factors including:

source authority,
freshness,
P01 context relevance,
core topic relevance,
and market-impact keywords.

Priority is classified as HIGH, MEDIUM, or LOW.

The ranking system is designed to be explainable rather than dependent on opaque LLM ranking.

Bilingual Intelligence Layer

P01-NEWS-005 introduced bilingual intelligence presentation.

The dashboard supports:

🇹🇼 Traditional Chinese
🇺🇸 English

Each intelligence item may contain:

Original Source Title
Source
Freshness
Priority
Relevance Score
Intelligence Summary
Why It Matters
Linked P01 Context
Ranking Reasons
Evidence
Limitations

Original source titles are preserved to maintain provenance. The bilingual layer applies to the intelligence interpretation rather than rewriting the original source headline.

Data Semantics

The dashboard explicitly labels three data types.

LIVE

Automatically retrieved market observations, such as U.S. Treasury Yield, DXY, VIX, BTC, and ETH.

GENERATED

Deterministic intelligence produced by the system, such as Market Regime, Market Risk, Attribution, Evidence Confidence, and News Relevance Score.

PROTOTYPE

Illustrative concepts that are not current production market evidence.

Prototype values are visually labeled and should not be interpreted as live data. This separation is a deliberate product design decision to prevent prototype concepts from being confused with production intelligence.

Bilingual Dashboard

The production interface supports switching between 繁體中文 and English.

Localization covers market intelligence labels, market status, risk and confidence descriptions, news metadata, intelligence summaries, ranking explanations, evidence descriptions, and limitations.

Automation

The project uses GitHub Actions to automate the intelligence pipeline:

Market Data Update
        ↓
Normalization
        ↓
Data Quality
        ↓
Signals
        ↓
Market Regime
        ↓
Market Risk
        ↓
Attribution
        ↓
Evidence Confidence
        ↓
News Intelligence
        ↓
Validation
        ↓
Generated Artifacts
        ↓
GitHub Pages

Generated artifacts are validated before being committed back to the repository.

Technology Stack
Data / Intelligence
Python
Requests
yfinance
CoinGecko Public API
Intelligence Architecture
Deterministic Signal Engine
Market Regime Engine
Market Risk Engine
Attribution Engine
Evidence Confidence Layer
News Intelligence Ranking
Frontend
HTML
CSS
JavaScript
Bilingual UI
DevOps
GitHub
GitHub Actions
GitHub Pages
Product Design Principles
Explainability over black-box conclusions — market conclusions should expose their supporting evidence.
Risk ≠ Confidence — a high-risk environment does not necessarily mean the supporting evidence is highly reliable.
Provenance matters — original sources and headlines are preserved whenever possible.
Graceful degradation — individual provider failures should not automatically break the complete intelligence pipeline.
Prototype ≠ Production — illustrative concepts are explicitly separated from live market evidence.
No causal overclaiming — attribution represents evidence alignment, not proof of market causality.
Project Roadmap
P01 — UNDERSTAND ✅

Macro & Web3 Risk Intelligence Engine

Market Data
    ↓
Signals
    ↓
Regime / Risk
    ↓
Attribution
    ↓
Evidence Confidence
    ↓
News Intelligence

Status: P01 v1.0

P02 — PREDICT / COMPARE 🔜

Tokenized Market & Prediction Intelligence

Planned exploration areas include:

Tokenized U.S. equities
24/7 market structure
Prediction markets
Polymarket / Kalshi intelligence
Implied probability
Liquidity analysis
Cross-market discrepancies
Crypto / stablecoin yield intelligence

The objective is to explore how always-on markets may change price discovery and cross-market intelligence.

P03 — ACT 🔜

AI Agent Wallet + x402

Planned product concepts include:

AI Agent execution
Wallet authorization
Account Abstraction
x402 payments
Spending policies
Spending limits
Whitelists
Human-in-the-loop approval
Multi-signature controls
Risk checks
Audit trails
On-chain execution

Conceptual flow:

Intelligence Signal
        ↓
AI Agent
        ↓
Risk Check
        ↓
Policy Check
        ↓
Human Approval
        ↓
Wallet Authorization
        ↓
x402 / Payment / Execution
        ↓
Audit Trail
Current Limitations

P01 is an experimental portfolio product and not a production trading system.

Known limitations include:

some data sources may rely on fallback routes,
news provider availability can vary,
not every market signal has sufficient historical context,
evidence coverage may be incomplete,
attribution does not establish causality,
prototype metrics are not live market evidence,
intelligence ranking is deterministic and rule-based,
and the system does not execute trades or manage user funds.
Disclaimer

This project is provided for research, product exploration, and portfolio demonstration purposes only.

Nothing presented by the dashboard constitutes investment, financial, legal, or trading advice.

Market risk assessments, attribution results, relevance scores, intelligence summaries, and evidence-confidence outputs should not be interpreted as predictions of future market performance.

Users should independently verify source information and perform their own due diligence before making financial decisions.

Author

Claire Lee

Technical Project Manager focused on:

Web3
RWA
AI / Agentic Systems
Cross-Market Intelligence
Product Strategy

Medium: https://medium.com/@claireli_79034
