"""
@author: Eirik Sakariassen

Visualization tools for football dataset
"""

import matplotlib.pyplot as plt
import pandas as pd 
from funcs import filter_team



def plot_team_stats(df, teams, figsize=(15,8), **kwargs):
    """
    Return a plot for each team containing custom statistics given a time period.
    
    params:
    df: dataframe containing games
    teams: list of teams in the dataframe to plot. 
    figsize: size of the plots. default size is (15,8)
    **kwargs: which statistics to include. 3 types supported:
                1. (key = df column, value = df column) 
                    -> key statistics is based on value column. e.g. HomeGoals only on HomeTeam
                2. (key = df column, value = None) 
                    -> key statistics for home and away if present in teams
                3. (key = description, value = lambda function) 
                    -> derive statistics for a match given value function
              
    """
    x = {t:{} for t in teams}
    stat_storage = {t:{} for t in teams}
    titles = {}
    
    #Initialize titles and team statistics storage
    for team in teams:
        #Define time range for each team. format mm.Y-mm.Y
        try:
            s = filter_team(df,team).head(1)
            e = filter_team(df,team).tail(1)
        except:
            print("Not a valid team: ",team)
            continue
        
        start = s.index.strftime('%Y')[0]
        end = e.index.strftime('%Y')[0]
        titles[team] = start + "-" + end
        for k, _ in kwargs.items():
            x[team][k] = []
            stat_storage[team][k] = [] #Store k statistics for team
        
        
    for date,match in df.iterrows():
        if (match.HomeTeam not in teams) and (match.AwayTeam not in teams):
            continue

        #Add statistics
        for k, v in kwargs.items():

            #v is a lambda function. k is the description
            if callable(v): 
                [x[match[i]][k].append(date) for i in ["HomeTeam","AwayTeam"] if match[i] in teams]
                #Series to dataframe before applying function
                stat = match.to_frame().apply(v,axis=0)[0]
                [stat_storage[match[i]][k].append(stat)  for i in ["HomeTeam","AwayTeam"] if match[i] in teams]

            #Not specified a column this key should look at
            elif not v: 
                [x[match[i]][k].append(date) for i in ["HomeTeam","AwayTeam"] if match[i] in teams]
                [stat_storage[match[i]][k].append(match[k]) for i in ["HomeTeam","AwayTeam"] if match[i] in teams]

            #Apply k statistics to based on v column
            else: 
                if match.HomeTeam in teams and v=="HomeTeam":
                    x[match.HomeTeam][k].append(date)
                    stat_storage[match[v]][k].append(match[k]) #Store k statistics for team
                    
                if match.AwayTeam in teams and v=="AwayTeam":
                    x[match.AwayTeam][k].append(date)
                    stat_storage[match[v]][k].append(match[k]) #Store k statistics for team

    #Plot all derived statistics
    for team in teams:
        _, ax = plt.subplots(figsize=figsize)
        for k, _ in kwargs.items():
            ax.plot(x[team][k],stat_storage[team][k],label=str(k))
        
        ax.set(title=str(team) + ":" + str(titles[team]), xlabel='date', ylabel='Amount')
        plt.legend()
        plt.show()