import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

# -----------------------------
# 1. Data Generators
# -----------------------------
def generate_scenario_a():
    np.random.seed(10)
    n_jobs = 20
    jobs = pd.DataFrame({"Job": [f"J{i+1}" for i in range(n_jobs)]})
    jobs["w"] = np.random.randint(1, 10, n_jobs)
    jobs["p"] = np.random.randint(50, 150, n_jobs) 
    jobs["d"] = np.random.randint(100, 1500, n_jobs)
    return jobs

def generate_scenario_b():
    np.random.seed(42)
    n_jobs = 40
    jobs = pd.DataFrame({"Job": [f"J{i+1}" for i in range(n_jobs)]})
    jobs["w"] = np.random.randint(1, 50, n_jobs) # Massive urgency variance
    jobs["p"] = np.random.randint(1, 10, n_jobs) 
    total_p = jobs["p"].sum()
    base_due_dates = np.random.randint(int(0.5 * total_p), int(1.0 * total_p), n_jobs)
    jobs["d"] = (base_due_dates - jobs["w"] * 4).clip(lower=jobs["p"] + 1)
    return jobs

# -----------------------------
# 2. Detailed Metrics Tracker
# -----------------------------
def get_detailed_metrics(sequence, rule_name):
    time = 0
    records = []
    for _, row in sequence.iterrows():
        time += row["p"]
        tard = max(0, time - row["d"])
        records.append({
            "Job": row["Job"],
            "Rule": rule_name,
            "Flow Time": time,
            "Tardiness": tard,
            "Weighted Tardiness": tard * row["w"],
            "Is Late": "Late" if tard > 0 else "On Time"
        })
    return pd.DataFrame(records)

def spt_schedule(jobs): return jobs.sort_values("p")
def edd_schedule(jobs): return jobs.sort_values("d")

# -----------------------------
# 3. The Hybrid Rules
# -----------------------------
def traditional_hybrid_schedule(jobs, alpha):
    remaining = jobs.copy()
    time = 0
    sequence = []
    while not remaining.empty:
        remaining["slack"] = remaining["d"] - time - remaining["p"]
        remaining["score"] = alpha * remaining["p"] + (1 - alpha) * remaining["slack"]
        idx = remaining["score"].idxmin()
        sequence.append(remaining.loc[idx])
        time += remaining.loc[idx, "p"]
        remaining = remaining.drop(idx)
    return pd.DataFrame(sequence)

def improved_hybrid_schedule(jobs, alpha):
    remaining = jobs.copy()
    time = 0
    sequence = []
    p_max = jobs["p"].max()
    while not remaining.empty:
        remaining["slack"] = remaining["d"] - time - remaining["p"]
        eff_factor = remaining["p"] / p_max
        urgency = remaining["w"] / (remaining["slack"].clip(lower=1)) 
        norm_urgency = urgency / urgency.max() if urgency.max() > 0 else 0
        remaining["score"] = (alpha * eff_factor) - ((1 - alpha) * norm_urgency)
        idx = remaining["score"].idxmin()
        sequence.append(remaining.loc[idx])
        time += remaining.loc[idx, "p"]
        remaining = remaining.drop(idx)
    return pd.DataFrame(sequence)

# -----------------------------
# 4. Run Simulation & Alpha Sweeps
# -----------------------------
jobs_A = generate_scenario_a()
jobs_B = generate_scenario_b()

def run_alpha_sweep(jobs_data):
    alphas = np.linspace(0, 1, 21)
    trad_res, imp_res = [], []
    for a in alphas:
        t_val = get_detailed_metrics(traditional_hybrid_schedule(jobs_data, a), "Trad")["Weighted Tardiness"].mean()
        i_val = get_detailed_metrics(improved_hybrid_schedule(jobs_data, a), "Imp")["Weighted Tardiness"].mean()
        trad_res.append(t_val)
        imp_res.append(i_val)
    return alphas, trad_res, imp_res

# Sweep for Scenario A
alphas_A, trad_A, imp_A = run_alpha_sweep(jobs_A)
spt_A_wt = get_detailed_metrics(spt_schedule(jobs_A), "SPT")["Weighted Tardiness"].mean()
edd_A_wt = get_detailed_metrics(edd_schedule(jobs_A), "EDD")["Weighted Tardiness"].mean()

# Sweep for Scenario B
alphas_B, trad_B, imp_B = run_alpha_sweep(jobs_B)
df_spt_B = get_detailed_metrics(spt_schedule(jobs_B), "SPT")
df_edd_B = get_detailed_metrics(edd_schedule(jobs_B), "EDD")

# Find optimal alpha for Improved rule in Scenario B
best_imp_idx = np.argmin(imp_B)
best_imp_alpha = alphas_B[best_imp_idx]

# Generate detailed data for the Best Improved sequence in Scenario B
df_best_imp_B = get_detailed_metrics(improved_hybrid_schedule(jobs_B, best_imp_alpha), f"Improved (α={best_imp_alpha:.2f})")
all_details_B = pd.concat([df_spt_B, df_edd_B, df_best_imp_B])

# -----------------------------
# 5. Terminal Output
# -----------------------------
print("==================================================")
print(" SCALING PROOF: MEAN SLACK")
print("==================================================")
print(f"Scenario A (Sweet Spot):")
print(f"  Mean Slack: {(jobs_A['d'] - jobs_A['p']).mean():.2f}")
print(f"\nScenario B (Real World):")
print(f"  Mean Slack:          {(jobs_B['d'] - jobs_B['p']).mean():.2f}")
print(f"  Mean Weighted Slack: {((jobs_B['d'] - jobs_B['p']) / jobs_B['w']).mean():.2f}\n")

print("==================================================")
print(" SCENARIO B: MEAN FLOW TIME & TARDINESS")
print("==================================================")
final_summary = all_details_B.groupby("Rule")[["Flow Time", "Tardiness", "Weighted Tardiness"]].mean().round(2)
final_summary = final_summary.reindex(["SPT", "EDD", f"Improved (α={best_imp_alpha:.2f})"])
print(final_summary)

# -----------------------------
# 6. Separate Visualizations (5 Windows)
# -----------------------------

# Plot 1: Scenario A Optimization Curve
plt.figure(figsize=(8, 6))
plt.plot(alphas_A, trad_A, marker='x', linestyle=':', color='orange', lw=2, label="Traditional Hybrid")
plt.plot(alphas_A, imp_A, marker='o', color='green', lw=2, label="Improved Hybrid")
plt.axhline(spt_A_wt, ls='--', color='red', alpha=0.5, label="SPT Baseline")
plt.axhline(edd_A_wt, ls='--', color='blue', alpha=0.5, label="EDD Baseline")
plt.title("Scenario A: Matched Scales & Low Variance\nTraditional formula forms a trade-off curve", fontsize=13)
plt.xlabel("Alpha (Speed Focus →)")
plt.ylabel("Mean Weighted Tardiness")
plt.legend()
plt.tight_layout()

# Plot 2: Scenario B Optimization Curve
plt.figure(figsize=(8, 6))
plt.plot(alphas_B, trad_B, marker='x', linestyle=':', color='orange', lw=2, label="Traditional Hybrid")
plt.plot(alphas_B, imp_B, marker='o', color='green', lw=2, label="Improved Hybrid")
plt.axhline(df_spt_B["Weighted Tardiness"].mean(), ls='--', color='red', alpha=0.5, label="SPT Baseline")
plt.axhline(df_edd_B["Weighted Tardiness"].mean(), ls='--', color='blue', alpha=0.5, label="EDD Baseline")
plt.title("Scenario B: Real-World Imbalance\nTraditional formula collapses; Improved formula finds optimum", fontsize=13)
plt.xlabel("Alpha (Speed Focus →)")
plt.ylabel("Mean Weighted Tardiness")
plt.legend()
plt.tight_layout()

# Plot 3: Scenario B Tardiness Distribution
plt.figure(figsize=(8, 6))
sns.histplot(data=all_details_B, x="Tardiness", hue="Rule", element="step", stat="density", common_norm=False, kde=True, palette=["red", "blue", "green"])
plt.title("Scenario B: Tardiness Distribution", fontsize=13)
plt.xlabel("Lateness")
plt.ylabel("Density")
plt.tight_layout()

# Plot 4: Scenario B Flow Time vs Tardiness Bar Chart
plt.figure(figsize=(8, 6))
summary_df = all_details_B.groupby("Rule")[["Flow Time", "Tardiness"]].mean().reset_index()
melted_summary = summary_df.melt(id_vars="Rule", var_name="Metric", value_name="Average Time")
sns.barplot(data=melted_summary, x="Rule", y="Average Time", hue="Metric", palette="Set2")
plt.title("Scenario B: Flow Time vs Tardiness", fontsize=13)
plt.ylabel("Time Units")
plt.tight_layout()

# Plot 5: Scenario B Service Level Pie Chart
plt.figure(figsize=(8, 6))
late_counts = df_best_imp_B["Is Late"].value_counts()
dynamic_colors = ['#ff9999' if label == 'Late' else '#66b3ff' for label in late_counts.index]
dynamic_explode = [0.05 if label == 'Late' else 0 for label in late_counts.index]
plt.pie(late_counts, labels=late_counts.index, autopct='%1.1f%%', startangle=90, colors=dynamic_colors, explode=dynamic_explode, shadow=True)
plt.title(f"Scenario B: Service Level\nImproved Hybrid (α={best_imp_alpha:.2f})", fontsize=13)
plt.tight_layout()

# Show all figures at once
plt.show()