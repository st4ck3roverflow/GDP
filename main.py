import pyfiglet
import threading
import time
import parser
import prog_config


def startup():
    f = pyfiglet.Figlet(font="isometric2")
    print(f.renderText(prog_config.project_name))


def read_data_txt(filename: str):
    f = open(filename, "r", encoding="utf-8")
    txt = f.read()
    f.close()
    result = []
    for i in txt.split("\n"):
        tmp = i.split("  ")
        result.append([tmp[0], parser.convert_date(tmp[2])])

    return result


def thread_func(i):
    print(parser.get_info(i[0], i[1]))


def main():
    threads_dict = []
    queue = []
    t = time.time()
    txt_data = read_data_txt("data.txt")
    len(txt_data)/3
    for i in :
    #     x = threading.Thread(target=thread_func, args=(i,))
    #     threads_dict.append(x)
    # for i in threads_dict:
    #     i.start()
    # for i in threads_dict:
    #     i.join()
        print("faggot:", i)
        thread_func(i)
    print("Finished in "+str(time.time() - t))


if __name__ == "__main__":
    startup()
    main()

