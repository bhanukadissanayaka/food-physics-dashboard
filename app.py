import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # <-- New: Required for calculating the trendline

# Set up the page title
st.title("Food Physics Data Visualizer")
st.write("Generate custom scatter plots and trendlines for your samples.")

# 1. Data Ingestion
uploaded_file = st.file_uploader("Upload your lab data (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Read the perfectly clean file automatically
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("### Data Preview")
    st.dataframe(df.head())
    
    st.write("### Build Your Graph")
    
    # 2. Dynamic Selection
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Choose X-Axis:", df.columns)
    with col2:
        y_axis = st.selectbox("Choose Y-Axis:", df.columns)
        
    category_col = st.selectbox("Color by Sample Type (Optional):", ["None"] + list(df.columns))
    
    # <-- New: A checkbox to turn the trendline on or off
    show_trendline = st.checkbox("Show Linear Trendline", value=False) 
    
    # 3. Visualization Engine
    fig, ax = plt.subplots()
    
    # Clean the data of any blank cells before doing math
    clean_df = df.dropna(subset=[x_axis, y_axis])
    
    if category_col != "None":
        categories = clean_df[category_col].unique()
        for cat in categories:
            subset = clean_df[clean_df[category_col] == cat]
            ax.scatter(subset[x_axis], subset[y_axis], label=f"{cat} Data", alpha=0.7)
            
            # Draw trendline for each category
            if show_trendline and len(subset) > 1:
                z = np.polyfit(subset[x_axis], subset[y_axis], 1)
                p = np.poly1d(z)
                ax.plot(subset[x_axis], p(subset[x_axis]), linestyle='--', label=f"{cat} Trendline")
                
        ax.legend()
    else:
        ax.scatter(clean_df[x_axis], clean_df[y_axis], color='#4C72B0', alpha=0.6, label="Sample Data")
        
        # Draw a single trendline
        if show_trendline and len(clean_df) > 1:
            z = np.polyfit(clean_df[x_axis], clean_df[y_axis], 1)
            p = np.poly1d(z)
            ax.plot(clean_df[x_axis], p(clean_df[x_axis]), color='#55A868', linewidth=2, label="Linear Trendline")
            
        ax.legend()

    # Automatically set the titles
    ax.set_title(f"{x_axis} vs. {y_axis}")
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Render the plot
    st.pyplot(fig)