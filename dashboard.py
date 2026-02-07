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

# Map study IDs to disease names
study_to_disease = {
    'PRJNA375935': 'Ankylosing Spondylitis',
    'PRJNA521587': 'Fibromyalgia',
    'PRJDB7767': 'Multiple Sclerosis',
    'PRJNA1289847': 'Cancer (FMT Trial)',
    'PRJEB6997': 'Rheumatoid Arthritis',
    'PRJEB6337': 'Rheumatoid Arthritis'
}

# Create display labels for filter
study_labels = {
    'PRJNA375935': 'PRJNA375935 - Ankylosing Spondylitis',
    'PRJNA521587': 'PRJNA521587 - Fibromyalgia',
    'PRJDB7767': 'PRJDB7767 - Multiple Sclerosis',
    'PRJNA1289847': 'PRJNA1289847 - Cancer (FMT Trial)',
    'PRJEB6997': 'PRJEB6997 - Rheumatoid Arthritis',
    'PRJEB6337': 'PRJEB6337 - Rheumatoid Arthritis'
}

# Sidebar filter - renamed to Studies
st.sidebar.header("Filters")
study_options = ["All Studies"] + [study_labels[s] for s in sorted(df["study_id"].dropna().unique().tolist())]
selected_display = st.sidebar.selectbox("Study", study_options)

# Map back to study_id
reverse_map = {v: k for k, v in study_labels.items()}
if selected_display != "All Studies":
    selected_study = reverse_map.get(selected_display)
else:
    selected_study = "All"

# Apply filter
filtered_df = df.copy()
if selected_study != "All":
    filtered_df = filtered_df[filtered_df["study_id"] == selected_study]

# Metrics
st.header("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Samples", len(filtered_df))
col2.metric("Studies", filtered_df["study_id"].nunique())
col3.metric("With BMI", filtered_df["bmi"].notna().sum())
col4.metric("With Age", filtered_df["host_age"].notna().sum())

# Conquest Map with disease names
st.header("Samples per Study")
study_counts = filtered_df.groupby("study_id").size().reset_index(name="samples")
study_counts["disease"] = study_counts["study_id"].map(study_to_disease)
study_counts["label"] = study_counts["study_id"] + "<br>" + study_counts["disease"]

fig1 = px.bar(study_counts, x="label", y="samples", color="samples", 
              color_continuous_scale="Viridis",
              labels={"label": "Study", "samples": "Samples"})
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

if selected_study == "All":
    # Forensics Heatmap - only on "All"
    st.header("Forensics Heatmap: Data Completeness by Study")
    clinical_cols = ["host_age", "host_sex", "bmi", "disease_status", "timepoint"]
    completeness_data = []
    for study in df["study_id"].unique():
        study_df = df[df["study_id"] == study]
        disease = study_to_disease.get(study, "Unknown")
        row = {"study": f"{study}\n{disease}"}
        for col in clinical_cols:
            if col in study_df.columns:
                pct = (study_df[col].notna().sum() / len(study_df)) * 100
                row[col] = pct
        completeness_data.append(row)

    completeness_df = pd.DataFrame(completeness_data).set_index("study")
    fig2 = px.imshow(completeness_df, color_continuous_scale="RdYlGn", aspect="auto",
                     labels=dict(x="Variable", y="Study", color="% Complete"))
    st.plotly_chart(fig2, use_container_width=True)

    # Disease Distribution
    st.header("Disease Distribution")
    disease_counts = filtered_df["disease_status"].value_counts().reset_index()
    disease_counts.columns = ["disease_status", "count"]
    fig_disease = px.pie(disease_counts, names="disease_status", values="count")
    st.plotly_chart(fig_disease, use_container_width=True)
    
    st.info("Select a specific study to view detailed demographics and sample data.")

else:
    # Show disease name for selected study
    disease_name = study_to_disease.get(selected_study, "Unknown")
    st.subheader(f"Disease: {disease_name}")
    
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
