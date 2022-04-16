import requests
import time
import json
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import prog_config


def convert_date(input_date: str):
    """
    convert date dd.mm.yy to yyyy-mm-dd
    :param input_date: dd.mm.yy
    :return: yyyy-mm-dd
    """
    temp = input_date.split(".")
    return f"20{temp[2]}-{temp[1]}-{temp[0]}"


def get_info(driver_number: int, start_date: str, proxy=None, thread_id=None):
    """
    get info about RF driver's license
    :param driver_number: series and number
    :param start_date: issue date in format yyyy-mm-dd
    :param proxy: None if you don't need it
    :param thread_id: Thread identification number
    :return: info in dict or err_PART_TEXT
    """
    retry_delay = 12  # in seconds
    params = {
        'num': driver_number,
        'date': start_date
    }
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    print(f"[+][{thread_id}] starting up...")
    while True:
        try:
            gibdd_request = requests.post(prog_config.parser_endpoint_url, params=params,
                                          proxies={"https": proxy} if proxy else None,
                                          headers=headers, timeout=160)
            print(f"-------thread {thread_id}--------")
            print(f"sent request. status_code:{gibdd_request.status_code}")
            print(f"content: {gibdd_request.text}")
            print("-------------------------")

            if gibdd_request.status_code == 200:
                print(f"[+][{thread_id}]Request was successful! Deserializing json...")
                try:
                    result = json.loads(gibdd_request.text)
                except Exception as ed:
                    print(f"[-][{thread_id}]Deserializing error! Error: {ed}")
                    result = f"err#deserialize#{ed}"
                break
            else:
                print(f"[-][{thread_id}]Request was unsuccessful by status code! Retrying in {retry_delay}")
                time.sleep(retry_delay)

        except Exception as er:
            print(f"[-][{thread_id}]Request was unsuccessful! Retrying in {retry_delay}")
            print(f"[-][{thread_id}]+{er}")
            time.sleep(retry_delay)

    return result
