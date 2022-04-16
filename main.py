import pyfiglet
from concurrent.futures import ThreadPoolExecutor
import time
import sqlite3
import parser
import prog_config

db_conn = sqlite3.connect("gdp.sqlite")
data_queue = []


def startup():
    f = pyfiglet.Figlet(font="isometric2")
    print(f.renderText(prog_config.project_name))


def equal_split(aList, partSize):
    return [aList[partSize * n:partSize * (n + 1)] for n in
            range(0, int(len(aList) / partSize) + (1 if len(aList) % partSize else 0))]


def read_data_txt(filename: str):
    f = open(filename, "r", encoding="utf-8")
    txt = f.read()
    f.close()
    result = []
    for i in txt.split("\n"):
        tmp = i.split("  ")
        result.append([tmp[0], parser.convert_date(tmp[2])])

    return result


def parser_thread(data, proxy, thread_id):
    for f in data:
        data = parser.get_info(int(f[0]), f[1], proxy=proxy, thread_id=thread_id)
        if "nameop" not in data['doc']:
            data["doc"]["nameop"] = "1337"
        if "codeop" not in data['doc']:
            data["doc"]["codeop"] = "1337"
        print("got info")
        data_queue.append(data)
        print("gaysex")
        time.sleep(2)


def main():
    proxies = [
        "socks5://Selxoxby:W3y6KaD@94.45.191.98:45786",
        "socks5://Selxoxby:W3y6KaD@93.88.79.66:45786",
        "socks5://Selxoxby:W3y6KaD@92.62.115.144:45786",
        "socks5://Selxoxby:W3y6KaD@85.202.87.115:45786",
        "socks5://Selxoxby:W3y6KaD@91.90.214.251:45786"
    ]
    queue = equal_split(read_data_txt("data.txt"), 3)
    t = time.time()
    with ThreadPoolExecutor() as executor:
        for i in queue:
            queue_index = queue.index(i)
            executor.submit(parser_thread, i, proxies[queue_index], queue_index)
    print(data_queue)
    for data in data_queue:
        request = f"INSERT INTO data (num,date,bdate,cat,srok,nameop,codeop,doc_status) VALUES ({data['doc']['num']}, {data['doc']['date']}, {data['doc']['bdate']}, '{data['doc']['cat']}', {data['doc']['srok']}, {data['doc']['nameop']}, {data['doc']['codeop']}, {data['doc']['type']})"
        print(request)
        db_conn.execute(request)
    db_conn.commit()
    print("Finished in " + str(time.time() - t))


if __name__ == "__main__":
    startup()
    main()
