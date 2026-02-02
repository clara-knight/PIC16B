### YOUR IMPORTS HERE ###
import pandas as pd


def read_NBA_stats(url: str) -> pd.DataFrame:
    stats = pd.read_csv(url)
    cols_to_keep = ["year", "PLAYER", "TEAM", "GP", "PTS", "REB", "AST", "STL", "BLK"]

    return stats[cols_to_keep]


def convert_to_averages(df: pd.DataFrame) -> pd.DataFrame:
    ave_df = df.copy()
    cols_to_avg = ["PTS", "REB", "AST", "STL", "BLK"]
    ave_df[cols_to_avg] = ave_df[cols_to_avg].div(df.GP, axis=0).round(1)
    return ave_df


def player_stat(df: pd.DataFrame, player: str, season: str, stat: str) -> pd.DataFrame:
    player_df = (
        df[(df["PLAYER"] == player) & (df["year"] == season)]
        .copy()
        .reset_index(drop=True)
    )
    player_df["STAT"] = stat
    player_df = player_df[["year", "PLAYER", "TEAM", "STAT", stat]]

    return player_df


def leader(df: pd.DataFrame, season: str) -> pd.DataFrame:
    stats = ["GP", "PTS", "REB", "AST", "STL", "BLK"]
    id_cols = ["year", "PLAYER", "TEAM"]

    season_df = df[df["year"] == season]

    season_df = season_df.melt(
        id_vars=id_cols, value_vars=stats, var_name="stat", value_name="value"
    )

    leader_indices = season_df.groupby("stat", sort=False)["value"].idxmax()

    leader_df = season_df.loc[leader_indices].reset_index(drop=True)

    return leader_df
