
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Holobiome Data Dashboard", layout="wide")
st.title("🦠 Holobiome Microbiome Metadata Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("harmonized_metadata.tsv", sep="\t")
    df = df.replace("NA", np.nan)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
diseases = ["All"] + list(df["disease_status"].dropna().unique())
selected_disease = st.sidebar.selectbox("Disease Status", diseases)

if selected_disease != "All":
    filtered_df = df[df["disease_status"] == selected_disease]
else:
    filtered_df = df

# Main metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Samples", len(filtered_df))
col2.metric("Studies", filtered_df["study_id"].nunique())
col3.metric("With Age Data", filtered_df["host_age"].notna().sum())
col4.metric("With BMI Data", filtered_df["bmi"].notna().sum())

# Conquest Map - Samples per study
st.header("📊 Conquest Map: Samples per Study")
study_counts = filtered_df["study_id"].value_counts().reset_index()
study_counts.columns = ["Study", "Samples"]
fig1 = px.bar(study_counts, x="Study", y="Samples", color="Samples")
st.plotly_chart(fig1, use_container_width=True)

# Forensics Heatmap - Data Missingness
st.header("🔍 Forensics Heatmap: Data Completeness by Study")
cols_to_check = ["host_age", "host_sex", "bmi", "disease_status", "timepoint"]
missingness = []
for study in df["study_id"].unique():
    study_df = df[df["study_id"] == study]
    row = {"study_id": study}
    for col in cols_to_check:
        if col in study_df.columns:
            pct = (study_df[col].notna().sum() / len(study_df)) * 100
        else:
            pct = 0
        row[col] = pct
    missingness.append(row)

miss_df = pd.DataFrame(missingness).set_index("study_id")
fig2 = px.imshow(miss_df, text_auto=".0f", aspect="auto",
                 labels=dict(color="% Complete"),
                 color_continuous_scale="RdYlGn")
st.plotly_chart(fig2, use_container_width=True)

# Disease distribution
st.header("🏥 Disease Distribution")
disease_counts = filtered_df["disease_status"].value_counts().reset_index()
disease_counts.columns = ["Disease", "Count"]
fig3 = px.pie(disease_counts, values="Count", names="Disease")
st.plotly_chart(fig3, use_container_width=True)

# Data table
st.header("📋 Sample Data")
st.dataframe(filtered_df.head(100))
