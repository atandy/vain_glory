import requests
import bs4
import pandas as pd
import time

heroes = [ 'alpha', 'ozo', 'reim', 'kestrel', 'blackfeather'
           'phinn', 'skye', 'rona', 'fortress', 'joule', 
           'ardan', 'skaarf', 'taka', 'krul', 'saw', 'petal',
           'glaive', 'koshka', 'adagio', 'ringo', 'catherine',
           'celeste', 'vox']

base_url = 'http://www.vainglorygame.com/heroes/'



def make_request(url):
    r = requests.get(url)
    return r.content

def get_stats_df(soup, hero_name):
    stats = soup.find('div', {'class': 'stats-wrapper'}).findAll('span', {'class': 'white'})
    stats = [stat.getText() for stat in stats]
    titles = soup.find('div', {'class': 'stats-wrapper'}).findAll('h6')
    titles = [title.getText() for title in titles]
    
    stats_dict = {}
    for idx, val in enumerate(titles):
        stats_dict[val] = stats[idx]
    stats_dict['hero_name'] = hero_name
    return pd.DataFrame(stats_dict, index=[0])

column_map = { 'Armor': 'armor',
               'Attack Range': 'attack_range',
               'Attack Speed': 'attack_speed',
               'EP Regen': 'ep_regen',
               'Energy Points(EP)': 'energy_points',
               'HP Regen': 'hp_regen',
               'Hit Points(HP)': 'hit_points',
               'Movement Speed': 'movement_speed',
               'Shield': 'shield',
               'Weapon Damage': 'weapon_damage' }

def run():
    all_hero_dfs = []
    for hero_name in heroes:
        time.sleep(1)
        request_url = base_url + hero_name
        content = make_request(request_url)
        soup = bs4.BeautifulSoup(content)
        try:
            stats_df = get_stats_df(soup, hero_name)
        except Exception as e:
            print e
            print "could not get stats for {}".format(hero_name)
            stats_df = pd.DataFrame()

        all_hero_dfs.append(stats_df)

    for key, value in column_map.iteritems():
        core_df.rename(columns={key: value}, inplace=True)

    core_df = pd.concat(all_hero_dfs)
    core_df.to_csv('heroes.csv')


if __name__ == '__main__':
    run()