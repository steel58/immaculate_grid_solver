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
            categories_top.append(hockey_teams[img['alt'].lower().replace(' ', '').replace('\t', '')])
            # add to list and make dictionary compliant

    rows = html.find_all('div', class_='flex items-center justify-center w-20 sm:w-36 md:w-48 h-24 sm:h-36 md:h-48')

    categories_side = []

    for div in rows:
        img = div.find('img', alt=True)
        if img is None:
            categories_side.append(div.find('div', class_ = 'leading-tight').text)
        else:
            categories_side.append(hockey_teams[img['alt'].lower().replace(' ', '').replace('\t', '')]) 
            # same as prev. comment

    return (categories_top, categories_side)


def played_for_two_teams(team_1: str, team_2: str, used_names: list[str]) -> str:
    new_page = requests.get(f'https://www.hockey-reference.com/friv/players-who-played-for-multiple-teams-franchises.fcgi?level=franch&t1={team_1}&t2={team_2}').text
    new_doc = BeautifulSoup(new_page, 'html.parser')
    players = new_doc.find_all('th', scope='row', class_='left')
    for player in players:
        if player.string in used_names:
            continue
        return player.string


def season_lead(cat: str, used_names: list[str], div_id: str) -> str:
    team_link = f'https://www.hockey-reference.com/teams/{cat}/leaders_season.html'

    link = team_link
    new_page = requests.get(link).text
    page = BeautifulSoup(new_page, 'html.parser')
    leader = page.find('div', id=div_id)
    candidates = leader.find_all('tr')
    for candidate in candidates:
        player_block = list(candidate.descendants)[4]
        player = list(player_block.children)[0].string
        if player not in used_names:
            return player


def career_leaders(team: str, career: str, used_names: list[str]) -> str:
    goals_link = 'https://stathead.com/tiny/m2k6x?utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'
    wins_link = 'https://stathead.com/tiny/ttSbw?utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'

    if career == '500+ Goalscareer':
        link = goals_link
    elif career == '300+ Winscareer':
        link = wins_link
    else:
        return "This shit's broken"

    new_page = requests.get(link).text
    page = BeautifulSoup(new_page, 'html.parser')
    scorers = page.find_all('tr', attrs={'class': False,})
    scorers.reverse()


    for player in scorers:
        stats = list(player.children)
        if team in stats[-1].string and stats[1].string not in used_names:
            return stats[1].string

def season_awards(team, award):
    link = f'https://www.hockey-reference.com/teams/{team}/skaters.html'
    new_page = requests.get(link).text
    page = BeautifulSoup(new_page, 'html.parser')
    table_rows = page.find_all('td', attrs={'data-stat': 'player'})
    year_start = page.find_all('td', attrs={'data-stat': 'year_min'})
    year_end = page.find_all('td', attrs={'data-stat': 'year_max'})
    player_data = zip(table_rows, year_start, year_end)

    player_list = [(p.string, s.string, e.string) for (p, s, e) in player_data]


    for (name, start, end) in player_list:
        if not name:
            continue
        last_name = name.split(' ')[-1]
        first_initial = name[0]
        short_name = f'{first_initial}. {last_name}'
        #print(short_name)
        for (trophy_name, trophy_start, trophy_end) in award:
            valid_time = int(start) <= int(trophy_start) and int(end) >= int(trophy_end)
            if trophy_name == short_name and valid_time:
                return name

def get_achievement(trophy_id):
    season_awards = 'https://www.hockey-reference.com/leagues/'
    trophy = requests.get(season_awards).text
    webite = BeautifulSoup(trophy, 'html.parser')
    rows = webite.find_all("td", attrs = {'data-stat': trophy_id})
    years = webite.find_all('th', attrs = {'data-stat': 'season'})

    player_data = zip(rows[1:], years[1:])

    player_names = [(p.string, y.string[0:4], y.string[0:2]+y.string[-2:]) for (p, y) in player_data if p.string]
    return player_names

def print_answers(top: list[str], side: list[str], answers: list[list[str]]):
    print(f'        | {top[0]} | {top[1]} | {top[2]}')
    for i in range(3):
        print(f'{side[i]} | {answers[i][0]} | {answers[i][1]} | {answers[i][2]}')

def main():

    (top, side) = get_categories(soup)
    all_categories = top + side
    print(top, side)
    used_names = []
    next_name = ''
    answers = [['' for i in range(3)] for i in range(3)]





    if "Calder Trophy" in all_categories:
        calder = get_achievement(calder_index)
    if "Vezina Trophy" in all_categories:
        vezina = get_achievement(vezina_index)
    if "Hart Trophy" in all_categories:
        hart = get_achievement(hart_index)
    if "Norris Trophy" in all_categories:
        norris = get_achievement(norris_index)
    if "ConnSmythe Trophy" in all_categories:
        smythe = get_achievement(smythe_index)


    #Max of strings returns the shorter one (usually the team tricode) while the min does the inverse
    for i, row in enumerate(side):
        for j, column in enumerate(top):
            #if answers[i][j]:
            #    continue

            if len(row) == 3 or len(column) == 3:
                if len(row) == 3:
                    team = row
                elif len(column) == 3:
                    team = column

                if row == '40+ Goalsseason' or column == '40+ Goalsseason':
                    next_name = season_lead(team, used_names, goal_leader_id)
                elif row =='100+ Pointsseason' or column == '100+ Pointsseason':
                    next_name = season_lead(team, used_names, point_leader_id)
                elif row == '50+ Assistsseason' or column == '50+ Assistsseason':
                    next_name = season_lead(team, used_names, assists_leader_id)
                elif row == '30+ Winseason' or column == '30+ Winseason':
                    next_name = season_lead(team, used_names, wins_leader_id)
                elif 'career' in row or 'career' in column:
                    next_name = career_leaders(team, min(row, column), used_names)
                elif 'Trophy' in row or 'Trophy' in column:
                    if "Calder" in row or "Calder" in column:
                        award_list = calder
                    elif "Vezina" in row or "Vezina" in column:
                        award_list = vezina
                    elif "Hart" in row or "Hart" in column:
                        award_list = hart
                    elif "Smythe" in row or "Smythe" in column:
                        award_list = smythe
                    elif "Norris" in row or "Norris" in column:
                        award_list = norris

                    next_name = season_awards(team, award_list)
                else:
                    next_name = played_for_two_teams(row, column, used_names)
            else:
                next_name = "Fuck"

            answers[i][j] = next_name

            used_names.append(next_name)
    print()
    print_answers(top, side, answers)

main()
