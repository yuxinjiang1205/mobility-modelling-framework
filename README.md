# Human Mobility Representation Framework

This repository contains the source code supporting Peter Jiang's MSc
Artificial Intelligence dissertation at the University of Stirling. It builds
a human mobility representation framework for Manchester District by
integrating eight demographic datasets from the 2021 Census, three behavioural evidence
datasets from the National Travel Survey (NTS), and POI data derived from
Ordnance Survey (OS).

The code is supplied as dissertation evidence.

## Code authorship and AI collaboration

Unless a file or code section says, the code was written by Peter Jiang. 
AI-generated, AI-assisted, and AI-derived sections contain in the cells of all notebooks.
[`AI_USAGE.md`] documents all the prompts and functions or the codes.

The AI tools used were ChatGPT (OpenAI), OpenAI Codex, and GitHub Copilot. 
Original development conversations were mainly in Chinese and are no longer available, 
so the prompt records are concise reconstructions rather than exact transcripts. 
Peter Jiang remained responsible for the research design, ontology and mapping
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
1. This path contains all the notebooks for constructing the proposed framework.
2. `notebook/behaviour` contains the three NTS datasets' processing procedures.
3. `notebook/demographic` includes all the seven Census 2021 datasets' processing procedures,
    excluding RM014.
4. `notebook/mobility` includes the processing of RM014.
5. `notebook/integration` includes: 
    (1) the construction of unconstrained and constrained representative profile space;
    (2) the construction of the Behavioural Evidence Layer;
    (3) the integration process of the Demographic Layer and the Behavioural Evidence Layer.
6. `notebook/opportunity` includes the construction of the Opportunity Layer and
    the Industry Opportunity Component.
7. 

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
