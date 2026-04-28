import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ROI Villa Simulator", layout="wide")

st.title("🏝️ ROI Simulator – Investasi Vila")

# ========================
# SCENARIO BUTTONS
# ========================
st.sidebar.header("🎯 Scenario")

if st.sidebar.button("Pesimis"):
    occupancy = 40
elif st.sidebar.button("Moderat"):
    occupancy = 60
elif st.sidebar.button("Optimis"):
    occupancy = 80
else:
    occupancy = 60

# ========================
# INPUT
# ========================
st.sidebar.header("Parameter Investasi")

investment = st.sidebar.number_input("Total Investasi (Rp)", value=1200000000)
occupancy = st.sidebar.slider("Occupancy (%)", 0, 100, occupancy)
price = st.sidebar.number_input("Harga per Malam (Rp)", value=1200000)
days = st.sidebar.number_input("Hari Operasional", value=365)
share = st.sidebar.slider("Share Investor (%)", 0, 100, 60)

# ========================
# CALCULATION
# ========================
revenue = occupancy/100 * price * days
income = revenue * share/100
roi = (income / investment) * 100

# ========================
# KPI
# ========================
col1, col2, col3 = st.columns(3)

col1.metric("Annual Revenue", f"Rp {revenue:,.0f}")
col2.metric("Investor Income", f"Rp {income:,.0f}")
col3.metric("ROI (%)", f"{roi:.2f}%")

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

    st.pyplot(fig)

# ========================
# BREAK EVEN
# ========================
st.subheader("📈 Break-even Analysis")

if income > 0:
    breakeven_year = investment / income
    st.info(f"Perkiraan balik modal: {breakeven_year:.1f} tahun")
else:
    st.warning("Belum bisa hitung break-even")

# ========================
# MONTE CARLO SIMULATION
# ========================
st.subheader("🎲 Probabilitas ROI (Simulasi Risiko)")

simulations = 1000

# asumsi variasi okupansi (normal distribution)
occ_sim = np.random.normal(loc=occupancy, scale=10, size=simulations)
occ_sim = np.clip(occ_sim, 10, 100)

roi_sim = []

for o in occ_sim:
    r = (o/100 * price * days * share/100) / investment * 100
    roi_sim.append(r)

roi_sim = np.array(roi_sim)

# Plot distribusi
fig2, ax2 = plt.subplots()
ax2.hist(roi_sim, bins=30)
ax2.set_xlabel("ROI (%)")
ax2.set_ylabel("Frekuensi")

st.pyplot(fig2)

# Statistik
mean_roi = np.mean(roi_sim)
prob_positive = np.sum(roi_sim > 5) / simulations * 100

st.write(f"📊 Rata-rata ROI: {mean_roi:.2f}%")
st.write(f"📊 Probabilitas ROI > 5%: {prob_positive:.1f}%")

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
# FOOTER
# ========================
st.markdown("---")
st.caption("Dikembangkan oleh Yuhka Sundaya | Ekonomi Pembangunan Unisba | 2026")
