import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="Sampling Variability & Confidence Intervals", layout="centered")

st.title("Sampling Variability & Confidence Intervals")
st.write(
    "This dashboard simulates repeated sampling from a chosen distribution and shows:\n"
    "- how sample means vary across samples (sampling variability)\n"
    "- how 95% confidence intervals behave (coverage)\n\n"
    "**Key idea:** A 95% CI procedure captures the true mean about 95% of the time in repeated sampling."
)

st.sidebar.header("Simulation Controls")
dist = st.sidebar.selectbox("Distribution", ["Normal", "Exponential", "Uniform", "Bernoulli"])
n = st.sidebar.slider("Sample size (n)", min_value=5, max_value=500, value=50, step=5)
B = st.sidebar.slider("Number of repeated samples (B)", min_value=100, max_value=5000, value=1000, step=100)
conf = st.sidebar.selectbox("Confidence level", [0.90, 0.95, 0.99], index=1)
seed = st.sidebar.number_input("Random seed", value=42, step=1)

np.random.seed(int(seed))

if dist == "Normal":
    mu = st.sidebar.slider("True mean (μ)", -5.0, 5.0, 0.0, 0.5)
    sigma = st.sidebar.slider("True std (σ)", 0.5, 5.0, 1.0, 0.5)
    samples = np.random.normal(loc=mu, scale=sigma, size=(B, n))
    true_mean = mu

elif dist == "Exponential":
    lam = st.sidebar.slider("Rate (λ)", 0.2, 3.0, 1.0, 0.1)
    samples = np.random.exponential(scale=1/lam, size=(B, n))
    true_mean = 1 / lam

elif dist == "Uniform":
    a = st.sidebar.slider("a", -5.0, 0.0, -1.0, 0.5)
    b = st.sidebar.slider("b", 0.5, 10.0, 2.0, 0.5)
    if b <= a:
        st.error("Uniform requires b > a.")
        st.stop()
    samples = np.random.uniform(a, b, size=(B, n))
    true_mean = (a + b) / 2

else:  # Bernoulli
    p = st.sidebar.slider("p", 0.05, 0.95, 0.3, 0.05)
    samples = np.random.binomial(1, p, size=(B, n))
    true_mean = p

# ---------- Compute sample means and CI ----------
means = samples.mean(axis=1)
stds = samples.std(axis=1, ddof=1)
ses = stds / np.sqrt(n)

alpha = 1 - conf
z = norm.ppf(1 - alpha/2)

ci_low = means - z * ses
ci_high = means + z * ses

covered = (ci_low <= true_mean) & (true_mean <= ci_high)
coverage_rate = covered.mean()

# ---------- Plot 1: Histogram of sample means ----------
st.subheader("1) Sampling variability of the sample mean")
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.hist(means, bins=40, density=True, alpha=0.8)
ax1.axvline(true_mean, linewidth=2)
ax1.set_xlabel("Sample mean")
ax1.set_ylabel("Density")
ax1.set_title(f"Distribution of sample means (n={n}, B={B})")
st.pyplot(fig1)

st.write(
    "The histogram shows how the **sample mean varies** across repeated samples. "
    "As you increase **n**, the distribution of sample means becomes tighter (less variability)."
)

# ---------- Plot 2: Confidence interval coverage plot ----------
st.subheader("2) Confidence intervals and coverage")
st.write(
    f"Each line below is a {int(conf*100)}% confidence interval for the mean from one sample. "
    "Intervals that include the true mean are 'covered'; others are 'misses'."
)

# To keep the plot readable, show at most 200 intervals
max_show = 200
idx = np.arange(B)
if B > max_show:
    idx = np.random.choice(B, size=max_show, replace=False)
    idx = np.sort(idx)

fig2, ax2 = plt.subplots(figsize=(8, 5))
y = np.arange(len(idx))

for k, i in enumerate(idx):
    ax2.plot([ci_low[i], ci_high[i]], [y[k], y[k]], linewidth=1)
ax2.axvline(true_mean, linewidth=2)
ax2.set_xlabel("Mean value")
ax2.set_ylabel("Sample index (subset)")
ax2.set_title(f"Confidence intervals (showing {len(idx)} of {B})")
st.pyplot(fig2)

# ---------- Metrics ----------
st.subheader("3) Coverage rate")
st.metric(label=f"Observed coverage (should be ~{int(conf*100)}%)", value=f"{coverage_rate*100:.1f}%")

st.write(
    "If the confidence interval method is working as intended, the observed coverage should be close to "
    f"{int(conf*100)}%. With larger B, the observed coverage stabilizes."
)
