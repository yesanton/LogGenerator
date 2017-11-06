import configparser

config = configparser.ConfigParser()

config.read("classes.set")

print(config['Order']['payload'])

for key in config['Order']: print(key)