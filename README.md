# Sampling Variability & Confidence Intervals (Streamlit)

This project is an interactive Streamlit dashboard that demonstrates:

- **Sampling variability**: how the sample mean changes across repeated samples
- **Confidence interval (CI) coverage**: how often a confidence interval contains the true population mean

**Key idea:** A 95% confidence interval procedure captures the true mean about 95% of the time in repeated sampling (in the long run).

---

## What the App Shows

### 1) Sampling variability of the sample mean  
The app repeatedly samples from a chosen distribution and plots a **histogram of sample means**.  
As the sample size **n** increases, the sample means concentrate more tightly around the true mean.

### 2) Confidence intervals and coverage  
For each repeated sample, the app builds a **(90%, 95%, or 99%) confidence interval** for the mean using a **z-based CI**:

\[
\bar{x} \pm z_{\alpha/2}\cdot \frac{s}{\sqrt{n}}
\]

It then visualizes many intervals and highlights how many of them include the true mean.

### 3) Coverage rate  
The app reports the **observed coverage rate** (fraction of intervals containing the true mean).  
With larger number of repetitions **B**, the observed coverage stabilizes near the selected confidence level.

---

## Distributions Supported

- **Normal**: user controls true mean (μ) and standard deviation (σ)
- **Exponential**: user controls rate (λ), true mean = 1/λ
- **Uniform**: user controls endpoints (a, b), true mean = (a + b)/2
- **Bernoulli**: user controls probability (p), true mean = p

---

## Files

- `app.py` — Streamlit application code
- `requirements.txt` — Python dependencies

---

## Setup & Run Locally

### 1) Create and activate a virtual environment (recommended)

**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
