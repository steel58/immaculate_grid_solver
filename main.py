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
            # This should not trigger for teams
            categories_top.append(div.find('div', class_='leading-tight').text)
        else:
            team_name = img['alt'].lower().replace(' ', '').replace('\t', '')
            split_name = team_name.split('(')
            categories_top.append(hockey_teams[split_name[0]])
            # add to list and make dictionary compliant

    rows = html.find_all('div', class_='flex items-center justify-center w-20 sm:w-36 md:w-48 h-24 sm:h-36 md:h-48')

    categories_side = []

    for div in rows:
        img = div.find('img', alt=True)
        if img is None:
            categories_side.append(div.find('div', class_='leading-tight').text)
        else:
            team_name = img['alt'].lower().replace(' ', '').replace('\t', '')
            split_name = team_name.split('(')
            categories_side.append(hockey_teams[split_name[0]])
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


def one_team_prompts(team, other, player_dict, used_names):
    name_only = ['Hall of Fame',
                 '300+ Winscareer',
                 '1000+ Pointscareer',
                 '500+ Goalscareer',
                 'Born Outside North America',
                 'Born Outside US 50 States and DC']

    if other in name_only:
        other_list = player_dict[other]
        team_list = player_dict[team]
        for p in team_list:
            if (p[0] in other_list and p[0] not in used_names):
                return p[0]

    elif "Trophy" in other or 'First Round Draft Pick' == other:
        player_list = player_dict[other]
        for p in player_list:
            if p[1] == team:
                return p[0]

    elif "season" in other:
        team_list = player_dict[team]
        full_other = player_dict[other]
        names_other = [p[0] for p in full_other]

        for p in team_list:
            name = p[0]
            if name in names_other:
                index = names_other.index(name)
                team_start = int(p[1])
                team_end = int(p[2])
                season_start = int(full_other[index][1])
                season_end = season_start + 1
                if season_start > team_start and season_end < team_end:
                    return name


def no_team_prompts(prompt1, prompt2, player_dict, used_names):
    list_1 = player_dict[prompt1]
    list_2 = player_dict[prompt2]

    if type(list_1[0]) is list:
        player_list_1 = [p[0] for p in list_1]
    else:
        player_list_1 = list_1

    if type(list_2[0] is list):
        player_list_2 = [p[0] for p in list_2]
    else:
        player_list_2 = list_2

    for name in player_list_1:
        if name in player_list_2 and name in used_names:
            return name


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
            next_name = 'Noppers'
            if len(row) == len(column) and len(row) == 3:
                # Just use names
                list_r = player_dict[row]

                list_c = [i[0] for i in player_dict[column]]
                for p in list_r:
                    if (p[0] in list_c and p[0] not in used_names):
                        next_name = p[0]
                        break

            elif len(row) == 3 or len(column) == 3:
                if len(row) == 3:
                    team = row
                    other = column
                else:
                    team = column
                    other = row
                next_name = one_team_prompts(team, other, player_dict, used_names)

            else:
                next_name = no_team_prompts(row, column, player_dict, used_names)

            answers[i][j] = next_name
            used_names.append(next_name)

    print()
    print_answers(top, side, answers)


main()
