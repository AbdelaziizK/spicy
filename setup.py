from setuptools import setup, find_packages
from pathlib import Path

def get_setup_kwargs():
	long_description = open("README.md").read()
	packages = find_packages(exclude = ["spicy.test"])
	return {
		"name": "spicy",
		"version": "1.0.0",
		"author": "Aziz K",
		"author_email": "aaziizkh2001@gmail.com",
		"keywords": "mobile-phone phone-specification gsmarena.com",
		"description": "Spicy is a library that parse 'GSMArena.com' and provides different functions to get mobile-phones information and specifications.",
		"long_description": long_description,
		"long_description_content_type": "markdown",
		"license": "MIT",
		"url": "https://www.github.com/abdelaziizk/spicy/",
		"packages": packages,
		"include_package_data": True,
		"install_requires": ["requests-html==0.10.0; python_full_version >= '3.6.0'"],
		"python_requires": ">=3.8",
		"classifiers": [
			"Intended Audience :: Developers",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3.8",
			"Programming Language :: Python :: 3.9",
			"Programming Language :: Python :: 3.10",
			"Programming Language :: Python :: 3.11",
			"Programming Language :: Python :: 3.12",
		]
	}
	

setup(**get_setup_kwargs())