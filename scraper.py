from framework import console, env, logger
from datetime import datetime
import requests
import xlwt
import json
import re

def main():
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Result')
	style_header = xlwt.easyxf('font: name Arial, color-index black, bold on')
	style_red = xlwt.easyxf('font: name Arial, color-index red', num_format_str='#,##0.0000000')
	style_green = xlwt.easyxf('font: name Arial, color-index dark_green_ega', num_format_str='#,##0.0000000')
	style_gray = xlwt.easyxf('font: name Arial, color-index gray_ega', num_format_str='#,##0.0000000')
	ws.write(0, 0, 'Hotspot', style_header)
	ws.write(0, 1, 'Date', style_header)
	ws.write(0, 2, 'Earnings', style_header)
	ws.col(0).width = 256 * 55
	ws.col(1).width = 256 * 10
	ws.col(2).width = 256 * 10
	excelCrt = 1

	heliumHotspots = json.loads(dotenv['HELIUM_HOTSPOTS'])
	heliumDateStart = dotenv['HELIUM_DATE_START'] + 'T00:00:00.000Z'
	heliumDateEnd = dotenv['HELIUM_DATE_END']  + 'T00:00:00.000Z'
	console.print(message=f'Starting date: {heliumDateStart} | Ending date: {heliumDateEnd}', color=console.HEADER)
	for heliumHotspot in heliumHotspots:
		console.print(message=f'Checking data for hotspot - {heliumHotspot}', color=console.HEADER)
		try:
			headers = {
				'user-agent': 'HeliumExplorerScraper/1.0.0'
			}
			r = requests.get(f'https://helium-api.stakejoy.com/v1/hotspots/{heliumHotspot}/rewards/sum?min_time={heliumDateStart}&max_time={heliumDateEnd}&bucket=day', headers=headers)
			if r.status_code == 200:
				j = json.loads(r.text)
				for _ in j['data']:
					earningDate = re.search(r'^([0-9]{4}-[0-9]{2}-[0-9]{2})', _['timestamp']).group(1)
					earningTotal = _['total']
					earningTotalFormatted = '{:.9f}'.format(earningTotal)

					earningDateDT = datetime.strptime(earningDate, '%Y-%m-%d')
					currentDateDT = datetime.now()
					
					if earningTotalFormatted == '0.000000000':
						color = console.FAIL
						colorXlwt = style_red
					else:
						color = console.OKGREEN
						colorXlwt = style_green
					if earningDateDT > currentDateDT:
						color = console.WARNING
						colorXlwt = style_gray

					ws.write(excelCrt, 0, heliumHotspot, colorXlwt)
					ws.write(excelCrt, 1, earningDate, colorXlwt)
					ws.write(excelCrt, 2, earningTotal, colorXlwt)
					excelCrt += 1
								
					msg = f'{heliumHotspot} {earningDate}: {earningTotalFormatted} HNT'
					console.print(message=msg, color=color)
					logger.info(msg)

			else:
				raise ConnectionError(f'Unexpected status code: {r.status_code}')

		except ConnectionError as e:
			logger.error(e)

	wb.save('result.xls')

if __name__ == "__main__":
	try:
		dotenv = env.Load()
	except Exception as e:
		console.print(e.args[0], console.FAIL)
		exit()
	main()