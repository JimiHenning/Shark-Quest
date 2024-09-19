# SHARK QUEST

## New Kids On The Block

### Project Overview

This project analyzes global shark attack data to uncover patterns and insights using data cleaning, preprocessing, and exploratory data analysis.

### Dataset

- **Shark Attack Data**: Loaded from containing detailed records of shark attacks worldwide.
- **Country Coordinates**: Loaded from used for geographical analysis and mapping.

### Data Cleaning and Preprocessing

1. **Column Formatting**: Standardized column names by:
   - Stripping leading and trailing whitespaces.
   - Replacing spaces with underscores.
   - Removing periods.
   - Converting all names to lowercase.

2. **Schema Enforcement**: Applied a data schema from `schema.json` to ensure consistent data types and categories across the dataset.

3. **New Columns**: Created a `severity` column based on the `Injury` field to categorize the severity of each shark attack.

4. **Column Selection**: Selected relevant columns as specified in the data schema for further analysis.

5. **String Stripping**: Removed leading and trailing whitespaces from all string-type columns to standardize the data.

6. **Handling Missing Values**: Replaced placeholder strings like `'N/A'`, `'null'`, and `'--'` with `NaN` to handle missing values.

7. **Duplicate Removal**: Dropped duplicate records.

8. **Index Reset**: Reset the DataFrame index after dropping duplicates for proper alignment.

9. **Value Reformatting**: Used `replacements.json` to replace specific string patterns in data fields for standardization.

10. **Country Name Unification**:
    - Converted all country names to lowercase.
    - Mapped variations of country names to a standardized form.
    - Used a list of valid countries from `countries_df` to filter and retain only recognized country names.

11. **Date Cleaning**:
    - Converted the `date` column to datetime objects, coercing invalid entries.
    - Formatted dates as `DD-MM-YYYY`.
    - Forward-filled missing dates to prevent gaps in the timeline.

12. **Data Type Casting**: Converted columns to appropriate data types as defined in the data schema, ensuring consistency.

13. **Category Cleaning**:
    - Converted categorical columns to string type.
    - Assigned categories based on the data schema.

14. **Clean Data Copy**: Created a clean DataFrame `shark_attacks_clean` for analysis, preserving the original data.
