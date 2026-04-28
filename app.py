import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ROI Villa Simulator", layout="wide")

st.title("🏝️ ROI Simulator – Investasi Vila")

# ========================
# SCENARIO BUTTON
# ========================
st.sidebar.header("🎯 Scenario")

if st.sidebar.button("Pesimis"):
    occupancy_default = 40
elif st.sidebar.button("Moderat"):
    occupancy_default = 60
elif st.sidebar.button("Optimis"):
    occupancy_default = 80
else:
    occupancy_default = 60

# ========================
# INPUT
# ========================
st.sidebar.header("Parameter Investasi")

investment = st.sidebar.number_input("Total Investasi (Rp)", value=1200000000)
occupancy = st.sidebar.slider("Occupancy (%)", 0, 100, occupancy_default)
price = st.sidebar.number_input("Harga per Malam (Rp)", value=1200000)
days = st.sidebar.number_input("Hari Operasional", value=365)
share = st.sidebar.slider("Share Investor (%)", 0, 100, 60)

# ========================
# CALCULATION
# ========================
revenue = occupancy / 100 * price * days
income = revenue * share / 100
roi = (income / investment) * 100 if investment > 0 else 0

# ========================
# KPI
# ========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"Rp {revenue:,.0f}")
col2.metric("Income", f"Rp {income:,.0f}")
col3.metric("ROI", f"{roi:.2f}%")

if income > 0:
    breakeven = investment / income
    col4.metric("Break-even", f"{breakeven:.1f} thn")
else:
    col4.metric("Break-even", "-")
# ========================
# CASHFLOW BULANAN
# ========================
st.subheader("💰 Simulasi Cashflow")

monthly_income = income / 12

st.metric("Estimasi Passive Income / Bulan", f"Rp {monthly_income:,.0f}")
# ========================
# INVESTMENT GRADING
# ========================
st.subheader("🎯 Penilaian Investasi")

if roi >= 12:
    grade = "A (Sangat Menarik)"
    st.success(f"Grade: {grade}")
elif roi >= 7:
    grade = "B (Cukup Menarik)"
    st.info(f"Grade: {grade}")
else:
    grade = "C (Perlu Dipertimbangkan)"
    st.warning(f"Grade: {grade}")
# ========================
# LAYOUT 2 KOLOM
# ========================
col_left, col_right = st.columns(2)

# ========================
# SENSITIVITY CHART
# ========================
with col_left:
    st.subheader("📊 Sensitivity")

    occ_range = np.arange(30, 91, 5)
    roi_list = []

    for o in occ_range:
        r = (o/100 * price * days * share/100) / investment * 100
        roi_list.append(r)

    fig, ax = plt.subplots()
    ax.plot(occ_range, roi_list)
    ax.set_xlabel("Occupancy (%)")
    ax.set_ylabel("ROI (%)")
fig, ax = plt.subplots()
ax.plot(occ_range, roi_list)

# 🔥 TAMBAHKAN INI
ax.axhline(y=5, linestyle='--')
ax.text(30, 5.3, "Deposito (~5%)")

ax.axhline(y=10, linestyle='--')
ax.text(30, 10.3, "Target Ideal")

# =================

ax.set_xlabel("Occupancy (%)")
ax.set_ylabel("ROI (%)")

st.pyplot(fig)
    st.pyplot(fig)
ax.axhline(y=5, linestyle='--')
ax.text(30, 5.5, "Batas Deposito (~5%)")
# ========================
# PROBABILITY (MONTE CARLO)
# ========================
with col_right:
    st.subheader("🎲 Probabilitas ROI")

    simulations = 1000
    occ_sim = np.random.normal(loc=occupancy, scale=10, size=simulations)
    occ_sim = np.clip(occ_sim, 10, 100)

    roi_sim = []

    for o in occ_sim:
        r = (o/100 * price * days * share/100) / investment * 100
        roi_sim.append(r)

    roi_sim = np.array(roi_sim)

    fig2, ax2 = plt.subplots()
    ax2.hist(roi_sim, bins=25)
    ax2.set_xlabel("ROI (%)")
    ax2.set_ylabel("Frekuensi")

    st.pyplot(fig2)

    mean_roi = np.mean(roi_sim)
    prob_good = np.sum(roi_sim > 5) / simulations * 100

    st.write(f"📊 Rata-rata ROI: {mean_roi:.2f}%")
    st.write(f"📊 Probabilitas ROI > 5%: {prob_good:.1f}%")

# ========================
# INTERPRETASI
# ========================
st.subheader("🧠 Interpretasi")

if roi < 5:
    st.warning("ROI rendah → di bawah deposito")
elif roi <= 10:
    st.info("ROI moderat → cocok untuk income stabil")
else:
    st.success("ROI menarik → potensial passive income")

# ========================
# FOOTER + LOGO UNISBA
# ========================
st.markdown("---")

col_logo, col_text = st.columns([1,4])

with col_logo:
    st.image("logo Unisba.png", width=100)

with col_text:
    st.caption("Dikembangkan oleh Yuhka Sundaya | Ekonomi Pembangunan Unisba | 2026")
