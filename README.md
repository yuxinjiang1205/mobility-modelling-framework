# Human Mobility Representation Framework

This repository contains the source code supporting my MSc
Artificial Intelligence dissertation at the University of Stirling. 
It builds a human mobility representation framework for Manchester District by
integrating eight demographic datasets from the 2021 Census, three behavioural evidence
datasets from the National Travel Survey (NTS), and POI data derived from
Ordnance Survey (OS).

The code is supplied as dissertation evidence.

## Code authorship and AI collaboration

Unless a file or code section says, the code was written by me. 
AI-generated, AI-assisted, and AI-derived sections contain in the cells of all notebooks.
[`AI_USAGE.md`] documents all the prompts and functions or the codes.

The AI tools used were ChatGPT (OpenAI), OpenAI Codex, and GitHub Copilot. 
Original development conversations were mainly in Chinese and are no longer available, 
so the prompt records are concise reconstructions rather than exact transcripts. 
I remained responsible for the research design, ontology and mapping
decisions, methodological interpretation, and revision of AI suggestions.

## Repository structure

```
data/                 Included all raw data and locations for external inputs
notebooks/            Processing, integration, framework, and validation code
ontology/             Regrouped framework categories and cross-dataset mappings
src/                  Reusable integration, constraint, and framework functions
AI_USAGE.md           AI collaboration and code-provenance register
requirements.txt      Python dependencies
```
### Notes for `data/` path:

1. `data/` path contains the folders for all the raw datasets and processed JSON files.
2. Even though RM014: Distance travelled to work by age dataset was downloaded from ONS
    and incorporated into the representative profile space, the file path is
    `data/mobility/raw/` instead of `data/demographic/raw/` due to the representation
    and information provided.
3. OS POI raw data is licensed. This project extracted this data through Digimap.
    The regrouped POI count is provided in the dissertation document. Users can rebuiled the dataset
    by extracting the numbers from the dissertation report.

### Notes for `notebook/` path:

1. This `notebook/` path contains all the notebooks for constructing the proposed framework.
2. `notebook/behaviour` contains:
    (1) NTS0611a trip-purpose by age and sex probability distribution construction;
    (2) NTS0502b trip-start-time by trip purpose probability distribution construction;
    (3) NTS0409a travel-mode by trip purpose probability distribution construction;
    (4) NTS0611a trip-purpose constraints;
    (5) NTS0409a travel-mode constraints
3. `notebook/demographic` includes all the seven Census 2021 datasets' processing procedures,
    excluding RM014.
4. `notebook/mobility` includes the processing of RM014.
5. `notebook/integration` includes: 
    (1) the construction of unconstrained representative profile space;
    (2) the construction of constrained representative profile space (Zero-value filtering, Employment);
    (3) the construction of the Behavioural Evidence Layer;
    (4) the integration process of the Demographic Layer and the Behavioural Evidence Layer.
6. `notebook/opportunity` includes the construction of the Opportunity Layer and
    the Industry Opportunity Component.
7. `notebook/framework` includes the final framework integration.
8. `notebook/validation` includes three validation approaches:
    (1) NTS0611a internal distribution consistency check
    (2) NTS0502b internal distribution consistency check and Constraint Validation
    (3) Log transformation sensitivity analysis

### Notes for `ontology/` path:

1. This `data/` path includes the following methodology decisions:
    (1) Framework age groups;
    (2) Framework household categories;
    (3) Framework trip purposes (for NTS datasets integration);
    (4) Framework trip purpose harmonisation (for NTS datasets integration);
    (5) 10 framework POI groups;
    (6) Framework Trip purpose to POI mapping (strategies and associated POI category of each trip purpose);
    (7) Industry to POI mapping (for Industry Opportunity Component);
    (8) Study area py file to filter the Manchester District (used in every Census dataset)

### Notes for `src/` path:

1. This `ontology/` path includes:
    (1) Reusable behavioural constraints (trip-purpose and travel-mode);
    (2) The integration function for the Demographic and Behavioural Evidence Layers;
    (3) The complete framework construction function

### Notes for `output/` path:

1. This `ontology/` path includes:
    (1) The Demographic Layer's output (the integration of 3 probability distributions)
    (2) The representative profile space (constrained and unconstrained)
    (3) The Opportunity Layer
    (4) All validation figures

## Environment and installation

Python 3.10 or newer is recommended. From the repository root, create and
activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\activate           # Windows PowerShell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

Open each notebook from its own directory so that its relative `../../data`
and `../../ontology` paths resolve correctly. The `%pip` installation command
retained in the OS POI notebook is not needed when `requirements.txt` has
already been installed.

## External data dependencies

Original datasets are excluded from the submission archive. Download
them from the official sources and save them using the following paths and
filenames before rerunning the relevant preprocessing notebooks.

1. Census 2021 TS007: Age by single year, `data/demographic/raw/age/TS007_Age.xlsx`
   [ONS TS007](https://www.ons.gov.uk/datasets/TS007/editions/2021/versions/3)
2. Census 2021 RM008: Car or van availability by household composition, 
   `data/demographic/raw/car_ownership_by_household/RM008_Car_ownership_by_household.xlsx`
   [ONS RM008](https://www.ons.gov.uk/datasets/RM008/editions/2021/versions/3)
3. Census 2021 RM024: Economic activity status by sex by age, 
   `data/demographic/raw/economic_activity_status/ RM024_Economic_activity_status_by_age.xlsx`
   [ONS RM024](https://www.ons.gov.uk/datasets/RM024/editions/2021/versions/3)
4. Census 2021 RM032: Ethnic group by sex by age, 
   `data/demographic/raw/ethnic_group/RM032_Ethnic_group_by_age.xlsx`
   [ONS RM032](https://www.ons.gov.uk/datasets/RM032/editions/2021/versions/1)
5. Census 2021 RM057: Household composition by age, 
   `data/demographic/raw/household_by_age/RM057_Household_composition_by_age.xlsx`
   [ONS RM057](https://www.ons.gov.uk/datasets/RM057/editions/2021/versions/1?showAll=hh_family_composition_15a)
6. Census 2021 RM062: Industry by age,
    `data/demographic/raw/industry/RM062_Industry_by_age.xlsx`
    [ONS RM062](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/labourmarketvariablescensus2021/industrycurrent/classifications)
7. Census 2021 RM121: Sex by age, `data/demographic/raw/sex/RM121_Sex.xlsx`
    [ONS RM121](https://www.ons.gov.uk/datasets/RM121/editions/2021/versions/1)
8. Census 2021 RM014: Distance travelled to work by age, 
    `data/mobility/raw/travel_distance/RM014_Distance_travelled_to_work_by_age.xlsx`
    [ONS RM014](https://www.ons.gov.uk/datasets/RM014/editions/2021/versions/3)
9. NTS0409, `data/nts/raw/nts0409.ods`
    [DfT NTS purpose-of-trip tables](https://www.gov.uk/government/statistical-data-sets/nts04-purpose-of-trips)
10. NTS0502, `data/nts/raw/nts0502.ods`
    [DfT NTS purpose-of-trip tables](https://www.gov.uk/government/statistical-data-sets/nts04-purpose-of-trips)
11. NTS0611, `data/nts/raw/nts0611.ods`
    [DfT NTS purpose-of-trip tables](https://www.gov.uk/government/statistical-data-sets/nts04-purpose-of-trips)

### Licensed OS Points of Interest data

The OS Points of Interest source data is licensed and is not included. The
processed `District_manchester_poi_counts.xlsx` file is also excluded from the
submission.

To recreate the required processed counts:

1. Open `notebooks/opportunity/os_poi_manchester_preprocessing.ipynb`.
2. Update the archive path in the `zipfile.ZipFile(...)` cell and the GeoPackage
   path in the `gpd.read_file(...)` cell to match the file name.
3. Run the notebook. It filters `Manchester District`, applies the
   author-defined ten-category POI regrouping, and checks that no categories are
   unmapped.
4. Run the final export cell. It creates
   `data/POI/processed/manchester/District_manchester_poi_counts.xlsx`, with
   worksheet `POI_Count_District_Manchester`, for the downstream opportunity
   notebooks.

### To Rebuild this framework
To rebuild this framework, the following is the recommended process:
1. Run `notebooks/demographic/representative_profile_construction.ipynb`
   to build the unconstrained representative profile space.
2. Run `notebooks/framework/constrained_representative_profile_space.ipynb`
   to build the constrained representative profile space. This is the input
   for this framework.
3. Run `notebooks/integration/behaviour_evidence_integration.ipynb`
   to integrate three NTS distributions. This is the output of the
   Behavioural Evidence Layer.
4. Run `notebooks/opportunity/opportunity_layer_construction.ipynb`
   to build the Opportunity Layer. The Opportunity Layer output is generated
   in this notebook.
5. Run `notebooks/opportunity/opportunity_industry_component.ipynb`
   to build the Industry Opportunity Component.
6. Run `notebooks/framework/complete_framework_construction.ipynb`
   to build the final model.