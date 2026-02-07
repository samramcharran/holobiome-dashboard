import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Holobiome Data Dashboard", layout="wide")
st.title("🦠 Holobiome Microbiome Metadata Dashboard")
st.caption("Educational project - Data from public repositories")

@st.cache_data
def load_data():
    df = pd.read_csv("harmonized_metadata.tsv", sep="\t", na_values=["NA", ""])
    return df

df = load_data()

# Map disease to study ID and data sources
study_info = {
    'Ankylosing Spondylitis': {
        'study_id': 'PRJNA375935',
        'paper': 'Wen C, et al. (2017)',
        'sources': 'CSV, Excel, PDF'
    },
    'Fibromyalgia': {
        'study_id': 'PRJNA521587',
        'paper': 'Minerbi A, et al. (2019)',
        'sources': 'CSV, GitHub, PDF'
    },
    'Multiple Sclerosis': {
        'study_id': 'PRJDB7767',
        'paper': 'Takewaki D, et al. (2020)',
        'sources': 'CSV, PDF'
    },
    'Cancer (FMT Trial)': {
        'study_id': 'PRJNA1289847',
        'paper': 'FMT-LUMINate (2025)',
        'sources': 'CSV, PDF'
    },
    'Rheumatoid Arthritis': {
        'study_id': 'PRJEB6997',
        'paper': 'Zhang X, et al. (2015)',
        'sources': 'CSV, Excel, PDF'
    }
}

disease_to_study = {k: v['study_id'] for k, v in study_info.items()}

# Sidebar filter
st.sidebar.header("Filters")
disease_options = ["All"] + sorted(disease_to_study.keys())
selected_disease = st.sidebar.selectbox("Disease", disease_options)

# Apply filter
filtered_df = df.copy()
if selected_disease != "All":
    selected_study = disease_to_study[selected_disease]
    filtered_df = filtered_df[filtered_df["study_id"] == selected_study]

# Metrics
st.header("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Samples", len(filtered_df))
col2.metric("Studies", filtered_df["study_id"].nunique())
col3.metric("With BMI", filtered_df["bmi"].notna().sum())
col4.metric("With Age", filtered_df["host_age"].notna().sum())

if selected_disease == "All":
    # Study Summary Table with paper and sources
    st.header("Study Overview")
    summary_data = []
    for disease, info in study_info.items():
        study_id = info['study_id']
        study_df = df[df['study_id'] == study_id]
        summary_data.append({
            'Disease': disease,
            'Study ID': study_id,
            'Paper': info['paper'],
            'Sources': info['sources'],
            'Samples': len(study_df),
            'With Age': study_df['host_age'].notna().sum(),
            'With BMI': study_df['bmi'].notna().sum()
        })
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # Samples per Study Bar Chart
    st.header("Samples by Disease")
    chart_df = summary_df[['Disease', 'Samples']].copy()
    fig1 = px.bar(chart_df, x='Disease', y='Samples', color='Samples', 
                  color_continuous_scale='Viridis',
                  hover_data=['Disease'])
    st.plotly_chart(fig1, use_container_width=True)

    # Forensics Heatmap
    st.header("Data Completeness Heatmap")
    clinical_cols = ["host_age", "host_sex", "bmi", "disease_status", "timepoint"]
    completeness_data = []
    for disease, info in study_info.items():
        study_id = info['study_id']
        study_df = df[df["study_id"] == study_id]
        row = {"Disease": disease}
        for col in clinical_cols:
            if col in study_df.columns:
                pct = (study_df[col].notna().sum() / len(study_df)) * 100
                row[col] = round(pct, 0)
        completeness_data.append(row)

    completeness_df = pd.DataFrame(completeness_data).set_index("Disease")
    fig2 = px.imshow(completeness_df, color_continuous_scale="RdYlGn", aspect="auto",
                     labels=dict(x="Variable", y="Disease", color="% Complete"),
                     text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Disease Distribution Pie
    st.header("Disease Distribution")
    pie_df = summary_df[['Disease', 'Samples']].copy()
    fig3 = px.pie(pie_df, names='Disease', values='Samples')
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info("Select a specific disease from the sidebar to view detailed demographics and sample data.")

else:
    # Show study ID for selected disease
    info = study_info[selected_disease]
    st.subheader(f"Study ID: {info['study_id']}")
    
    # Demographics
    st.header("Demographics")
    col1, col2 = st.columns(2)

    with col1:
        age_df = filtered_df[filtered_df["host_age"].notna()]
        if len(age_df) > 0:
            fig3 = px.histogram(age_df, x="host_age", nbins=15, title="Age Distribution")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.write("No age data available.")

    with col2:
        sex_df = filtered_df[filtered_df["host_sex"].notna()]
        if len(sex_df) > 0:
            fig4 = px.pie(sex_df, names="host_sex", title="Sex Distribution")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.write("No sex data available.")

    # BMI
    st.header("BMI Distribution")
    bmi_df = filtered_df[filtered_df["bmi"].notna()]
    if len(bmi_df) > 0:
        fig5 = px.box(bmi_df, y="bmi", title="BMI Distribution")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.write("No BMI data for this study.")

    # Data Table - show all columns with NA
    st.header("Sample Data")
    display_df = filtered_df.fillna("NA")
    st.dataframe(display_df.head(50), use_container_width=True)
