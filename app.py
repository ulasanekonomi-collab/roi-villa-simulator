import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ROI Villa Simulator", layout="wide")

st.title("🏝️ ROI Simulator – Investasi Vila")
st.markdown("Simulasi interaktif untuk memahami potensi income & risiko")

# INPUT
st.sidebar.header("Parameter Investasi")

investment = st.sidebar.number_input("Total Investasi (Rp)", value=1200000000)
occupancy = st.sidebar.slider("Occupancy (%)", 0, 100, 60)
price = st.sidebar.number_input("Harga per Malam (Rp)", value=1200000)
days = st.sidebar.number_input("Hari Operasional", value=365)
share = st.sidebar.slider("Share Investor (%)", 0, 100, 60)

# CALCULATION
revenue = occupancy/100 * price * days
income = revenue * share/100
roi = (income / investment) * 100

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Annual Revenue", f"Rp {revenue:,.0f}")
col2.metric("Investor Income", f"Rp {income:,.0f}")
col3.metric("ROI (%)", f"{roi:.2f}%")

# CHART
st.subheader("Sensitivity Analysis")

occ_range = np.arange(30, 91, 5)
roi_list = []

for o in occ_range:
    r = (o/100 * price * days * share/100) / investment * 100
    roi_list.append(r)

df = pd.DataFrame({
    "Occupancy": occ_range,
    "ROI": roi_list
})

fig, ax = plt.subplots()
ax.plot(df["Occupancy"], df["ROI"])
ax.set_xlabel("Occupancy (%)")
ax.set_ylabel("ROI (%)")

st.pyplot(fig)

# INTERPRETATION
st.subheader("Interpretasi")

if roi < 5:
    st.warning("ROI rendah → di bawah deposito")
elif roi <= 10:
    st.info("ROI moderat → cocok untuk income stabil")
else:
    st.success("ROI menarik → potensial passive income")
st.markdown("---")
st.caption("Dikembangkan oleh Yuhka Sundaya | Ekonomi Pembangunan Unisba | 2026")
col1, col2 = st.columns(2)

with col1:
    st.image("unisba.png", width=120)

with col2:
    st.image("terra.png", width=120)

st.markdown("---")
st.caption("Dikembangkan oleh Yuhka Sundaya | Ekonomi Pembangunan Unisba | 2026")
