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


def get_teams():
    team_list = [hockey_teams[i] for i in list(hockey_teams)]

    for team in team_list:
        link = f'https://www.hockey-reference.com/teams/{team}/skaters.html'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')

        players = soup.find_all('tr', attrs={'class': False})
        player_list = []
        for player in players:
            stats = player.findChildren()
            name = stats[1].string
            start = stats[3].string
            end = stats[4].string
            data = (name, start, end)
            print(data)
            player_list.append(data)


get_teams()
