import logging
from datetime import datetime
from dotenv import dotenv_values

class console:
	def timestamp():
		return datetime.now().strftime('%H:%M:%S.%f')[:-4]

	def print(message, color=''):
		print(f'[{console.timestamp()}] {color}{str(message)}{console.ENDC}')

	HEADER    = '\033[95m'
	OKBLUE    = '\033[94m'
	OKGREEN   = '\033[92m'
	WARNING   = '\033[93m'
	FAIL      = '\033[91m'
	BOLD      = '\033[1m'
	UNDERLINE = '\033[4m'
	ENDC      = '\033[0m'

class env:
	def Load():
		envValues = dotenv_values()
		if envValues == {}:
			e = 'Dotenv file not found or empty!'
			logger.error(e)
			raise FileNotFoundError(e)
		else:
			envHotspot = envValues['HELIUM_HOTSPOTS'] if envValues['HELIUM_HOTSPOTS'] != '[]' else env.NotFound('HELIUM_HOTSPOTS')
			envDateStart = envValues['HELIUM_DATE_START'] if envValues['HELIUM_DATE_START'] != '' else env.NotFound('HELIUM_DATE_START') 
			envDateEnd = envValues['HELIUM_DATE_END'] if envValues['HELIUM_DATE_END'] != '' else env.NotFound('HELIUM_DATE_END') 
			return {
				'HELIUM_HOTSPOTS': envHotspot,
				'HELIUM_DATE_START': envDateStart,
				'HELIUM_DATE_END': envDateEnd,
			}

	def NotFound(key):
		e = f'Key "{key}" not found in Dotenv file!'
		logger.error(e)
		raise KeyError(e)

class logger:
	logging.basicConfig(filename=f'result.log', filemode='w', level=logging.DEBUG, format='%(asctime)s § %(name)-24s § %(filename)-38s § %(threadName)-36s § %(lineno)-7s § %(levelname)-8s § %(message)s', datefmt='%Y-%m-%d %T%Z')
	
	def start(filename='result.log', level=logging.INFO, loggername='helium.logger'):
		logger = logging.getLogger(loggername); logger.setLevel(level)
		assert logger.parent == logging.root
		return logger

logger = logger.start()