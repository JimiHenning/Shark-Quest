# SHARK QUEST

## New Kids On The Block

### Overview

**SHARK QUEST** is a data analysis project aimed at exploring patterns and insights in historical shark attack incidents worldwide. By cleaning and analyzing the dataset, we aim to answer specific hypotheses related to the timing, severity, and circumstances of shark attacks.

### Data Cleaning Steps

- **Column Renaming**: Aligned all column names with the predefined data schema.
- **Adding/Dropping Columns**: Added necessary columns and removed irrelevant ones based on the schema.
- **String Manipulation**: Stripped whitespace and standardized text cases.
- **Handling Missing Values**: Replaced placeholders like 'N/A', 'null' with `NaN`.
- **Removing Duplicates**: Eliminated duplicate records.
- **Data Type Casting**: Converted columns to appropriate data types as specified in the schema.
- **Date Cleaning**: Standardized date formats for consistency.
- **Category Validation**: Ensured all categorical data matched expected values.
- **Value Replacement**: Applied specific replacements from a JSON configuration to standardize entries.

### Analysis and Findings

#### Hypothesis 1: Shark attacks are more concentrated in the PM

- **Approach**: Analyzed the distribution of shark attacks across different times of the day.
- **Findings**: Contrary to the hypothesis, the data revealed that shark attacks are most concentrated around noon.
- **Visualization**: Created a bar plot showing the number of attacks by time category.

#### Hypothesis 2: Some shark species are more dangerous than others

- **Approach**: Assigned a severity score to each attack and grouped the data by shark species.
- **Findings**:
  - Identified the top six most dangerous shark species based on the highest percentage of fatal attacks.
  - Also identified the "friendliest" shark species with the highest percentage of non-injury incidents and a fatality rate below 5%.
- **Visualization**: Generated bar plots to illustrate the most dangerous and friendliest shark species.

#### Hypothesis 3: Some countries have a higher provoked to total attack ratio

- **Approach**: Compared the number of provoked attacks to unprovoked attacks by country, both over all time and within the last 50 years.
- **Findings**: Certain countries exhibit a higher ratio of provoked attacks, indicating regional differences in human-shark interactions.
- **Visualization**: Plotted the provoked vs. unprovoked attack ratios for the top countries.

#### Hypothesis 4: Provoked attacks have higher severity than unprovoked attacks

- **Approach**: Analyzed the severity distribution between provoked and unprovoked attacks.
- **Findings**: The data did not support the hypothesis; provoked attacks did not have a higher severity compared to unprovoked attacks.
- **Visualization**: Used a categorical plot to compare the severity percentages between attack types.

### Presentation : [Presentation](https://prezi.com/view/WsnTyCtr55yQJoHtGzep/)
