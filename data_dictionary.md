# Data Dictionary

## Overview
This document defines all columns in harmonized_metadata.tsv (1,535 samples, 28 columns)

## Required Columns (Holobiome Standard)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| study_id | string | BioProject ID | PRJNA521587 |
| subject_id | string | Unique patient identifier | Pt_Fibro_122 |
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

### Cancer FMT Trial (PRJNA1289847)
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| disease_stage | string | Cancer stage | IV_or_unresectable |
| min_age | string | Minimum age requirement | 18+ |

## Controlled Vocabulary

### disease_status
- Fibromyalgia
- Ankylosing Spondylitis
- Multiple Sclerosis
- Rheumatoid Arthritis
- Cancer (FMT Trial)
- Healthy Control

### host_sex
- Male
- Female

### antibiotic_status
- no_antibiotics_2_months (Fibromyalgia - exclusion if antibiotics in preceding 2 months)
- no_antibiotics_1_month (RA - exclusion if antibiotics within 1 month)
- no_antibiotics_at_collection (MS - exclusion if antibiotics during sample collection)

### ethnicity
- Chinese (RA studies - conducted at Peking Union Medical College Hospital)
- majority_caucasian (Fibromyalgia - paper states majority were Caucasian)

### source_provenance
- SRA (from NCBI SRA metadata)
- SRA;Table_S1 (SRA + Excel supplement)
- SRA;GitHub_Supplement (SRA + GitHub repository)
- SRA;Inferred_From_Paper (SRA + implicit data from paper text)

## Missingness Codes
- NA: Data not available or not applicable

## Data Sources by Study

| Study ID | Disease | Primary Source | Supplement Source | Implicit Data |
|----------|---------|----------------|-------------------|---------------|
| PRJNA375935 | Ankylosing Spondylitis | SRA CSV | Excel Table S1 | - |
| PRJNA521587 | Fibromyalgia | SRA CSV | GitHub | ethnicity, antibiotic_status |
| PRJDB7767 | Multiple Sclerosis | SRA CSV | - | antibiotic_status, relapse_status |
| PRJNA1289847 | Cancer (FMT Trial) | SRA CSV | - | disease_stage, treatment |
| PRJEB6997 | Rheumatoid Arthritis | SRA CSV | - | ethnicity, age_range, antibiotic_status |
| PRJEB6337 | Rheumatoid Arthritis | SRA CSV | - | ethnicity, age_range, antibiotic_status |
