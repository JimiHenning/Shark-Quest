import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def group_and_filter_by_type(df, groupby_cols, attack_type=None, count_threshold=0):
    """
    Groups the DataFrame by specified columns and applies filter conditions.

    Parameters:
    - df: The DataFrame to group and filter
    - groupby_cols: List of columns to group by
    - filter_conditions: A dictionary containing column names and their corresponding filter conditions

    Returns:
    - A filtered DataFrame grouped by specified columns with a 'count' column
    """
    # Group by the specified columns and calculate the count of each group
    grouped_df = df.groupby(groupby_cols).size().reset_index(name='count')

    # Apply the count filter
    grouped_df = grouped_df[grouped_df['count'] > count_threshold]

    # Apply the type filter if attack_type is provided
    if attack_type:
        grouped_df = grouped_df[grouped_df['type'] == attack_type]

    return grouped_df


def clean_merge_and_plot(p_sa, up_sa, merge_on="country", provoked_col="count_x", unprovoked_col="count_y", drop_columns=None):
    """
    Merges two dataframes, calculates totals and provoked/unprovoked ratios, and visualizes results.

    Parameters:
    - p_sa: DataFrame for provoked attacks
    - up_sa: DataFrame for unprovoked attacks
    - merge_on: Column name to merge on (default: 'country')
    - provoked_col: Column name for provoked counts (default: 'count_x')
    - unprovoked_col: Column name for unprovoked counts (default: 'count_y')
    - drop_columns: list of column names to drop, default None

    Returns:
    - A DataFrame sorted by the provoked/unprovoked ratio
    - A seaborn plot showing the ratio of provoked attacks by country
    """
    # Merge the dataframes
    merged_df = pd.merge(
        left=p_sa,
        right=up_sa,
        on=merge_on,
        how='inner'
    ).reset_index(drop=True).rename(
        columns={
            provoked_col: "provoked",
            unprovoked_col: "unprovoked"
        }
    )

    # Calculate total and ratio directly on columns (vectorized)
    merged_df["total"] = merged_df["provoked"] + merged_df["unprovoked"]
    merged_df["ratio"] = (merged_df["provoked"] /
                          merged_df["total"] * 100).round(2)

    # Sort by the 'ratio' column in descending order
    merged_df = merged_df.sort_values(
        by="ratio", ascending=False).reset_index(drop=True)

    # Drop columns if provided
    if drop_columns:
        columns_to_drop = [
            col for col in drop_columns if col in merged_df.columns]
        merged_df = merged_df.drop(columns=columns_to_drop)

    # Print the cleaned DataFrame
    # display(merged_df)

    # Plotting the ratio of provoked attacks by country
    sns.catplot(data=merged_df, kind="bar", x=merge_on, y="ratio", hue="total")
    plt.xticks(rotation=90)
    plt.ylabel("Provoked / Total attacks")
    plt.tight_layout()
    plt.show()

    return merged_df
