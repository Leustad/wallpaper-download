import os
import re
import requests
import json
import urllib.request
import logging
import logging.config

BING_URL = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
BASE_URL = 'http://www.bing.com'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DESTINATION_PATH = 'C:/wallpapers'


def setup_logging(default_path=os.path.join(ROOT_DIR, 'logging.json'), default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()

try:
    img_data = json.loads(requests.get(BING_URL).text)
    img_url = str(BASE_URL) + img_data['images'][0]['url']

    # high quality image
    img_dl_url = 'http://www.bing.com/hpwp/' + img_data['images'][0]['hsh']
    img_name = img_url[re.search("rb/", img_url).end():re.search('_EN', img_url).start()] + '.jpg'

    file_path = os.path.join(DESTINATION_PATH, img_name)  # <-- Change accordingly

    if os.path.exists(file_path) is False:
        try:
            # Download high Quality image
            urllib.request.urlretrieve(img_dl_url, filename=file_path)
            logging.info('Downloaded: ' + img_name + ' - High Quality')
        except urllib.error.HTTPError:
            # Download low quality image
            urllib.request.urlretrieve(img_url, filename=file_path)
            logging.info('Downloaded: ' + img_name + ' - Low Quality')
    else:
        logging.info('Image exists. Not Downloading')
except Exception as e:
    logging.error(e, exc_info=True)
