import pyfiglet
import threading
import time
import parser
import prog_config


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


def thread_func(i, proxy):
    for f in i:
        print(parser.get_info_test(f[0], f[1]))


def main():
    proxies = [
        "https://217.174.106.15:8118",
        "https://188.170.233.107:3128",
        "https://91.224.62.194:8080",
        "https://188.170.233.108:3128",
        "https://188.170.233.111:3128"
    ]
    threads_dict = []
    queue = equal_split(read_data_txt("data.txt"), 3)

    t = time.time()
    for i in queue:
        x = threading.Thread(target=thread_func, args=(i, proxies[queue.index(i)],))
        threads_dict.append(x)
    for i in threads_dict:
        i.start()
    for i in threads_dict:
        i.join()
    print("Finished in "+str(time.time() - t))


def test():
    num = 9913926549
    issue_date = "2019-12-27"
    for i in range(5):
        parser.get_info_test(str(num), issue_date, "socks5://195.2.71.201:16072")
        num += 1


if __name__ == "__main__":
    startup()
    test()

