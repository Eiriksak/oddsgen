import matplotlib.pyplot as plt
import pandas as pd 



def plot_goal_stats(df_season,teams,figsize=(17,8)):
    x = {}
    st = {} #Shots target
    s = {} #Shots
    ftg = {} #Full time goals
    season = str(df_season[:1].index.year[0]) + "/" + str(int(df_season[:1].index.year[0])+1)
    
    for team in teams:
        x[team] = []
        st[team] = []
        s[team] = []
        ftg[team]  = []
        
    for date,match in df_season.iterrows():
        #Add match date on x axis
        x[match.HomeTeam].append(date)
        x[match.AwayTeam].append(date)
        
        #Add shot and goal stats
        st[match.HomeTeam].append(match.HST)
        st[match.AwayTeam].append(match.AST)
        
        s[match.HomeTeam].append(match.HS)
        s[match.AwayTeam].append(match.AS)
        
        ftg[match.HomeTeam].append(match.FTHG)
        ftg[match.AwayTeam].append(match.FTAG)
        
        
    for team in teams:
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(x[team], st[team],label="Target shots")
        ax.plot(x[team], s[team],label="Shots")
        ax.plot(x[team], ftg[team],label="Full time goals")
        ax.set(title=str(team) + " :" + str(season), xlabel='date', ylabel='Amount')
        plt.legend()
        plt.show()