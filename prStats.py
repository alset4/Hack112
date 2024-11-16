import pandas as pd
from nba_api.stats.static import players

def getPlayerID(name):
    player_dict = players.get_players()
    playerx = ([player for player in player_dict if player['full_name'] == 
                                                                str(name)][0])
    playerx_id = playerx['id']
    return playerx_id

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscoretraditionalv3

def getGameLog(name, season): #dataframe of player's stats in a given season
    game_log = playergamelog.PlayerGameLog(player_id=getPlayerID(name), season = str(season))
    df_gamelog = game_log.get_data_frames()
    return df_gamelog[0]

def getMetricList(name, metric, season=2023): #individual stats for each player
    df = getGameLog(name, season)
    result = []
    for index, row in df.iterrows():
        val = df.loc[index, metric]
        result.append(val)
    return result

def getGameID(name, season=2023): #list of gameID that player has played in 
    result = []
    df = getGameLog(name, season)
    for index, row in df.iterrows():
        val = df.loc[index, 'Game_ID']
        result.append(val)
    return result

def getStatsList(player, stat):#team stats for each game player plays in
    result = []
    gameIDs = getGameID(player)
    for index in range(len(gameIDs)):
        id = gameIDs(index)
        boxscore = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=str(id))
        df = boxscore.get_data_frames()[2]
        L = df.values.tolist()
        team = getTeam(player, index)
        if team in L[0]:
            val = df.loc[0, stat]
        else:
            val = df.loc[1, stat]
        result.append(val)
    return result

def getTeam(player, index):
    teams = {'GSW': 'Warriors', 'CHI': 'Bulls', 'CLE': 'Cavaliers', 'ATL': 'Hawks', 'BOS': 'Celtics', 'BKN': 'Nets', 'CHA': "Hornets", 
     'DAL': 'Mavericks', 'DEN': 'Nuggets', 'DET': 'Pistons', 'HOU': 'Rockets', 'IND': 'Pacers', 'LAC': 'Clippers', 
     'LAL': 'Lakers', 'MEM': 'Grizzlies', 'MIA':'Heat', 'MIL': 'Bucks', 'MIN': 'Timberwolves',
      'NOP': 'Pelicans', 'NYK': 'Knicks', 'OKC':'Thunder', 'ORL': 'Magic', 'PHI': '76ers', 'PHX': 'Suns',
      'POR': 'Trail Blazers', 'SAC': 'Kings', 'SAS': 'Spurs', 'TOR':'Raptors', 'UTA':'JAZZ', 'WAS': 'Wizards'}
    matchups = getMetricList(str(player), 'MATCHUP')
    teamStr = matchups[index]
    team = teamStr[:3]
    return teams[team]
