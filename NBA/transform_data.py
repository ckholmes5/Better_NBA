import pandas as pd
import numpy as np


def change_CHO_to_NOP():
    gamelog = pd.read_csv('./Data/bb_ref_gamelog.csv')
    playerlog = pd.read_csv('./Data/bb_ref.csv')

    # Changing Hornets to Pelicans
    gamelog.team_id[gamelog.team_id=='NOH'] = 'NOP'
    gamelog.opp_id[gamelog.team_id=='NOH'] = 'NOP'
    playerlog.team_id[playerlog.team_id=='NOH'] = 'NOP'
    playerlog.opp_id[playerlog.team_id=='NOH'] = 'NOP'

    # Changing Nets to Brooklyn
    gamelog.team_id[gamelog.team_id=='NJN'] = 'BRK'
    gamelog.opp_id[gamelog.team_id=='NJN'] = 'BRK'
    playerlog.team_id[playerlog.team_id=='NJN'] = 'BRK'
    playerlog.opp_id[playerlog.team_id=='NJN'] = 'BRK'

    # Changing Charlotte Bobcats to Charlotte hornets, which for some reason changed the acronym
    gamelog.team_id[gamelog.team_id=='CHO'] = 'CHA'
    gamelog.opp_id[gamelog.team_id=='CHO'] = 'CHA'
    playerlog.team_id[playerlog.team_id=='CHO'] = 'CHA'
    playerlog.opp_id[playerlog.team_id=='CHO'] = 'CHA'

    playerlog.to_csv('./Data/bb_ref_update.csv')
    gamelog.to_csv('./Data/bb_ref_gamelog_update.csv')


def determine_year(row):
    if (row['date_game'] >= pd.to_datetime('2011-10-25')) & (row['date_game'] <= pd.to_datetime('2012-6-26')):
        return 2012
    if (row['date_game'] >= pd.to_datetime('2012-10-30')) & (row['date_game'] <= pd.to_datetime('2013-4-17')):
        return 2013
    if (row['date_game'] >= pd.to_datetime('2013-10-29')) & (row['date_game'] <= pd.to_datetime('2014-4-16')):
        return 2014
    if (row['date_game'] >= pd.to_datetime('2014-10-28')) & (row['date_game'] <= pd.to_datetime('2015-6-16')):
        return 2015
    if (row['date_game'] >= pd.to_datetime('2015-10-27')) & (row['date_game'] <= pd.to_datetime('2016-6-19')):
        return 2016
    if (row['date_game'] >= pd.to_datetime('2016-10-25')) & (row['date_game'] <= pd.to_datetime('2017-6-18')):
        return 2017

#
def calculate_df_points_allowed(df):
    df['dk_points_allowed'] = df['opp_pts'] + df['opp_fg3']*.5
    #df['dk_points'] = df['PTS'] + df['FG3M']*.5 + df['REB']*1.25 + df['AST']*1.5 + df['STL']*2 + df['BLK']*2 + df['TOV']*-.5
    return df

#
def transform_gamelog():
    gamelog = pd.read_csv('./Data/bb_ref_gamelog_update.csv')
    gamelog['date_game'] = pd.to_datetime(gamelog['date_game'])

    gamelog['year'] = gamelog.apply(lambda row: determine_year(row),axis=1)

    gamelog = calculate_df_points_allowed(gamelog)
    gamelog.to_csv('./Data/bb_ref_gamelog_points.csv')
    return gamelog

#
def transform_playerlog():
    playerlog = pd.read_csv('./Data/bb_ref_update.csv')
    playerlog['date_game'] = pd.to_datetime(playerlog['date_game'])

    playerlog['year'] = playerlog.apply(lambda row: determine_year(row),axis=1)
    import pdb; pdb.set_trace()
    playerlog.to_csv('./Data/bb_ref_playerlog.csv')

    return playerlog

# Merges DK Salary data with player statistics.
def merge_dksalary_data():
    salary_log = pd.read_csv('./Data/bb_ref_dksalaries.csv', names = ['index', 'date_game', 'player', 'salary', 'dk_points'])
    player_log = pd.read_csv('./Data/bb_ref_playerlog.csv')
    player_log['date_game'] = pd.to_datetime(player_log['date_game'])
    player_log['date_game'] = player_log['date_game'].dt.strftime('%-m/%-d/%y')

    merged = player_log.merge(salary_log, on = ['player', 'date_game'])
    merged.to_csv('./Data/bb_ref_playerlog.csv')

def filter_top_teams(num_teams = 10):
    gamelog = pd.read_csv('./Data/bb_ref_gamelog_points.csv')
    gamelog = gamelog.groupby(by='team_id').sum().dk_points_allowed.nlargest(num_teams)
    return gamelog

def filter_players_from_top_teams(num_teams = 10):
    player_log = pd.read_csv('./Data/bb_ref_playerlog.csv')
    teams = filter_top_teams(num_teams).index.values

    # Filtering out all players not on one of the top teams
    new_log = player_log[player_log['team_id'].isin(teams)]

    return new_log

def transform():
    change_CHO_to_NOP()
    transform_playerlog()
    transform_gamelog()
    merge_dksalary_data()

#transform()

# TODO: Write a function that takes in draft`kings API and filters the playerlog data based on who is active and available that day. Merge playerlog data with draftkings data, should have position and current salary.
# TODO: Write the algorithm that compares how each algorithm would have done using historical data
# TODO: Use the player data to figure out how many draftkings points were allowed each game (more columns than the gamelog data)
# TODO: rerun algorithm using those stats instead of the just the pts + three pointers
