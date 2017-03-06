import requests
import lxml.html
import pandas as pd

def get_all_days():

    days = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    months = ['10','11','12','1','2','3','4','5', '6']
    years = ['2014','2015','2016', '2017']
    player_prices = pd.DataFrame()
    for year in years:
        for month in months:
            for day in days:
                if get_single_day(day, month, year):

                    player_prices = player_prices.append(get_single_day(day, month, year))
                    print day, month, year, len(player_prices)
                else:
                    pass
    player_prices.to_csv('./Data/bb_ref_dksalaries.csv')


def get_single_day(day, mon, year):
    scrape_url = 'http://rotoguru1.com/cgi-bin/hyday.pl?mon=' + mon + '&day=' + day + '&year=' + year + '&game=dk&scsv=10'
    scraped_guru_page = requests.get(scrape_url).content
    t = lxml.html.fromstring(scraped_guru_page)
    raw_day_data = t.xpath('//pre/pre/text()')
    if raw_day_data:
        rawDayDataList = raw_day_data[0].split('\n')

        prices = []

        for i in rawDayDataList:
            prices.append(i.split(';'))

        del prices[0]
        del prices[-1]

        players = []

        for player in prices:

            if player[3] != '':

                name = player[3].split(', ')
                name = name[1] + ' ' + name[0]
                #name = name.replace(' ', '_').lower()

                #renameDict = {'j.j._barea': 'jose_barea', 'lou_williams': 'louis_williams', "d'angelo_russell": 'dangelo_russell', 'larry_nance_jr.': 'larry_nance', 'o.j._mayo': 'oj_mayo', "kyle_o'quinn": 'kyle_oquinn', "e'twaun_moore" : 'etwaun_moore', 'louis_amundson': 'lou_amundson', "tim_hardaway_jr.": 'timothy_hardaway', "johnny_o'bryant": 'johnny_obryant'}

                #if name in renameDict:
                #    name = renameDict[name]


                #date = player[0][0:4] + '-' + player[0][4:6] + '-' + player[0][6:8]
                date = mon + '/' + day + '/' + year[2:]

                newPlayer = [date, name, player[6],player[12]]
                players.append(newPlayer)

        return players
    else:
        return None


# TODO: 3-5: Turn the player prices into a pandas dataframe
get_all_days()
