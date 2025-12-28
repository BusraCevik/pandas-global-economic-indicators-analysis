import pandas as pd
import os
import pycountry


def prepare_data(input_path, output_path, drop_na=True, fill_method=None, save_cleaned=True):

    df = pd.read_csv(input_path)

    df.rename(columns={
        'country_name': 'Country',
        'country_id': 'Country_ID',
        'year': 'Year',
        'Inflation (CPI %)': 'Inflation_CPI',
        'GDP (Current USD)': 'GDP',
        'GDP per Capita (Current USD)': 'GDP_per_Capita',
        'Unemployment Rate (%)': 'Unemployment_Rate',
        'Interest Rate (Real, %)': 'Interest_Rate',
        'Inflation (GDP Deflator, %)': 'Inflation_GDP_Deflator',
        'GDP Growth (% Annual)': 'GDP_Growth',
        'Current Account Balance (% GDP)': 'Current_Account',
        'Government Expense (% of GDP)': 'Gov_Expense',
        'Government Revenue (% of GDP)': 'Gov_Revenue',
        'Tax Revenue (% of GDP)': 'Tax_Revenue',
        'Gross National Income (USD)': 'GNI',
        'Public Debt (% of GDP)': 'Public_Debt'
    }, inplace=True)

    # -----------------------------
    # 🚨 Year FIX (NO datetime)
    # -----------------------------
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    # keep only realistic years
    df = df[(df["Year"] >= 1900) & (df["Year"] <= 2100)]
    df["Year"] = df["Year"].astype(int)

    # -----------------------------
    # ISO3
    # -----------------------------
    import pycountry
    def to_iso3(country_name):
        try:
            return pycountry.countries.lookup(country_name).alpha_3
        except:
            return None

    df["Country_ISO3"] = df["Country"].apply(to_iso3)

    # -----------------------------
    # Missing values
    # -----------------------------
    critical_cols = ['GDP', 'Inflation_CPI', 'Unemployment_Rate']

    if drop_na:
        df.dropna(subset=critical_cols, inplace=True)

    if fill_method:
        df[critical_cols] = df[critical_cols].fillna(method=fill_method)

    df.sort_values(["Country", "Year"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    if save_cleaned:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ Cleaned data saved to: {output_path}")

    return df

    return df
