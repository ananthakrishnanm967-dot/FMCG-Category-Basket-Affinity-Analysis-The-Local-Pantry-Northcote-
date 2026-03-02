FMCG Category & Basket Affinity Analysis — The Local Pantry (Northcote)
Problem Statement

Independent grocery retailers often operate without structured transaction-level analytics. While sales totals may be available, deeper insights into which products drive baskets, which items are purchased together, and how categories interact are typically not quantified.

Without this analysis, merchandising decisions such as shelf placement, bundling, and promotional targeting rely on intuition rather than measurable basket behaviour.

This project applies basket affinity modelling to 14,963 transaction baskets to identify:

High-frequency co-purchase patterns

Cross-category relationships

Basket size behaviour

Commercially actionable cross-sell opportunities

The objective is to translate transaction data into measurable merchandising strategies.

Key Insights
1. Milk Functions as a Basket Anchor

Whole milk appears in the highest-frequency co-purchase pairs.

The top pair (Other Vegetables + Whole Milk) occurs in 1.48% of all baskets (~222 baskets).

Multiple top-10 pairs include milk as a component.

This indicates that dairy staples act as anchor products around which other purchases cluster.

2. Produce–Dairy and Bakery–Dairy Show Strong Co-Occurrence

Category-level aggregation reveals:

Produce–Dairy and Bakery–Dairy combinations show the highest average support.

These patterns reflect meal-based and breakfast-based shopping missions.

This suggests natural cross-merchandising zones.

3. Basket Size Indicates Mission Shopping Behaviour

Basket size distribution analysis shows:

Majority of baskets contain 2–3 items

Very few exceed 6 items

This indicates the store operates primarily as a top-up / mission-based retailer rather than a weekly bulk shopping destination.

4. High Lift Does Not Equal High Revenue Impact

Some item pairs show high statistical lift but extremely low support (rare combinations).

This highlights a key retail principle:

Frequency (support) drives revenue impact

Rare but statistically strong pairs are commercially insignificant

Business Recommendations

Based on the quantified findings:

1. Position Anchor Products Strategically

Place high-frequency anchor items (e.g., milk) near high-affinity categories such as:

Produce

Bakery

Yogurt and secondary dairy

2. Create Mission-Based Bundles

Examples:

Breakfast bundle: Milk + Rolls

Cooking bundle: Vegetables + Dairy

Even small bundle conversion improvements can increase average basket value.

3. Optimize Store Layout by Category Affinity

Align shelving zones to reflect observed category co-occurrence rather than traditional category silos.

4. Focus on High-Support Pairs for Promotions

Prioritize high-frequency combinations over rare high-lift anomalies.

Methodology
Dataset

14,963 unique baskets

Transaction-level grocery data

Each basket defined as: Member ID + Date

Item-level purchase records

Basket Construction

Each unique shopping visit was converted into a Basket ID.

Example:
Member_1808 + 21-07-2015 → One basket

Association Metrics Defined

Three core metrics were calculated for every item pair:

Support

Support measures how frequently two items appear together across all baskets.

Formula:

Support(A,B) =
Number of baskets containing both A and B
divided by
Total number of baskets

Interpretation:
If Support = 0.0148, then 1.48% of all baskets contain both items.

Support indicates commercial frequency.

Confidence

Confidence measures conditional probability.

Confidence(A→B) =
Probability of B appearing in a basket given A is already present.

Interpretation:
If Confidence = 0.12, then 12% of shoppers who buy A also buy B.

Lift

Lift measures how much more likely two items are purchased together compared to random chance.

Lift(A,B) =
Observed co-occurrence
divided by
Expected co-occurrence under independence

Interpretation:

Lift > 1 → Stronger than random association

Lift = 1 → Independent

Lift < 1 → Slightly weaker than independence

In staple-heavy grocery datasets, lift often remains below 1 due to high marginal probabilities.

Stability Filtering

To avoid statistical noise:

Only pairs appearing in at least 30 baskets were retained.

This removed rare, artificially inflated lift combinations.

Category Mapping

Items were programmatically mapped into retail categories:

Dairy

Bakery

Produce

Beverages

Meat

Household

Other

This enabled category-level aggregation and cross-category insight generation.

Visual Analysis Explained
1. Basket Size Distribution

This histogram shows the number of items per basket.

Key takeaway:
The concentration at 2–3 items confirms mission-based shopping behaviour.

Interpretation for stakeholders:
Most customers are entering with a specific need rather than conducting full weekly grocery runs.

2. Category Affinity Heatmap

This matrix shows the average support between category pairs.

Brighter cells indicate higher average co-purchase frequency.

Interpretation:
Produce–Dairy and Bakery–Dairy combinations are most commercially meaningful.

This supports adjacency planning in store layout.

3. Support vs Lift Scatter Plot

Each bubble represents one item pair.

X-axis: Support (frequency)

Y-axis: Lift (strength relative to independence)

Bubble size: Support magnitude

Interpretation:
High-lift pairs often occur infrequently.
High-support pairs drive revenue impact.

This visualization clarifies the trade-off between statistical strength and commercial significance.

Quantifiable Outcomes

14,963 baskets analysed

200+ SKUs evaluated

Top pair frequency: 1.48% of all baskets (~222 occurrences)

Majority basket size: 2–3 items

Stable pairs filtered using ≥30 basket threshold

Category-level cross-affinity matrix constructed

Tools Used

Python (pandas, itertools, matplotlib)

Association Rule Metrics (Support, Confidence, Lift)

Retail Category Mapping

Basket Construction Logic
