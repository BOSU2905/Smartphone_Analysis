import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("final_data_cleaned_smartphones.csv")
df.drop(columns=['Unnamed: 0'],inplace=True, errors='ignore')

st.title("Smartphone Analysis 2024", text_alignment='center')
st.subheader("Smartphone analysis base by their specs and see which phone is value for money", text_alignment='center')
st.header("About Data: ")
st.write(df)
st.set_page_config(layout='wide')
st.write("**Data Source:** Smartphone Specifications 2024 Dataset via **Kaggle**")
st.write("**Created by**: Dilkush Singh")
st.write("**Status:** Cleaned & Standardized (RAM/Storage/Batter)")
st.header("Number of Smartphones Based on Chipset and Display Type", text_alignment='center')
st.divider()
show_brand_hue = st.checkbox("Comparison per Brand (Add Hue)")
col1, col2 = st.columns(2)
with col1 :
    st.subheader("Based on Chipset", text_alignment='center')
    
    if show_brand_hue == True:
        top_brands = df['Brand'].value_counts().nlargest(5).index
        df_top_brands = df[df['Brand'].isin(top_brands)]
        
        chart_data_chipset = df_top_brands.groupby(['Chipset', 'Brand']).size().unstack(fill_value=0)
        
        top_chipsets = df['Chipset'].value_counts().nlargest(5).index
        
        safe_chart_data_chipset = chart_data_chipset.reindex(top_chipsets).fillna(0)
        st.bar_chart(safe_chart_data_chipset)
    else:
        st.bar_chart(df['Chipset'].value_counts().head(10))
        
with col2:
    st.subheader("Based on Display", text_alignment='center')
    if show_brand_hue == True:
        top_brands = df['Brand'].value_counts().nlargest(5).index
        df_top_brands = df[df['Brand'].isin(top_brands)]
        
        chart_data_display = df_top_brands.groupby(['Display', 'Brand']).size().unstack(fill_value=0)
        
        top_display = df['Display'].value_counts().nlargest(5).index
        
        safe_chart_data_display = chart_data_display.reindex(top_display).fillna(0)
        st.bar_chart(safe_chart_data_display)
    else:
        st.bar_chart(df['Display'].value_counts().head(10))



st.info("**Insight:** MediaTek and Snapdragon dominate the landscape, powering Android devices across all segments—from entry-level to flagship.")
