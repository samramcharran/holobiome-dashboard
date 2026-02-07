import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Holobiome Data Dashboard", layout="wide")
st.title("Holobiome Microbiome Metadata Dashboard")

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

studies = ["All"] + list(df["study_id"].dropna().unique())
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

# Conquest Map - Samples per study
st.header("Conquest Map: Samples per Study")
study_counts = filtered_df.groupby("study_id").size().reset_index(name="samples")
fig_conquest = px.bar(study_counts, x="study_id", y="samples", 
                      title="Samples Banked per Study",
                      color="samples", color_continuous_scale="Viridis")
st.plotly_chart(fig_conquest, use_container_width=True)

# Forensics Heatmap - Data Missingness
st.header("Forensics Heatmap: Data Completeness by Study")

clinical_cols = ["host_age", "host_sex", "bmi", "disease_status", 
                 "antibiotic_status", "ethnicity", "age_range",
                 "ibs", "smoking", "pain_intensity", "depression", "anxiety",
                 "disease_duration_years", "hla_b27_status", "treatment",
                 "relapse_status", "disease_stage"]

# Calculate completeness percentage by study
completeness_data = []
for study in df["study_id"].unique():
    study_df = df[df["study_id"] == study]
    row = {"study_id": study}
    for col in clinical_cols:
        if col in study_df.columns:
            pct = (study_df[col].notna().sum() / len(study_df)) * 100
            row[col] = pct
        else:
            row[col] = 0
    completeness_data.append(row)

completeness_df = pd.DataFrame(completeness_data)
completeness_df = completeness_df.set_index("study_id")

fig_heatmap = px.imshow(completeness_df, 
                        labels=dict(x="Clinical Variable", y="Study", color="Completeness %"),
                        title="Data Completeness Heatmap (% non-missing)",
                        color_continuous_scale="RdYlGn",
                        aspect="auto")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Clinical Data Summary
st.header("Clinical Data Summary")
col1, col2 = st.columns(2)

with col1:
    # Age distribution
    if filtered_df["host_age"].notna().sum() > 0:
        fig_age = px.histogram(filtered_df, x="host_age", nbins=20,
                               title="Age Distribution",
                               color="study_id")
        st.plotly_chart(fig_age, use_container_width=True)

with col2:
    # Sex distribution
    if filtered_df["host_sex"].notna().sum() > 0:
        sex_counts = filtered_df["host_sex"].value_counts().reset_index()
        sex_counts.columns = ["sex", "count"]
        fig_sex = px.pie(sex_counts, values="count", names="sex",
                         title="Sex Distribution")
        st.plotly_chart(fig_sex, use_container_width=True)

# BMI by Study
st.header("BMI Distribution by Study")
bmi_df = filtered_df[filtered_df["bmi"].notna()]
if len(bmi_df) > 0:
    fig_bmi = px.box(bmi_df, x="study_id", y="bmi", 
                     title="BMI Distribution by Study",
                     color="study_id")
    st.plotly_chart(fig_bmi, use_container_width=True)
else:
    st.write("No BMI data available for selected filters.")

# Ethnicity and Antibiotic Status
st.header("Implicit Data Summary")
col1, col2 = st.columns(2)

with col1:
    eth_df = filtered_df[filtered_df["ethnicity"].notna()]
    if len(eth_df) > 0:
        eth_counts = eth_df["ethnicity"].value_counts().reset_index()
        eth_counts.columns = ["ethnicity", "count"]
        fig_eth = px.pie(eth_counts, values="count", names="ethnicity",
                         title="Ethnicity Distribution")
        st.plotly_chart(fig_eth, use_container_width=True)

with col2:
    ab_df = filtered_df[filtered_df["antibiotic_status"].notna()]
    if len(ab_df) > 0:
        ab_counts = ab_df["antibiotic_status"].value_counts().reset_index()
        ab_counts.columns = ["antibiotic_status", "count"]
        fig_ab = px.pie(ab_counts, values="count", names="antibiotic_status",
                        title="Antibiotic Status Distribution")
        st.plotly_chart(fig_ab, use_container_width=True)

# Data Table
st.header("Sample Data")
st.dataframe(filtered_df.head(100), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**References and Data Sources**")
st.markdown('''
- PRJNA521587: Fibromyalgia (GitHub: gonzalezem/Fibromyalgia)
- PRJNA375935: Ankylosing Spondylitis (Excel Table S1)
- PRJDB7767: Multiple Sclerosis (SRA + implicit data)
- PRJEB6997/PRJEB6337: Rheumatoid Arthritis (implicit data only - no bridge key)
- PRJNA1289847: Cancer FMT Trial (implicit data)

Data sources: NCBI SRA, BioProject, Excel supplements, GitHub repositories, implicit data from papers.
''')
