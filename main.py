import os

from src.data_preparation import prepare_data
from src.economic_analysis import (
    create_country_summary,
    create_intermediate_dataset,
    compute_country_trends,
    analyze_global_trends
)
from src.visualization import (
    plot_country_gdp_trend,
    plot_country_inflation_trend,
    plot_global_inflation_trend,
    plot_global_gdp_growth_trend,
    plot_crisis_years_by_country,
    plot_top_countries_by_avg_gdp
)

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

RAW_DATA = os.path.join(DATA_DIR, "raw", "dataset.csv")
CLEANED_DATA = os.path.join(DATA_DIR, "cleaned", "cleaned_data.csv")
INTERMEDIATE_DATA = os.path.join(DATA_DIR, "intermediate", "intermediate_data.csv")

CSV_DIR = os.path.join(OUTPUT_DIR, "csv")
PNG_DIR = os.path.join(OUTPUT_DIR, "png")

COUNTRY_SUMMARY_CSV = os.path.join(CSV_DIR, "country_summary.csv")
COUNTRY_TRENDS_CSV = os.path.join(CSV_DIR, "country_trends.csv")
GLOBAL_TRENDS_CSV = os.path.join(CSV_DIR, "global_trends.csv")

PNG_GLOBAL_INFLATION = os.path.join(PNG_DIR, "global_inflation_trend.png")
PNG_GLOBAL_GDP_GROWTH = os.path.join(PNG_DIR, "global_gdp_growth_trend.png")
PNG_TOP_COUNTRIES_GDP = os.path.join(PNG_DIR, "top_countries_avg_gdp.png")
PNG_CRISIS_COUNTRIES = os.path.join(PNG_DIR, "crisis_years_by_country.png")
PNG_COUNTRY_GDP = os.path.join(PNG_DIR, "country_gdp_trend_TR.png")
PNG_COUNTRY_INFLATION = os.path.join(PNG_DIR, "country_inflation_trend_TR.png")

# -------------------------------------------------
# Pipeline (explicit & readable)
# -------------------------------------------------
prepare_data(RAW_DATA, CLEANED_DATA)

create_intermediate_dataset(
    CLEANED_DATA,
    INTERMEDIATE_DATA,
    rolling_window=5
)

create_country_summary(
    CLEANED_DATA,
    COUNTRY_SUMMARY_CSV
)

compute_country_trends(
    INTERMEDIATE_DATA,
    COUNTRY_TRENDS_CSV
)

analyze_global_trends(
    INTERMEDIATE_DATA,
    GLOBAL_TRENDS_CSV
)

plot_global_inflation_trend(
    GLOBAL_TRENDS_CSV,
    PNG_GLOBAL_INFLATION
)

plot_global_gdp_growth_trend(
    GLOBAL_TRENDS_CSV,
    PNG_GLOBAL_GDP_GROWTH
)

plot_top_countries_by_avg_gdp(
    COUNTRY_SUMMARY_CSV,
    PNG_TOP_COUNTRIES_GDP
)

plot_crisis_years_by_country(
    COUNTRY_TRENDS_CSV,
    PNG_CRISIS_COUNTRIES
)

plot_country_gdp_trend(
    INTERMEDIATE_DATA,
    country_id="tr",
    output_path=PNG_COUNTRY_GDP
)

plot_country_inflation_trend(
    INTERMEDIATE_DATA,
    country_id="tr",
    output_path=PNG_COUNTRY_INFLATION
)


def main():
    pass


if __name__ == "__main__":
    main()
