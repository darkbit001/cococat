import configparser
def getconfig():
	config = configparser.ConfigParser()
	config.read('config')
	return config