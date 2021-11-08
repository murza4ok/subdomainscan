import requests
import socks
import socket
import time
import csv

# вывод оригинального айпи
print(requests.get("http://httpbin.org/ip").text, "вывод оригинального айпи")

#  проверка изменения нашего айпи
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
# вывод рабочего айпи
print(requests.get("http://httpbin.org/ip").text,"вывод рабочего айпи")


# домен для поиска поддоменов "github.com"
domain = "github.com"
# читать все поддомены
file = open("subdomains-100.txt")
# прочитать весь контент
content = file.read()
# разделить на новые строки
subdomains = content.splitlines()
# список обнаруженных поддоменов
discovered_subdomains = []
ip_discovered_subdomains = []
undiscovered_subdomains = []
csv.register_dialect('my_dialect', delimiter=',', lineterminator="\r")

for subdomain in subdomains:
    # создать URL
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
