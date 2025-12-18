import streamlit as st
import pandas as pd
import os
from utils import load_data, plot_ghi_dni_dhi, plot_correlation_heatmap, plot_histograms, plot_boxplot

# Set page config
st.set_page_config(page_title="Solar Data Dashboard", layout="wide", page_icon="☀️")

def main():
    st.title("☀️ Solar Radiation Dashboard")
    st.markdown("Interactive dashboard to analyze solar radiation data for Benin, Togo, and Sierra Leone.")

    # --- Sidebar Configuration ---
    st.sidebar.header("Settings")
    
    # Country Selection
    country_map = {
        "Benin": "../dashboard/data/benin_clean.csv",
        "Togo": "../dashboard/data/togo_clean.csv",
        "Sierra Leone": "../dashboard/data/Sierraleone_clean.csv"
    }
    
    selected_country = st.sidebar.selectbox("Select Country", list(country_map.keys()))
    data_path = country_map[selected_country]
    
    # Load Data
    df = load_data(data_path)
    
    if not df.empty:
        # --- Sidebar Filters ---
        st.sidebar.subheader("Filter Data")
        # Date Slider
        min_date = df['Timestamp'].min().date()
        max_date = df['Timestamp'].max().date()
        
        start_date, end_date = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        
        # Filter dataframe based on selection
        mask = (df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        # --- Key Metrics Row ---
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg GHI (W/m²)", f"{df_filtered['GHI'].mean():.2f}")
        col2.metric("Avg DNI (W/m²)", f"{df_filtered['DNI'].mean():.2f}")
        col3.metric("Avg Temp (°C)", f"{df_filtered['Tamb'].mean():.2f}")
        col4.metric("Max Wind Speed (m/s)", f"{df_filtered['WS'].max():.2f}")
        
        st.markdown("---")

        # --- Tab Layout ---
        tab1, tab2, tab3 = st.tabs(["📊 Data Visualization", "📈 Statistics & Top Values", "🌪️ Wind & Correlations"])
        
        with tab1:
            # Time Series
            plot_ghi_dni_dhi(df_filtered)
            
            # Boxplot
            plot_boxplot(df_filtered, ['GHI', 'DNI', 'DHI', 'ModA', 'ModB'])
            
            

        with tab2:
            st.subheader("Summary Statistics")
            st.dataframe(df_filtered.describe())
            
            st.subheader("Top High-GHI Events")
            # Displaying 'Top Regions' equivalent (Top time periods since region col is missing)
            top_ghi = df_filtered.nlargest(10, 'GHI')[['Timestamp', 'GHI', 'DNI', 'DHI', 'Tamb']]
            st.table(top_ghi)

        with tab3:
            col_a, col_b = st.columns(2)
            with col_a:
                plot_correlation_heatmap(df_filtered)
                
            with col_b:
                st.subheader("Wind Speed Distribution")
                plot_histograms(df_filtered, "WS")
    else:
        st.info("Please ensure the CSV files are located in the 'data/' directory.")

if __name__ == "__main__":
    main()