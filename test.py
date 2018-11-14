import re
import requests
from PIL import Image
from io import BytesIO
import lxml
from bs4 import BeautifulSoup as bs
with open('./douba1.html', 'r', encoding='utf-8') as fp:
    page_text = fp.read()
    soup = bs(page_text, 'lxml')
    cap = soup.find('div', {'class':'item item-captcha'}).find('img')
    check_id = soup.find('div', {'class':'captcha_block'}).find('input', {'name':'captcha-id'})
    check_value = re.findall('value="(.*)"', str(check_id))[0]
    print(check_value)
    img_src = re.findall('src="(.*)"', str(cap))[0]
    response = requests.get(img_src)
    image = Image.open(BytesIO(response.content))
    image.show()
    check_code = input('请输入验证码').strip()
