import yaml
from spire import Session

config = {}
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(-1)

s = Session(config['user'], config['password'], config['spire-id'])
results = s.search_area('SY', 'DB')

