from bs4 import BeautifulSoup
import requests
import json
import time

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


def get_teams():
    team_list = [hockey_teams[i] for i in list(hockey_teams)]

    for team in team_list:
        link = f'https://www.hockey-reference.com/teams/{team}/skaters.html'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('tbody')
        players = table.find_all('tr', attrs={'class': False})
        player_list = []

        for player in players:
            stats = player.findChildren(recursive=False)
            name = stats[1].find('a').string
            start = stats[2].string
            end = stats[3].string
            data = (name, start, end)
            player_list.append(data)

        time.sleep(3.1)

        link = f'https://www.hockey-reference.com/teams/{team}/goalies.html'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('tbody')
        players = table.find_all('tr', attrs={'class': False})

        for player in players:
            stats = player.findChildren(recursive=False)
            name = stats[1].find('a').string
            start = stats[2].string
            end = stats[3].string
            data = (name, start, end)
            player_list.append(data)

        categories[team] = player_list
        time.sleep(3.1)

    first_rounders = []
    for team in team_list:
        link = f'https://www.hockey-reference.com/teams/{team}/draft.html'
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')

        table = soup.find('tbody')
        players = table.find_all('tr', attrs={'class': False})

        for player in players:
            stats = player.findChildren(recursive=False)
            if stats[1].string == '1' and stats[8].string is not None:
                name = stats[3].string
                data = (name, team)
                first_rounders.append(data)

        time.sleep(3.1)

    categories['First Round Draft Pick'] = first_rounders


def get_season_leads(key, link):
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody')
    rows = table.find_all('tr', attrs={'class': False})

    player_list = []
    for row in rows:
        stats = row.findChildren(recursive=False)
        name = stats[1].find('a').string
        start = stats[3].string[:4]
        data = (name, start)
        player_list.append(data)

    categories[key] = player_list


def get_career_leads(key, link, req):
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody')
    rows = table.find_all('tr', attrs={'class': False})

    player_list = []
    for row in rows:
        stats = row.findChildren(recursive=False)
        number = int(stats[3].string)
        if number >= req:
            name = stats[1].find('a').string
            player_list.append(name)

    categories[key] = player_list


def get_hof():
    link = 'https://www.hockey-reference.com/awards/hhof.html'
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody')
    rows = table.find_all('tr', attrs={'class': False})

    player_list = []
    for row in rows:
        stats = row.findChildren()
        name = stats[1].string
        player_list.append(name)

    categories['Hall of Fame'] = player_list


def get_season_trophies(key, link):
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody')
    rows = table.find_all('tr', attrs={'class': False})

    player_list = []
    for row in rows:
        stats = row.findChildren(recursive=False)
        name = stats[2].string
        team = stats[4].string
        data = (name, team)
        player_list.append(data)

    categories[key] = player_list


def get_birth_places():
    link = 'https://www.hockey-reference.com/friv/birthplaces.cgi'
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html.parser')

    div = soup.find('div', attrs={'id': 'birthplace_3'})
    p_list = div.findChildren(recursive=False)
    count_a_list = [p.find('a') for p in p_list[1:]]
    count_links = [a['href'] for a in count_a_list]

    base_link = 'https://www.hockey-reference.com'

    player_list = []

    for link in count_links:
        new_page = requests.get(base_link + link).text
        new_soup = BeautifulSoup(new_page, 'html.parser')

        table = new_soup.find('tbody')
        rows = table.find_all('tr', attrs={'class': False})

        for row in rows:
            stats = row.findChildren(recursive=False)
            name = stats[1].string
            player_list.append(name)

        time.sleep(3.1)

    categories['Born Outside North America'] = player_list

    # Get Canadian Players
    div = soup.find('div', attrs={'id': 'birthplace_1'})
    p_list = div.findChildren(recursive=False)
    prov_a_list = [p.find('a') for p in p_list[1:]]
    prov_links = [a['href'] for a in prov_a_list]

    for link in prov_links:
        new_page = requests.get(base_link + link).text
        new_soup = BeautifulSoup(new_page, 'html.parser')

        table = new_soup.find('tbody')
        rows = table.find_all('tr', attrs={'class': False})

        for row in rows:
            stats = row.findChildren(recursive=False)
            name = stats[1].string
            player_list.append(name)

        time.sleep(3.1)

    categories['Born Outside US 50 States and DC'] = player_list

    # You need to do out of usa you stupid goof


def main():
    goals_link = 'https://www.hockey-reference.com/leaders/goals_season.html'
    points_link = 'https://www.hockey-reference.com/leaders/points_season.html'
    w_link = 'https://www.hockey-reference.com/leaders/wins_goalie_season.html'
    assist_link = 'https://www.hockey-reference.com/leaders/assists_season.html'
    # WE NEED TO GET ASSIST HOLDERS

    print("    >Geting 40+ goal scorers...(1/17)\n")
    get_season_leads('40+ Goalsseason', goals_link)
    time.sleep(3.1)

    print("    >Gettin 50+ assist scorers...(2/17)\n")
    get_season_leads('50+ Assistsseason', assist_link)
    time.sleep(3.1)

    print("    >Geting 100+ point scorers...(3/17)\n")
    get_season_leads('100+ Pointsseason', points_link)
    time.sleep(3.1)

    print("    >Geting 30+ win goalies...(4/17)\n")
    get_season_leads('30+ Winseason', w_link)
    time.sleep(3.1)

    goals_link = 'https://www.hockey-reference.com/leaders/goals_career.html'
    points_link = 'https://www.hockey-reference.com/leaders/points_career.html'
    w_link = 'https://www.hockey-reference.com/leaders/wins_goalie_career.html'

    print("    >Geting 500+ goal career...(5/17)\n")
    get_career_leads('500+ Goalscareer\n', goals_link, 500)
    time.sleep(3.1)

    print("    >Geting 1000+ point career...(6/17)\n")
    get_career_leads('1000+ Pointscareer', points_link, 1000)
    time.sleep(3.1)

    print("    >Geting 300+ win career...(7/17)\n")
    get_career_leads('300+ Winscareer', w_link, 300)
    time.sleep(3.1)

    byng_link = 'https://www.hockey-reference.com/awards/byng.html'
    ross_link = 'https://www.hockey-reference.com/awards/ross.html'
    hart_link = 'https://www.hockey-reference.com/awards/hart.html'
    calder_link = 'https://www.hockey-reference.com/awards/calder.html'
    vezina_link = 'https://www.hockey-reference.com/awards/vezina.html'
    norris_link = 'https://www.hockey-reference.com/awards/norris.html'
    smythe_link = 'https://www.hockey-reference.com/awards/smythe.html'

    print("    >Geting Lady Byng Trophy winners...(8/17)\n")
    get_season_trophies('Lady Byng Trophy', byng_link)
    time.sleep(3.1)

    print("    >Geting Art Ross Trophy winners...(9/17)\n")
    get_season_trophies('Art Ross Trophy', ross_link)
    time.sleep(3.1)

    print("    >Geting Hart Trophy winners...(10/17)\n")
    get_season_trophies('Hart Trophy', hart_link)
    time.sleep(3.1)

    print("    >Geting Calder Trophy winners...(11/17)\n")
    get_season_trophies('Calder Trophy', calder_link)
    time.sleep(3.1)

    print("    >Geting Vezina Trophy winners...(12/17)\n")
    get_season_trophies('Vezina Trophy', vezina_link)
    time.sleep(3.1)

    print("    >Geting Norris Trophy winners...(13/17)\n")
    get_season_trophies('Norris Trophy', norris_link)
    time.sleep(3.1)

    print("    >Geting Conn Smythe Trophy winners...(14/17)\n")
    get_season_trophies('Conn Smythe Trophy', smythe_link)
    time.sleep(3.1)

    print("    >Geting all players and first round draft picks...(15/17)\n")
    get_teams()
    time.sleep(3.1)

    print("    >Getting all hall of fame winners...(16/17)\n")
    get_hof()
    time.sleep(3.1)

    print("    >Geting birthplace data...(17/17)\n")
    get_birth_places()
    time.sleep(3.1)

    print("    >Serializing data...\n")
    data = json.dumps(categories, indent=2)

    print("    >Writing to file...\n")
    with open('data.json', 'w') as outfile:
        outfile.write(data)

    print("Data written to file, complete\n")


def remove_category(category):
    with open('data.json', 'r') as data:
        categories = json.load(data)
    categories.pop(category)
    print(f'Removed {category} from dictionary')


if __name__ == "__main__":
    main()
