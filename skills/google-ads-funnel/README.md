# Google Ads Funnel-as-Code

A Agy skill that provides structured workflows for Google Ads account management using the Funnel-as-Code methodology. Works with the [Google Ads API Developer Assistant](https://github.com/googleads/google-ads-api-developer-assistant) extension for API access and code execution.

## What It Does

This skill treats your Google Ads account as a system that can be queried, analyzed, and optimized programmatically through the CLI rather than manual dashboard navigation. It provides six structured workflows:

1. **Account Health Audit** — Systematic inspection covering structure, spend, quality, and tracking with a scored report and prioritized action items.
2. **Spend Efficiency Analysis** — Deep analysis of budget allocation, wasted spend, and optimization opportunities across keywords, devices, schedules, and geographies.
3. **Creative Performance Lab** — RSA asset analysis, ad strength review, competitive positioning, and creative testing recommendations.
4. **Search Term Mining** — Categorized search term analysis with negative keyword lists and keyword expansion opportunities.
5. **Conversion Funnel Diagnostics** — Conversion tracking health checks, volume trend analysis, attribution review, and funnel stage metrics.
6. **Campaign Structure Review** — Account hierarchy evaluation, anti-pattern detection, and restructuring recommendations.

## Prerequisites

This skill requires the **Google Ads API Developer Assistant extension** to be installed and configured. The extension provides:

- GAQL query generation and validation
- Python code generation for API calls
- Direct API execution from the CLI
- CSV export of results

Install the extension:

```bash
git clone https://github.com/googleads/google-ads-api-developer-assistant
cd google-ads-api-developer-assistant
./setup.sh
```

You also need:
- A Google Ads API developer token
- Configured API credentials
- A customer ID for the account to analyze

## When Does It Activate?

The skill activates when you ask Agy about Google Ads performance or management:

```
Audit my Google Ads account
```

```
Where am I wasting ad spend?
```

```
Analyze my campaign performance for the last 30 days
```

```
Find negative keyword opportunities from my search terms
```

```
Check if my conversion tracking is set up correctly
```

```
Review my RSA creative performance
```

## How It Works

```
User Request → Skill selects workflow → GAQL queries constructed
                                              ↓
Report generated ← Data analyzed ← Extension executes queries
      ↓
Recommendations with code (review before running)
```

1. The skill identifies the appropriate workflow based on the user's request.
2. It constructs GAQL queries using recipes from the reference files.
3. The Google Ads API Developer Assistant extension generates and executes Python code for each query.
4. Results are analyzed through the workflow's framework.
5. A structured report is generated with findings and recommendations.
6. For any changes, code is generated but never auto-executed — the user reviews and runs it.

## Workflow Selection

| If you want to... | Use this workflow |
|-------------------|-------------------|
| Get a full account health check | Account Health Audit |
| Find and eliminate wasted spend | Spend Efficiency Analysis |
| Improve your ad creative | Creative Performance Lab |
| Clean up search terms and keywords | Search Term Mining |
| Verify conversion tracking | Conversion Funnel Diagnostics |
| Evaluate account organization | Campaign Structure Review |

Workflows can be combined for deeper analysis. See `references/funnel-playbook.md` for common combinations.

## Installation

### Option A: Agy native

```bash
agy skills install https://github.com/duboc/agy-skills.git --path skills/google-ads-funnel
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- google-ads-funnel
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- google-ads-funnel --scope user
```

### Option C: Manual

```bash
cp -r skills/google-ads-funnel ~/.gemini/config/skills/google-ads-funnel
```

## Usage Examples

### Full account audit

```
Run a complete health audit on my Google Ads account for the last 30 days.
My customer ID is 123-456-7890.
```

### Find wasted spend

```
Analyze my search terms from the past 60 days and find where I'm wasting money.
Generate a negative keyword list I can apply.
```

### Creative testing

```
Review my RSA performance across all campaigns. Which headlines and descriptions
should I replace? Suggest new variations based on what's working.
```

### Conversion tracking check

```
Check all my conversion actions and tell me if anything looks misconfigured.
I'm seeing fewer conversions this month and want to rule out tracking issues.
```

### Campaign restructuring

```
Review my campaign structure. I have 40 campaigns and think I need to consolidate.
Show me which ones overlap and recommend a cleaner organization.
```

### Budget reallocation

```
Show me the Pareto distribution of my campaigns — which 20% drive 80% of conversions?
Then recommend how to reallocate budget from the underperformers.
```

## Included References

| File | Description |
|------|-------------|
| `references/audit-checklist.md` | 40+ point audit checklist organized by category (Structure, Bidding, Keywords, Creative, Tracking, Targeting, Spend) with severity ratings and scoring guide |
| `references/gaql-recipes.md` | Ready-to-use GAQL query patterns for every workflow — account structure, spend analysis, quality signals, creative performance, search terms, conversions, and campaign structure |
| `references/funnel-playbook.md` | The Funnel-as-Code methodology explained: the analysis loop, workflow selection guide, workflow combinations, metrics reference, and data considerations (conversion lag, learning periods, statistical significance) |

## Safety

This skill follows a strict **read-only by default** policy:

- All queries are read-only (`search` / `get` operations only)
- Mutate operations (pausing keywords, adding negatives, changing bids) generate code but never execute automatically
- The user must review and manually run any code that modifies the account
- This matches the Google Ads API Developer Assistant extension's own safety policies
