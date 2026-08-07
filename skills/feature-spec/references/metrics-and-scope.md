# Success Metrics, Counter-Metrics and Scope Management

## Metric Framework

### 1. Leading Indicators
Immediate telemetry signals of adoption and usability (0–30 days post-launch):
- **Activation Rate**: % of eligible users who complete the core action within 7 days.
- **Task Completion Rate**: % of initiated user flows completed without error or dropoff.
- **Time to First Value (TTFV)**: Duration from landing to completing the core action.
- **Feature Frequency**: # of repeat feature invocations per active user per week.

### 2. Lagging Indicators
Long-term business and retention impacts (30–90+ days post-launch):
- **Retention Delta**: Difference in 30/60/90-day retention between users who adopt the feature vs non-users.
- **LTV / Expansion Revenue**: Impact on upsells, seat additions, or tier upgrades.
- **NPS / CSAT Impact**: Net score change in user satisfaction surveys post-launch.

### 3. Safeguard Counter-Metrics
Guardrail metrics ensuring feature adoption does not degrade overall product health:
- **Support Ticket Velocity**: Ensures new feature doesn't drive support ticket spikes (`< 5%` total ticket volume).
- **System Latency / CPU Load**: Ensures background processing or logging doesn't degrade overall app latency.
- **Unsubscribe / Churn Rate**: Ensures engagement features do not feel intrusive or spammy.

---

## Scope Bounding & Scope Creep Prevention

### The Scope Trade-off Equalizer
When new requirements emerge mid-flight, enforce the strict Trade-off Rule:

```
[ New Requirement Introduced ]  →  MUST  →  [ Extend Target Release Date ]
                                     OR  →  [ Remove Equivalent P0/P1 Story ]
                                     OR  →  [ Move to v2 Scope Parking Lot ]
```

### Scope Creep Red Flags
- Requirements introduced without supporting user pain or telemetry data.
- "While we're refactoring this module..." engineering add-ons.
- Shifting launch dates without explicit stakeholder re-commitment.
