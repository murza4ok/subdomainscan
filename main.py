import requests
import socks
import socket
import time
import csv
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
print(requests.get("http://httpbin.org/ip").text)


# домен для поиска поддоменов
domain = "github.com"
# читать все поддомены
file = open("subdomains-100.txt")
# прочитать весь контент
content = file.read()
# разделить на новые строки
subdomains = content.splitlines()
# список обнаруженных поддоменов
discovered_subdomains = []
undiscovered_subdomains = []

for subdomain in subdomains:
    # создать URL
    url = f"https://{subdomain}.{domain}"
    try:
        # если возникает ОШИБКА, значит, субдомен не существует
        requests.get(url)
        start_time = time.time()
        Close = 3
    except requests.ConnectionError:
        # запомним незарезолв
        print("[+] Поддомен не обнаружен:", url)
        undiscovered_subdomains.append(url)

    else:
        print("[+] Обнаружен поддомен:", url)
        # добавляем обнаруженный поддомен в наш список
        discovered_subdomains.append(url)

    # сохраняем обнаруженные поддомены в файл
    with open("discovered_subdomains.txt", "w") as f:
        for subdomain in discovered_subdomains:
            print(subdomain, file=f)
    with open("undiscovered_subdomains.txt", "w") as f:
        for subdomain in undiscovered_subdomains:
            print(subdomain, file=f)




