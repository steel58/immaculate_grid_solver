from bs4 import BeautifulSoup
import requests
import json

hart_index = "hart_winner_name"
vezina_index = "vezina_winner_name"
calder_index = "calder_winner_name"
norris_index = "norris_winner_name"
smythe_index = "smythe_winner_name"

goal_leader_id = 'leaders_goals'
point_leader_id = 'leaders_points'
wins_leader_id = 'leaders_wins_goalie'
assists_leader_id = 'leaders_assists'
hall_of_fame = []
hart = []
vezina = []
calder = []
norris = []
smythe = []

hockey_teams = {
        'anaheimducks': 'ANA',
        'arizonacoyotes': 'PHX',
        'bostonbruins': 'BOS',
        'buffalosabres': 'BUF',
        'calgaryflames': 'CGY',
        'carolinahurricanes': 'CAR',
        'chicagoblackhawks': 'CHI',
        'coloradoavalanche': 'COL',
        'columbusbluejackets': 'CBJ',
        'dallasstars': 'DAL',
        'detroitredwings': 'DET',
        'edmontonoilers': 'EDM',
        'floridapanthers': 'FLA',
        'losangeleskings': 'LAK',
        'minnesotawild': 'MIN',
        'montrealcanadiens': 'MTL',
        'nashvillepredators': 'NSH',
        'newjerseydevils': 'NJD',
        'newyorkislanders': 'NYI',
        'newyorkrangers': 'NYR',
        'ottawasenators': 'OTT',
        'philadelphiaflyers': 'PHI',
        'pittsburghpenguins': 'PIT',
        'sanjosesharks': 'SJS',
        'seattlekraken': 'SEA',
        'st.louisblues': 'STL',
        'tampabaylightning': 'TBL',
        'torontomapleleafs': 'TOR',
        'vancouvercanucks': 'VAN',
        'vegasgoldenknights': 'VEG',
        'washingtoncapitals': 'WSH',
        'winnipegjets': 'WPG'
        }

categories = dict()

team_list = [hockey_teams[i] for i in list(hockey_teams)]


def get_teams():
    team_list = [hockey_teams[i] for i in list(hockey_teams)]

    for team in team_list:
        link = f'https://www.hockey-reference.com/teams/{team}/skaters.html'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')

        table_rows = soup.find_all('td', attrs={'data-stat': 'player'})
        year_start = soup.find_all('td', attrs={'data-stat': 'year_min'})
        year_end = soup.find_all('td', attrs={'data-stat': 'year_max'})
        player_data = zip(table_rows, year_start, year_end)

        categories[team] = [(p.string, s.string, e.string) for (p, s, e) in player_data]


def get_goals_leaders():
    goals_link = 'https://stathead.com/tiny/m2k6x?utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'

    new_page = requests.get(goals_link).text
    page = BeautifulSoup(new_page, 'html.parser')
    scorers = page.find_all('tr', attrs={'class': False})

    player_list = []
    for player in scorers:
        stats = list(player.children)
        teams = stats[-1].string
        team_list = teams.split(',')
        player_name = stats[1].string
        data = {player_name: team_list}
        player_list.append(data)

    categories['500+ Goalscareer'] = player_list


def get_wins_leaders():
    wins_link = 'https://stathead.com/tiny/ttSbw?utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'

    new_page = requests.get(wins_link).text
    page = BeautifulSoup(new_page, 'html.parser')
    goalies = page.find_all('tr', attrs={'class': False})

    player_list = []
    for player in goalies:
        stats = list(player.children)
        teams = stats[-1].string
        team_list = teams.split(',')
        player_name = stats[1].string
        data = {player_name: team_list}
        player_list.append(data)

    categories['300+ Winscareer'] = player_list

    season_link = 'https://www.hockey-reference.com/leaders/wins_goalie_season.html'

    new_page = requests.get(season_link).text
    page = BeautifulSoup(new_page, 'html.parser')
    table = page.find('tbody')
    goalies = table.find_all('tr', attrs={'class': False})

    player_list = []
    for player in goalies:
        stats = list(player.children)
        years = stats[-2].string
        player_name = stats[1].find('a').string
        yr_splt = years.split('-')
        start = yr_splt[0]
        end = yr_splt[0][0:2] + yr_splt[1]

        data = (player_name, start, end)
        print(data)
        player_list.append(data)


get_wins_leaders()
