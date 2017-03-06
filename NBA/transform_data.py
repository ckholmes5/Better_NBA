import pandas as pd
import numpy as np

start_dates = [['2012-10-30','2013-4-17'], ['2013-10-29','2014-4-16'],['2014-10-28','2015-6-16'],['2015-10-27','2016-6-19'],['2016-10-25','2017-6-18']]

def determine_year(df, start_date, end_date):
    df['year'] = np.where((df['date_game'] > pd.to_datetime(start_date)) & (df['date_game'] < pd.to_datetime(end_date)), 2017, 2016)
    return df

def calculate_df_points_allowed(df):
    df['dk_points_allowed'] = df['opp_pts'] + df['opp_fg3']*.5
    #df['dk_points'] = df['PTS'] + df['FG3M']*.5 + df['REB']*1.25 + df['AST']*1.5 + df['STL']*2 + df['BLK']*2 + df['TOV']*-.5

    return df

def transform_gamelog():
    gamelog = pd.read_csv('./Data/bb_ref_gamelog.csv')
    gamelog['date_game'] = pd.to_datetime(gamelog['date_game'])

    for start_date, end_date in start_dates:
        gamelog = determine_year(gamelog, start_date, end_date)

        print gamelog.head()

    gamelog = calculate_df_points_allowed(gamelog)
    print gamelog.head()
    return gamelog

def transform_playerlog():
    playerlog = pd.read_csv('./Data/bb_ref.csv')
    playerlog['date_game'] = pd.to_datetime(gamelog['date_game'])

    for start_date, end_date in start_dates, end_dates:
        playerlog = determine_year(playerlog, start_date, end_date)

    return playerlog

# TODO: Merge player price data with player logs data
# TODO: Create algorithm that determines which team lets up the most points
# TODO: Filter data based on those teams letting up the most ponits
# TODO: Get the lineup chooser to choose the best lineup based on those characteristics
# TODO: Write the algorithm that compares how each algorithm would have done using historical data

print transform_gamelog()
