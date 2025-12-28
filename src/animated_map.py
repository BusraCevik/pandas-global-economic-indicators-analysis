
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


# -----------------------------
# Global style (pastel turquoise)
# -----------------------------
MAIN_COLOR = "#5FA8A8"
LIGHT_COLOR = "#9ED6D6"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
REF_LINE_COLOR = "#7A7A7A"
BORDER_COLOR = "#000000"


def _standard_layout(fig, y_title=None):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_COLOR),
        title_font_color=DARK_COLOR,
        xaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            tickangle=45,
            showline=True,
            linecolor=BORDER_COLOR,
            linewidth=1,
            mirror=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            title=y_title,
            showline=True,
            linecolor=BORDER_COLOR,
            linewidth=1,
            mirror=True
        )
    )

    # dış çerçeve
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=0, y0=0,
        x1=1, y1=1,
        line=dict(color=BORDER_COLOR, width=1)
    )

    return fig


def build_dashboard(
    intermediate_csv,
    global_trends_csv,
    country_summary_csv,
    country_id="tr",
    output_html_path="docs/index.html"
):
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    df_inter = pd.read_csv(intermediate_csv)
    df_global = pd.read_csv(global_trends_csv)
    df_country = pd.read_csv(country_summary_csv)

    # =================================================
    # Animated GDP Map
    # =================================================
    df_map = df_inter[df_inter["GDP"] > 0]

    z_min = np.log10(df_map["GDP"].min())
    z_max = np.log10(df_map["GDP"].max())

    map_fig = px.choropleth(
        df_map,
        locations="Country_ISO3",
        locationmode="ISO-3",
        color=np.log10(df_map["GDP"]),
        hover_name="Country",
        animation_frame="Year",
        projection="natural earth",
        color_continuous_scale=[GRID_COLOR, LIGHT_COLOR, MAIN_COLOR],
        labels={"color": "GDP (log scale)"},
        title="Global GDP Distribution Over Time",
        range_color=[z_min, z_max]
    )

    map_fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        margin=dict(t=60, b=0),
        font=dict(color=DARK_COLOR),
        coloraxis=dict(cmin=z_min, cmax=z_max)
    )

    # =================================================
    # Global Inflation Trend
    # =================================================
    inflation_fig = go.Figure()
    inflation_fig.add_trace(
        go.Scatter(
            x=df_global["Year"],
            y=df_global["global_mean_inflation"],
            mode="lines",
            line=dict(color=MAIN_COLOR, width=2)
        )
    )
    inflation_fig.update_layout(title="Global Inflation Trend Over Time")
    inflation_fig = _standard_layout(inflation_fig, "Inflation (%)")

    # =================================================
    # Global GDP Growth Trend
    # =================================================
    gdp_growth_fig = go.Figure()
    gdp_growth_fig.add_trace(
        go.Scatter(
            x=df_global["Year"],
            y=df_global["mean_global_gdp_growth"],
            mode="lines",
            line=dict(color=MAIN_COLOR, width=2)
        )
    )
    gdp_growth_fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=REF_LINE_COLOR
    )
    gdp_growth_fig.update_layout(title="Global GDP Growth Trend")
    gdp_growth_fig = _standard_layout(gdp_growth_fig, "GDP Growth (%)")

    # =================================================
    # Top Countries by Average GDP
    # =================================================
    top_df = df_country.sort_values("avg_gdp", ascending=False).head(10)

    top_fig = go.Figure()
    top_fig.add_trace(
        go.Bar(
            x=top_df["country_name"],
            y=top_df["avg_gdp"],
            marker_color=LIGHT_COLOR
        )
    )
    top_fig.update_layout(title="Top Countries by Average GDP")
    top_fig = _standard_layout(top_fig, "Average GDP")

    # =================================================
    # Country GDP Trend
    # =================================================
    country_df = df_inter[df_inter["Country_ID"] == country_id]

    gdp_country_fig = go.Figure()
    gdp_country_fig.add_trace(
        go.Scatter(
            x=country_df["Year"],
            y=country_df["GDP"],
            mode="lines",
            line=dict(color=LIGHT_COLOR, width=1.8)
        )
    )
    gdp_country_fig.add_trace(
        go.Scatter(
            x=country_df["Year"],
            y=country_df["GDP_rolling_avg"],
            mode="lines",
            line=dict(color=MAIN_COLOR, width=2.5)
        )
    )
    gdp_country_fig.update_layout(title=f"GDP Trend for {country_id.upper()}")
    gdp_country_fig = _standard_layout(gdp_country_fig, "GDP")

    # =================================================
    # Country Inflation Trend
    # =================================================
    infl_country_fig = go.Figure()
    infl_country_fig.add_trace(
        go.Scatter(
            x=country_df["Year"],
            y=country_df["Inflation_CPI"],
            mode="lines",
            line=dict(color=LIGHT_COLOR, width=1.8)
        )
    )
    infl_country_fig.add_trace(
        go.Scatter(
            x=country_df["Year"],
            y=country_df["Inflation_rolling_avg"],
            mode="lines",
            line=dict(color=MAIN_COLOR, width=2.5)
        )
    )
    infl_country_fig.update_layout(title=f"Inflation Trend for {country_id.upper()}")
    infl_country_fig = _standard_layout(infl_country_fig, "Inflation (%)")

    # =================================================
    # Write Dashboard
    # =================================================
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Global Economic Indicators Dashboard</title></head><body>")
        f.write("<h1 style='color:#3E7C7C'>Global Economic Indicators Analysis</h1>")

        f.write(pio.to_html(map_fig, full_html=False, include_plotlyjs="cdn"))
        f.write(pio.to_html(inflation_fig, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(gdp_growth_fig, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(top_fig, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(gdp_country_fig, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(infl_country_fig, full_html=False, include_plotlyjs=False))

        f.write("</body></html>")
