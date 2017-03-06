import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_all_gamelog_urls():
    all_urls = []
    offset_range = 135
    for page in range(0,offset_range):
        gamelog_url = 'http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2012&year_max=2017&is_range=N&game_num_type=team&order_by=pts&offset=' + str(page*100)
        all_urls.append(gamelog_url)
    return all_urls

def get_single_stat(soup, stat, double_nested = False):
    stat_list = []

    if double_nested:
        for thing in soup.find_all('td', {'data-stat' : stat}):
             stat_list.append(thing.contents[0].contents[0])

    else:
        for thing in soup.find_all('td', {'data-stat' : stat}):
            if stat == 'game_location' and thing.contents == []:
                stat_list.append('Home')
            elif thing.contents == []:
                stat_list.append('')
            else:
                stat_list.append(thing.contents[0])
    return pd.Series(stat_list)

def get_stats_from_single_page(soup):
    categories = ['game_location', 'game_result', 'mp', 'fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'pts','opp_fg', 'opp_fga', 'opp_fg_pct', 'opp_fg2', 'opp_fg2a', 'opp_fg2_pct', 'opp_fg3', 'opp_fg3a', 'opp_fg3_pct', 'opp_ft', 'opp_fta', 'opp_ft_pct', 'opp_pts']
    double_nested_categories = ['date_game', 'team_id', 'opp_id']

    stats_df = pd.DataFrame()

    for stat in categories:
        stats_df[stat] = get_single_stat(soup, stat, False)

    for stat in double_nested_categories:
        stats_df[stat] = get_single_stat(soup, stat, True)

    return stats_df


def get_player_data():
    urls = get_all_gamelog_urls()

    r = requests.get(urls[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    bb_ref_stats = get_stats_from_single_page(soup)
    for url in urls[1:]:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        bb_ref_stats = bb_ref_stats.append(get_stats_from_single_page(soup))
        print len(bb_ref_stats)
        if len(bb_ref_stats) % 10000 == 0:
            bb_ref_stats.to_csv('./Data/bb_ref_gamelog.csv')

    return bb_ref_stats

get_player_data()
