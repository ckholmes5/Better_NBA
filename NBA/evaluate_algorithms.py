import pandas as pd

# Cycle through every day in the data we have:
# Run the algorithm on that day to pick the best lineup.
# Determine the number of points that lineup would have received.
# Pick the best possible lineup from that day using the  actual df points.
# Log the predicted/actual ratio and save it for later.

player_log = pd.read_csv('./Data/bb_ref_playerlog.csv')

def cycle_through_every_day():
    i = 0
    for date in player_log.date_game:
        i += 1
        daily_all_players = player_log[player_log.date_game.str.match(date)]

        

        print daily_all_players
        if i % 5 == 0:
            break


cycle_through_every_day()
