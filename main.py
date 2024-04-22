from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.immaculategrid.com/hockey'

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

page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')


def get_categories(html) -> tuple[list[str], list[str]]:
    columns = html.find_all('div', class_='flex items-center justify-center w-24 sm:w-36 md:w-48 h-16 sm:h-24 md:h-36')
    # This tag is the top row of items

    categories_top = []

    for div in columns:
        img = div.find('img', alt=True)
        if img is None:
            # print(div.find('div', class_ = 'leading-tight'))
            categories_top.append(div.find('div', class_='leading-tight').text)
        else:
            team_name = img['alt'].lower().replace(' ', '').replace('\t', '')
            categories_top.append(hockey_teams[team_name])
            # add to list and make dictionary compliant

    rows = html.find_all('div', class_='flex items-center justify-center w-20 sm:w-36 md:w-48 h-24 sm:h-36 md:h-48')

    categories_side = []

    for div in rows:
        img = div.find('img', alt=True)
        if img is None:
            categories_side.append(div.find('div', class_='leading-tight').text)
        else:
            team_name = img['alt'].lower().replace(' ', '').replace('\t', '')
            categories_side.append(hockey_teams[team_name])
            # same as prev. comment

    return (categories_top, categories_side)


def print_answers(top: list[str], side: list[str], answers: list[list[str]]):
    print(f'        | {top[0]} | {top[1]} | {top[2]}')
    for i in range(3):
        print(f'{side[i]} | {answers[i][0]} | {answers[i][1]} | {answers[i][2]}')


def main():

    (top, side) = get_categories(soup)
    print(top, side)
    used_names = []
    next_name = ''
    answers = [['' for i in range(3)] for i in range(3)]




    #Max of strings returns the shorter one (usually the team tricode) while the min does the inverse
    for i, row in enumerate(side):
        for j, column in enumerate(top):
            answers[i][j] = next_name

            used_names.append(next_name)
    print()
    print_answers(top, side, answers)

main()

