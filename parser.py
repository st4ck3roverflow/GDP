import requests
import json
import prog_config


def convert_date(input_date: str):
    """
    convert date dd.mm.yy to yyyy-mm-dd
    :param input_date: dd.mm.yy
    :return: yyyy-mm-dd
    """
    temp = input_date.split(".")
    return f"20{temp[2]}-{temp[1]}-{temp[0]}"


def get_info(driver_number: str, start_date: str, proxy):
    """
    get info about RF driver's license
    :param proxy: 1
    :param driver_number: series and number
    :param start_date: issue date in format yyyy-mm-dd
    :return: info in dict
    """
    params = {
        'num': driver_number,
        'date': start_date
    }
    proxies = {
        proxy.split(":")[0]: proxy
    }
    print(proxies)
    req_answ_json = requests.post(prog_config.parser_endpoint_url, params=params, proxies=proxies)
    gaysex1 = req_answ_json.cookies
    print("gay party: "+req_answ_json.text)
    while True:
        if req_answ_json.status_code == "200":
            break
        else:
            req_answ_json = requests.post(prog_config.parser_endpoint_url, params=params, proxies=proxies, cookies=gaysex1)
    req_answ = json.loads(req_answ_json.text)

    return req_answ
