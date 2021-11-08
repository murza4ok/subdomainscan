import requests
import socks
import socket
import numpy as np, numba, timeit
import csv
import argparse
import string

"""
#
parser = argparse.ArgumentParser('main.py',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
                                 epilog="Specify a custom insertion point with %% in the domain name, such as: main.py -d dev-%%.example.org")
target = parser.add_mutually_exclusive_group(required=True)  # Allow a user to specify a list of target domains
target.add_argument('-d', '--domain', help='Target domains (separated by commas)', dest='domain', required=True)
target.add_argument('-n', '--list', help='Target amount of the symbols in pswd', dest='domain_list', required=True)
args = parser.parse_args()
"""
"""
# вывод оригинального айпи
print(requests.get("http://httpbin.org/ip").text, "вывод оригинального айпи")

#  проверка изменения нашего айпи
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
print(requests.get("http://httpbin.org/ip").text,"вывод рабочего айпи")
"""
@numba.njit(cache = True)
def ncomb(s, k):
    a = np.zeros((len(s),), dtype = np.uint32)
    for i, ch in enumerate(s):
        a[i] = ord(ch)
    n = a.size
    cnt = n ** k
    c = np.empty((cnt, k), dtype = np.uint32)
    idx = np.zeros((k,), dtype = np.uint32)
    pos = 0
    while True:
        for i in range(k):
            c[pos, i] = a[idx[i]]
        pos += 1
        for i in range(k - 1, -1, -1):
            if idx[i] >= n - 1:
                idx[i] = 0
            else:
                idx[i] += 1
                break
        else:
            break
    assert pos == cnt
    return c


def comb(s, kmin, kmax):
    l = []
    for k in range(kmin, kmax + 1):
        r = ncomb(s, k).tobytes().decode('utf-32-le')
        l.extend([r[i : i + k] for i in range(0, len(r), k)])
        print(r, " ")
    return r


def test():
    ntests = 5
    ftest = lambda: comb('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 1, 6)
    cnt = len(ftest())


# домен для поиска поддоменов "github.com"
print(comb('abcdefg',1,4), " ")
domain = "github.com"
# читать все поддомены
file = open("subdomains-10000.txt")
# прочитать весь контент
content = file.read()
# разделить на новые строки
# subdomains = content.splitlines()
# список обнаруженных поддоменов
lenword = 7
discovered_subdomains = []
ip_discovered_subdomains = []
undiscovered_subdomains = []
csv.register_dialect('my_dialect', delimiter=',', lineterminator="\r")


for symbols in lenword:
    subdomain = comb('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',1,1 )
    url = f"https://{subdomain}.{domain}"
    try:
        # если возникает ОШИБКА, значит, субдомен не существует
       r = requests.get(url,timeout=5)

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
        if r.status_code  >= 400:
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
    """
    #with open("discovered_subdomains.txt", "w") as f:
        for subdomain in discovered_subdomains:
            print(subdomain, file=f)
    with open("undiscovered_subdomains.txt", "w") as f:
        for subdomain in undiscovered_subdomains:
            print(subdomain, file=f)
    """
    with open("discovered_subdomains.csv", "w") as file:
        file_writer = csv.writer(file, 'my_dialect')
        i = 0
        for subdomain in discovered_subdomains:
            i = i+1
            file_writer.writerow([i, subdomain])
    with open("undiscovered_subdomains.csv", "w") as file:
        file_writer = csv.writer(file, 'my_dialect')
        i = 0
        for subdomain in undiscovered_subdomains:
            i = i+1
            file_writer.writerow([i, subdomain])
