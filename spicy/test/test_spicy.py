import unittest
import random as rm
import json

from spicy import (
get_all_brands,
get_brand_devices,
get_device_specs,
search,
daily_deals)


class TestSpicy(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		cls.brands = json.loads(get_all_brands())
		cls.random_brand = rm.choice(cls.brands["brands"])
		cls.devices = json.loads(get_brand_devices(brand_path=cls.random_brand["path"]))
		cls.random_device = rm.choice(cls.devices["devices"])
		
	def test_get_all_brands(self):
		brands = self.brands
		
		self.assertIn("brands", brands)
		self.assertTrue(len(brands["brands"]) > 120)
		self.assertIsInstance(brands["brands"], list)
		self.assertIsInstance(brands["brands"][0], dict)
		self.assertEqual(len(brands["brands"][rm.randint(1, 124)]), 2)
	
	def test_get_brand_devices(self):
		random_brand = self.random_brand
		devices = self.devices
		
		self.assertIn("devices", devices)
		self.assertIsInstance(devices["devices"], list)
		self.assertIsInstance(devices["devices"][0], dict)
		self.assertEqual(len(devices["devices"][0]), 3)
		
		self.assertRaises(TypeError, get_brand_devices, brand=4)
		self.assertRaises(TypeError, get_brand_devices, brand_path = 5)
		self.assertRaises(TypeError, get_brand_devices, next= "1")
		self.assertRaises(TypeError, get_brand_devices, prev="1")
		self.assertRaises(TypeError, get_brand_devices, next=True, prev=True)
		self.assertRaises(TypeError, get_brand_devices)
		self.assertRaises(TypeError, get_brand_devices, brand="apple",\
			brand_path="apple-phones-48.php")
		self.assertRaises(ValueError, get_brand_devices,\
			brand_path="wrog path for testing")
		self.assertRaises(ValueError, get_brand_devices,\
			brand="wrong brand name for testing")
		self.assertRaises(ValueError, get_brand_devices,\
			brand_path="apple-phones-48.php", prev=True)
	
	def test_get_device_specs(self):
		random_device = self.random_device
		specs = json.loads(get_device_specs(random_device["path"]))
		
		self.assertIn("image_url", specs)
		self.assertIn("specifications", specs)
		self.assertIsInstance(specs["image_url"], str)
		self.assertIsInstance(specs["specifications"], dict)
		self.assertIsInstance(specs["specifications"], dict)
		
		self.assertRaises(TypeError, get_device_specs, 45)
		self.assertRaises(ValueError, get_device_specs,\
			"wrog device_path for testing")
		
	def test_search(self):
		results = json.loads(search(device_name=self.random_device["name"]))
		
		self.assertIn("message", results)
		self.assertIn("results", results)
		
		if results["results"]:
			self.assertIsInstance(results, dict)
			self.assertIsInstance(results["results"], list)
			self.assertIsInstance(results["results"][0], dict)
			
		self.assertRaises(TypeError, search, device_name=5)
	
	def test_daily_deals(self):
		deals = json.loads(daily_deals())
		
		self.assertIn("message", deals)
		self.assertIn("deals", deals)
		
		self.assertIsInstance(deals["message"], str)
		self.assertIsInstance(deals["deals"], list)
		self.assertIsInstance(deals["deals"][0], dict)


if __name__ == '__main__':
	unittest.main()