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
st.write("**Status:** Cleaned & Standardized (RAM/Storage/Battery)")
st.divider()
st.header("Number of Smartphones Based on Chipset and Display Type", text_alignment='center')

show_brand_hue = st.checkbox("Comparison per Brand (Add Hue)")
col1, col2 = st.columns(2)
with col1 :
    st.subheader("Based on Chipset", text_alignment='center')
    
    if show_brand_hue == True:
        top_brands = df['Brand'].value_counts().nlargest(10).index
        df_top_brands = df[df['Brand'].isin(top_brands)]
        
        chart_data_chipset = df_top_brands.groupby(['Chipset', 'Brand']).size().unstack(fill_value=0)
        
        top_chipsets = df['Chipset'].value_counts().nlargest(10).index
        
        safe_chart_data_chipset = chart_data_chipset.reindex(top_chipsets).fillna(0)
        st.bar_chart(safe_chart_data_chipset)
    else:
        st.bar_chart(df['Chipset'].value_counts().head(10), color='green')
        
with col2:
    st.subheader("Based on Display", text_alignment='center')
    if show_brand_hue == True:
        top_brands = df['Brand'].value_counts().nlargest(10).index
        df_top_brands = df[df['Brand'].isin(top_brands)]
        
        chart_data_display = df_top_brands.groupby(['Display', 'Brand']).size().unstack(fill_value=0)
        
        top_display = df['Display'].value_counts().nlargest(10).index
        
        safe_chart_data_display = chart_data_display.reindex(top_display).fillna(0)
        st.bar_chart(safe_chart_data_display)
    else:
        st.bar_chart(df['Display'].value_counts().head(10), color='#FFFFFF')


if show_brand_hue:
    st.info("**Insight:** While major players lead, a significant portion of the market is driven by long-tail brands. This highlights how MediaTek and Snapdragon have successfully penetrated the entire ecosystem, becoming the standard for reliability across both elite and emerging manufacturers.")
    st.info("**Insight:** Based on display, Samsung leads the AMOLED segment with proprietary tech, while IPS remains the primary engine for long-tail brands to win the Value-for-Money battle in the mid-range market.")
    
else :
    st.info("**Insight:** MediaTek and Snapdragon dominate the landscape, powering Android devices across all segments—from entry-level to flagship.")
    st.info("**Insight:** IPS remains the market leader in volume, dominating the entry-level and mid-range segments. Its low production cost makes it the ideal ""Value for Money"" choice for devices focused on balancing price and performance. AMOLED follows as the premium standard, prevalent in mid-range to flagship devices.")
st.divider()
st.header("Phone Prices Distribution Based on Brand", text_alignment='center')
st.scatter_chart(df, x='Price_USD', y='Brand', color='blue', height=750)
st.info("""
**The Price Ceiling:** Samsung holds the highest peak in the dataset with the Galaxy Z Fold 6 (1TB) at 2,210.99USD, slightly edgeing out the iPhone 15 Pro Max (1TB) at 2,083.40USD.
""")
st.info('**Android\'s Volume Base:** Samsung and other Android brands show a massive concentration in the 100USD – 600USD range. This "bottom-heavy" distribution reflects a strategy of dominating the entry-to-mid-range market through sheer volume.')
st.info('**Apple’s Premium Floor:** Unlike its competitors, Apple’s data points consistently shift toward the premium spectrum. There is no "entry-level" clutter,  every generation moves the price floor upward, maintaining an elite brand positioning regardless of hardware specs.')
st.divider()
st.header("Number of Smartphones based on their RAM", text_alignment='center')
add_hue = st.checkbox("Comparison Per OS (Add Hue)")
ram_count = df['Ram_Capacity'].value_counts().sort_index()

if add_hue != True:
    st.bar_chart(ram_count, horizontal=True)
    st.info("**The 8GB Standard:** 8GB RAM dominates the market as the versatile baseline. It provides the optimal balance for multi-tasking, productivity, and modern mobile gaming without excessive cost.")
    st.info("**Performance Enthusiasts:** Higher tiers (12GB, 16GB, and up to 32GB) represent the enthusiast and professional segments. These are typically found in high-end gaming devices like the Nubia Red Magic or premium ""Max"" configurations where extreme performance is a necessity.")
    st.info("**Strategic Upselling:** The presence of high-RAM variants indicates a market strategy focused on ""future-proofing"" and catering to power users who demand PC-level specifications in their pockets.")
else :
    chart = df.groupby(['Ram_Capacity','OS']).size().unstack(fill_value=0).sort_index()
    st.bar_chart(chart, horizontal=True, height=450)