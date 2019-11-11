import csv
from pathlib import Path
from urllib.request import urlretrieve

#tmp = Path('/tmp')
#stats = tmp / 'bites.csv'
stats = Path('./bites.csv')

if not stats.exists():
    urlretrieve('https://bit.ly/2MQyqXQ', stats)


def get_most_complex_bites(N=10, stats=stats):
    """Parse the bites.csv file (= stats variable passed in), see example
       output in the Bite description.
       Return a list of Bite IDs (int or str values are fine) of the N
       most complex Bites.
    """
    with open(stats, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=';')
        bites = list(reader)
    bites = [bite for bite in bites if bite['Difficulty'] != 'None']
    bites = sorted(bites, reverse=True, key=lambda x: x['Difficulty']) 
    return [bite['Bite'].split(" ")[1][:-1] for bite in bites[:N]]

if __name__ == '__main__':
    res = get_most_complex_bites()
    print(res)
