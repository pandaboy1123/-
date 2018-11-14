import random
import re
import requests
from PIL import Image
from io import BytesIO
import lxml
from bs4 import BeautifulSoup as bs
import json
import math
import sys
import time
with open('./total.json', 'r', encoding='utf-8') as f:
    json_list = json.loads(f.read())
    for i in json_list:
        print(i['url'])
