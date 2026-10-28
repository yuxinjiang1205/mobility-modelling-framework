# AI Usage and Code Provenance

## Authorship convention

Unless otherwise indicated, source code in this repository was written by
me. AI-generated, AI-assisted, or AI-derived sections are identified
by inline comments that refer to an entry in this file. Code reused in more than
one location retains the same provenance reference; reuse does not create a
fictitious second prompt.

The tools used were ChatGPT (OpenAI), OpenAI Codex, and GitHub Copilot.
The original development conversations were mainly in Mandarin and are no 
longer available. Prompts below are therefore concise reconstructed final 
prompts based on the confirmed task requirements and retained code. 

I remained responsible for the research design, framework
architecture, ontology and mapping decisions identified below, execution of the
code, inspection of outputs, methodological interpretation, and acceptance or
revision of AI suggestions. The final demonstration should be read together with
this record as evidence of critical human review.

## Non-code assistance

AI assisted with the organisation of notebook, headings and short
Markdown explanations. I designed the processing workflow and decided
the notebook content. This documentation assistance does not change
the code-authorship records below.

## AI collaboration register

### AI-01 — Framework-age aggregation pattern

- **Prompt:** "Group the remapped age data by local authority and framework age
  group, then sum the relevant population count."
- **Mandarin Prompt:** "幫我把age group套到現在的function 然後算每個group的total"
- **Locations:** `notebooks/demographic/age_dataset.ipynb` cell 18; the adapted
  aggregation statements in `sex_dataset.ipynb` cell 17,
  `ethnic_group_dataset.ipynb` cell 18,
  `economic_activity_status_by_age_dataset.ipynb` cell 17,
  `industry_by_age_dataset.ipynb` cell 18,
  `household_by_age_dataset.ipynb` cell 22; and
  `notebooks/mobility/travel_distance_dataset.ipynb` cell 18.
- **Human contribution and evaluation:** I (Peter Jiang) designed each dataset
  workflow, mapping, filtering, function structure, ordering, and export. The
  aggregation pattern was adapted to each dimension and checked against source
  totals.

### AI-02 — Household-category reverse lookup

- **Prompt:** "Convert `FRAMEWORK_HOUSEHOLD_CATEGORY` into an old-to-new
  category mapping and apply it to the `Household Category` column."
- **Mandarin Prompt:** "幫我把merge好的household composition套到現在的function 
  然後算每個group的total"
- **Locations:** `notebooks/demographic/car_ownership_by_household_dataset.ipynb`
  cells 19–20 and `household_by_age_dataset.ipynb` cells 20–21.
- **Human contribution and evaluation:** I (Peter Jiang) designed the household
  ontology and surrounding processing. The mapped categories and resulting
  counts were inspected before reuse.

### AI-03 — Reshape NTS0409a from wide to long format

- **Prompt:** "Reshape the wide NTS0409a table into long format with `Purpose`
  and `Trips` columns so that it matches the structure of the other project
  datasets."
- **Mandarin Prompt:** "幫我把nts0409的資料結構轉成跟另外兩個一樣 travel mode跟trip purpose一對一"
- **Location:** `notebooks/behaviour/nts0409_dataset.ipynb` cell 16.
- **Human contribution and evaluation:** AI identified the wide-table structure
  after I (Peter Jiang) supplied the source data. I confirmed that the long
  format met the integration requirement and inspected the transformed records.

### AI-04 — NTS0409a travel-mode probabilities

- **Prompt:** "Aggregate trips by year, purpose, and main mode, then calculate
  each mode's probability within its purpose as trips divided by total trips."
- **Mandarin Prompt:** "我需要計算nts0409 travel mode by age的p, 跟另外兩個nts datasets一樣"
- **Location:** `notebooks/behaviour/nts0409_dataset.ipynb` cell 20.
- **Evaluation:** The output was checked by purpose and passed the probability
  validation recorded in the notebook.

### AI-05 — NTS0409a probability validation

- **Prompt:** "Validate that every purpose-specific probability distribution
  sums to one and that every probability is between zero and one."
- **Mandarin Prompt:** "我現在需要驗證nts0409每一row的總和都是1"
- **Location:** `notebooks/behaviour/nts0409_dataset.ipynb` cell 21.
- **Evaluation:** I (Peter Jiang) ran and inspected the validation table and
  assertions.

### AI-06 — NTS0409a readable probability matrix

- **Prompt:** "Pivot the processed data into a readable purpose-by-main-mode
  probability matrix."
- **Mandarin Prompt:** "幫我把整個nts0409整合成matrix版讓他更好閱讀"
- **Location:** `notebooks/behaviour/nts0409_dataset.ipynb` cell 22.
- **Human contribution:** I (Peter Jiang) requested the matrix presentation to make
  the processed evidence easier to read; subsequent inspection and JSON export
  were performed by me.

### AI-07 — Convert NTS0502b percentages to probabilities

- **Prompt:** "Convert the hourly percentage columns to probabilities by
  dividing them by 100."
- **Mandarin Prompt:** "nts0502的p跟另外兩個不一樣 我要轉成一樣的"
- **Location:** `notebooks/behaviour/nts0502_dataset.ipynb` cell 18, conversion
  statement only.
- **Human contribution:** I (Peter Jiang) selected the reporting period and hourly
  fields and wrote the removal of the `All day (%)` column.

### AI-08 — NTS0502b row-distribution validation

- **Prompt:** "Check that each row's hourly trip-start-time probabilities sums
  to one."
- **Mandarin Prompt:** "我要算nts0502每行的p總和是1"
- **Location:** `notebooks/behaviour/nts0502_dataset.ipynb` cell 20.
- **Evaluation:** The vectorised check was run on all retained purpose rows.

### AI-09 — NTS0611a trip-purpose probabilities

- **Prompt:** "Calculate total trips across the trip-purpose columns and divide
  each purpose count by its row total to obtain trip-purpose probabilities."
- **Mandarin Prompt:** "幫我把nts0611的trips 除以總total然後算出p"
- **Location:** `notebooks/behaviour/nts0611_dataset.ipynb` cells 19–21.
- **Human contribution:** I (Peter Jiang) selected and named the framework trip
  purposes and approved the probability representation.

### AI-10 — NTS0611a probability validation

- **Prompt:** "Validate that every trip-purpose probability distribution sums
  to one."
- **Mandarin Prompt:** "我要驗證nts0611的每一row總和是1"
- **Locations:** `notebooks/behaviour/nts0611_dataset.ipynb` cells 22 and 40.
- **Evaluation:** The checks were executed before export of the harmonised
  evidence.

### AI-11 — Census population helper for NTS age harmonisation

- **Prompt:** "Load and filter the Census single-year age data for the study
  area, then create a function that returns the population within a supplied age
  range."
- **Mandarin Prompt:** "因為兩個data的age分類不同 我要用weighted average的方式把兩個age groups對齊"
- **Location:** `notebooks/behaviour/nts0611_dataset.ipynb` cells 24–26 and
  29–30.
- **Human contribution:** I (Peter Jiang) independently defined the framework-to-NTS
  age overlaps in cell 27.

### AI-12 — Population-weighted NTS age harmonisation

- **Prompt:** "Use Census population weights for overlapping NTS age bands to
  harmonise trip-purpose probabilities by framework age group and sex."
  - **Mandarin Prompt:** "因為兩個data的age分類不同 我要用weighted average的方式把兩個age groups
    對齊 然後再算p 幫我計算+寫出過程 我需要理解"
- **Location:** `notebooks/behaviour/nts0611_dataset.ipynb` cells 32–36.
- **Human contribution and evaluation:** AI proposed the interpolation method;
  I (Peter Jiang) evaluated and accepted it for the framework age groups and
  inspected the harmonised distributions.

### AI-13 — POI log transformation

- **Prompt:** "Transform the POI counts so that larger counts still have more
  influence but do not dominate the opportunity distribution."
- **Mandarin Prompt:** "因為我沒有資料證明一對多poi的trip purpose的實際distribution 所以我要把raw
  count列入考慮 假設opportunities較多 然後再去做normalise 但是這樣raw count影響力會太大 
  所以我需要一個方法把所有raw count數值壓到一個範圍 再做normalise"
- **Locations:** `notebooks/opportunity/opportunity_layer_construction.ipynb`
  cell 12 and the reused function in
  `opportunity_industry_component.ipynb` cell 19.
- **Human contribution and evaluation:** I (Peter Jiang) defined the modelling
  requirement. AI proposed `log1p`; I accepted it after inspecting its
  effect and later designed a framework-wide sensitivity test.

### AI-14 — Opportunity-distribution implementation

- **Prompt:** "Build POI probability distributions from the mapping table: skip
  excluded mappings, assign probability one to direct and representative
  mappings, and normalise log-transformed POI counts for context-dependent
  mappings."
- **Mandarin Prompt:** "我要做出opportunity layer 裡面要包含我設計的四種mappings 還有trip to poi 
  的分別機率"
- **Location:** `notebooks/opportunity/opportunity_layer_construction.ipynb`
  cell 17.
- **Human contribution:** I (Peter Jiang) designed the mapping strategies and every
  trip-purpose-to-POI mapping.

### AI-15 — Opportunity-layer validation and nested output

- **Prompt:** "Validate the opportunity probabilities, mapping uniqueness and
  excluded outcomes; then construct and validate the complete nested
  opportunity-layer output."
- **Mandarin Prompt:** "我現在要驗證機率分布是對的 然後要產出一個json output 就跟另外兩個layer一樣"
- **Location:** `notebooks/opportunity/opportunity_layer_construction.ipynb`
  cells 21 and 23–26.
- **Evaluation:** I (Peter Jiang) ran the checks, inspected the output, and exported
  the approved JSON.

### AI-16 — Industry-mapping coverage checks

- **Prompt:** "Report industries missing from the industry-to-POI ontology and
  ontology entries not present in the profile data."
- **Mandarin Prompt:** "幫我檢查一下每個industry都有map到了"
- **Location:** `notebooks/opportunity/opportunity_industry_component.ipynb`
  cell 13.
- **Human contribution:** The ontology itself was designed by I (Peter Jiang).

### AI-17 — Industry-specific POI distributions

- **Prompt:** "Use Industry I as an example to calculate probabilities for its
  two mapped POI categories, then generalise the logic to every industry: retain
  null mappings, normalise log counts for multiple categories, and assign
  probability one to single-category mappings."
- **Mandarin Prompt:** "industry I是唯一的一對多 所以我要套用log算機率分布"
- **Location:** `notebooks/opportunity/opportunity_industry_component.ipynb`
  cells 20–23.
- **Human contribution:** I (Peter Jiang) defined the industry mappings and
  identified Industry I as the only multi-category case.

### AI-18 — Industry-distribution validation

- **Prompt:** "Validate that every non-null industry POI distribution sums to
  one."
- **Mandarin Prompt:** "確定一下每個industry的機率是不是除了I以外都是1"
- **Location:** `notebooks/opportunity/opportunity_industry_component.ipynb`
  cell 25.

### AI-19 — Prevent duplicated car-ownership profiles

- **Prompt:** "Aggregate car ownership by household category and car-ownership
  category before merging to prevent duplicate profile rows, then verify that
  every household category contains four car-ownership categories."
- **Mandarin Prompt:** "我發現CAR OWNERSHIP DATASET的數值剛好是兩倍 問題是甚麼? 
  我現在要解決他"
- **Location:** `notebooks/integration/representative_profile_construction.ipynb`
  cells 11–12.
- **Human contribution and evaluation:** I (Peter Jiang) identified the doubled car
  counts during integration. Collaborative diagnosis found two source rows for
  each harmonised household-category and car-ownership combination. I
  verified the corrected totals.

### AI-20 — Representative-profile merge workflow

- **Prompt:** "Construct a representative profile space by starting with age
  and sequentially merging the processed demographic and mobility datasets on
  their shared attributes."
- **Mandarin Prompt:** "我現在要建立representative profile sapce 要怎麼進行?"
- **Location:** `notebooks/integration/representative_profile_construction.ipynb`
  cells 14 and 16–33.
- **Human modification:** I (Peter Jiang) changed cells 14 and 16 to retain `Age
  Population` and `Sex Population` for subsequent source-support filtering.

### AI-21 — Representative-profile source-total validation

- **Prompt:** "Create a reusable check that compares every source-dataset total
  with the corresponding deduplicated total retained in the representative
  profile space."
- **Mandarin Prompt:** "我現在需要做驗證 確定每個count都跟source data一樣 沒有變多或變少"
- **Location:** `notebooks/integration/representative_profile_construction.ipynb`
  cells 35–36.

### AI-22 — Extract mapped NTS evidence

- **Prompt:** "Create functions that use `NTS_TRIP_PURPOSE_MAPPING` to extract
  matching NTS0611a trip-purpose, NTS0409a travel-mode, and NTS0502b start-time
  evidence for a framework trip purpose, and test them with Business."
- **Mandarin Prompt:** "我要設計一個py file然後可以import讓每個nts dataset都套用 然後產出
  shared trip purpose classification"
- **Location:** `notebooks/integration/behaviour_evidence_integration.ipynb`
  cells 17–24.
- **Human contribution:** I (Peter Jiang) designed every cross-table mapping.

### AI-23 — Assemble and export the Behavioural Evidence Layer

- **Prompt:** "Combine the three extracted NTS distributions for each framework
  trip purpose, assemble them for every mapped purpose, convert the DataFrames
  to records, and export the evidence layer as JSON."
- **Mandarin Prompt:** "我要把3個nts datasets結合起來成為behavioural layer 然後export成一個json"
- **Location:** `notebooks/integration/behaviour_evidence_integration.ipynb`
  cells 26–39.
- **Human modification:** I (Peter Jiang) revised variable names in the generated
  assembly code.

### AI-24 — Demographic-behaviour integration implementation

- **Prompt:** "Implement the demographic-behaviour integration:
  retrieve age- and sex-specific trip-purpose probabilities, apply the
  trip-purpose constraint, attach each retained purpose's start-time and
  travel-mode distributions, apply the travel-mode constraint, validate every
  distribution, and return the profile with its behavioural representation."
- **Mandarin Prompt:** "現在opportunity layer還沒做 但是我要先試試看我兩層layer能不能結合
  先試試看 可以我再繼續往下做"
- **Locations:** `notebooks/integration/demographic_behaviour_layers_integration.ipynb`
  cell 10 and `src/demographic_behaviour_layers_integration.py`.
- **Human contribution:** I (Peter Jiang) defined the integration logic and output
  structure. The reusable source file shares the notebook provenance.

### AI-25 — Demographic-behaviour validation cases

- **Prompt:** "Implement the validation profiles and verify the
  exact trip-purpose and travel-mode removals, unchanged start-time evidence,
  and renormalised probabilities."
- **Mandarin Prompt:** "現在已經結合好 我要先看幾個代表性的profile有沒有成功被調整 先測
  一個完全沒constraint的 再來側一個小孩然後沒工作的 然後我要測travel mode沒車的profile
  然後還有wfh的"
- **Location:** `notebooks/integration/demographic_behaviour_layers_integration.ipynb`
  cells 12–18.
- **Human contribution:** I (Peter Jiang) defined the constraints and validation
  cases.

### AI-26 — Display one integrated behavioural profile

- **Prompt:** "Present one integrated profile as readable demographic,
  trip-purpose, start-time and travel-mode tables with probability sums."

- **Location:** `notebooks/integration/demographic_behaviour_layers_integration.ipynb`
  cell 20.
- **Mandarin Prompt:** "先幫我跑一個profile看看有沒有成功"

### AI-27 — General source-support filter

- **Prompt:** "Remove representative-profile combinations where any retained
  source-count column is missing or zero, and report the numbers before,
  removed, and remaining."
- **Mandarin Prompt:** "我現在要直接用zero filter 只要有一個column的值是0就刪除"
- **Location:** `notebooks/integration/constrained_representative_profile_space.ipynb`
  cell 8.
- **Human contribution:** I (Peter Jiang) changed to this general method after
  retaining the source-count fields in the preceding integration notebook.

### AI-28 — Child and employment profile constraints

- **Prompt:** "Implement the profile rules: child profiles must
  have non-applicable economic status; employed profiles must have applicable
  industry and work-distance values; non-employed profiles must have `Does not
  apply` for both employment fields."
- **Mandarin Prompt:** "我要把我已經設計好的constraints寫成code 首先只要是0~11的人就不能有工作 然後
  有工作的人 travel distance跟economic status都不能是does not apply"
- **Location:** `notebooks/integration/constrained_representative_profile_space.ipynb`
  cells 10 and 12.
- **Human contribution:** I (Peter Jiang) defined both rules. The child rule remains
  as an additional confirmation after the general source-support filter.

### AI-29 — Constrained-profile validation

- **Prompt:** "Validate the positive source counts, employment consistency,
  inactive-profile information, and absence of demographic or complete-row
  duplicates."
- **Mandarin Prompt:** "幫我看一下我設定的constraints有沒有成功applied"
- **Location:** `notebooks/integration/constrained_representative_profile_space.ipynb`
  cells 13–16.

### AI-30 — Trip-purpose constraint implementation

- **Prompt:** "Implement the trip-purpose constraint: remove
  Commuting and Business when industry does not apply, remove Commuting for
  work-from-home profiles.
- **Mandarin Prompt:** "現在設定trip purpose的constraint 只要沒工作的人就不能有commuting跟
  business 然後wfh的人不能commuting"
- **Locations:** `notebooks/behaviour/trip_purpose_constraint.ipynb` cell 9 and
  the corresponding function in `src/constraints.py`.
- **Human contribution:** I (Peter Jiang) defined the rules.

### AI-31 — Trip-purpose constraint tests

- **Prompt:** "Implement the selected test profiles and validate the exact
  purpose removals and probability renormalisation."
- **Mandarin Prompt:** "測試constraints有沒有作用 找一個沒工作的人 還有一個wfh的人 然後還有
  一個完全沒constrained的人"
- **Location:** `notebooks/behaviour/trip_purpose_constraint.ipynb` cells 12–14.
- **Human contribution:** I (Peter Jiang) selected the test cases.

### AI-32 — Travel-mode constraint implementation

- **Prompt:** "Implement the travel-mode constraints: remove driver and
  motorcycle for young children, remove driver and passenger for no-car
  households, remove London-specific modes outside London, and renormalise the
  remaining probabilities."
- **Mandarin Prompt:** "現在把我已經設計好的travel mode constraint寫成code 只要0~11不能開車+mortor
  然後家裡沒車的就不能passenger跟driver 然後移除london相關交通工具 最後p總和要是1"
- **Locations:** `notebooks/behaviour/travel_mode_constraint.ipynb` cell 10 and
  the corresponding function in `src/constraints.py`.
- **Human contribution:** I (Peter Jiang) defined the age and car-ownership rules.
  Following supervisor feedback, I revised the earlier category
  merging so London-only modes are removed for the Manchester study area.

### AI-33 — Travel-mode constraint tests

- **Prompt:** "Implement the selected age and car-ownership test cases and
  validate exact mode removals, probability sums, taxi availability, and
  unchanged unaffected distributions."
- **Mandarin Prompt:** "現在可以測有車的小孩看是不是只有motor driver被移除 沒車的小孩三個都要移除
  成年人有車跟沒車這樣"
- **Location:** `notebooks/behaviour/travel_mode_constraint.ipynb` cells 12–14.
- **Human contribution:** I (Peter Jiang) selected the test cases.

### AI-34 — Reproducible complete-framework example

- **Prompt:** "Select a reproducible random representative profile, construct
  its complete framework output, and display the resulting tables."
- **Mandarin Prompt:** "我現在要設定一個固定的profile去跑我的完整framework 然後display的方式
  我需要每個martix都完整展開 不要混成一張 要總共四張"
- **Location:** `notebooks/framework/complete_framework_construction.ipynb`
  cell 13.

### AI-35 — Complete framework integration

- **Prompt:** "Develop a reusable function that combines all three layers and industry"
- **Mandarin Prompt:** "我現在想直接設定一個function把我三層layer全部結合在一起 也包含  
  ndustry component"
- **Location:** `src/complete_framework.py`, `construct_complete_framework`.
- **Human contribution:** I (Peter Jiang) defined the complete integration logic,
  Commuting-only refinement, and preservation requirements.

### AI-36 — Display excluded POI probabilities as N/A

- **Prompt:** "Preserve underlying `None`/`NaN` probabilities for excluded POI
  mappings, but display them as `N/A`; format valid probabilities to four decimal
  places without modifying the original DataFrame."
- **Mandarin Prompt:** "visiting home這個沒有POI 我要讓他出來是n/a不是none"
- **Location:** `src/complete_framework.py`, `display_complete_framework`.
- **Human contribution:** I (Peter Jiang) requested the change after inspecting the
  original display.

### AI-37 — Unconstrained NTS0611 consistency validation

- **Prompt:** "For every unique Age-Sex profile that triggers no constraint,
  compare the framework trip-purpose distribution with the corresponding
  NTS0611 distribution and fail if any category or probability differs. Save
  plots for all passing cases, display only three representative plots, and do
  not create plots if validation fails."
- **Mandarin Prompt:** "先測試0611 只要沒constraint的age-sex組合 看0611分布是不是
  一樣的 要一樣才能畫圖 然後只要畫三張在notebook 其他全部存到folder"
- **Location:** `notebooks/validation/unconstrained_0611_consistency.ipynb`, all
  code except the setup.
- **Human contribution:** I (Peter Jiang) proposed the validation, required all
  unique cases, specified the plot-saving/display behaviour, and required
  fail-fast execution before plot generation.

### AI-38 — Constraint and distribution validation

- **Prompt:** The complete consolidated prompt is retained in the notebook's
  `AI Collaboration Record` and is not duplicated here.
- **Location:** `notebooks/validation/constraint_distribution_validation_2.ipynb`,
  all code cells.
- **Human contribution and evaluation:** I (Peter Jiang) reviewed the constraint
  rules against the dissertation methodology, required coverage of every
  retained profile row, ran the final notebook, inspected failures and figures,
  and approved the reported interpretation.

### AI-39 — POI log-transformation sensitivity test

- **Prompt:** "Implement a methodology sensitivity test comparing
  log-transformed and raw POI-count normalisation for every affected
  multi-category mapping in the Opportunity Layer and Industry component.
  Validate both distributions, summarise the differences."
- **Mandarin Prompt:** "我要畫一張圖去測試有log跟沒有log的分布圖 做我的sensitivity
  analysis"
- **Location:** `notebooks/validation/poi_log_transformation_sensitivity_test.ipynb`,
  all code cells.
- **Human contribution:** I (Peter Jiang) proposed the test because the research
  proposal specified sensitivity analysis, chose the comparison and complete
  mapping scope, and specified both figures.

### AI-40 — Framework age-group code

- **Prompt:** "Implement the nine framework age boundaries as a
  conversion function and ordered category list."
- **Mandarin Prompt:** "我要做一個py file然後包含age group跟order的function"
- **Location:** `ontology/FRAMEWORK_AGE_GROUP.py`.
- **Human contribution:** Every boundary was defined by I (Peter Jiang).

### AI-41 — Framework trip-purpose list

- **Prompt:** "Format the and framework trip purposes as a Python list."
- **Mandarin Prompt:** "把framework trip purpose做成一個py"
- **Location:** `ontology/FRAMEWORK_TRIP_PURPOSE.py`.

### AI-42 — Cross-NTS trip-purpose mapping formatting

- **Prompt:** "Format the mappings between framework trip purposes and the 
  NTS0409a and NTS0502b purpose categories as a nested Python
  dictionary."
- **Mandarin Prompt:** "我要設定一個py把3個datasets都map在一起"
- **Location:** `ontology/NTS_TRIP_PURPOSE_MAPPING.py`.

### AI-43 — Trip-purpose-to-POI mapping formatting

- **Prompt:** "Format the trip-purpose-to-POI categories and mapping strategies as a 
  pandas DataFrame, including the excluded private-home outcome."
- **Mandarin Prompt:** "幫我把trip poi mapping這個output做成dataframe 要包含
  strategies還有excluded的poi allocation"
- **Location:** `ontology/TRIP_PURPOSE_TO_POI_MAPPING.py`.

### AI-44 — Readable Manchester POI count pivot

- **Prompt:** "Pivot the Manchester District activity-category counts into a
  readable table with one column per POI category."
- **Mandarin Prompt:** "我覺得改成pivot好了 現在這樣很難看懂"
- **Location:** `notebooks/opportunity/os_poi_manchester_preprocessing.ipynb`,
  the `borough_activity_pivot` code cell.
- **Human contribution and evaluation:** I (Peter Jiang) selected Manchester
  District, designed every regrouping category, and checked the pivot against
  the long-form counts.

### AI-45 — Regrouped POI spatial plot

- **Prompt:** "Plot the regrouped POI activity categories for Manchester
  District with a legend and small point markers."
- **Mandarin Prompt:** "我現在想畫一張plot看一下整體poi分布情形 然後跟boundary重疊再一起"
- **Location:** `notebooks/opportunity/os_poi_manchester_preprocessing.ipynb`,
  the spatial visualisation code cell after the pivot.
- **Human contribution and evaluation:** I (Peter Jiang) selected the data,
  geographic scope, and category mapping, then inspected the plot. Saved plot
  output is omitted because the underlying OS data is licensed.

### AI-46 — Log-transformed POI count function

- **Prompt:** "Extend the POI count function to add a `log1p`
  transformation of each POI count."
- **Mandarin Prompt:** "我們已經決定要用log了 幫我打function"
- **Location:** `notebooks/opportunity/os_poi_manchester_preprocessing.ipynb`,
  `get_poi_data_with_log`.
- **Human contribution and evaluation:** I (Peter Jiang) wrote `get_poi_data`,
  chose the modelling need for count-based opportunity strength, and inspected
  the transformed result.

### AI-47 — Reproducible processed-count export

- **Prompt:** "Export the `get_poi_data('Manchester District')`
  result to the processed Excel path and sheet name used by the downstream
  framework."
- **Mandarin Prompt:** "因為現在的Excel在本機 幫我寫個code然後把poi raw count(合併後的)
  寫成function for reproducibitily"
- **Location:** `notebooks/opportunity/os_poi_manchester_preprocessing.ipynb`,
  final export code cell.
- **Purpose:** Added during submission preparation so that the excluded
  licensed input can be processed into the required downstream dependency.