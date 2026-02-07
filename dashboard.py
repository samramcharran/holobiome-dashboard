import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Holobiome Data Dashboard", layout="wide")
st.title("Holobiome Microbiome Metadata Dashboard")
st.caption("Educational project - Data from public repositories")

@st.cache_data
def load_data():
    df = pd.read_csv("harmonized_metadata.tsv", sep="\t")
    return df

df = load_data()

# Create display labels with study IDs
study_disease_map = {
    'Ankylosing Spondylitis': 'Ankylosing Spondylitis (PRJNA375935)',
    'Fibromyalgia': 'Fibromyalgia (PRJNA521587)',
    'Healthy Control': 'Healthy Control (PRJNA521587)',
    'Multiple Sclerosis': 'Multiple Sclerosis (PRJDB7767)',
    'Cancer (FMT Trial)': 'Cancer FMT Trial (PRJNA1289847)',
    'Rheumatoid Arthritis': 'Rheumatoid Arthritis (PRJEB6997)'
}

# Sidebar filter
st.sidebar.header("Filters")
disease_options = ["All"] + [study_disease_map.get(d, d) for d in sorted(df["disease_status"].dropna().unique().tolist())]
selected_display = st.sidebar.selectbox("Disease Status", disease_options)

# Map back to original value for filtering
reverse_map = {v: k for k, v in study_disease_map.items()}
if selected_display != "All":
    selected_disease = reverse_map.get(selected_display, selected_display)
else:
    selected_disease = "All"

# Apply filter
filtered_df = df.copy()
if selected_disease != "All":
    filtered_df = filtered_df[filtered_df["disease_status"] == selected_disease]

# Metrics
st.header("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Samples", len(filtered_df))
col2.metric("Studies", filtered_df["study_id"].nunique())
col3.metric("With BMI", filtered_df["bmi"].notna().sum())
col4.metric("With Age", filtered_df["host_age"].notna().sum())

# Conquest Map - always show
st.header("Samples per Study")
study_counts = filtered_df.groupby("study_id").size().reset_index(name="samples")
fig1 = px.bar(study_counts, x="study_id", y="samples", color="samples", color_continuous_scale="Viridis")
st.plotly_chart(fig1, use_container_width=True)

if selected_disease == "All":
    # Forensics Heatmap - only on "All"
    st.header("Forensics Heatmap: Data Completeness by Study")
    clinical_cols = ["host_age", "host_sex", "bmi", "disease_status", "timepoint"]
    completeness_data = []
    for study in df["study_id"].unique():
        study_df = df[df["study_id"] == study]
        row = {"study_id": study}
        for col in clinical_cols:
            if col in study_df.columns:
                pct = (study_df[col].notna().sum() / len(study_df)) * 100
                row[col] = pct
        completeness_data.append(row)

    completeness_df = pd.DataFrame(completeness_data).set_index("study_id")
    fig2 = px.imshow(completeness_df, color_continuous_scale="RdYlGn", aspect="auto",
                     labels=dict(x="Variable", y="Study", color="% Complete"))
    st.plotly_chart(fig2, use_container_width=True)

    # Disease Distribution
    st.header("Disease Distribution")
    disease_counts = filtered_df["disease_status"].value_counts().reset_index()
    disease_counts.columns = ["disease_status", "count"]
    fig_disease = px.pie(disease_counts, names="disease_status", values="count")
    st.plotly_chart(fig_disease, use_container_width=True)
    
    st.info("Select a specific disease status to view detailed demographics and sample data.")

else:
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
        fig5 = px.box(bmi_df, x="study_id", y="bmi", color="study_id")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.write("No BMI data for this study.")

    # Data Table
    st.header("Sample Data")
    display_df = filtered_df.copy()
    cols_to_keep = []
    for col in display_df.columns:
        if display_df[col].notna().sum() > 0:
            cols_to_keep.append(col)

    display_df = display_df[cols_to_keep]
    st.dataframe(display_df.head(50), use_container_width=True)
