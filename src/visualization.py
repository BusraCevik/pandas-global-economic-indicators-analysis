import pandas as pd
import matplotlib.pyplot as plt
import os


# -----------------------------
# Global style (pastel turquoise)
# -----------------------------
MAIN_COLOR = "#5FA8A8"
LIGHT_COLOR = "#9ED6D6"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
REF_LINE_COLOR = "#7A7A7A"


# =================================================
# Global Trends Visualizations
# =================================================
def plot_global_inflation_trend(input_path, output_path):
    df = pd.read_csv(input_path)

    df["Year"] = df["Year"].astype(int)
    df = df.sort_values("Year")

    plt.figure(figsize=(10, 5))
    plt.plot(
        df["Year"],
        df["global_mean_inflation"],
        color=MAIN_COLOR,
        linewidth=2
    )
    plt.title("Global Inflation Trend Over Time")
    plt.xlabel("Year")
    plt.ylabel("Inflation (%)")
    plt.grid(True, color=GRID_COLOR)

    years = df["Year"].unique()
    plt.xticks(years[::2], rotation=45)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_global_gdp_growth_trend(input_path, output_path):
    df = pd.read_csv(input_path)

    df["Year"] = df["Year"].astype(int)
    df = df.sort_values("Year")

    plt.figure(figsize=(10, 5))
    plt.plot(
        df["Year"],
        df["mean_global_gdp_growth"],
        color=MAIN_COLOR,
        linewidth=2
    )
    plt.axhline(
        0,
        linestyle="--",
        color=REF_LINE_COLOR,
        linewidth=1
    )
    plt.title("Global GDP Growth Trend")
    plt.xlabel("Year")
    plt.ylabel("GDP Growth (%)")
    plt.grid(True, color=GRID_COLOR)

    years = df["Year"].unique()
    plt.xticks(years[::2], rotation=45)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# =================================================
# Country Comparison Visualizations
# =================================================
def plot_top_countries_by_avg_gdp(input_path, output_path, top_n=10):
    df = pd.read_csv(input_path)

    top_df = (
        df.sort_values("avg_gdp", ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(
        top_df["country_name"],
        top_df["avg_gdp"],
        color=LIGHT_COLOR
    )
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_n} Countries by Average GDP")
    plt.ylabel("Average GDP")
    plt.grid(axis="y", color=GRID_COLOR)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_crisis_years_by_country(input_path, output_path, top_n=10):
    df = pd.read_csv(input_path)

    top_df = (
        df.sort_values("crisis_year_count", ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(
        top_df["Country"],
        top_df["crisis_year_count"],
        color=DARK_COLOR
    )
    plt.title("Countries with Most Crisis Years")
    plt.ylabel("Number of Crisis Years")
    plt.xlabel("Country")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", color=GRID_COLOR)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# =================================================
# Country Case Study Visualizations
# =================================================
def plot_country_gdp_trend(input_path, country_id, output_path):
    df = pd.read_csv(input_path)

    df["Year"] = df["Year"].astype(int)
    country_df = df[df["Country_ID"] == country_id]

    if country_df.empty:
        print(f"No data found for country_id: {country_id}")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(
        country_df["Year"],
        country_df["GDP"],
        label="GDP",
        color=LIGHT_COLOR,
        linewidth=1.8
    )
    plt.plot(
        country_df["Year"],
        country_df["GDP_rolling_avg"],
        label="Rolling Average",
        color=MAIN_COLOR,
        linewidth=2.5
    )

    plt.title(f"GDP Trend for {country_id}")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.legend()
    plt.grid(True, color=GRID_COLOR)

    years = country_df["Year"].unique()
    plt.xticks(years[::2], rotation=45)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_country_inflation_trend(input_path, country_id, output_path):
    df = pd.read_csv(input_path)

    df["Year"] = df["Year"].astype(int)
    country_df = df[df["Country_ID"] == country_id]

    if country_df.empty:
        print(f"No data found for country_id: {country_id}")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(
        country_df["Year"],
        country_df["Inflation_CPI"],
        label="Inflation",
        color=LIGHT_COLOR,
        linewidth=1.8
    )
    plt.plot(
        country_df["Year"],
        country_df["Inflation_rolling_avg"],
        label="Rolling Average",
        color=MAIN_COLOR,
        linewidth=2.5
    )

    plt.title(f"Inflation Trend for {country_id}")
    plt.xlabel("Year")
    plt.ylabel("Inflation (%)")
    plt.legend()
    plt.grid(True, color=GRID_COLOR)

    years = country_df["Year"].unique()
    plt.xticks(years[::2], rotation=45)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
