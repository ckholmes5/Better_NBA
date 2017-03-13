import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_all_gamelog_urls():
    all_urls = []
    offset_range = 1448
    for page in range(0,offset_range):
        gamelog_url = 'http://www.basketball-reference.com/play-index/pgl_finder.cgi?request=1&player_id=&match=game&year_min=2012&year_max=2017&age_min=0&age_max=99&team_id=&opp_id=&is_playoffs=N&round_id=&game_num_type=&game_num_min=&game_num_max=&game_month=&game_day=&game_location=&game_result=&is_starter=&is_active=&is_hof=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&is_dbl_dbl=&is_trp_dbl=&order_by=pts&order_by_asc=&offset=' + str(page*100)
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
    categories = ['age', 'pos', 'game_location', 'game_result', 'gs', 'mp', 'fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'game_score']
    double_nested_categories = ['player', 'date_game', 'team_id', 'opp_id']

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

    bb_ref_stats.to_csv('../Data/bb_ref.csv')
    return bb_ref_stats
