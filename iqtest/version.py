__version__ = "0.2.5.1"

import os
import json
import time
from datetime import datetime, timedelta
import requests
from pkg_resources import parse_version

version_log = {
    "0.2.4.5": "fix pack tar file is None exception",
    "0.2.5": "remove default multiprocess supporting, simplify sdk",
    "0.2.5.1": "add gpu support, update example run model"
}


def version_report():
    split_symbol = '*' * 60
    banner = "Official SDK for IQTest"
    version = "sdk version %s" % __version__
    print(split_symbol)
    print('*%s*' % banner.center(58, ' '))
    print('*%s*' % version.center(58, ' '))
    print(split_symbol)


def version_update_info(msg):
    split_symbol = '*' * 80
    print(split_symbol)
    print('*%s*' % msg.center(78, ' '))
    print(split_symbol)
    time.sleep(1)


CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".iqtest")
# {last_update, data_version, sdk_version}
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")


URL = "https://api.iqtest.pub:8003/api/quiz/sdk_version"
DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"

LOCAL_DATA_VERSION_TMP = None
LOCAL_DATA_VERSION_KEY = "local_data_version"
SDK_VERSION_KEY = "sdk"
DATA_VERSION_KEY = "datas"


def load_config():
    if not os.path.exists(CONFIG_DIR) or not os.path.exists(CONFIG_FILE):
        return 1, None

    with open(CONFIG_FILE, "r", encoding='utf-8') as fh:
        config_data = json.load(fh)
    last_update = config_data.get('last_update')

    if not last_update or datetime.now() - datetime.strptime(last_update, DATE_FORMAT) > timedelta(days=1):
        return 1,  config_data

    return 0, config_data


def update_config(config_info, absorb_origin=True):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if absorb_origin and os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding='utf-8') as fh:
            origin_info = json.load(fh)
        origin_info.update(config_info)
        config_info = origin_info

    with open(CONFIG_FILE, "w", encoding='utf-8') as fh:
        json.dump(config_info, fh, indent=2, ensure_ascii=False)


def get_sdk_info():
    sdk_info = dict()
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            sdk_info.update(response.json())
            sdk_info['last_update'] = datetime.now().strftime(DATE_FORMAT)
    except:
        pass
    return sdk_info


def version_update():
    status, config_data = load_config()
    if status == 0:
        # no need to update
        return config_data

    if not config_data:
        config_data = dict()
    # need update user/password
    print('updating information from remote')

    new_config_data = get_sdk_info()
    if not new_config_data:
        print("retrieve information failed")
        return config_data

    config_data.update(new_config_data)
    update_config(config_data, False)
    return config_data


def version_check():
    global LOCAL_DATA_VERSION_TMP
    config_data = version_update()

    data_version = config_data.get(DATA_VERSION_KEY)
    sdk_version = config_data.get(SDK_VERSION_KEY)
    LOCAL_DATA_VERSION_TMP = config_data.get(LOCAL_DATA_VERSION_KEY)

    sdk_version_update = sdk_version and parse_version(sdk_version) > parse_version(__version__)
    # compare last used data version with remote data version
    data_version_update = LOCAL_DATA_VERSION_TMP and data_version and parse_version(
        data_version) > parse_version(LOCAL_DATA_VERSION_TMP)
    if sdk_version_update:
        version_update_info("new sdk %s updated, please update from website" % sdk_version)
    if data_version_update:
        print("new date %s updated, please update from website" % data_version)


def update_local_data_version(data_version):
    if LOCAL_DATA_VERSION_TMP != data_version:
        update_config({LOCAL_DATA_VERSION_KEY: data_version})
