import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ROI Villa Simulator", layout="wide")

st.title("🏝️ ROI Simulator – Investasi Vila (Realistis)")

# ========================
# SCENARIO
# ========================
st.sidebar.header("🎯 Scenario")

if st.sidebar.button("Pesimis"):
    occ_default = 40
elif st.sidebar.button("Moderat"):
    occ_default = 60
elif st.sidebar.button("Optimis"):
    occ_default = 80
else:
    occ_default = 60

# ========================
# INPUT
# ========================
st.sidebar.header("Parameter Investasi")

investment = st.sidebar.number_input("Total Investasi (Rp)", value=120000000)
unit_price = st.sidebar.number_input("Harga 1 Unit Vila (Rp)", value=1200000000)

occupancy = st.sidebar.slider("Occupancy (%)", 0, 100, occ_default)
price = st.sidebar.number_input("Harga per Malam (Rp)", value=1200000)
days = st.sidebar.number_input("Hari Operasional", value=365)
share = st.sidebar.slider("Share Investor (%)", 0, 100, 60)
cost_ratio = st.sidebar.slider("Biaya Operasional (%)", 0, 80, 30)
cost_ratio = cost_ratio / 100
# ========================
# CALCULATION (REALISTIS)
# ========================
ownership = investment / unit_price if unit_price > 0 else 0

revenue = occupancy / 100 * price * days
cost_ratio = st.sidebar.slider("Biaya Operasional (%)", 0, 80, 30)
cost_ratio = cost_ratio / 100
income = revenue * (1 - cost_ratio) * share / 100 * ownership
roi = (income / investment) * 100 if investment > 0 else 0
st.write("Cost ratio aktif:", cost_ratio)
# ========================
# KPI
# ========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue (Unit)", f"Rp {revenue:,.0f}")
col2.metric("Income Anda", f"Rp {income:,.0f}")
col3.metric("ROI", f"{roi:.2f}%")

if income > 0:
    breakeven = investment / income
    col4.metric("Break-even", f"{breakeven:.1f} thn")
else:
    col4.metric("Break-even", "-")

# ========================
# INFO OWNERSHIP
# ========================
st.info(f"Porsi kepemilikan Anda: {ownership*100:.2f}% dari 1 unit vila")

# ========================
# CASHFLOW
# ========================
st.subheader("💰 Simulasi Cashflow")
monthly = income / 12
st.metric("Passive Income / Bulan", f"Rp {monthly:,.0f}")

# ========================
# GRADING
# ========================
st.subheader("🎯 Penilaian Investasi")

if roi >= 12:
    st.success("Grade A (Sangat Menarik)")
elif roi >= 7:
    st.info("Grade B (Cukup Menarik)")
else:
    st.warning("Grade C (Perlu Dipertimbangkan)")

# ========================
# LAYOUT
# ========================
col_left, col_right = st.columns(2)

# ========================
# SENSITIVITY
# ========================
with col_left:
    st.subheader("📊 Sensitivity")

    occ_range = np.arange(30, 91, 5)
    roi_list = []

    for o in occ_range:
        inc = (o / 100 * price * days * share / 100) * ownership
        r = (inc / investment) * 100 if investment > 0 else 0
        roi_list.append(r)

    fig, ax = plt.subplots()
    ax.plot(occ_range, roi_list)

    ax.axhline(y=5, linestyle="--")
    ax.text(40, 5.3, "Deposito (~5%)")

    ax.axhline(y=10, linestyle="--")
    ax.text(40, 10.3, "Target Ideal")

    ax.set_xlabel("Occupancy (%)")
    ax.set_ylabel("ROI (%)")

    st.pyplot(fig)

# ========================
# PROBABILITY
# ========================
with col_right:
    st.subheader("🎲 Probabilitas ROI")

    simulations = 1000

    occ_sim = np.random.normal(loc=occupancy, scale=20, size=simulations)
    occ_sim = np.clip(occ_sim, 10, 100)

    roi_sim = []

    for o in occ_sim:
        inc = (o / 100 * price * days * share / 100) * ownership
        r = (inc / investment) * 100 if investment > 0 else 0
        roi_sim.append(r)

    roi_sim = np.array(roi_sim)

    fig2, ax2 = plt.subplots()
    ax2.hist(roi_sim, bins=25)

    ax2.axvline(x=5, linestyle="--")
    ax2.axvline(x=10, linestyle="--")

    ax2.set_xlabel("ROI (%)")
    ax2.set_ylabel("Frekuensi")

    st.pyplot(fig2)

    st.write(f"Rata-rata ROI: {np.mean(roi_sim):.2f}%")
    st.write(f"Median ROI: {np.median(roi_sim):.2f}%")
    st.write(f"Probabilitas ROI > 5%: {(roi_sim > 5).mean()*100:.1f}%")

# ========================
# INTERPRETASI
# ========================
st.subheader("🧠 Interpretasi")

if roi < 5:
    st.warning("ROI di bawah deposito")
elif roi <= 10:
    st.info("ROI moderat dan stabil")
else:
    st.success("ROI menarik sebagai passive income")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("Dikembangkan oleh Yuhka Sundaya | Ekonomi Pembangunan Unisba | 2026")

# ========================
# FOOTER + LOGO UNISBA
# ========================
st.markdown("---")

col_logo, col_text = st.columns([1,4])

with col_logo:
    st.image("logo Unisba.png", width=90)

with col_text:
    st.caption("Dikembangkan oleh Yuhka Sundaya | Ekonomi Pembangunan Unisba | 2026")
