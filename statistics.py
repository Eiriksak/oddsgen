import pandas as pd
from funcs import lastx_games

def add_recent_match_statistics(df,lim,stat_type):
    """
    Return match statistics from last lim games.
    
    params:
    df: a season of games
    lim: number of recent games to look at
    stat_type: type of match statistics. e.g. S=shots, ST = target shots, F=Team Fouls Committed
                
    """
    _h = {"H"+str(stat_type)+"_"+str(i+1):[] for i in range(lim)} # e.g. {'HS_1': []} = home team shots 1 match ago
    _a = {"A"+str(stat_type) + "_"+str(i+1):[] for i in range(lim)}
    
    date_filter = 0
    for _, row in df.iterrows():
        #last lim games for home and away team
        home_team = lastx_games(df[:date_filter],row["HomeTeam"],lim) 
        away_team = lastx_games(df[:date_filter],row["AwayTeam"],lim)
        
        #Insert goals over the past lim games
        if len(home_team) == lim: #lim games have been played
            hst = []
            for _,r in home_team.iterrows():
                if r.HomeTeam == row["HomeTeam"]:
                    hst.append(r["H"+str(stat_type)])
                else:
                    hst.append(r["A"+str(stat_type)]) 
        else:
            hst = [None for i in range(lim)]
            
            
        if len(away_team) == lim: 
            ast = []
            for _,r in away_team.iterrows():
                if r.HomeTeam == row["AwayTeam"]:
                    ast.append(r["H"+str(stat_type)])
                else:
                    ast.append(r["A"+str(stat_type)]) 
        else:
            ast = [None for i in range(lim)]
            
        #Want newest game first
        hst.reverse() 
        ast.reverse()
            
        for i in range(lim):
            _h["H"+str(stat_type)+"_"+str(i+1)].append(hst[i])
            _a["A"+str(stat_type) + "_"+str(i+1)].append(ast[i])
            
        date_filter = date_filter + 1
        
    for k,v in _h.items():
        df[k] = v
    for k,v in _a.items():
        df[k] = v
        
    return df



def add_goal_statistics(df,lim,home_filter,away_filter):
    """
    Return goal statistics from last lim games.
    
    params:
    df: a season of games
    lim: number of recent games to look at
    home_filter: goal stat for home team. typically FTHG(Full time home goals)
    away_filter: goal stat for away team. typically FTAG(Full away home goals)
                
    """
    _h = {str(home_filter)+"_"+str(i+1):[] for i in range(lim)} # e.g. {'FTHG_1': []} 
    _a = {str(away_filter) + "_"+str(i+1):[] for i in range(lim)}
    
    date_filter = 0
    for _, row in df.iterrows():
        #last lim games for home and away team
        home_team = lastx_games(df[:date_filter],row["HomeTeam"],lim) 
        away_team = lastx_games(df[:date_filter],row["AwayTeam"],lim)
        
        #Insert goals over the past lim games
        if len(home_team) == lim: #lim games have been played
            hst = []
            for _,r in home_team.iterrows():
                if r.HomeTeam == row["HomeTeam"]:
                    hst.append(r[str(home_filter)])
                else:
                    hst.append(r[str(away_filter)]) 
        else:
            hst = [None for i in range(lim)]
            
            
        if len(away_team) == lim: 
            ast = []
            for _,r in away_team.iterrows():
                if r.HomeTeam == row["AwayTeam"]:
                    ast.append(r[str(home_filter)])
                else:
                    ast.append(r[str(away_filter)]) 
        else:
            ast = [None for i in range(lim)]
            
        #Want newest game first
        hst.reverse() 
        ast.reverse()
            
        for i in range(lim):
            _h[str(home_filter)+"_"+str(i+1)].append(hst[i])
            _a[str(away_filter)+"_"+str(i+1)].append(ast[i])
            
        date_filter = date_filter + 1
        
    for k,v in _h.items():
        df[k] = v
    for k,v in _a.items():
        df[k] = v
        
    return df