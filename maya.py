import streamlit as st
import pandas as pd
import math
import altair as alt
#from bidi.algorithm import get_display

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
    # הצגת גרף בעזרת Altair
    values = [rent_total_e3, rent_total_c3]
    labels = ['Enlight', 'מתחרה']
    colors = ['orange', 'blue']

    df_chart = pd.DataFrame({'label': labels, 'value': values})
    chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('label:N', title=''),
        y=alt.Y('value:Q', title=''),
        color=alt.Color('label:N', scale=alt.Scale(domain=labels, range=colors), legend=None)
    ).properties(width=600, height=400)

    text = alt.Chart(df_chart).mark_text(
        align='center',
        baseline='bottom',
        dy=-5
    ).encode(
        x='label:N',
        y='value:Q',
        text=alt.Text('value:Q', format=',.1f')
    )

    st.altair_chart(chart + text, use_container_width=True)
