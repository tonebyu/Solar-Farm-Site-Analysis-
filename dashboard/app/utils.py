import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

@st.cache_data
def load_data(file_path):
    """
    Loads CSV data and parses the Timestamp column.
    """
    try:
        df = pd.read_csv(file_path)
        # Ensure Timestamp is datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please ensure data is in the 'data/' folder.")
        return pd.DataFrame()

def plot_ghi_dni_dhi(df):
    """
    Creates a time series plot for GHI, DNI, and DHI.
    """
    st.subheader("Solar Irradiance Over Time")
    # Melting for easier plotting with Plotly
    df_melt = df.melt(id_vars=['Timestamp'], value_vars=['GHI', 'DNI', 'DHI'], 
                      var_name='Variable', value_name='Irradiance (W/m²)')
    
    fig = px.line(df_melt, x='Timestamp', y='Irradiance (W/m²)', color='Variable',
                  title="GHI, DNI, and DHI Trends")
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_heatmap(df):
    """
    Plots a correlation heatmap for key solar and weather variables.
    """
    st.subheader("Correlation Matrix")
    cols = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD', 'Tamb', 'RH']
    corr = df[cols].corr()
    
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r',
                    title="Correlation Between Variables")
    st.plotly_chart(fig, use_container_width=True)

def plot_histograms(df, column):
    """
    Plots a histogram for a selected column.
    """
    fig = px.histogram(df, x=column, title=f"Distribution of {column}", nbins=50)
    st.plotly_chart(fig, use_container_width=True)

def plot_boxplot(df, columns):
    """
    Plots boxplots to visualize outliers and spread.
    """
    st.subheader("Boxplot Analysis")
    df_melt = df.melt(id_vars=['Timestamp'], value_vars=columns, 
                      var_name='Variable', value_name='Value')
    
    fig = px.box(df_melt, x='Variable', y='Value', color='Variable', 
                 title="Distribution & Outliers (Boxplot)")
    st.plotly_chart(fig, use_container_width=True)