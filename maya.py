import streamlit as st
import pandas as pd
import math
import altair as alt
import matplotlib.pyplot as plt
import io
from bidi.algorithm import get_display

st.set_page_config(page_title="מחשבון Enlight", layout="wide")

# --- לוגו גדול בראש הדף ----------------
st.image("logo.png")

# --- קלטים לשתי העמודות: Enlight ו-מתחרה --------
left_col, right_col = st.columns([1, 2])

with left_col:
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        st.subheader("Enlight")
        dunam_e = st.slider("דונם", 0, 500, value=0, step=50, key="dunam_e")
        rent_e = st.number_input("שכירות שנתית פר דונם (ש״ח)", min_value=0, value=0, step=500, key="rent_e")
        bonus_e = st.number_input("מענק חתימה (ש״ח)", min_value=0, value=100000, step=100000, key="bonus_e")
        duration_e = st.number_input("משך הפרויקט (שנים)", min_value=25, value=35, step=1, key="duration_e")

        # חשב ופורמט תשלומים עבור Enlight
        rent_total_e = duration_e * dunam_e * rent_e
        total_rent_e_str = f"{rent_total_e:,.1f}"
        #st.text_input('דמי שכירות אנלייט', value=total_rent_e_str, disabled=False, key='total_rent_e')

        rent_total_e2 = rent_total_e + bonus_e
        total_rent_e2_str = f"{rent_total_e2:,.1f}"
        #st.text_input('תשלום כולל אנלייט', value=total_rent_e2_str, disabled=False, key='total_rent_e2')

        discounted_factor_e = (1 - (1 / ((1 + 0.05) ** float(duration_e)))) / 0.05
        rent_total_e3 = discounted_factor_e * float(dunam_e) * float(rent_e) + float(bonus_e)
        total_rent_e3_str = f"{rent_total_e3:,.1f}"
        st.text_input('תשלום מהוון אנלייט', value=total_rent_e3_str, disabled=False, key='total_rent_e3')

    with subcol2:
        st.subheader("מתחרה")
        dunam_c = st.slider("דונם", 0, 500, value=0, step=50, key="dunam_c")
        rent_c = st.number_input("שכירות שנתית פר דונם (ש״ח)", min_value=0, value=0, step=500, key="rent_c")
        bonus_c = st.number_input("מענק חתימה (ש״ח)", min_value=0, value=100000, step=100000, key="bonus_c")
        duration_c = st.number_input("משך הפרויקט (שנים)", min_value=25, value=35, step=1, key="duration_c")

        # חשב ופורמט תשלומים עבור המתחרה
        rent_total_c = duration_c * dunam_c * rent_c
        total_rent_c_str = f"{rent_total_c:,.1f}"
        #st.text_input('דמי שכירות מתחרה', value=total_rent_c_str, disabled=False, key='total_rent_c')

        rent_total_c2 = rent_total_c + bonus_c
        total_rent_c2_str = f"{rent_total_c2:,.1f}"
        #st.text_input('תשלום כולל מתחרה', value=total_rent_c2_str, disabled=False, key='total_rent_c2')

        discounted_factor_c = (1 - (1 / ((1 + 0.05) ** float(duration_c)))) / 0.05
        rent_total_c3 = discounted_factor_c * float(dunam_c) * float(rent_c) + float(bonus_c)
        total_rent_c3_str = f"{rent_total_c3:,.1f}"
        st.text_input('תשלום מהוון מתחרה', value=total_rent_c3_str, disabled=False, key='total_rent_c3')

with right_col:
    # Data
    values = [rent_total_e3, rent_total_c3]
    colors = ['orange', 'blue']
    labels = ['Enlight', "מתחרה"]

    # Create figure (6×4 inches) with higher DPI for clarity
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    bars = ax.bar(labels, values, color=colors)

    # Determine a small vertical offset for the value-text
    max_val = max(values) if len(values) > 0 else 0
    offset = max_val * 0.02  # 2% of the maximum value

    # Extend Y-axis to 1.5× the highest bar
    ax.set_ylim(0, max_val * 1.5)

    for bar, label, value in zip(bars, labels, values):
        h = bar.get_height()
        # Label inside the bar (75% of bar height)
        try:
            label_shaped = get_display(label)
        except Exception:
            label_shaped = label

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h * 0.75,
            label_shaped,
            ha='center',
            va='center',
            color='white',
            fontweight='bold'
        )
        # Value just above the bar
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + offset,
            f"{value:,.1f}",
            ha='center',
            va='bottom',
            color='black',
            fontweight='bold'
        )

    ax.set_xticks([])  # Remove x‐axis ticks
    ax.set_yticks([])  # Remove y‐axis ticks
    #ax.set_title('Enlight vs. Competitor')
    plt.tight_layout()

    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Display the (non‐stretched) image
    right_col.image(buf)
