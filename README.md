# Individualized cortical gradient and network topology reveal symptom-linked disruptions and neurobiological subtypes in schizophrenia

This repository contains scripts and notebooks for processing cortical thickness data and performing network, gradient, subtyping, and clinical association analyses in the ENIGMA schizophrenia (SCZ) dataset. Preprint: https://doi.org/10.64898/2026.04.25.26351736
* Correspondence to Bin Wan and Matthias Kirchner
* Department of Psychiatry, University Hospitals of Genève, Thonex, Switzerland.
* Synapsy Center for Neuroscience and Mental Health Research, University of Genève, Genève, Switzerland.
------------
## 📂 Workflow Overview
- Data harmonization & preprocessing
- Individual network construction
- Group-level analysis
- Case–control comparisons
- Subtyping
- Clinical associations
- Normative modeling
  
## 🧠 Scripts and Notebooks
`py01_data_processing_enigma.py `
- Harmonizes cortical thickness data across sites using ComBat
- Imputes missing values for individuals with fewer than 6 missing regions
- Outputs processed dataset: data_impute.csv

`py02_network_achitecture.py `
- Computes individual thickness distance matrices
- Applies sparsity thresholds (10%, 20%, 30%, 40%)
- Derives small-world topology measures (rescaled to 0–1)
- Aligns individual gradients to group-level gradients

`vis01_ENIGMA-group.ipynb `
- Computes group-level covariance matrices for SCZ and CTR
- Applies sparsity thresholds (10–40%)
- Derives group-level small-world topology and gradient maps
- Uses 20% sparsity as the primary threshold

`vis02_ENIGMA-case-control.ipynb `
- Compares SCZ vs CTR on:
  - Gradient loadings
  - mall-world topology (shortest path length, clustering coefficient)
- Tests group-by-age and group-by-sex interactions (linear regression)
- Assesses associations with disease duration (SCZ only)
- Computes spatial correlations between statistical maps

`vis03_ENIGMA-subtyping.ipynb `
- Performs k-means clustering based on significant case–control features
- Visualizes clusters in principal component space
- Validates clustering using a half-split approach
- Compares demographic and neurobiological differences between subtypes

`vis04_ENIGMA-clinic.ipynb `
- Applies partial least squares (PLS) to link clinical symptoms and brain features
- Uses bootstrap resampling for statistical inference
- Examines subtype differences in clinical profiles (including age interactions)


`vis05_ENIGMA-GAM.ipynb `
- Builds normative age–thickness models in CTR using GAM
- Computes deviation scores in SCZ
- Examines subtype differences in cortical thickness reductions
- Assesses spatial correlations with gradient and topology measures
- Analyzes subgroup effects by age and disease duration

## ⚙️ Requirements
- BrainSpace
- ENIMGA toolbox
- Scikit-learn
- Statsmodel
- NetworkX
- pyGAM
--------------------------
