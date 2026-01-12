import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# =================================================
# Aggregations
# =================================================
def create_country_summary(input_path, output_path):
    """
    Creates a country-level summary from cleaned economic data.

    Metrics per country:
    - Average Inflation
    - Average GDP
    - Average Unemployment
    - Max Inflation
    - Min Inflation
    """

    df = pd.read_csv(input_path)

    summary_df = (
        df.groupby("Country_ID")
        .agg(
            country_name=("Country", "first"),
            avg_inflation=("Inflation_CPI", "mean"),
            avg_gdp=("GDP", "mean"),
            avg_unemployment=("Unemployment_Rate", "mean"),
            max_inflation=("Inflation_CPI", "max"),
            min_inflation=("Inflation_CPI", "min"),
        )
        .reset_index()
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summary_df.to_csv(output_path, index=False)

    print(f"Country summary saved to: {output_path}")
    return summary_df


# =================================================
# Feature Engineering (Intermediate Dataset)
# =================================================
def create_intermediate_dataset(input_path, output_path, rolling_window=5):
    """
    Creates an enriched time-series dataset with derived economic indicators.

    Features:
    - GDP growth rate (pct_change)
    - Inflation change
    - Rolling averages for GDP and Inflation
    """

    df = pd.read_csv(input_path)


    df["Year"] = df["Year"].astype(int)


    df = df.sort_values(["Country_ID", "Year"])

    # GDP growth rate (%)
    df["GDP_growth_pct"] = (
        df.groupby("Country_ID")["GDP"]
        .pct_change() * 100
    )

    # Inflation change (%)
    df["Inflation_pct_change"] = (
        df.groupby("Country_ID")["Inflation_CPI"]
        .pct_change() * 100
    )

    # Rolling averages (trend indicators)
    df["GDP_rolling_avg"] = (
        df.groupby("Country_ID")["GDP"]
        .rolling(window=rolling_window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["Inflation_rolling_avg"] = (
        df.groupby("Country_ID")["Inflation_CPI"]
        .rolling(window=rolling_window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Intermediate dataset saved to: {output_path}")
    return df




# =================================================
# Country-Level Trend Analysis
# =================================================
def compute_country_trends(input_path, output_path, recent_years=5):
    """
    Computes country-level economic trend indicators.

    Metrics:
    - Mean GDP growth over the last N years
    - GDP volatility (standard deviation)
    - Mean inflation rate
    - Inflation trend direction
    - Number of crisis years (negative GDP growth)
    """

    df = pd.read_csv(input_path)
    df["Year"] = pd.to_datetime(df["Year"])
    df = df.sort_values(["Country_ID", "Year"])

    country_names = (
        df.groupby("Country_ID")["Country"]
        .first()
        .rename("Country")
    )

    # GDP growth rate
    df["GDP_growth_pct"] = (
        df.groupby("Country_ID")["GDP"]
        .pct_change() * 100
    )

    # Mean GDP growth (recent years)
    mean_recent_growth = (
        df.groupby("Country_ID")
        .tail(recent_years)
        .groupby("Country_ID")["GDP_growth_pct"]
        .mean()
        .rename("mean_gdp_growth_last_years")
    )

    # GDP volatility (economic stability indicator)
    gdp_volatility = (
        df.groupby("Country_ID")["GDP"]
        .std()
        .rename("gdp_volatility_std")
    )

    # Mean inflation
    inflation_mean = (
        df.groupby("Country_ID")["Inflation_CPI"]
        .mean()
        .rename("mean_inflation")
    )

    # Inflation trend direction (simple slope approximation)
    inflation_trend_value = (
        df.groupby("Country_ID")["Inflation_CPI"]
        .apply(lambda x: x.iloc[-1] - x.iloc[0])
    )

    inflation_trend_direction = (
        inflation_trend_value
        .apply(lambda x: "Upward" if x > 0 else "Downward")
        .rename("inflation_trend_direction")
    )

    # Crisis years count (negative GDP growth)
    crisis_year_count = (
        df[df["GDP_growth_pct"] < 0]
        .groupby("Country_ID")
        .size()
        .rename("crisis_year_count")
    )

    # Combine all indicators
    trends_df = pd.concat(
        [
            country_names,
            mean_recent_growth,
            gdp_volatility,
            inflation_mean,
            inflation_trend_direction,
            crisis_year_count,
        ],
        axis=1
    ).reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    trends_df.to_csv(output_path, index=False)

    print(f"Country trends saved to: {output_path}")
    return trends_df


# =================================================
# Global Trend Analysis
# =================================================
def analyze_global_trends(input_path, output_path):
    df = pd.read_csv(input_path)

    # Year must be integer
    df["Year"] = df["Year"].astype(int)

    # Sort by year
    df = df.sort_values("Year")

    global_df = (
        df.groupby("Year")
        .agg(
            global_mean_inflation=("Inflation_CPI", "mean"),
            mean_global_gdp_growth=("GDP_growth_pct", "mean")
        )
        .reset_index()
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    global_df.to_csv(output_path, index=False)

    print(f"Global trends saved to: {output_path}")

    return global_df
