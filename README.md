# Spicy

## Contents
-[Description](#description)
-[Installation](#installation)
-[Features](#features)
-[Usage](#usage)
-[Contribution](#contribution)

## Description
Spicy is a library that parse 'GSMArena.com' and provides different functions provide mobile-phones information and specifications. It provides up-to-date and comprehensive information about all brands devices.
### Why?
I wanted to make a telegram bot that provides mobile-phones information and specifications, but I didn't find any library or an API that provides phone-devices information. So I thought of doing this library first, then use it for the telegram bot.

## Installation
### Prerequisites
You need`requests_html` installed first because it's needed to parse the source website. 
### Using pip
Use pip to install it directly:
```bash
pip install spicy
```

## Features
Spicy provides 5 functions:
- `get_all_brands()`:
Fetches brands, returns them as a JSON string contains a list of brands, each has it's name and it's path; (the path is the part of the URL that comes after the '/', "https://www.GSMArena.com/*path*")
- `get_brand_devices(brand, brand_path, next, prev)`:
Fetches devices of the brand, all devices if they are less than 50. or 50 at a time if they are more than 50. And returns them as a JSON string contains `brand_path` and a list of devices each has it's `name`, `path` and `image_url`. The `brand_path` argument is the path we get from `search`.
If a brand has more than 50 devices, when calling this function and it returns it's response we can call it again with the `brand_path` in the response with the `next` argument set to True to get the next 50 devices. There's also`prev` to get the previous 50 if this is not the first 50, else it'll raise ValueError.
If called with `brand` and `brand_path` together, it raise ValueError and same with `next` and `prev`.
- `get_device_specs(device_path)`:
Fetches device's information (specifications ) and returns them as JSON string contains all information about the device.
`device_path` can be obtained from `search` or one of `brand_devices`.
- `search(device_name)`:
Fetches the resulted devices (if found) of searching `device_name` and return the results in a JSON string containing a massage header describing the result and a list of results.
If more than 70 results founded it returns the most popular 70 of the search.
- `daily_deals()`:
GSMArena.com constantly monitoring the prices of devices and every day they provide best deals for different devices and different online stores.
This function fetches these deals and return it as a JSON string containing a list of these deals with all details about each deal.

## Usage
First you need to import spicy in your script
```python
From spicy import *
```
Then you can use any of it's functions:
- calling `get_all_devices()`
returns:
```JSON
{
  "brands": [
    {
      "name": "Acer",
      "path": "acer-phones-59.php"
    },
    .
    .
    .
    {
      "name": "ZTE",
      "path": "zte-phones-62.php"
    }
  ]
}
```

- calling `get_brand_devices(brand="applle")` or `get_brand_devices(brand_path="applle-phones-48.php")`
returns:
```JSON
{
  "brand_path": "apple-phones-48.php",
  "devices": [
    {
      "name": "iPad Pro 13 (2024)",
      "path": "apple_ipad_pro_13_(2024)-12987.php",
      "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-ipad-pro-13-2024.jpg"
    },
    .
    .
  ]
}
```
If `next` set to True, it will return the next 50 devices and returns the path of it.

- calling `get_device_specs("apple_iphone_15_pro_max-12548.php")`
returns:
```JSON
{
  "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg",
  "specifications": {
    "Versions": [
      "A3106 (International)",
      "A2849 (USA)",
      "A3105 (Canada, Japan)",
      "A3108 (China, Hong Kong)"
    ],
    "Network": {
      "Technology": [
        "GSM / CDMA / HSPA / EVDO / LTE / 5G"
      ],
      "2G bands": [
        "GSM 850 / 900 / 1800 / 1900 - SIM 1 & SIM 2 (dual-SIM)",
        "CDMA 800 / 1900"
      ],
      "3G bands": [
        "HSDPA 850 / 900 / 1700(AWS) / 1900 / 2100",
        "CDMA2000 1xEV-DO"
      ],
      "4G bands": [
        "1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 30, 32, 34, 38, 39, 40, 41, 42, 46, 48, 53, 66 - A3106",
        "1, 2, 3, 4, 5, 7, 8, 12, 13, 14, 17, 18, 19, 20, 25, 26, 28, 29, 30, 32, 34, 38, 39, 40, 41, 42, 46, 48, 53, 66, 71 - A2849",
        "1, 2, 3, 4, 5, 7, 8, 11, 12, 13, 14, 17, 18, 19, 20, 21, 25, 26, 28, 29, 30, 32, 34, 38, 39, 40, 41, 42, 46, 48, 53, 66, 71 - A3105",
        "1, 2, 3, 4, 5, 7, 8, 12, 13, 17, 18, 19, 20, 25, 26, 28, 30, 32, 34, 38, 39, 40, 41, 42, 46, 48, 66 - A3108"
      ],
      "5G bands": [
        "1, 2, 3, 5, 7, 8, 12, 20, 25, 26, 28, 30, 38, 40, 41, 48, 53, 66, 70, 77, 78, 79 SA/NSA/Sub6 - A3106",
        "1, 2, 3, 5, 7, 8, 12, 14, 20, 25, 26, 28, 29, 30, 38, 40, 41, 48, 53, 66, 70, 71, 77, 78, 79, 258, 260, 261 SA/NSA/Sub6/mmWave - A2849",
        "1, 2, 3, 5, 7, 8, 12, 14, 20, 25, 26, 28, 29, 30, 38, 40, 41, 48, 53, 66, 70, 71, 75, 76, 77, 78, 79 SA/NSA/Sub6 - A3105",
        "1, 2, 3, 5, 7, 8, 12, 20, 25, 26, 28, 30, 38, 40, 41, 48, 66, 70, 77, 78, 79 SA/NSA/Sub6 - A3108"
      ],
      "Speed": [
        "HSPA, LTE, 5G, EV-DO Rev.A 3.1 Mbps"
      ]
    },
    "Launch": {
      "Announced": [
        "2023, September 12"
      ],
      "Status": [
        "Available. Released 2023, September 22"
      ]
    },
    "Body": {
      "Dimensions": [
        "159.9 x 76.7 x 8.3 mm (6.30 x 3.02 x 0.33 in)"
      ],
      "Weight": [
        "221 g (7.80 oz)"
      ],
      "Build": [
        "Glass front (Corning-made glass), glass back (Corning-made glass), titanium frame (grade 5)"
      ],
      "SIM": [
        "Nano-SIM and eSIM - International",
        "Dual eSIM with multiple numbers - USA",
        "Dual SIM (Nano-SIM, dual stand-by) - China"
      ]
    },
    "Display": {
      "Type": [
        "LTPO Super Retina XDR OLED, 120Hz, HDR10, Dolby Vision, 1000 nits (typ), 2000 nits (HBM)"      ],
      "Size": [
        "6.7 inches, 110.2 cm2 (~89.8% screen-to-body ratio)"
      ],
      "Resolution": [
        "1290 x 2796 pixels, 19.5:9 ratio (~460 ppi density)"
      ],
      "Protection": [
        "Ceramic Shield glass"
      ]
    },
    "Platform": {
      "OS": [
        "iOS 17, upgradable to iOS 17.5.1, planned upgrade to iOS 18"
      ],
      "Chipset": [
        "Apple A17 Pro (3 nm)"
      ],
      "CPU": [
        "Hexa-core (2x3.78 GHz + 4x2.11 GHz)"
      ],
      "GPU": [
        "Apple GPU (6-core graphics)"
      ]
    },
    "Memory": {
      "Card slot": [
        "No"
      ],
      "Internal": [
        "256GB 8GB RAM, 512GB 8GB RAM, 1TB 8GB RAM"
      ]
    },
    "Main Camera": {
      "Triple": [
        "48 MP, f/1.8, 24mm (wide), 1/1.28\", 1.22µm, dual pixel PDAF, sensor-shift OIS",
        "12 MP, f/2.8, 120mm (periscope telephoto), 1/3.06\", 1.12µm, dual pixel PDAF, 3D sensor‑shift OIS, 5x optical zoom",
        "12 MP, f/2.2, 13mm, 120˚ (ultrawide), 1/2.55\", 1.4µm, dual pixel PDAF",
        "TOF 3D LiDAR scanner (depth)"
      ],
      "Features": [
        "Dual-LED dual-tone flash, HDR (photo/panorama)"
      ],
      "Video": [
        "4K@24/25/30/60fps, 1080p@25/30/60/120/240fps, 10-bit HDR, Dolby Vision HDR (up to 60fps), ProRes, Cinematic mode (4K@24/30fps), 3D (spatial) video, stereo sound rec."
      ]
    },
    "Selfie Camera": {
      "Single": [
        "12 MP, f/1.9, 23mm (wide), 1/3.6\", PDAF, OIS",
        "SL 3D, (depth/biometrics sensor)"
      ],
      "Features": [
        "HDR, Cinematic mode (4K@24/30fps)"
      ],
      "Video": [
        "4K@24/25/30/60fps, 1080p@25/30/60/120fps, gyro-EIS"
      ]
    },
    "Sound": {
      "Loudspeaker": [
        "Yes, with stereo speakers"
      ],
      "3.5mm jack": [
        "No"
      ]
    },
    "Comms": {
      "WLAN": [
        "Wi-Fi 802.11 a/b/g/n/ac/6e, dual-band, hotspot"
      ],
      "Bluetooth": [
        "5.3, A2DP, LE"
      ],
      "Positioning": [
        "GPS (L1+L5), GLONASS, GALILEO, BDS, QZSS, NavIC"
      ],
      "NFC": [
        "Yes"
      ],
      "Radio": [
        "No"
      ],
      "USB": [
        "USB Type-C 3.2 Gen 2, DisplayPort"
      ]
    },
    "Features": {
      "Sensors": [
        "Face ID, accelerometer, gyro, proximity, compass, barometer"
      ]
    },
    "Battery": {
      "Type": [
        "Li-Ion 4441 mAh, non-removable"
      ],
      "Charging": [
        "Wired, PD2.0, 50% in 30 min (advertised)",
        "15W wireless (MagSafe)",
        "15W wireless (Qi2) - requires iOS 17.2 update",
        "4.5W reverse wired"
      ]
    },
    "Misc": {
      "Colors": [
        "Black Titanium, White Titanium, Blue Titanium, Natural Titanium"
      ],
      "Models": [
        "A2849, A3105, A3106, A3108, iPhone16,2"
      ],
      "SAR": [
        "1.07 W/kg (head)     1.11 W/kg (body)"
      ],
      "SAR EU": [
        "0.98 W/kg (head)     0.98 W/kg (body)"
      ],
      "Price": [
        "$ 935.95 / € 1,165.29 / £ 959.50 / ₹ 148,900"
      ]
    },
    "Tests": {
      "Performance": [
        "AnTuTu: 1487203 (v10)",
        "GeekBench: 7237 (v6.0)"
      ],
      "Display": [
        "Contrast ratio: Infinite (nominal)"
      ],
      "Camera": [
        "Photo / Video"
      ],
      "Loudspeaker": [
        "-24.5 LUFS (Very good)"
      ],
      "Battery (new)": [
        "Active use score 16:01h"
      ],
      "Battery (old)": [
        "Endurance rating 118h"
      ]
    }
  }
}
```

- calling `search("apple iPhone X")`
returns:
```JSON
{
  "message": "Your search returned 4 results.",
  "results": [
    {
      "name": "Apple iPhone XS Max",
      "path": "apple_iphone_xs_max-9319.php",
      "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-xs-max-new1.jpg"
    },
    {
      "name": "Apple iPhone XR",
      "path": "apple_iphone_xr-9320.php",
      "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-xr-new.jpg"
    },
    {
      "name": "Apple iPhone X",
      "path": "apple_iphone_x-8858.php",
      "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-x.jpg"
    },
    {
      "name": "Apple iPhone XS",
      "path": "apple_iphone_xs-9318.php",
      "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-xs-new.jpg"
    }
  ]
}
```

- calling `daily_deals()`
returns:
```JSON
{
  "message": "We constantly monitor phone prices and these are some of the best discounts we've spotted. The listed discounts are estimated based on the average price in the last 30 days (or less for new listings). We can't guarantee prices or availability - please check with the seller for more details. We may earn a commission from the links below.",
  "deals": [
    {
      "name": "Motorola Edge 30 Pro",
      "path": "motorola_edge_30_pro-11320.php",
      "image_link": "https://m.media-amazon.com/images/I/31DFe7DU0oL._SL500_.jpg",
      "device_info": "Motorola Edge 30 Pro 256 GB mobiele telefoon, donkerblauw, Cosmos Blue, Dual SIM, Android 12",
      "storage_and_ram": "256GB 12GB RAM",
      "deal": {
        "store_url": "https://www.amazon.nl/dp/B09TWPRC9Y?tag=gsmarena0b7-21&linkCode=osi&th=1&psc=1",
        "price": "356.36",
        "currency": "€",
        "discount_percentage": "8.0",
        "previous_price": "395.95",
        "min_price": "395.95",
        "max_price": "1,199.00",
        "30_days_average": "452.80"
      }
    },
    .
    .
    .
  ]
}
```

## Contribution
This might be a mini project. but it can be better with your help. Everyone are welcome to contribute.