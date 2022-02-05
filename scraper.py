from framework import console, env, logger
from datetime import datetime
import requests
import xlwt
import json
import time
import re

def main():
	# Create a workbook
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Result')
	# Workbook styling set-up: bold for headers, red for "no earnings", green for "any earnings", gray for "future dates"
	style_arial_black_bold = xlwt.easyxf(strg_to_parse='font: name Arial, color-index black, bold on')
	style_arial_red = xlwt.easyxf(strg_to_parse='font: name Arial, color-index red', num_format_str='#,##0.0000000')
	style_arial_green = xlwt.easyxf(strg_to_parse='font: name Arial, color-index dark_green_ega', num_format_str='#,##0.0000000')
	style_arial_gray = xlwt.easyxf(strg_to_parse='font: name Arial, color-index gray_ega', num_format_str='#,##0.0000000')
	# Write header row to the table using bold styling
	ws.write(r=0, c=0, label='Hotspot', style=style_arial_black_bold)
	ws.write(r=0, c=1, label='Date', style=style_arial_black_bold)
	ws.write(r=0, c=2, label='Earnings HNT', style=style_arial_black_bold)
	ws.write(r=0, c=3, label='Earnings USD', style=style_arial_black_bold)
	ws.write(r=0, c=4, label='Market USD', style=style_arial_black_bold)
	# Set-up the column width
	ws.col(0).width = 256 * 55
	ws.col(1).width = 256 * 12
	ws.col(2).width = 256 * 12
	ws.col(3).width = 256 * 12
	ws.col(4).width = 256 * 12
	excelCurrentRow = 1
	# Load data from dotenv variable created at line :105
	heliumHotspots = json.loads(dotenv['HELIUM_HOTSPOTS'])
	heliumDateStart = dotenv['HELIUM_DATE_START'] + 'T00:00:00.000Z'
	heliumDateEnd = dotenv['HELIUM_DATE_END']  + 'T00:00:00.000Z'
	# Print current status in console using header color
	console.print(message=f'Starting date: {heliumDateStart} | Ending date: {heliumDateEnd}', color=console.HEADER)
	for hotspot in heliumHotspots:
		console.print(message=f'Checking data for hotspot - {hotspot}', color=console.HEADER)
		try:
			# Set request headers to our custom user agent 
			headers = {
				'user-agent': 'HeliumExplorerScraper/1.0.0'
			}
			# Request data from Helium API for this particular hotspot (between the defined start and end dates)
			r = requests.get(url=f'https://helium-api.stakejoy.com/v1/hotspots/{hotspot}/rewards/sum?min_time={heliumDateStart}&max_time={heliumDateEnd}&bucket=day', headers=headers, timeout=10)
			# If request is successful
			if r.status_code == 200:
				# Parse response using json
				j = json.loads(r.text)
				for _ in j['data']:
					# Set variables needed for our report
					currentDateDT = datetime.now()
					earningDate = re.search(r'^([0-9]{4}-[0-9]{2}-[0-9]{2})', _['timestamp']).group(1)
					earningDateDT = datetime.strptime(earningDate, '%Y-%m-%d')
					earningDateString = datetime.strftime(earningDateDT, '%d-%m-%Y')
					earningTotalHNT = _['total']
					earningTotalHNTFormatted = '{:.9f}'.format(earningTotalHNT)
					
					# Try to request data from Coingecko API regarding USD value of HNT at the time of earning
					try:
						# Request data from Goingecko API for this particular earning date
						r = requests.get(url=f'https://api.coingecko.com/api/v3/coins/helium/history?date={earningDateString}', headers=headers, timeout=10)
						# If request is successful, parse market data in USD
						if r.status_code == 200:
							j = json.loads(r.text)
							marketDataUSD, earningTotalUSD, earningTotalUSDFormatted = '', '', 'ERROR'
							marketDataUSD = j['market_data']['current_price']['usd']
							earningTotalUSD = earningTotalHNT * marketDataUSD
							earningTotalUSDFormatted = '{:.4f}'.format(earningTotalUSD)

						# If request is unsuccessful, throw ConnectionError
						else:
							raise ConnectionError(f'Unexpected status code {r.status_code}')
					
					# If there is no market data in the Coingecko API, throw warning
					except KeyError as e:
						if e.args[0] == 'market_data':
							e_userFriendly = f'{type(e).__name__}: {e.args[0]}'
							logger.warning(e_userFriendly)
					
					# If there is a connection error to the Coingecko API, throw warning
					except ConnectionError as e:
						e_userFriendly = f'{type(e).__name__}: {e.args[0]}'
						console.print(message=e_userFriendly, color=console.FAIL)
						logger.warning(e_userFriendly)

					# If there are no earnings, format using red styling
					if earningTotalHNTFormatted == '0.000000000':
						color = console.FAIL
						colorXlwt = style_arial_red
					# If there are earnings, format using green styling
					else:
						color = console.OKGREEN
						colorXlwt = style_arial_green
					# If requested future date, format using gray styling
					if earningDateDT > currentDateDT:
						color = ''
						colorXlwt = style_arial_gray

					# Write data to excel on current row and advance row
					ws.write(excelCurrentRow, 0, hotspot, colorXlwt)
					ws.write(excelCurrentRow, 1, earningDate, colorXlwt)
					ws.write(excelCurrentRow, 2, earningTotalHNT, colorXlwt)
					ws.write(excelCurrentRow, 3, earningTotalUSD, colorXlwt)
					ws.write(excelCurrentRow, 4, marketDataUSD, colorXlwt)
					excelCurrentRow += 1

					# Print current status in console using color set above
					msg = f'{hotspot} {earningDate}: {earningTotalHNTFormatted} HNT ({earningTotalUSDFormatted} USD)'
					console.print(message=msg, color=color)
					logger.info(msg)

					# Sleep 1 sec
					time.sleep(1)

			# If request is unsuccessful
			else:
				raise ConnectionError(f'Unexpected status code {r.status_code}')

		except ConnectionError as e:
			e_userFriendly = f'{type(e).__name__}: {e.args[0]}'
			console.print(message=e_userFriendly, color=console.FAIL)
			logger.error(e_userFriendly)

	# Save result as xls
	wb.save('result.xls')

if __name__ == '__main__':
	dotenv = env.load()
	logger.info(f'Loaded dotenv file: {dotenv}')
	main()