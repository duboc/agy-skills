# Funnel-as-Code Playbook

This reference describes the Funnel-as-Code methodology and how to apply it to Google Ads management using the Gemini CLI.

---

## What is Funnel-as-Code?

Funnel-as-Code treats your advertising account as a system that can be:

- **Queried** — Pull performance data via GAQL instead of navigating dashboards
- **Analyzed** — Apply structured frameworks to identify issues and opportunities
- **Acted upon** — Generate executable code for changes, reviewed before deployment
- **Versioned** — Track changes, save reports, and maintain audit history

The marketer shifts from dashboard operator to systems architect. The CLI becomes the control surface for the entire funnel.

---

## The Analysis Loop

Every Funnel-as-Code workflow follows a four-phase loop:

### Phase 1: Query

Pull structured data from the Google Ads API using GAQL. The Google Ads API Developer Assistant extension translates natural language into validated queries and executes them.

**Principles:**
- Pull only the fields you need — reduces response size and processing time
- Always scope queries with date ranges and status filters
- Use `SearchGoogleAdsStream` for large result sets
- Save raw data to CSV for reference and comparison

### Phase 2: Analyze

Apply structured frameworks to the queried data. This is where the skill's workflows provide value — each workflow defines a specific analytical lens.

**Principles:**
- Compare against benchmarks (account averages, historical performance, industry norms)
- Look for outliers in both directions (unusually good and unusually bad)
- Check for statistical significance before drawing conclusions
- Cross-reference multiple data points (don't judge a keyword by cost alone)

### Phase 3: Recommend

Generate specific, implementable recommendations based on the analysis. Each recommendation should include:

- **What** to change
- **Why** it matters (grounded in data)
- **Expected impact** (quantified where possible)
- **How** to implement (GAQL or code snippet)
- **Risk** (what could go wrong)

**Principles:**
- Prioritize by impact, not by ease
- Batch related changes together
- Consider interaction effects (changing bids affects impression share affects quality score)
- Always include a "do nothing" baseline for comparison

### Phase 4: Execute (Human-in-the-Loop)

Generate the code to implement changes but never execute mutating operations automatically. The human reviews, approves, and runs the code.

**Principles:**
- Generate code that is readable and well-commented
- Include rollback instructions for every change
- Batch changes into logical groups
- Log all changes for audit trail

---

## Workflow Selection Guide

| User Need | Workflow | Key Output |
|-----------|----------|------------|
| "Is my account healthy?" | Account Health Audit | Health scorecard with prioritized actions |
| "Where am I wasting money?" | Spend Efficiency Analysis | Waste report with negative keyword list and budget reallocation plan |
| "Are my ads performing well?" | Creative Performance Lab | Asset report with replacement and testing recommendations |
| "What are people searching for?" | Search Term Mining | Categorized search term report with keyword expansion and negative lists |
| "Is my tracking working?" | Conversion Funnel Diagnostics | Tracking health report with funnel stage metrics |
| "Is my account structured well?" | Campaign Structure Review | Structure assessment with reorganization recommendations |

---

## Combining Workflows

Workflows are designed to be composable. Common combinations:

### Full Account Review
1. Start with **Account Health Audit** for the big picture
2. Drill into **Spend Efficiency Analysis** for the worst-performing areas
3. Run **Search Term Mining** on high-spend campaigns
4. Check **Conversion Funnel Diagnostics** if tracking issues are flagged

### Pre-Scale Check
1. Run **Campaign Structure Review** to ensure the foundation is solid
2. Run **Spend Efficiency Analysis** to eliminate waste before increasing budget
3. Check **Creative Performance Lab** to ensure creative can support higher volume

### Monthly Maintenance
1. **Search Term Mining** — Add negatives and expand keyword list
2. **Creative Performance Lab** — Replace underperforming assets
3. **Spend Efficiency Analysis** — Rebalance budgets based on latest data

---

## Metrics Reference

### Core Metrics

| Metric | GAQL Field | Calculation Notes |
|--------|-----------|-------------------|
| Cost | `metrics.cost_micros` | Divide by 1,000,000 for currency |
| Impressions | `metrics.impressions` | Raw count |
| Clicks | `metrics.clicks` | Raw count |
| CTR | `metrics.ctr` | clicks / impressions |
| Average CPC | `metrics.average_cpc` | cost / clicks (in micros) |
| Conversions | `metrics.conversions` | Uses primary conversion actions |
| Conversion Rate | `metrics.conversions_from_interactions_rate` | conversions / clicks |
| CPA | `metrics.cost_per_conversion` | cost / conversions (in micros) |
| Conversion Value | `metrics.conversions_value` | Revenue or value attributed |
| ROAS | Computed | conversions_value / (cost_micros / 1,000,000) |
| All Conversions | `metrics.all_conversions` | Includes secondary actions |

### Competitive Metrics

| Metric | GAQL Field | Notes |
|--------|-----------|-------|
| Search Impression Share | `metrics.search_impression_share` | % of available impressions won |
| Budget Lost IS | `metrics.search_budget_lost_impression_share` | % lost due to budget |
| Rank Lost IS | `metrics.search_rank_lost_impression_share` | % lost due to rank |

### Quality Metrics

| Metric | GAQL Field | Scale |
|--------|-----------|-------|
| Quality Score | `ad_group_criterion.quality_info.quality_score` | 1-10 |
| Ad Relevance | `ad_group_criterion.quality_info.creative_quality_score` | BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE |
| Landing Page Experience | `ad_group_criterion.quality_info.post_click_quality_score` | BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE |
| Expected CTR | `ad_group_criterion.quality_info.search_predicted_ctr` | BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE |
| Ad Strength | `ad_group_ad.ad.strength` | EXCELLENT, GOOD, AVERAGE, POOR |

---

## Data Considerations

### Conversion Lag
Recent conversion data may be incomplete. The Google Ads API reports conversions attributed to the click date, but conversions can take days or weeks to register. Always note this when analyzing recent data:
- For short conversion cycles (e-commerce): 3-7 day lag
- For long conversion cycles (B2B, SaaS): 14-30+ day lag

### Learning Period
Smart Bidding campaigns enter a learning period after significant changes. Performance during learning (typically 1-2 weeks) is not representative. Exclude learning period data from trend analysis.

### Statistical Significance
Do not draw conclusions from small samples:
- Keywords with fewer than 100 clicks: insufficient for conversion rate analysis
- Ad variations with fewer than 1,000 impressions: insufficient for CTR comparison
- Time periods shorter than 2 weeks: may reflect weekly seasonality

### Seasonality
Compare performance against the same period in previous years, not just the previous period. Week-over-week changes may reflect seasonality rather than optimization impact.
