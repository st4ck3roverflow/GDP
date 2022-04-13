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
        print(parser.get_info(f[0], f[1], proxy))


def main():
    proxies = [
        "http://82.198.188.10:80",
        "http://185.221.161.85:80",
        "http://185.221.160.176:80",
        "http://185.174.138.19:80"
    ]
    threads_dict = []
    txt_data = read_data_txt("data.txt")
    queue = equal_split(txt_data, 3)
    t = time.time()

    for i in queue:
        x = threading.Thread(target=thread_func, args=(i, proxies[queue.index(i)],))
        threads_dict.append(x)
    for i in threads_dict:
        i.start()
    for i in threads_dict:
        i.join()
    print("Finished in "+str(time.time() - t))


if __name__ == "__main__":
    startup()
    main()

