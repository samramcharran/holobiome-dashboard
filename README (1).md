# Holobiome Microbiome Metadata Harmonization

## Project Overview
Harmonization of 5 microbiome study datasets into a single, ML-ready TSV file.

## Deliverables
1. harmonized_metadata.tsv - Unified metadata file (1,223 samples, 28 columns)
2. dashboard.py - Streamlit visualization dashboard
3. data_dictionary.md - Column definitions and controlled vocabulary
4. README.md - This file

## Live Dashboard
https://holobiome-dashboard-mdypf2e3sxnbppavf6sdhh.streamlit.app/

## Studies Processed (5 studies)
| Study ID | Disease | Samples | Clinical Richness |
|----------|---------|---------|-------------------|
| PRJNA375935 | Ankylosing Spondylitis | 211 | RICH - BMI, age, sex, HLA-B27, treatment |
| PRJNA521587 | Fibromyalgia | 156 | RICH - BMI, age, sex, IBS, depression, anxiety |
| PRJDB7767 | Multiple Sclerosis | 118 | RICH - age, sex, disease_status, relapse_status (100%) |
| PRJEB6997 | Rheumatoid Arthritis | 530 | PARTIAL - ethnicity, age_range, antibiotic_status (implicit) |
| PRJNA1289847 | Cancer (FMT Trial) | 208 | PARTIAL - disease_status only |

## Data Completeness
- host_age: 37.0% (452/1223)
- host_sex: 37.0% (452/1223)
- bmi: 27.5% (336/1223)
- disease_status: 100%
- run_accessions: 100%

## Clinically Rich Datasets (3 of 5)

### 1. Ankylosing Spondylitis (PRJNA375935)
- Source: Excel supplement (Table S1)
- Bridge key: "AS2raw" -> "AS2"
- Data merged: age, sex, BMI, HLA-B27 status, disease duration, treatment
- Samples with clinical data: 180 of 211

### 2. Fibromyalgia (PRJNA521587)
- Source: GitHub repository (https://github.com/gonzalezem/Fibromyalgia)
- Discovery: Found link in paper's Data Availability section
- Bridge key: "Pt_Fibro_122" -> "122"
- Data merged: age, sex, BMI, IBS, smoking, alcohol, pain intensity, depression, anxiety, fatigue, sleep satisfaction
- Implicit data: ethnicity (majority Caucasian), antibiotic_status (no antibiotics 2 months)
- Samples with clinical data: 156 of 156

### 3. Multiple Sclerosis (PRJDB7767)
- Source: SRA metadata + implicit data from paper
- Data: age, sex, disease_status (100% complete for all 118 samples)
- Implicit data: antibiotic_status (no antibiotics at collection), relapse_status (inactive at enrollment)
- Samples with clinical data: 118 of 118 (100%)

## AI/LLM Usage (Agentic Workflow)

### Tools Used
- Claude (Anthropic) - Primary AI assistant via web chat interface
- Google Colab - Cloud Python execution environment

### Agentic Approach: How AI Accelerated This Work

**1. PDF Text Parsing**
- Used PyMuPDF (fitz) library with Claude-generated code to extract text from all PDF papers
- Claude searched extracted text for keywords: "github", "zenodo", "data availability", "inclusion criteria"
- This led to discovering the Fibromyalgia GitHub repository containing rich clinical data

**2. Code Generation**
- Claude wrote all Python scripts for:
  - Loading and exploring CSV/Excel files
  - Schema harmonization (mapping different column names to standard names)
  - Bridge key discovery and data merging
  - Implicit data extraction from paper text
  - Streamlit dashboard creation

**3. Bridge Key Discovery**
- AI analyzed sample IDs across data sources to find linkable patterns:
  - AS study: "AS2raw" in CSV -> "AS2" in Excel (strip "raw" suffix)
  - Fibromyalgia: "Pt_Fibro_122" in CSV -> "122" in GitHub (extract numeric ID)
  - RA study: "SAMEA2737881" in CSV vs "D99" in Excel (no match - identified as trap)

**4. Implicit Data Extraction**
- Claude searched paper text for statements that apply to all samples:
  - "antibiotic treatment in the preceding 2 months" (exclusion criteria) -> antibiotic_status
  - "majority of participants were of Caucasian ethnicity" -> ethnicity
  - "No patients had an active relapse at the time of study enrollment" -> relapse_status
  - "between 18 and 65 years old" -> age_range

### Workflow
1. Uploaded CSVs and Excel supplements to Google Colab
2. Used Claude to explore data structures and identify column mappings
3. Searched PDF papers for external data links (GitHub, Zenodo)
4. Found Fibromyalgia GitHub link -> downloaded supplementary Excel with BMI, IBS, pain scores
5. Merged clinical data using bridge keys (AS from Excel, FM from GitHub)
6. Searched all papers for implicit data (antibiotic status, ethnicity, age ranges)
7. Applied implicit data to appropriate study samples
8. Generated Streamlit dashboard
9. Documented methodology

## Gap Analysis

### Prioritization Strategy
1. First pass: Process all CSVs and Excel supplements for explicit data
2. Second pass: Search PDFs for external links and hidden data sources
3. Third pass: Extract implicit data from paper methods/inclusion criteria
4. Result: Maximized data extraction from all available sources

### Successfully Harmonized (Clinically Rich)
- PRJNA375935 (Ankylosing Spondylitis): Full clinical data from Excel Table S1
- PRJNA521587 (Fibromyalgia): Full clinical data from GitHub supplement + implicit data
- PRJDB7767 (Multiple Sclerosis): Complete demographics from SRA + implicit data from paper

### Partially Harmonized (Implicit Data Only)
- PRJEB6997 (Rheumatoid Arthritis): No bridge key for Excel data, but extracted implicit data (Chinese ethnicity, age 18-65, no antibiotics 1 month)
- PRJNA1289847 (FMT Cancer Trial): Disease status from SRA only

### Trap Dataset Explanation
- PRJEB6997 (RA): Excel supplement has rich individual data (D99, D98 sample IDs with BMI, age, treatment) but CSV uses different IDs (SAMEA2737881). Searched for mapping in paper and supplement - none exists. Confirmed as trap dataset. Extracted all available implicit data instead.

### External Sources Checked
- PDF papers: Read all 5 main papers and PDF supplements using PyMuPDF
- Excel supplements: Parsed all provided Excel files
- CSV files: PRJNA521587.csv, PRJDB7767.csv, PRJEB6997.csv, PRJNA1289847.csv, ERP005860_SRP100575.csv
- GitHub: Found and used https://github.com/gonzalezem/Fibromyalgia
- Zenodo: Checked FMT paper link (https://zenodo.org/records/12820832) - only contained reference genomes, not patient clinical data

## References (Papers Used)

1. **Fibromyalgia (PRJNA521587)**
   - Minerbi A, Gonzalez E, Brereton NJB, et al. "Altered microbiome composition in individuals with fibromyalgia." *Pain*. 2019.

2. **Multiple Sclerosis (PRJDB7767)**
   - Takewaki D, Suda W, Sato W, et al. "Alterations of the gut ecological and functional microenvironment in different stages of multiple sclerosis." *PNAS*. 2020.

3. **Rheumatoid Arthritis (PRJEB6997)**
   - Zhang X, et al. "The oral and gut microbiomes are perturbed in rheumatoid arthritis and partly normalized after treatment." *Nature Medicine*. 2015;21(8):895.

4. **Cancer FMT Trial (PRJNA1289847)**
   - "Fecal microbiota transplantation plus immunotherapy in non-small cell lung cancer and melanoma: the phase 2 FMT-LUMINate trial." *Nature Medicine*. 2025.

5. **Ankylosing Spondylitis (PRJNA375935 / ERP005860)**
   - Wen C, Zheng Z, Shao T, et al. "Quantitative metagenomics reveals unique gut microbiome biomarkers in ankylosing spondylitis." *Genome Biology*. 2017.

## Input Files Used

### CSV Files (from SRA)
- PRJNA521587.csv (156 samples) - Fibromyalgia
- PRJDB7767.csv (118 samples) - Multiple Sclerosis
- PRJEB6997.csv (530 samples) - Rheumatoid Arthritis
- PRJNA1289847.csv (208 samples) - Cancer FMT Trial
- ERP005860_SRP100575.csv (211 samples) - Ankylosing Spondylitis

### Excel Supplements
- supp-ERP005860_SRP100575.xlsx - AS clinical data (BMI, age, sex, HLA-B27)
- supp-PRJEB6997.xlsx - RA clinical data (trap - no bridge key)
- fibro_supplement.xlsx - FM clinical data from GitHub

### PDF Papers & Supplements
- 5 main papers (listed above)
- supp-PRJDB7767.pdf - MS supplement (group averages only)
- supp-PRJNA521587.pdf - FM supplement (led to GitHub discovery)
- supp-PRJNA1289847.pdf - FMT supplement (no patient-level data)

## Running the Dashboard
```bash
pip install streamlit pandas plotly
streamlit run dashboard.py
```

## Files
- harmonized_metadata.tsv - Final harmonized dataset (1,223 samples, 28 columns)
- dashboard.py - Streamlit dashboard
- data_dictionary.md - Column definitions
- README.md - This documentation
