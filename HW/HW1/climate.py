### YOUR IMPORTS HERE ###
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def query_climate(
    df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int
) -> pd.DataFrame:
    query_df = df[df["Country"] == country]
    query_df = query_df[query_df["Year"].isin(range(year_begin, year_end + 1))]
    query_df["Month"] = month
    query_df["Temp"] = query_df["VALUE" + str(month)]

    query_df = query_df[
        ["NAME", "LATITUDE", "LONGITUDE", "Country", "Year", "Month", "Temp"]
    ]

    return query_df


def get_mean_temp(
    df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int
) -> pd.DataFrame:
    temp_df = query_climate(df, country, year_begin, year_end, month)
    temp_df["Mean_Temp"] = (
        temp_df.groupby(["NAME", "LATITUDE", "LONGITUDE"])["Temp"]
        .transform("mean")
        .round(2)
    )

    return temp_df


def temperature_plot(
    df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int
) -> go.Figure:
    df = get_mean_temp(df, country, year_begin, year_end, month)

    hover_data_dict = {"LATITUDE": False, "LONGITUDE": False, "Mean_Temp": True}

    fig_title = (
        "Average temperature at each station during "
        + str(year_begin)
        + " to "
        + str(year_end)
        + " in Month "
        + str(month)
    )

    fig = px.scatter_map(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="NAME",
        hover_data=hover_data_dict,
        color="Mean_Temp",
        title="Map title",
        zoom=5,
        height=500,
    )

    fig.update_layout()

    fig.update_layout(
        map_style="open-street-map",
        title_text=fig_title,  # Set the main text
        title_x=0.5,  # Center the title
        title_xanchor="center",
        title_y=0.9,
        title_yanchor="top",
    )
    fig.update_layout(margin={"r": 25, "t": 100, "l": 25, "b": 50})

    return fig
