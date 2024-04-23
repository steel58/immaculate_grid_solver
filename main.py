from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.immaculategrid.com/hockey'

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


def print_answers(top: list[str], side: list[str], ans: list[list[str]]):
    print(f'        | {top[0]} | {top[1]} | {top[2]}')
    for i in range(3):
        print(f'{side[i]} | {ans[i][0]} | {ans[i][1]} | {ans[i][2]}')


def get_players():
    data = None
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)

    return data


# Team: (name, start, end)
# Trophy: (name, team)
# Career Achievement: (name)
# Season Acheivement: (name, start, end)
# Birthplace: (name)
# First_draft: (name)
# Hall of Fame: (name)
def main():
    (top, side) = get_categories(soup)
    print(top, side)

    player_dict = get_players()

    used_names = []
    answers = [['' for i in range(3)] for i in range(3)]

    for i, row in enumerate(side):
        for j, column in enumerate(top):
            next_name = 'None'
            if len(row) == len(column) and len(row) == 3:
                # Just use names
                list_r = player_dict[row]

                list_c = [i[0] for i in player_dict[column]]
                for player in list_r:
                    if (player[0] in list_c and not player[0] in used_names):
                        next_name = player[0]
                        break

            if len(row) == 3 or len(column) == 3:
                if len(row) == 3:
                    team = row
                    other = column
                else:
                    team = column
                    other = row
                if other == "First Round Draft Pick":
                    player_list = player_dict['First Round ' + team]
                    for player in player_list:
                        if not player[0] in used_names:
                            next_name = player[0]
                            break

            answers[i][j] = next_name
            used_names.append(next_name)

    print()
    print_answers(top, side, answers)


main()
