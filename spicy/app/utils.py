from requests_html import HTML, HTMLSession
import json
from requests.exceptions import ConnectionError as rce


def get_html_from_url(url: str):
	session = HTMLSession()
	try:
		html = session.get(f'https://m.gsmarena.com/{url}').html
	except rce:
		raise rce("Failed to establish a new connection")
	
	return html