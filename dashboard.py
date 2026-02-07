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

# Sidebar filters
st.sidebar.header("Filters")
diseases = ["All"] + sorted(df["disease_status"].dropna().unique().tolist())
selected_disease = st.sidebar.selectbox("Disease Status", diseases)

studies = ["All"] + sorted(df["study_id"].dropna().unique().tolist())
selected_study = st.sidebar.selectbox("Study", studies)

# Apply filters
filtered_df = df.copy()
if selected_disease != "All":
    filtered_df = filtered_df[filtered_df["disease_status"] == selected_disease]
if selected_study != "All":
    filtered_df = filtered_df[filtered_df["study_id"] == selected_study]

# Metrics
st.header("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Samples", len(filtered_df))
col2.metric("Studies", filtered_df["study_id"].nunique())
col3.metric("With BMI", filtered_df["bmi"].notna().sum())
col4.metric("With Age", filtered_df["host_age"].notna().sum())

# Conquest Map
st.header("Samples per Study")
study_counts = filtered_df.groupby("study_id").size().reset_index(name="samples")
fig1 = px.bar(study_counts, x="study_id", y="samples", color="samples", color_continuous_scale="Viridis")
st.plotly_chart(fig1, use_container_width=True)

# Forensics Heatmap
st.header("Data Completeness Heatmap")
clinical_cols = ["host_age", "host_sex", "bmi", "disease_status"]
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
                 labels=dict(x="Variable", y="Study", color="%"))
st.plotly_chart(fig2, use_container_width=True)

# Age and Sex
st.header("Demographics")
col1, col2 = st.columns(2)

with col1:
    age_df = filtered_df[filtered_df["host_age"].notna()]
    if len(age_df) > 0:
        fig3 = px.histogram(age_df, x="host_age", nbins=15, title="Age Distribution")
        st.plotly_chart(fig3, use_container_width=True)

with col2:
    sex_df = filtered_df[filtered_df["host_sex"].notna()]
    if len(sex_df) > 0:
        fig4 = px.pie(sex_df, names="host_sex", title="Sex Distribution")
        st.plotly_chart(fig4, use_container_width=True)

# BMI
st.header("BMI by Study")
bmi_df = filtered_df[filtered_df["bmi"].notna()]
if len(bmi_df) > 0:
    fig5 = px.box(bmi_df, x="study_id", y="bmi", color="study_id")
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.write("No BMI data for selected filters.")

# Data Table
st.header("Sample Data")
st.dataframe(filtered_df.head(50), use_container_width=True)
