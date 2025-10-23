# 🚀 Startup Idea Evaluation Report

## 📋 Executive Summary
**Idea:** {{idea}}  
**Target Market:** {{target_market}}  
**Evaluation Date:** {{timestamp}}  
**Overall Viability:** {{viability_label}} (Score: {{viability_score}}/100)

---

## 🏪 Market Analysis

### Market Overview
{{#market_analysis.market_summary}}
- **Market Size:** {{market_size}}
- **Market Maturity:** {{market_maturity}}
- **Growth Potential:** {{growth_potential}}
- **Key Trends:** {{#market_trends}}- {{.}}{{/market_trends}}
{{/market_analysis.market_summary}}

### Competitive Landscape
{{#market_analysis.competitors}}
**Competitive Intensity:** {{competitive_landscape}}

**Direct Competitors:**
{{#direct_competitors}}
- **{{name}}**
  - Strength: {{strength}}
  - Weakness: {{weakness}}
{{/direct_competitors}}

**Indirect Competitors:**
{{#indirect_competitors}}
- **{{name}}** (Threat Level: {{threat_level}})
{{/indirect_competitors}}
{{/market_analysis.competitors}}

### Customer Segments
{{#market_analysis.customer_segments}}
**Primary Segment:**
- **Description:** {{primary_segment.description}}
- **Size:** {{primary_segment.size}}
- **Pain Points:** {{#primary_segment.pain_points}}- {{.}}{{/primary_segment.pain_points}}
- **Willingness to Pay:** {{primary_segment.willingness_to_pay}}

**Secondary Segments:**
{{#secondary_segments}}
- **{{description}}** (Size: {{size}})
{{/secondary_segments}}
{{/market_analysis.customer_segments}}

---

## 💰 Financial Analysis

### Revenue Projections
{{#financial_analysis.revenue_projection}}
**Revenue Model:** {{revenue_model}}  
**Pricing Strategy:** {{pricing_strategy}}

| Year | Revenue | Customers | Avg Revenue/Customer | Growth Rate |
|------|---------|-----------|---------------------|-------------|
| Year 1 | ${{year_1.revenue}} | {{year_1.customers}} | ${{year_1.avg_revenue_per_customer}} | - |
| Year 2 | ${{year_2.revenue}} | {{year_2.customers}} | ${{year_2.avg_revenue_per_customer}} | {{year_2.growth_rate}} |
| Year 3 | ${{year_3.revenue}} | {{year_3.customers}} | ${{year_3.avg_revenue_per_customer}} | {{year_3.growth_rate}} |
{{/financial_analysis.revenue_projection}}

### Cost Analysis
{{#financial_analysis.costs}}
**Operational Costs by Year:**

| Year | Personnel | Technology | Marketing | Operations | Total |
|------|-----------|------------|-----------|------------|-------|
| Year 1 | ${{operational_costs.year_1.personnel}} | ${{operational_costs.year_1.technology}} | ${{operational_costs.year_1.marketing}} | ${{operational_costs.year_1.operations}} | ${{operational_costs.year_1.total}} |
| Year 2 | ${{operational_costs.year_2.personnel}} | ${{operational_costs.year_2.technology}} | ${{operational_costs.year_2.marketing}} | ${{operational_costs.year_2.operations}} | ${{operational_costs.year_2.total}} |
| Year 3 | ${{operational_costs.year_3.personnel}} | ${{operational_costs.year_3.technology}} | ${{operational_costs.year_3.marketing}} | ${{operational_costs.year_3.operations}} | ${{operational_costs.year_3.total}} |

**One-Time Costs:** ${{one_time_costs.total}}
- Initial Setup: ${{one_time_costs.initial_setup}}
- Equipment: ${{one_time_costs.equipment}}
- Legal: ${{one_time_costs.legal}}

**Cost Breakdown:** {{cost_breakdown}}
{{/financial_analysis.costs}}

### Breakeven Analysis
{{#financial_analysis.breakeven_analysis}}
- **Breakeven Month:** {{breakeven_month}}
- **Customers to Breakeven:** {{breakeven_customers}}
- **Customer Acquisition Cost:** ${{key_metrics.customer_acquisition_cost}}
- **Lifetime Value:** ${{key_metrics.lifetime_value}}
- **LTV/CAC Ratio:** {{key_metrics.lifetime_value_to_cac_ratio}}
- **Gross Margin:** {{key_metrics.gross_margin}}
{{/financial_analysis.breakeven_analysis}}

### Funding Requirements
{{#financial_analysis.funding_requirements}}
- **Total Funding Needed:** ${{total_funding_needed}}
- **Runway:** {{runway_months}} months
- **Funding Breakdown:**
  - Product Development: ${{funding_breakdown.product_development}}
  - Marketing: ${{funding_breakdown.marketing}}
  - Operations: ${{funding_breakdown.operations}}
  - Working Capital: ${{funding_breakdown.working_capital}}

**Funding Recommendations:** {{funding_recommendations}}
{{/financial_analysis.funding_requirements}}

---

## 🎯 Strategic Advisory

### Executive Summary
{{#advisor.executive_summary}}
**Overall Assessment:** {{overall_assessment}}  
**Strategic Position:** {{strategic_position}}

**Key Opportunities:**
{{#key_opportunities}}- {{.}}{{/key_opportunities}}

**Critical Challenges:**
{{#critical_challenges}}- {{.}}{{/critical_challenges}}
{{/advisor.executive_summary}}

### Risk Analysis
{{#advisor.risk_analysis}}
**Risk Summary:** {{risk_summary}}

**High Priority Risks:**
{{#high_priority_risks}}
- **{{risk}}** (Impact: {{impact}}, Probability: {{probability}})
  - Mitigation: {{mitigation}}
{{/high_priority_risks}}

**Medium Priority Risks:**
{{#medium_priority_risks}}
- **{{risk}}** (Impact: {{impact}}, Probability: {{probability}})
  - Mitigation: {{mitigation}}
{{/medium_priority_risks}}
{{/advisor.risk_analysis}}

### Strengths & Weaknesses
{{#advisor.strengths_weaknesses}}
**Key Strengths:**
{{#key_strengths}}
- **{{strength}}**
  - Impact: {{impact}}
  - Sustainability: {{sustainability}}
{{/key_strengths}}

**Key Weaknesses:**
{{#key_weaknesses}}
- **{{weakness}}**
  - Impact: {{impact}}
  - Improvement: {{improvement}}
{{/key_weaknesses}}
{{/advisor.strengths_weaknesses}}

### Recommendations
{{#advisor.recommendations}}
**Immediate Actions:**
{{#immediate_actions}}
- **{{action}}** (Priority: {{priority}}, Timeline: {{timeline}})
  - Expected Impact: {{expected_impact}}
{{/immediate_actions}}

**Strategic Recommendations:**
{{#strategic_recommendations}}
- **{{recommendation}}**
  - Rationale: {{rationale}}
  - Implementation: {{implementation}}
{{/strategic_recommendations}}

**Partnership Opportunities:**
{{#partnership_opportunities}}
- {{.}}
{{/partnership_opportunities}}
{{/advisor.recommendations}}

### Viability Assessment
{{#advisor.viability_assessment}}
**Overall Score:** {{viability_score}}/100 ({{viability_label}})

**Scoring Breakdown:**
- Market Opportunity: {{scoring_breakdown.market_opportunity}}/20
- Competitive Advantage: {{scoring_breakdown.competitive_advantage}}/20
- Financial Feasibility: {{scoring_breakdown.financial_feasibility}}/20
- Team Execution: {{scoring_breakdown.team_execution}}/20
- Market Timing: {{scoring_breakdown.market_timing}}/20

**Key Success Factors:**
{{#key_success_factors}}- {{.}}{{/key_success_factors}}

**Failure Risks:**
{{#failure_risks}}- {{.}}{{/failure_risks}}
{{/advisor.viability_assessment}}

### Next Steps
{{#advisor.next_steps}}
**Immediate Priorities:**
{{#immediate_priorities}}- {{.}}{{/immediate_priorities}}

**Key Milestones:**
{{#milestones}}
- **{{milestone}}** (Timeline: {{timeline}})
  - Success Metrics: {{success_metrics}}
{{/milestones}}

**Funding Recommendations:** {{funding_recommendations}}
{{/advisor.next_steps}}

### Market Positioning
{{#advisor.market_positioning}}
**Unique Value Proposition:** {{unique_value_proposition}}  
**Competitive Differentiation:** {{competitive_differentiation}}  
**Customer Validation Strategy:** {{target_customer_validation}}  
**Go-to-Market Strategy:** {{go_to_market_strategy}}
{{/advisor.market_positioning}}

---

## 📊 Summary

**Final Viability Score:** {{viability_score}}/100 ({{viability_label}})

This comprehensive analysis provides a detailed evaluation of your startup idea across market opportunity, financial feasibility, and strategic positioning. Use the recommendations and next steps to refine your approach and increase your chances of success.

---
*Report generated on {{timestamp}}*
