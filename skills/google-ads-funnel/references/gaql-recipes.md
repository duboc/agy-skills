# GAQL Recipes for Funnel-as-Code Workflows

This reference contains ready-to-use GAQL query patterns for each workflow. Adapt date ranges, filters, and limits to the user's specific request.

**Important**: Compute all dates dynamically at runtime. Never use constants like `LAST_30_DAYS`. The Google Ads API Developer Assistant extension handles date computation in generated code.

---

## Account Structure

### Active campaigns overview

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    campaign.advertising_channel_type,
    campaign.bidding_strategy_type,
    campaign_budget.amount_micros,
    campaign_budget.delivery_method,
    metrics.cost_micros,
    metrics.impressions,
    metrics.clicks,
    metrics.conversions,
    metrics.conversions_value
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
```

### Ad groups per campaign

```sql
SELECT
    campaign.id,
    campaign.name,
    ad_group.id,
    ad_group.name,
    ad_group.status,
    ad_group.type,
    metrics.cost_micros,
    metrics.conversions
FROM ad_group
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY campaign.id, metrics.cost_micros DESC
```

### Ads per ad group

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_ad.ad.id,
    ad_group_ad.ad.type,
    ad_group_ad.status,
    ad_group_ad.ad.responsive_search_ad.headlines,
    ad_group_ad.ad.responsive_search_ad.descriptions,
    ad_group_ad.policy_summary.approval_status
FROM ad_group_ad
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND ad_group_ad.status = 'ENABLED'
```

---

## Spend Analysis

### Campaign cost and efficiency

```sql
SELECT
    campaign.id,
    campaign.name,
    metrics.cost_micros,
    metrics.impressions,
    metrics.clicks,
    metrics.ctr,
    metrics.average_cpc,
    metrics.conversions,
    metrics.cost_per_conversion,
    metrics.conversions_value,
    metrics.conversions_from_interactions_rate
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
```

### Impression share analysis

```sql
SELECT
    campaign.id,
    campaign.name,
    metrics.search_impression_share,
    metrics.search_budget_lost_impression_share,
    metrics.search_rank_lost_impression_share,
    metrics.cost_micros,
    metrics.conversions
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND campaign.advertising_channel_type = 'SEARCH'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.search_budget_lost_impression_share DESC
```

### Keyword spend with zero conversions

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    metrics.cost_micros,
    metrics.clicks,
    metrics.impressions,
    metrics.conversions
FROM keyword_view
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND metrics.conversions = 0
    AND metrics.cost_micros > 0
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

### Device performance breakdown

```sql
SELECT
    campaign.name,
    segments.device,
    metrics.cost_micros,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_per_conversion,
    metrics.conversions_from_interactions_rate
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY campaign.name, segments.device
```

### Hour-of-day performance

```sql
SELECT
    campaign.name,
    segments.hour,
    metrics.cost_micros,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_per_conversion
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY campaign.name, segments.hour
```

### Day-of-week performance

```sql
SELECT
    campaign.name,
    segments.day_of_week,
    metrics.cost_micros,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_per_conversion
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY campaign.name, segments.day_of_week
```

### Geographic performance

```sql
SELECT
    campaign.name,
    geographic_view.country_criterion_id,
    geographic_view.location_type,
    metrics.cost_micros,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_per_conversion
FROM geographic_view
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

---

## Quality Signals

### Keyword quality scores

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    ad_group_criterion.quality_info.quality_score,
    ad_group_criterion.quality_info.creative_quality_score,
    ad_group_criterion.quality_info.post_click_quality_score,
    ad_group_criterion.quality_info.search_predicted_ctr,
    metrics.cost_micros,
    metrics.impressions
FROM keyword_view
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND ad_group_criterion.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY ad_group_criterion.quality_info.quality_score ASC
```

### Disapproved ads

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_ad.ad.id,
    ad_group_ad.ad.type,
    ad_group_ad.policy_summary.approval_status,
    ad_group_ad.policy_summary.policy_topic_entries
FROM ad_group_ad
WHERE ad_group_ad.policy_summary.approval_status != 'APPROVED'
    AND campaign.status = 'ENABLED'
```

---

## Creative Performance

### RSA asset performance

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_ad.ad.id,
    ad_group_ad.ad.responsive_search_ad.headlines,
    ad_group_ad.ad.responsive_search_ad.descriptions,
    ad_group_ad.ad.strength,
    metrics.impressions,
    metrics.clicks,
    metrics.ctr,
    metrics.conversions,
    metrics.cost_micros
FROM ad_group_ad
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND ad_group_ad.status = 'ENABLED'
    AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.impressions DESC
```

### Ad strength distribution

```sql
SELECT
    ad_group_ad.ad.strength,
    metrics.impressions,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_micros
FROM ad_group_ad
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND ad_group_ad.status = 'ENABLED'
    AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
```

### Auction insights (competitive data)

```sql
SELECT
    campaign.name,
    metrics.auction_insight_search_impression_share,
    metrics.auction_insight_search_overlap_rate,
    metrics.auction_insight_search_outranking_share,
    metrics.auction_insight_search_position_above_rate,
    metrics.auction_insight_search_top_impression_percentage
FROM campaign_audience_view
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
```

---

## Search Terms

### Search term report with performance

```sql
SELECT
    campaign.name,
    ad_group.name,
    search_term_view.search_term,
    search_term_view.status,
    segments.search_term_match_type,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value
FROM search_term_view
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

### High-spend non-converting search terms

```sql
SELECT
    campaign.name,
    ad_group.name,
    search_term_view.search_term,
    segments.search_term_match_type,
    metrics.cost_micros,
    metrics.clicks,
    metrics.impressions
FROM search_term_view
WHERE campaign.status = 'ENABLED'
    AND metrics.conversions = 0
    AND metrics.cost_micros > 0
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

---

## Conversion Tracking

### All conversion actions

```sql
SELECT
    conversion_action.id,
    conversion_action.name,
    conversion_action.category,
    conversion_action.type,
    conversion_action.status,
    conversion_action.primary_for_goal,
    conversion_action.attribution_model_settings.attribution_model,
    conversion_action.counting_type,
    conversion_action.click_through_lookback_window_days,
    conversion_action.view_through_lookback_window_days
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
ORDER BY conversion_action.name
```

### Conversion volume by day

```sql
SELECT
    segments.date,
    segments.conversion_action_name,
    metrics.conversions,
    metrics.conversions_value,
    metrics.all_conversions,
    metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY segments.date DESC, segments.conversion_action_name
```

### Conversion action performance summary

```sql
SELECT
    segments.conversion_action_name,
    segments.conversion_action_category,
    metrics.conversions,
    metrics.conversions_value,
    metrics.cost_per_conversion
FROM campaign
WHERE campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.conversions DESC
```

---

## Campaign Structure

### Keyword overlap detection

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    metrics.impressions,
    metrics.cost_micros
FROM keyword_view
WHERE campaign.status = 'ENABLED'
    AND ad_group.status = 'ENABLED'
    AND ad_group_criterion.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY ad_group_criterion.keyword.text, campaign.name
```

### Shared budget utilization

```sql
SELECT
    campaign_budget.name,
    campaign_budget.amount_micros,
    campaign_budget.total_amount_micros,
    campaign_budget.explicitly_shared,
    campaign.name,
    campaign.status,
    metrics.cost_micros
FROM campaign
WHERE campaign_budget.explicitly_shared = TRUE
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY campaign_budget.name, campaign.name
```

### Performance Max campaigns

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    campaign_budget.amount_micros,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value,
    metrics.cost_per_conversion
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
    AND campaign.status = 'ENABLED'
    AND segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.cost_micros DESC
```

---

## Notes on GAQL Usage

- **Date segments**: If `segments.date` appears in SELECT, a finite date range filter is required in WHERE.
- **Metrics currency**: `cost_micros` values are in micros (divide by 1,000,000 for actual currency).
- **Match type segment**: `segments.search_term_match_type` must be in SELECT if used in WHERE.
- **Field compatibility**: Not all metrics are available on all resources. The extension validates fields before execution.
- **Streaming**: The extension uses `SearchGoogleAdsStream` for result retrieval. Large result sets are handled automatically.
- **Rate limits**: Be mindful of API quota when running multiple queries. Chain queries sequentially rather than in parallel.
