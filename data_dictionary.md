# Data Dictionary

## Overview
This document defines all columns in harmonized_metadata.tsv (1,223 samples, 28 columns)

## Studies Included (5 studies)

| Study ID | Disease | Samples | Paper | Data Sources |
|----------|---------|---------|-------|--------------|
| PRJNA375935 | Ankylosing Spondylitis | 211 | Wen C, et al. (2017) | CSV, Excel (Table S1), PDF |
| PRJNA521587 | Fibromyalgia | 156 | Minerbi A, et al. (2019) | CSV, GitHub Excel, PDF |
| PRJDB7767 | Multiple Sclerosis | 118 | Takewaki D, et al. (2020) | CSV, PDF |
| PRJNA1289847 | Cancer (FMT Trial) | 208 | FMT-LUMINate (2025) | CSV, PDF |
| PRJEB6997 | Rheumatoid Arthritis | 530 | Zhang X, et al. (2015) | CSV, Excel (trap), PDF |

## Required Columns (Holobiome Standard)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| study_id | string | BioProject ID | PRJNA521587 |
| subject_id | string | Unique patient identifier | Pt_Fibro_122, D69_G |
| sample_id | string | Unique biological sample ID | SAMN10886076 |
| timepoint | string | Collection timepoint | T1, V4, baseline |
| run_accessions | string | Semicolon-delimited SRA Run IDs | SRR8556877;SRR8556878 |
| source_provenance | string | Data source(s) | SRA, SRA;Table_S1, SRA;GitHub_Supplement |
| host_age | float | Age in years | 45.0 |
| host_sex | string | Sex | Male, Female |
| disease_status | string | Disease condition | Fibromyalgia, Ankylosing Spondylitis |
| bmi | float | Body mass index (kg/m2) | 23.5 |

## Implicit Data Columns (Inferred from Papers)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| antibiotic_status | string | Antibiotic use before sample collection | no_antibiotics_2_months |
| ethnicity | string | Participant ethnicity | Chinese, majority_caucasian |
| age_range | string | Age inclusion criteria | 18-65 |

## Study-Specific Clinical Columns

### Ankylosing Spondylitis (PRJNA375935)
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| disease_duration_years | float | Years since diagnosis | 5.0 |
| hla_b27_status | string | HLA-B27 genetic marker | Positive, Negative |
| treatment | string | Current treatment | NSAID, TNF-inhibitor |

### Fibromyalgia (PRJNA521587)
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| ibs | int | Irritable bowel syndrome (0=No, 1=Yes) | 0, 1 |
| smoking | int | Smoking status (0=No, 1=Yes) | 0, 1 |
| alcohol_per_month | float | Alcohol consumption per month | 4.0 |
| pain_intensity | float | Pain intensity score | 7.5 |
| depression | float | Depression score | 3.0 |
| anxiety | float | Anxiety score | 2.5 |
| fatigue | float | Fatigue score | 4.0 |
| years_diagnosed_fm | float | Years since FM diagnosis | 8.0 |
| sleep_satisfaction | float | Sleep satisfaction score | 2.0 |

### Multiple Sclerosis (PRJDB7767)
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| relapse_status | string | Relapse status at enrollment | inactive_at_enrollment |

## Controlled Vocabulary

### disease_status
- Fibromyalgia
- Ankylosing Spondylitis
- Multiple Sclerosis
- Rheumatoid Arthritis
- Cancer (FMT Trial)

### host_sex
- Male
- Female

### antibiotic_status
- no_antibiotics_2_months (Fibromyalgia - exclusion if antibiotics in preceding 2 months)
- no_antibiotics_1_month (RA - exclusion if antibiotics within 1 month)
- no_antibiotics_at_collection (MS - exclusion if antibiotics during sample collection)

### ethnicity
- Chinese (RA study - conducted at Peking Union Medical College Hospital)
- majority_caucasian (Fibromyalgia - paper states majority were Caucasian)

### source_provenance
- SRA (from NCBI SRA metadata)
- SRA;Table_S1 (SRA + Excel supplement)
- SRA;GitHub_Supplement (SRA + GitHub repository)
- SRA;Inferred_From_Paper (SRA + implicit data from paper text)

## Missingness Codes
- NA: Data not available for this sample
- 0: Actual zero value (e.g., ibs=0 means "No IBS", smoking=0 means "Non-smoker")

Note: Missing data is represented as "NA" in the TSV file. Zeros are real values, not placeholders for missing data.

## Data Sources by Study

| Study ID | Disease | CSV | Excel | PDF | GitHub | Zenodo |
|----------|---------|-----|-------|-----|--------|--------|
| PRJNA375935 | Ankylosing Spondylitis | Yes (ERP005860_SRP100575.csv) | Yes (supp-ERP005860_SRP100575.xlsx) | Yes | - | - |
| PRJNA521587 | Fibromyalgia | Yes (PRJNA521587.csv) | Yes (fibro_supplement.xlsx) | Yes | Yes (github.com/gonzalezem/Fibromyalgia) | - |
| PRJDB7767 | Multiple Sclerosis | Yes (PRJDB7767.csv) | - | Yes | - | - |
| PRJNA1289847 | Cancer (FMT Trial) | Yes (PRJNA1289847.csv) | - | Yes | - | Checked (no patient data) |
| PRJEB6997 | Rheumatoid Arthritis | Yes (PRJEB6997.csv) | Yes (supp-PRJEB6997.xlsx - trap) | Yes | - | - |
