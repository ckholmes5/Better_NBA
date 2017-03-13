import pandas as pd
import requests
from transform_data import filter_players_from_top_teams
import time

filtered_data = filter_players_from_top_teams(15)
filtered_data = filtered_data[filtered_data.year.isin([2017])]

def get_average_points(data, filter_num, player):
    filtered_data = filter_players_from_top_teams(filter_num)
    name = str(player['fnu'] + ' ' + player['lnu'])
    pts = filtered_data[filtered_data.player.str.match(name)].pts.mean()
    rebs = filtered_data[filtered_data.player.str.match(name)].trb.mean()
    asts = filtered_data[filtered_data.player.str.match(name)].ast.mean()
    stl = filtered_data[filtered_data.player.str.match(name)].stl.mean()
    blk = filtered_data[filtered_data.player.str.match(name)].blk.mean()
    tov = filtered_data[filtered_data.player.str.match(name)].tov.mean()
    fg3m = filtered_data[filtered_data.player.str.match(name)].fg3.mean()

    dk_points = pts + rebs * 1.25 + asts*1.5 + stl*2 + blk*2 + tov*-.5 + fg3m *.5
    return dk_points

def get_todays_players_stats(url_number):
    todays_players = requests.get('https://www.draftkings.com/lineup/getavailableplayers?draftGroupId=' + str(url_number))
    todays_players = todays_players.json()['playerList']

    return todays_players

def statArraySetup(url_number):
    # Get filtered dataset by calling that function
    # Initially include all teams. Check if player is in the filtered dataset, if he's not, then use rename dict to find him cause he should be.
    # Once you find him, average his points this year, and that is the prediction!
    todays_players = get_todays_players_stats(url_number)

    playerArray = "Date;GID;Pos;Name;Starter;DK Pts;DK Salary;Team;H/A;Oppt;Team Score;Oppt Score;Minutes;Stat line\n"

    for player in todays_players:
        statArray = ""

        name = player['fnu'] + ' ' + player['lnu']
        name = name.replace(' ', '_').lower()

        statArray = statArray + time.strftime("%Y%m%d") + ';'
        statArray = statArray + 'None' + ';' #'gameID'
        statArray = statArray + str(player['pn']) + ';'
        statArray = statArray + str(name) + ';'
        statArray = statArray + 'None' + ';' #'Starter?

        # TODO: This is the only thing that has to change!
        print name, get_average_points(player)
        statArray = statArray + str(get_average_points(player)) + ';'
        statArray = statArray + str(10) + ';'

        statArray = statArray + str(player['s']) + ';'
        statArray = statArray + 'None' + ';' #'Team'
        statArray = statArray + 'None' + ';' #'Home?'
        statArray = statArray + 'None' + ';' #'Opponent'
        statArray = statArray + 'None' + ';' #'teamScore'
        statArray = statArray + 'None' + ';' #'opponentScore'
        statArray = statArray + 'None' + ';' #'minutes'
        statArray = statArray + 'None' + ';' #'statLine'
        playerArray = playerArray + statArray + "|||"

    return [playerArray]

statArraySetup(12418)
