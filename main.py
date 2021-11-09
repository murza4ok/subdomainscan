import requests
import socks
import socket
import numpy as np, numba, timeit
import csv
import argparse
import string
import  itertools
# цсвшник
csv.register_dialect('my_dialect', delimiter=',', lineterminator="\r")


def perebor(subdomain):
    url = f"https://{subdomain}.{domain}"
    try:
        # если возникает ОШИБКА, значит, субдомен не существует
        r = requests.get(url, timeout=5)

    # слипы для того, чтобы не выключало нас, мб при торе не понадобится
    except requests.Timeout:
        # запомним незарезолв
        print("[+] Поддомен не обнаружен:", url)
        undiscovered_subdomains.append(url)

    except requests.ConnectionError:
        print("[+] Поддомен не обнаружен:", url)
        undiscovered_subdomains.append(url)

    except requests.URLRequired:
        print("[+] Поддомен не обнаружен:", url)
        undiscovered_subdomains.append(url)

    else:
        if r.status_code >= 400:
            print("[+] Поддомен не обнаружен:", url)
            undiscovered_subdomains.append(url)
        else:
            print("[+] Обнаружен поддомен:", url)
            try:
                print(socket.gethostbyname(url))
            except socket.gaierror:
                pass
            else:
                ip_discovered_subdomains.append(socket.gethostbyname(url))
            # добавляем обнаруженный поддомен в наш список
            discovered_subdomains.append(url)

    # сохраняем обнаруженные поддомены в файл
    
    with open("discovered_subdomains.txt", "w") as f:
        for subdomain in discovered_subdomains:
            print(subdomain, file=f)
    with open("undiscovered_subdomains.txt", "w") as f:
        for subdomain in undiscovered_subdomains:
            print(subdomain, file=f)
 
    with open("discovered_subdomains.csv", "w") as file:
        file_writer = csv.writer(file, 'my_dialect')
        i = 0
        for subdomain in discovered_subdomains:
            i = i + 1
            file_writer.writerow([i, subdomain])
    with open("undiscovered_subdomains.csv", "w") as file:
        file_writer = csv.writer(file, 'my_dialect')
        i = 0
        for subdomain in undiscovered_subdomains:
            i = i + 1
            file_writer.writerow([i, subdomain])


def Tor():
    # вывод оригинального айпи
    print(requests.get("http://httpbin.org/ip").text, "вывод оригинального айпи")

    #  проверка изменения нашего айпи
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
    socket.socket = socks.socksocket
    print(requests.get("http://httpbin.org/ip").text,"вывод рабочего айпи")


Tor()
parser = argparse.ArgumentParser('main.py',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
                                 epilog="Specify a custom insertion point with %% in the domain name, such as: main.py -d dev-%%.example.org")

parser.add_argument('-d', '--domain', help='Target domain', dest='domain', required=True)
parser.add_argument('-a', '--amount', help='Target amount of the symbols in subdomain', dest='amount', default=1,
                    required=False)
parser.add_argument('-m', '--mode', help='Choose mode (dict/enum) default is enum(print e or d after key)', dest='mode', default="e",
                    required=False)
parser.add_argument('-l', '--list', help='Choose list of the names', dest='list', default="subdomains-10000.txt",
                    required=False)
args = parser.parse_args()
# домен для поиска поддоменов "github.com"
domain = args.domain
print(domain)
# список обнаруженных поддоменов
discovered_subdomains = []
ip_discovered_subdomains = []
undiscovered_subdomains = []
symbols = ('abcdefghijklmnopqrstuvwxyz0123456789')
count = args.amount
count = int(count)
if args.mode == "e":
    for i in range(1, count+1):
        list_of_1_element_subdomain = itertools.product(symbols, repeat=i)
        for var in list_of_1_element_subdomain:
            list_subdomains = ["".join(var)]
            subdomains = list_subdomains[0]
            perebor(subdomains)
else:
    # читать все поддомены для словаря
    file = open(args.list)
    # прочитать весь файлик
    content = file.read()
    # разделить на новые строки
    subdomains = content.splitlines()
    for subdomain in subdomains:
        perebor(subdomain)