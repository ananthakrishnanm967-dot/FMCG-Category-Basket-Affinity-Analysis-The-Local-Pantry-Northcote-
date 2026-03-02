import os
from itertools import combinations
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# 0) CONFIG
# -----------------------------
DATA_PATH = "/kaggle/input/datasets/ananthumurali/northcote/Groceries_dataset.csv"
MIN_BASKETS = 30
HEATMAP_METRIC = "Support"   # "Support" recommended for this dataset

OUTPUT_DIR = "."
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)


# -----------------------------
# 1) LOAD + BASKET BUILD
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Basket ID = Member + Date (as used in your project)
df["BasketID"] = df["Member_number"].astype(str) + "_" + df["Date"].astype(str)

# Basket list per BasketID
basket = df.groupby("BasketID")["itemDescription"].apply(list)
total_baskets = len(basket)

print(f"Loaded rows: {len(df):,}")
print(f"Total baskets: {total_baskets:,}")


# -----------------------------
# 2) ITEM-PAIR AFFINITY (Support/Confidence/Lift)
# -----------------------------
item_counts = Counter()
pair_counts = Counter()

for items in basket:
    unique_items = list(set(items))
    for item in unique_items:
        item_counts[item] += 1
    for a, b in combinations(sorted(unique_items), 2):
        pair_counts[(a, b)] += 1

rows = []
for (a, b), count_ab in pair_counts.items():
    support_ab = count_ab / total_baskets
    support_a = item_counts[a] / total_baskets
    support_b = item_counts[b] / total_baskets

    confidence_a_b = support_ab / support_a if support_a else 0
    confidence_b_a = support_ab / support_b if support_b else 0
    lift = support_ab / (support_a * support_b) if (support_a and support_b) else 0

    rows.append([a, b, support_ab, confidence_a_b, confidence_b_a, lift])

affinity = pd.DataFrame(
    rows,
    columns=["Item_A", "Item_B", "Support", "Confidence_A_to_B", "Confidence_B_to_A", "Lift"]
)

# Stable pairs filter (avoid 1-basket “fake” lift)
affinity_clean = affinity[(affinity["Support"] * total_baskets) >= MIN_BASKETS].copy()

# Sort by Support (commercial frequency first)
affinity_clean = affinity_clean.sort_values(["Support"], ascending=False).reset_index(drop=True)


# -----------------------------
# 3) CATEGORY MAPPING
# -----------------------------
def map_category(item: str) -> str:
    item = str(item).lower()

    if any(x in item for x in ["milk", "yogurt", "cream", "butter", "curd", "margarine"]):
        return "Dairy"
    if any(x in item for x in ["bread", "roll", "bun"]):
        return "Bakery"
    if any(x in item for x in ["vegetable", "fruit", "apple", "banana", "citrus",
                               "onion", "tomato", "potato", "carrot", "root"]):
        return "Produce"
    if any(x in item for x in ["beer", "wine", "water", "juice", "soda", "coffee", "tea"]):
        return "Beverages"
    if any(x in item for x in ["sausage", "chicken", "beef", "pork", "meat"]):
        return "Meat"
    if any(x in item for x in ["detergent", "cleaner", "napkin", "bag"]):
        return "Household"
    return "Other"

affinity_clean["Cat_A"] = affinity_clean["Item_A"].apply(map_category)
affinity_clean["Cat_B"] = affinity_clean["Item_B"].apply(map_category)

# Add Rank and reorder columns
affinity_clean["Rank"] = np.arange(1, len(affinity_clean) + 1)

affinity_clean = affinity_clean[
    ["Rank", "Item_A", "Item_B", "Support",
     "Confidence_A_to_B", "Confidence_B_to_A",
     "Lift", "Cat_A", "Cat_B"]
]

# Save final clean table
affinity_clean.to_csv(os.path.join(OUTPUT_DIR, "basket_affinity_pairs_clean_final.csv"), index=False)
print("Saved: basket_affinity_pairs_clean_final.csv")


# -----------------------------
# 4) BASKET SIZE DISTRIBUTION TABLE
# -----------------------------
basket_size = df.groupby("BasketID")["itemDescription"].nunique().reset_index()
basket_size.columns = ["BasketID", "ItemsInBasket"]
basket_size.to_csv(os.path.join(OUTPUT_DIR, "basket_size_distribution.csv"), index=False)
print("Saved: basket_size_distribution.csv")


# -----------------------------
# 5) VISUAL 1: CATEGORY HEATMAP (single colour, labelled)
# -----------------------------
df_pairs = affinity_clean.copy()
metric = HEATMAP_METRIC

# Keep only non-Other for readability (optional)
df_pairs_hm = df_pairs[(df_pairs["Cat_A"] != "Other") & (df_pairs["Cat_B"] != "Other")].copy()

mat = (df_pairs_hm
       .groupby(["Cat_A", "Cat_B"], as_index=False)[metric]
       .mean()
       .pivot(index="Cat_A", columns="Cat_B", values=metric)
       .fillna(0.0))

mat = mat.sort_index().reindex(sorted(mat.columns), axis=1)

values = mat.values
rows = mat.index.tolist()
cols = mat.columns.tolist()

fig, ax = plt.subplots(figsize=(9, 6))
im = ax.imshow(values, cmap="Blues", aspect="auto")

ax.set_xticks(np.arange(len(cols)))
ax.set_yticks(np.arange(len(rows)))
ax.set_xticklabels(cols, rotation=35, ha="right")
ax.set_yticklabels(rows)

ax.set_title(f"Category Affinity Heatmap (Avg {metric})")
ax.set_xlabel("Category B")
ax.set_ylabel("Category A")

fmt = "{:.3f}" if metric == "Support" else "{:.2f}"
vmax = values.max() if values.size else 1

for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        v = values[i, j]
        ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=9, color="black")

cbar = fig.colorbar(im, ax=ax)
cbar.set_label(f"Avg {metric}")

plt.tight_layout()
heatmap_path = os.path.join(IMAGES_DIR, "category_affinity_heatmap.png")
plt.savefig(heatmap_path, dpi=200)
plt.close()
print(f"Saved: {heatmap_path}")


# -----------------------------
# 6) VISUAL 2: BASKET SIZE HISTOGRAM
# -----------------------------
basket_sizes = basket.apply(lambda x: len(set(x)))

plt.figure(figsize=(8, 5))
plt.hist(
    basket_sizes,
    bins=range(1, int(basket_sizes.max()) + 2),
    color="#4C72B0",
    edgecolor="black"
)
plt.title("Basket Size Distribution")
plt.xlabel("Items per Basket")
plt.ylabel("Number of Baskets")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()

hist_path = os.path.join(IMAGES_DIR, "basket_size_distribution.png")
plt.savefig(hist_path, dpi=200)
plt.close()
print(f"Saved: {hist_path}")


# -----------------------------
# 7) VISUAL 3: SUPPORT vs LIFT SCATTER (bubble size ~ support)
# -----------------------------
aff3 = affinity.copy()
aff3 = aff3[aff3["Support"] > 0.001].copy()
aff3["Cat_A"] = aff3["Item_A"].apply(map_category)

plt.figure(figsize=(8, 5))
plt.scatter(
    aff3["Support"],
    aff3["Lift"],
    s=(aff3["Support"] * 20000).clip(10, 200),
    alpha=0.7
)
plt.title("Support vs Lift (Bubble size ~ Support)")
plt.xlabel("Support")
plt.ylabel("Lift")
plt.tight_layout()

scatter_path = os.path.join(IMAGES_DIR, "support_vs_lift_scatter.png")
plt.savefig(scatter_path, dpi=200)
plt.close()
print(f"Saved: {scatter_path}")


print("Done.")
