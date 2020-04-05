import pandas as pd 
import os 
import datetime 

#Load and prepare the data
class DataLoader(object):

    def __init__(self,**kwargs):
        self.leagues = {}

        _df_list = []
        if len(kwargs) > 0:
            for league, v in kwargs.items():
                if v: #specific seasons
                    _league_df = self._import_dir(league,*v)
                else:
                    _league_df = self._import_dir(league)
                
                _df_list.append(_league_df.copy())
                self.leagues[league] = _league_df
        else:
            leagues = ["bl","nl","pl","sp"]
            for league in leagues:
                _league_df = self._import_dir(league)
                _df_list.append(_league_df.copy())
                self.leagues[league] = _league_df


        self.data = self._concat(_df_list)

    
    def get_league(self,league):
        return self.leagues[league]


    def _concat(self,_df_list):
        _lm = {
            "bl":"D1",
            "nl":"N1",
            "pl":"E0",
            "sp":"SP1"
             }
        return pd.concat(_df_list, sort=False).sort_index()


    def _import_dir(self,name,*args):
        _df_list = []
        for entry in os.scandir(os.getcwd() + "/data/odds/"+str(name)):
            filename = entry.path.split("/")[-1]
            if len(args) > 0:
                #Check filename is in among the required seasons
                valid = False
                for season in args:
                    if season in filename:
                        valid = True
                        break
                if not valid:
                    continue
                        

            if filename.endswith(".csv"):
                try:
                    _df = pd.read_csv(entry.path)
                    _df = self._clean(_df)
                    _df_list.append(_df)
                except:
                    print("Failed to import ", filename)
                    continue
            else:
                continue

        return pd.concat(_df_list,sort=False).sort_index()



    def _clean(self,data):

        data.dropna(axis=0, how="all", inplace=True)
        data.dropna(axis=1, how="all", inplace=True)

        if len(data[:1].Date.values[0].split("/")[2]) > 2: #2018
            data.index = pd.to_datetime(data.Date,format="%d/%m/%Y")
        else: #18
            data.index = pd.to_datetime(data.Date,format="%d/%m/%y")
        return data




