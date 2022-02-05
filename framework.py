import logging
from datetime import datetime
from dotenv import dotenv_values
import json

# Define console class used for printing colored timestamped messages
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

# Define env class used for loading env variables from ".env" file into one array
class env:
	def empty(key):
		e = f'Key "{key}" empty in Dotenv file!'
		logger.error(e)
		raise KeyError(e)

	def load():
		try:
			envValues = dotenv_values()
			if envValues != {}:
				# If key is empty, raise KeyError using env.empty(key)
				envHotspots = envValues['HELIUM_HOTSPOTS'] if envValues['HELIUM_HOTSPOTS'] != '[]' else env.empty('HELIUM_HOTSPOTS')
				envDateStart = envValues['HELIUM_DATE_START'] if envValues['HELIUM_DATE_START'] != '' else env.empty('HELIUM_DATE_START') 
				envDateEnd = envValues['HELIUM_DATE_END'] if envValues['HELIUM_DATE_END'] != '' else env.empty('HELIUM_DATE_END') 
				try:
					json.loads(envHotspots)
				except json.decoder.JSONDecodeError as e:
					raise KeyError('HELIUM_HOTSPOTS')
				return {
					'HELIUM_HOTSPOTS': envHotspots,
					'HELIUM_DATE_START': envDateStart,
					'HELIUM_DATE_END': envDateEnd,
				}
			else:
				e_userFriendly = 'Dotenv file not found or empty!'
				raise FileNotFoundError(e_userFriendly)

		# Catch blank file or inexistent file
		except FileNotFoundError as e:
			e_userFriendly = f'{type(e).__name__}: {e.args[0]}'
			console.print(e_userFriendly, color=console.FAIL)
			logger.error(e_userFriendly)
			exit()
		
		# Catch miconfigured values (general)
		except KeyError as e:
			e_userFriendly = f'{type(e).__name__}: Key "{e.args[0]}" is misconfigured!'
			console.print(e_userFriendly, color=console.FAIL)
			logger.error(e_userFriendly)
			exit()

# Define logger class used for logging events to a log file set on line :67
class logger:
	logging.basicConfig(filename=f'result.log', filemode='w', level=logging.INFO, format='%(asctime)s § %(name)-24s § %(filename)-38s § %(threadName)-36s § %(lineno)-7s § %(levelname)-8s § %(message)s', datefmt='%Y-%m-%d %T%Z')
	
	def start(filename='result.log', level=logging.INFO, loggername='helium.logger'):
		logger = logging.getLogger(loggername); logger.setLevel(level)
		assert logger.parent == logging.root
		return logger

logger = logger.start()