import requests
from csv import DictReader


def server_stats(stats_server_ip):
    response = requests.get(f'http://{stats_server_ip}:9999/stats?stats;csv;norefresh')
    reader = DictReader(response.text.lstrip('# ').split('\n'), delimiter = ',')
    servers = {}
    for line in reader:
        dct = dict(line)
        svname = dct['svname']
        if 'webapp' in svname or svname == 'BACKEND':
            servers[svname] = dct
    return servers
