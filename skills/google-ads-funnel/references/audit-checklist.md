# Account Health Audit Checklist

Use this checklist to guide a systematic account inspection. Each section maps to GAQL queries in `gaql-recipes.md`.

---

## 1. Account Structure

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Campaign count | More than 25 active campaigns may indicate fragmentation | Medium |
| Campaign naming | Inconsistent naming conventions make management harder | Low |
| Campaign types | Mix of Search, PMax, Display, Video — is each type justified? | Medium |
| Ad groups per campaign | More than 20 ad groups per campaign reduces control | Medium |
| Keywords per ad group | More than 30 keywords per ad group dilutes relevance | Medium |
| Ads per ad group | Fewer than 2 active ads limits testing capability | High |
| Single keyword ad groups | SKAGs may be legacy structure worth consolidating | Low |
| Paused entities | Large numbers of paused campaigns/ad groups add clutter | Low |

## 2. Bidding and Budgets

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Bidding strategy alignment | Similar campaigns using different strategies without reason | Medium |
| Budget-limited campaigns | Impression share lost to budget > 10% on converting campaigns | High |
| Shared budgets | Shared budgets causing one campaign to starve another | High |
| Target CPA/ROAS targets | Targets set too aggressively (limiting volume) or too loosely (wasting spend) | High |
| Maximize conversions without target | Campaigns set to maximize with no cap — can overspend | Medium |
| Budget distribution | Top campaign consuming > 60% of total budget — is this intentional? | Medium |

## 3. Keyword Health

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Zero-conversion keywords | Keywords with significant spend (> 2x target CPA) and no conversions | High |
| Low quality scores | Keywords with QS below 5 — especially high-spend ones | High |
| Quality score components | Which component is weakest: relevance, landing page, or CTR? | Medium |
| Match type distribution | Over-reliance on broad match without smart bidding | Medium |
| Keyword overlap | Same keyword in multiple ad groups/campaigns (cannibalization) | High |
| Negative keyword coverage | Are negatives in place to prevent waste? | High |
| Keyword to search term ratio | High ratio of irrelevant search terms to keywords | Medium |

## 4. Ad Creative

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| RSA adoption | Any ad groups still running only ETAs (legacy) | Medium |
| Ad strength | RSAs with "Poor" or "Average" strength | Medium |
| Headline count | RSAs with fewer than 8 unique headlines | Medium |
| Description count | RSAs with fewer than 3 unique descriptions | Medium |
| Asset performance labels | Assets rated "Low" that should be replaced | High |
| Pinning overuse | More than 30% of assets pinned reduces optimization flexibility | Medium |
| Disapproved ads | Any ads with policy violations | Critical |
| Ad variation testing | Ad groups with only 1 active ad | High |

## 5. Conversion Tracking

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Conversion actions defined | At least one primary conversion action exists | Critical |
| Primary vs secondary | Are the right actions marked as primary for bidding? | Critical |
| Zero-conversion actions | Enabled conversion actions with no conversions in 30 days | High |
| Counting method | Lead gen using "every" instead of "one" (inflates numbers) | High |
| Attribution model | Using last-click when data-driven is available | Medium |
| Lookback windows | Windows appropriate for the sales cycle | Medium |
| Conversion lag | Recent data may be incomplete due to lag — flag this | Medium |
| Duplicate tracking | Multiple actions tracking the same event | High |

## 6. Audience and Targeting

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Location targeting | Targeting "presence or interest" when "presence" is more appropriate | Medium |
| Language targeting | Mismatched language targeting for the market | Medium |
| Audience segments | Are observation audiences attached for learning? | Low |
| Remarketing lists | Active remarketing lists with sufficient size? | Medium |
| Customer match | Are customer lists uploaded and current? | Low |
| Exclusion lists | Are existing customers excluded from acquisition campaigns? | Medium |

## 7. Spend Efficiency

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Cost per conversion trend | CPA trending upward over 30/60/90 days | High |
| ROAS trend | ROAS trending downward | High |
| Wasted spend ratio | Spend on non-converting terms / total spend > 20% | High |
| Device performance gaps | One device with 3x+ CPA compared to others | Medium |
| Time-of-day waste | Specific hours with high spend and zero conversions | Medium |
| Geographic waste | Locations with spend but no conversions | Medium |
| Campaign efficiency spread | Campaigns with CPA more than 2x account average | High |

---

## Scoring Guide

### Category Scores

For each category, assign a score based on findings:

| Score | Criteria |
|-------|----------|
| **Optimized** | No critical or high-severity issues. Minor improvements only. |
| **Healthy** | No critical issues. 1-2 high-severity issues identified. |
| **Needs Attention** | 1+ critical or 3+ high-severity issues found. |
| **Critical** | Multiple critical issues affecting spend efficiency or tracking accuracy. |

### Overall Health Score

The overall score is the lowest category score. One critical category brings the entire account to that level.

### Impact Estimation

When recommending actions, estimate impact as:

| Impact | Criteria |
|--------|----------|
| **High** | Expected to affect > 10% of account spend or conversions |
| **Medium** | Expected to affect 3-10% of account spend or conversions |
| **Low** | Expected to affect < 3% of account spend or conversions |

Priority = Severity x Impact. Address Critical+High items first.
