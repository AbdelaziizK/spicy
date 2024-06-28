import json
from .utils import get_html_from_url


def get_all_brands():
	
	"""
	Fetches brands returns them as a JSON string.

	Returns:
		str: A JSON string containing a list of brands, each brand is represented as 
		a dictionary with the following keys:
		"name": the name of the brand
		"path": the path of the brand page's URL
    """
	
	html_page = ''
	try:
		html_page = get_html_from_url('makers.php3')
	except Exception as e:
		raise e
	
	brands = html_page.find('div#list-brands', first=True)
	response = {"brands": []}
	
	for brand in brands.find('li'):
		brand_info = {}
		
		brand_info["name"] = brand.text.strip()
		brand_info["path"] = brand.find('a', first=True).attrs["href"]
		
		response["brands"].append(brand_info)
	
	response = json.dumps(response, indent=2, ensure_ascii = False)
	
	return response


def get_brand_devices(*, brand: str = '', brand_path: str = '',\
next: bool = False, prev: bool = False):
	
	"""

	Fetch devices of brand based on the provided parameters,
	and returns them as a JSON string. if brand has more than 50 devices, 
	it returns the first 50. 50 devices at a time.
	
	Args:
		brand (str): Name of the brand. must be the same nemr! (but case doesn't matter).
		brand_path (str): The path of the brand page's URL. obtained from 
		get_brand(). can be a path of brand's first page or any other page.
		next (bool, optional): If True fitches next page to this link. if there's no next page, raises ValueError.
		prev (bool, optional): If True fitches previous page to this link.if there's no previous page, raises ValueError.
		
	Returns:
		str: A JSON containing a list of devices.
		
	"""
	
	
	if not isinstance(brand, str):
		raise TypeError(f"'brand' must be str, not {brand.__class__.__name__}")
	if not isinstance(brand_path, str):
		raise TypeError(f"'brand_path' must be str, not {brand_path.__class__.__name__}")
	if not isinstance(next, bool):
		raise TypeError(f"'next' must be bool, not {next.__class__.__name__}")
	if not isinstance(prev, bool):
		raise TypeError(f"'prev' must be bool, not {prev.__class__.__name__}")
	
	if next and prev:
		raise TypeError("Only one of 'next' or 'prev' must be provided")
	
	if not (brand or brand_path):
		raise TypeError("At least one of 'brand' or 'brand_path' must be provided")
	
	if brand and brand_path:
		raise TypeError("Only one of 'brand' or 'brand_path' must be provided, not both")
		
	if brand_path:
		if not ('-phones-' in brand_path and '.php' in brand_path):
			raise ValueError("'brand_path' is not valid")
	
	brands = json.loads(get_all_brands())['brands']
	for i in brands:
		if brand.lower() == i['name'].lower() or brand_path.split('-')[0]\
		.lower() == i['name'].lower():
			if not brand_path:
				brand_path = i['path']
			if not brand:
				brand = i['name']
			break
	if not (brand and brand_path):
		if not brand:
			raise ValueError(f"brand {brand} not found")
		if not brand_path:
			raise ValueError(f"brand_path {brand_path} not found")
	
	if next:
		next = 1
	if prev:
		prev = -1
	
	if next or prev:
		if '-f-' in brand_path and '-0-' in brand_path:
			try:
				brand_path = brand_path.replace('.php', '')
				brand_path = brand_path.split('-')
				num = eval(brand_path.pop().replace('p', ''))
				
				if next:
					num = (num + next)
				if prev:
					num = (num + prev)
				
				if num == 1:
					brand_path = brand_path[0] + '-' + brand_path[1] + '-' + brand_path[3] + '.php' 
				else:
					brand_path.append('p'+ str(num))
					brand_path = '-'.join(brand_path) + '.php'
			except Exception as e:
				raise e
		
		else:
			try:
				brand_path = brand_path.replace('.php', '')
				brand_path = brand_path.split('-')
				
				if prev:
					raise ValueError("There's no previous page, this is the first")
				
				brand_path.insert(-1, 'f')
				brand_path.append('0')
				brand_path.append('p')
				brand_path = '-'.join(brand_path)
				
				if next:
					brand_path += f'{next+1}.php'
				
			except ValueError as e:
				raise e
			except Exception as e:
				raise e
	
	try:
		html_page = get_html_from_url(brand_path)
	except Exception as e:
		raise e
	response = {"brand_path": brand_path, "devices": []}
	
	devices_list = html_page.find('div.general-menu',first=True)
	for device in devices_list.find('li'):
		device_info = {}
		
		device_info["name"] = device.text
		device_info["path"] = device.find('a',first=True).attrs["href"]
		device_info["image_url"] = device.find('img', first=True).attrs["src"]
		
		response["devices"].append(device_info)
		
	response = json.dumps(response, indent=2, ensure_ascii = False)
	
	return response


def get_device_specs(device_path: str):
	
	"""
	returns the specifications of a device as a JSON string.
	
	Args:
		device_path (str): The path of the device page's URL (obtained
		from get_brand_devices()of a brand, or search() a certain phone)
		
		Returns:
			str: A JSON string containing the device specifications, organized into a nested dictionary.
	
	Raises:
		TypeError: If the 'device_path' argument is not a string.
		ValueError: If the 'device_path' argument is not a valid URL.
	"""
	
	if not isinstance(device_path, str):
		raise TypeError(f"'device_path' must be str, not {device_path.__class__.__name__}")
	
	if not ('-' in device_path and '.php' in device_path):
		raise ValueError("'device_path' is not valid")
	
	try:
		html_page = get_html_from_url(device_path)
	except Exception as e:
		raise e
	
	image_url = html_page.find('div.specs-cp-pic-rating',\
		first=True).find('img', first=True).attrs['src']
	
	specs_list = html_page.find('div#specs-list', first=True)
	if not specs_list:
		raise ValueError(f"Device not found, check device_path '{device_path}'")
	
	response = {"image_url": image_url, "specifications": {}}
	
	comment = specs_list.find('p.specs-comment', first=True)
	if comment and (':' in comment.text):
		comment = comment.text.split(':')
		comment[1] = comment[1].strip().split('; ')
		response['specifications'][comment[0]] = comment[1]
	
	tables = specs_list.find('table')
	for table in tables:
		heading = table.find('th', first=True).text.strip()
		response['specifications'][heading] = {}
		
		rows = table.find('tr')
		for j in range(len(rows)):
			if len(rows[j].text.strip()) == 0:
				continue
		
			sub_heading = rows[j].find('td.ttl', first=True)
			sub_heading = sub_heading.text.strip() if sub_heading\
			else None
			
			if not sub_heading:
				continue
			
			info = rows[j].find('td.nfo', first=True)
			info = info.text.split('\n') if info else None
			
			x = 1
			while (j + x) < len(rows) - 1:
				next_row_sub_heading = rows[j+x].find('td.ttl',\
				first=True).text.strip()
				next_row_sub_heading = next_row_sub_heading\
				if next_row_sub_heading else None
				
				if not next_row_sub_heading:
					next_row_info = rows[j+x].find('td.nfo',\
					first=True)
					
					if next_row_info:
						if len(next_row_info.text) > 0:
							info.append(next_row_info.text)
				else:
					response['specifications'][heading]\
					[sub_heading] = info
					break
				x += 1
			response['specifications'][heading]\
			[sub_heading] = info
	
	response = json.dumps(response, indent=2, ensure_ascii = False)
	
	return response


def search(device_name: str):
	
	"""
	Searches for devices based on the provided device name and returns the results as a JSON string.
	
	Args:
		device_name (str): The name of the device to search for.
	
	Returns:
		str: A JSON string containing the search results (if more than 70 results found, 
		return must popular 70.
	
	Raises:
		TypeError: If the `device_name` parameter is not a string.
	"""
	
	if not isinstance(device_name, str):
		raise TypeError(f"'device_name' must be str, not {device_name.__class__.__name__}")
	
	path = f'results.php3?sQuickSearch=yes&sName={device_name}'
	try:
		html_page = get_html_from_url(path)
	except Exception as e:
		raise e
	
	response = {}
	message = html_page.find('div.st-text', first=True)
	message = message.text if message else None
	response["message"] = message
	
	if not html_page.find('div.general-menu', first=True).text:
		response["message"] = 'Phone not found! check your spelling'
		response["results"] = []
		response = json.dumps(response, indent=2, ensure_ascii=True)
		return response
	
	results_list = html_page.find('div.general-menu', first=True).find('li')
	response["results"] = []
	
	for device in results_list:
		device_info = {}
		
		name = ' '.join(device.find('strong', first=True).text\
		.split('\n'))
		path = device.find('a', first=True).attrs["href"]
		image_url = device.find('img', first=True)\
		.attrs["src"]
		
		device_info["name"] = name
		device_info["path"] = path
		device_info["image_url"] = image_url
		
		response["results"].append(device_info)
	
	response = json.dumps(response, indent=2, ensure_ascii = False)
	
	return response


def daily_deals():
	
	"""
	Fetches the daily deals information from a website and returns it as a JSON string.
	
	Returns:
		str: A JSON string containing the devices of the daily deals, and deal information.
	"""
	
	try:
		html_page = get_html_from_url('deals.php3')
	except Exception as e:
		raise e
	
	response = {}
	
	message = html_page.find('div.st-text', first=True).text
	response["message"] = message
	response["deals"] = []
	
	deals_devices = html_page.find('div.pricecut')
	for device in deals_devices:
		name = device.find('h3', first=True).text
		path = device.find('a.button', first=True).attrs['href']
		image_url = device.find('img', first=True).attrs['src']
		device_info = device.find('p', first=True).find('a')[0].text
		storage_and_ram = device.find('p', first=True).find('a')[1].text
		
		store_url = device.find('a.store', first=True).attrs['href']
		price = device.find('a.price', first=True).text.split()[1]
		currency = str(device.find('a.cutprice', first=True).attrs['symbol'])
		discount_percentage = device.find('a.discount', first=True).text
		previous_price, min_price, max_price, avg_in_30_days =\
			device.find('div.stats', first=True).find('b')
		previous_price = previous_price.text.split()[1]
		min_price = min_price.text.split()[1]
		max_price = max_price.text.split()[1]
		avg_in_30_days = avg_in_30_days.text.split()[1]
		
		deal_info = {
			"name": name,
			"path": path,
			"image_link": image_url,
			"device_info": device_info,
			"storage_and_ram": storage_and_ram,
			"deal": {
				"store_url": store_url,
				"price": price,
				"currency": currency,
				"discount_percentage": discount_percentage,
				"previous_price": previous_price,
				"min_price": min_price,
				"max_price": max_price,
				"30_days_average": avg_in_30_days
			}
		}
		
		response["deals"].append(deal_info)
		
	response = json.dumps(response, indent=2, ensure_ascii = False)
	
	return response