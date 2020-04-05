import pandas as pd
import datetime

#filter_team will return all games played by a certain team
def filter_team(df,name):
    return df[(df.HomeTeam == name) | (df.AwayTeam == name)].sort_index()


#home_games will return all home games for a certain team
def home_games(df,name):
    return df[df.HomeTeam == name].sort_index()


#away_games will return all away games for a certain team
def away_games(df,name):
    return df[df.AwayTeam == name].sort_index()


#filter_season will return all games played within a Season format = xx/xx
def filter_season(df,season):
    return df.loc['20'+season.split("/")[0] + '-07-15':'20' + season.split("/")[1] + '-07-12'].sort_index()
    

#lastx_games returns the last x games for a certain team.
def lastx_games(df,team,x):
    return filter_team(df,team)[-x:].sort_index()


#get_teams will return an array of teams (usually for a season)
def get_teams(df):
    return df.HomeTeam.unique()


#filter_history will return all matches between two teams
def filter_history(df,t1,t2):
    _df1 = df[(df.HomeTeam==t1) & (df.AwayTeam ==t2)]
    _df2 = df[(df.HomeTeam==t2) & (df.AwayTeam ==t1)]
    _l = [i for i in [_df1,_df2] if len(i) > 0]
    if len(_l) > 0:
        return pd.concat([_df1,_df2],sort=False).sort_index()
    else: 
        return None