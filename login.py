import yaml
import spire
import sys

config = {}
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)

s = spire.Session(config['user'], config['password'], config['spire_id'])
results = s.search_area('SY', 'DB')

