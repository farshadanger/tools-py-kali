import os
import sys
import socket
import requests
import json
import time
import re
import ipaddress
from urllib.parse import urlparse
from datetime import datetime
import threading
import queue
import subprocess
import dns.resolver
import whois
import ssl
import argparse
from bs4 import BeautifulSoup

# رنگ‌های ترمینال
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ابزار نمایش منو
class Menu:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def header(title):
        print(f"{Colors.CYAN}{'='*60}")
        print(f"{Colors.BOLD}{title.center(60)}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    @staticmethod
    def option(number, text):
        print(f"{Colors.YELLOW}[{number}]{Colors.END} {text}")
    
    @staticmethod
    def separator():
        print(f"{Colors.BLUE}{'-'*60}{Colors.END}")
    
    @staticmethod
    def success(msg):
        print(f"{Colors.GREEN}[✓]{Colors.END} {msg}")
    
    @staticmethod
    def error(msg):
        print(f"{Colors.RED}[✗]{Colors.END} {msg}")
    
    @staticmethod
    def warning(msg):
        print(f"{Colors.YELLOW}[!]{Colors.END} {msg}")
    
    @staticmethod
    def info(msg):
        print(f"{Colors.CYAN}[i]{Colors.END} {msg}")

# کلاس اصلی PenTest Toolkit
class TerminalPenTest:
    def __init__(self):
        self.target = ""
        self.results = {}
        self.history = []
        
    def main_menu(self):
        """منوی اصلی"""
        while True:
            Menu.clear_screen()
            Menu.header("🔐 PENETRATION TESTING TOOLKIT")
            
            print(f"{Colors.WHITE}هدف فعلی: {Colors.CYAN}{self.target if self.target else 'تعیین نشده'}{Colors.END}")
            print()
            
            Menu.option("1", "🎯 تعیین هدف جدید")
            Menu.option("2", "🌐 دریافت اطلاعات IP/دامنه")
            Menu.option("3", "🔍 اسکن پورت")
            Menu.option("4", "📋 اطلاعات WHOIS")
            Menu.option("5", "🔒 آنالیز SSL/TLS")
            Menu.option("6", "🌐 آنالیز وب سایت")
            Menu.option("7", "📊 تحلیل DNS")
            Menu.option("8", "🎭 تشخیص فیشینگ")
            Menu.option("9", "📡 تست شبکه (Ping/Traceroute)")
            Menu.option("10", "📝 مشاهده تاریخچه")
            Menu.option("11", "💾 ذخیره گزارش")
            Menu.option("12", "🗑️ پاک کردن نتایج")
            Menu.option("0", "🚪 خروج")
            
            Menu.separator()
            
            try:
                choice = input(f"{Colors.GREEN}➜ انتخاب شما [0-12]: {Colors.END}")
                
                if choice == "0":
                    print(f"\n{Colors.YELLOW}خدانگهدار! 👋{Colors.END}")
                    sys.exit(0)
                elif choice == "1":
                    self.set_target()
                elif choice == "2":
                    self.ip_info()
                elif choice == "3":
                    self.port_scan()
                elif choice == "4":
                    self.whois_lookup()
                elif choice == "5":
                    self.ssl_analyze()
                elif choice == "6":
                    self.website_analyze()
                elif choice == "7":
                    self.dns_analyze()
                elif choice == "8":
                    self.phishing_check()
                elif choice == "9":
                    self.network_test()
                elif choice == "10":
                    self.show_history()
                elif choice == "11":
                    self.save_report()
                elif choice == "12":
                    self.clear_results()
                else:
                    Menu.error("گزینه نامعتبر!")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}خروج از برنامه...{Colors.END}")
                sys.exit(0)
    
    def set_target(self):
        """تعیین هدف جدید"""
        Menu.clear_screen()
        Menu.header("🎯 تعیین هدف جدید")
        
        target = input(f"{Colors.CYAN}آدرس IP یا دامنه را وارد کنید: {Colors.END}").strip()
        
        if target:
            self.target = target
            self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - هدف تعیین شد: {target}")
            Menu.success(f"هدف '{target}' تعیین شد.")
        else:
            Menu.error("آدرس وارد نشد!")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def ip_info(self):
        """دریافت اطلاعات IP"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"🌐 اطلاعات IP/دامنه: {self.target}")
        
        try:
            # تشخیص IP یا دامنه
            try:
                ipaddress.ip_address(self.target)
                ip = self.target
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "نامشخص"
            except:
                hostname = self.target
                ip = socket.gethostbyname(self.target)
            
            print(f"{Colors.WHITE}📡 آدرس IP: {Colors.GREEN}{ip}{Colors.END}")
            print(f"{Colors.WHITE}🏷️  نام هاست: {Colors.CYAN}{hostname}{Colors.END}")
            
            # دریافت اطلاعات جغرافیایی
            Menu.info("دریافت اطلاعات جغرافیایی...")
            
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('status') == 'success':
                        print(f"\n{Colors.BOLD}📍 اطلاعات جغرافیایی:{Colors.END}")
                        print(f"  └ کشور: {data.get('country', 'نامشخص')}")
                        print(f"  └ شهر: {data.get('city', 'نامشخص')}")
                        print(f"  └ منطقه: {data.get('regionName', 'نامشخص')}")
                        print(f"  └ ISP: {data.get('isp', 'نامشخص')}")
                        print(f"  └ سازمان: {data.get('org', 'نامشخص')}")
                        print(f"  └ AS: {data.get('as', 'نامشخص')}")
                        print(f"  └ مختصات: {data.get('lat', '')}, {data.get('lon', '')}")
                        print(f"  └ منطقه زمانی: {data.get('timezone', 'نامشخص')}")
            except Exception as e:
                Menu.warning(f"خطا در دریافت اطلاعات جغرافیایی: {str(e)}")
            
            # ذخیره نتایج
            self.results['ip_info'] = {
                'target': self.target,
                'ip_address': ip,
                'hostname': hostname,
                'timestamp': datetime.now().isoformat()
            }
            
            self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - اطلاعات IP دریافت شد برای {self.target}")
            Menu.success("عملیات با موفقیت انجام شد!")
            
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def port_scan(self):
        """اسکن پورت"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"🔍 اسکن پورت: {self.target}")
        
        # تشخیص IP
        try:
            try:
                ipaddress.ip_address(self.target)
                ip = self.target
            except:
                ip = socket.gethostbyname(self.target)
        except:
            Menu.error("نامعتبر!")
            input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
            return
        
        print(f"{Colors.WHITE}🎯 IP هدف: {Colors.GREEN}{ip}{Colors.END}")
        
        # انتخاب پورت‌ها
        print(f"\n{Colors.CYAN}نوع اسکن:{Colors.END}")
        print("  1. اسکن سریع (پورت‌های رایج)")
        print("  2. اسکن کامل (1-1000)")
        print("  3. اسکن سفارشی")
        
        try:
            scan_type = input(f"{Colors.GREEN}➜ انتخاب [1-3]: {Colors.END}")
            
            if scan_type == "1":
                ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 
                        587, 993, 995, 3306, 3389, 5432, 8080, 8443]
                scan_name = "سریع"
            elif scan_type == "2":
                ports = range(1, 1001)
                scan_name = "کامل"
            elif scan_type == "3":
                custom = input(f"{Colors.CYAN}پورت‌ها را با کاما جدا کنید (مثال: 80,443,8080): {Colors.END}")
                ports = [int(p.strip()) for p in custom.split(',')]
                scan_name = "سفارشی"
            else:
                Menu.error("انتخاب نامعتبر!")
                return
        except:
            Menu.error("ورودی نامعتبر!")
            return
        
        # شروع اسکن
        open_ports = []
        print(f"\n{Colors.YELLOW}[!] شروع اسکن {scan_name}...{Colors.END}")
        print(f"{Colors.BLUE}{'-'*40}{Colors.END}")
        
        total_ports = len(ports) if isinstance(ports, list) else 1000
        
        for i, port in enumerate(ports):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                
                if result == 0:
                    service = self.get_service_name(port)
                    open_ports.append({'port': port, 'service': service})
                    print(f"{Colors.GREEN}[+] پورت {port} باز ({service}){Colors.END}")
                else:
                    print(f"{Colors.WHITE}[-] پورت {port} بسته{Colors.END}", end='\r')
                
                sock.close()
                
                # نمایش پیشرفت
                progress = ((i + 1) / total_ports) * 100
                sys.stdout.write(f"\r{Colors.CYAN}پیشرفت: {progress:.1f}%{Colors.END}")
                sys.stdout.flush()
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] اسکن متوقف شد{Colors.END}")
                break
            except:
                pass
        
        print(f"\n{Colors.BLUE}{'-'*40}{Colors.END}")
        
        # نمایش نتایج
        if open_ports:
            print(f"\n{Colors.GREEN}✅ {len(open_ports)} پورت باز یافت شد:{Colors.END}")
            for p in open_ports:
                print(f"  └ پورت {p['port']}: {p['service']}")
        else:
            print(f"\n{Colors.YELLOW}⚠️ هیچ پورت بازی یافت نشد{Colors.END}")
        
        # ذخیره نتایج
        self.results['port_scan'] = {
            'target': self.target,
            'ip': ip,
            'scan_type': scan_name,
            'open_ports': open_ports,
            'total_scanned': total_ports,
            'timestamp': datetime.now().isoformat()
        }
        
        self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - اسکن پورت انجام شد برای {self.target}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def get_service_name(self, port):
        """نام سرویس بر اساس پورت"""
        services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            465: "SMTPS",
            587: "SMTP",
            993: "IMAPS",
            995: "POP3S",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP Proxy",
            8443: "HTTPS Alt"
        }
        return services.get(port, "Unknown")
    
    def whois_lookup(self):
        """جستجوی WHOIS"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"📋 اطلاعات WHOIS: {self.target}")
        
        try:
            # تمیز کردن دامنه
            domain = self.target
            if domain.startswith(('http://', 'https://')):
                domain = urlparse(domain).netloc
            
            Menu.info(f"دریافت اطلاعات WHOIS برای {domain}...")
            
            w = whois.whois(domain)
            
            print(f"{Colors.BOLD}📌 اطلاعات ثبت:{Colors.END}")
            if w.registrar:
                print(f"  └ ثبت‌کننده: {w.registrar}")
            
            if w.creation_date:
                dates = w.creation_date
                if isinstance(dates, list):
                    dates = dates[0]
                print(f"  └ تاریخ ثبت: {dates}")
            
            if w.expiration_date:
                dates = w.expiration_date
                if isinstance(dates, list):
                    dates = dates[0]
                print(f"  └ تاریخ انقضا: {dates}")
            
            if w.updated_date:
                dates = w.updated_date
                if isinstance(dates, list):
                    dates = dates[0]
                print(f"  └ آخرین به‌روزرسانی: {dates}")
            
            print(f"\n{Colors.BOLD}🌍 اطلاعات مالک:{Colors.END}")
            if w.org:
                print(f"  └ سازمان: {w.org}")
            if w.country:
                print(f"  └ کشور: {w.country}")
            
            print(f"\n{Colors.BOLD}🌐 سرورهای نام:{Colors.END}")
            if w.name_servers:
                for ns in w.name_servers[:5]:  # فقط 5 تا اول
                    print(f"  └ {ns}")
            
            print(f"\n{Colors.BOLD}📧 ایمیل‌ها:{Colors.END}")
            if w.emails:
                emails = w.emails if isinstance(w.emails, list) else [w.emails]
                for email in emails[:3]:  # فقط 3 تا اول
                    print(f"  └ {email}")
            
            # ذخیره نتایج
            self.results['whois'] = {
                'domain': domain,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'updated_date': str(w.updated_date),
                'name_servers': w.name_servers,
                'emails': w.emails,
                'org': w.org,
                'country': w.country,
                'timestamp': datetime.now().isoformat()
            }
            
            self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - WHOIS دریافت شد برای {domain}")
            Menu.success("عملیات با موفقیت انجام شد!")
            
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def ssl_analyze(self):
        """آنالیز SSL/TLS"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"🔒 آنالیز SSL/TLS: {self.target}")
        
        try:
            # تمیز کردن آدرس
            hostname = self.target
            if hostname.startswith(('http://', 'https://')):
                hostname = urlparse(hostname).netloc
            
            port = 443
            
            Menu.info(f"بررسی SSL برای {hostname}:{port}...")
            
            context = ssl.create_default_context()
            
            try:
                with socket.create_connection((hostname, port), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        
                        print(f"{Colors.GREEN}✅ گواهی SSL معتبر است{Colors.END}")
                        
                        print(f"\n{Colors.BOLD}📜 اطلاعات گواهی:{Colors.END}")
                        
                        # Issuer
                        if 'issuer' in cert:
                            issuer = cert['issuer']
                            for item in issuer:
                                for key, value in item:
                                    if key == 'organizationName':
                                        print(f"  └ صادرکننده: {value}")
                        
                        # Subject
                        if 'subject' in cert:
                            subject = cert['subject']
                            for item in subject:
                                for key, value in item:
                                    if key == 'commonName':
                                        print(f"  └ نام مشترک: {value}")
                        
                        # تاریخ‌ها
                        print(f"  └ اعتبار از: {cert.get('notBefore', 'نامشخص')}")
                        print(f"  └ اعتبار تا: {cert.get('notAfter', 'نامشخص')}")
                        
                        # Cipher
                        cipher = ssock.cipher()
                        if cipher:
                            print(f"  └ رمزنگاری: {cipher[0]}")
                        
                        # محاسبه روزهای باقی‌مانده
                        if 'notAfter' in cert:
                            from datetime import datetime
                            expiry_str = cert['notAfter']
                            try:
                                expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
                                days_left = (expiry_date - datetime.now()).days
                                
                                if days_left > 30:
                                    color = Colors.GREEN
                                    status = "ایمن"
                                elif days_left > 0:
                                    color = Colors.YELLOW
                                    status = "هشدار"
                                else:
                                    color = Colors.RED
                                    status = "منقضی"
                                
                                print(f"  └ روزهای باقی‌مانده: {color}{days_left} ({status}){Colors.END}")
                            except:
                                pass
                
                # ذخیره نتایج
                self.results['ssl'] = {
                    'hostname': hostname,
                    'has_ssl': True,
                    'issuer': str(cert.get('issuer', '')),
                    'subject': str(cert.get('subject', '')),
                    'not_before': cert.get('notBefore', ''),
                    'not_after': cert.get('notAfter', ''),
                    'cipher': cipher[0] if cipher else '',
                    'timestamp': datetime.now().isoformat()
                }
                
                self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - SSL آنالیز شد برای {hostname}")
                Menu.success("عملیات با موفقیت انجام شد!")
                
            except ssl.SSLError:
                Menu.error("SSL معتبر نیست یا وجود ندارد!")
                self.results['ssl'] = {
                    'hostname': hostname,
                    'has_ssl': False,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def website_analyze(self):
        """آنالیز وب سایت"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"🌐 آنالیز وب سایت: {self.target}")
        
        try:
            url = self.target
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            Menu.info(f"در حال بارگذاری {url}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (PenTest Toolkit)'
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            print(f"{Colors.GREEN}✅ وب سایت قابل دسترس است{Colors.END}")
            print(f"{Colors.WHITE}📊 کد وضعیت: {Colors.CYAN}{response.status_code}{Colors.END}")
            print(f"{Colors.WHITE}📦 حجم داده: {Colors.CYAN}{len(response.content)} بایت{Colors.END}")
            
            # تحلیل HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print(f"\n{Colors.BOLD}🏷️  اطلاعات صفحه:{Colors.END}")
            
            # عنوان
            title = soup.title.string if soup.title else "بدون عنوان"
            print(f"  └ عنوان: {title[:50]}" + ("..." if len(title) > 50 else ""))
            
            # متا تگ‌ها
            meta_tags = soup.find_all('meta')
            print(f"  └ تعداد متا تگ: {len(meta_tags)}")
            
            # لینک‌ها
            links = soup.find_all('a')
            print(f"  └ تعداد لینک: {len(links)}")
            
            # فرم‌ها
            forms = soup.find_all('form')
            print(f"  └ تعداد فرم: {len(forms)}")
            
            # اسکریپت‌ها
            scripts = soup.find_all('script')
            print(f"  └ تعداد اسکریپت: {len(scripts)}")
            
            # تشخیص تکنولوژی
            print(f"\n{Colors.BOLD}🔧 تشخیص تکنولوژی:{Colors.END}")
            
            tech_detected = []
            content = response.text.lower()
            
            # سرور
            server = response.headers.get('Server', 'نامشخص')
            print(f"  └ سرور: {server}")
            
            # فریمورک‌ها
            if 'wp-content' in content or 'wordpress' in content:
                tech_detected.append('WordPress')
            if 'joomla' in content:
                tech_detected.append('Joomla')
            if 'drupal' in content:
                tech_detected.append('Drupal')
            if 'laravel' in content:
                tech_detected.append('Laravel')
            if 'jquery' in content:
                tech_detected.append('jQuery')
            if 'bootstrap' in content:
                tech_detected.append('Bootstrap')
            
            if tech_detected:
                print(f"  └ فریمورک: {', '.join(tech_detected)}")
            
            # هدرهای امنیتی
            print(f"\n{Colors.BOLD}🛡️  هدرهای امنیتی:{Colors.END}")
            
            security_headers = {
                'X-Frame-Options': response.headers.get('X-Frame-Options'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
                'X-XSS-Protection': response.headers.get('X-XSS-Protection'),
                'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security')
            }
            
            found = 0
            for header, value in security_headers.items():
                if value:
                    print(f"  └ {header}: {Colors.GREEN}✓{Colors.END}")
                    found += 1
                else:
                    print(f"  └ {header}: {Colors.RED}✗{Colors.END}")
            
            print(f"\n{Colors.WHITE}امتیاز امنیتی: {Colors.CYAN}{found}/5{Colors.END}")
            
            # ذخیره نتایج
            self.results['website'] = {
                'url': url,
                'status_code': response.status_code,
                'title': title,
                'server': server,
                'technologies': tech_detected,
                'security_headers': security_headers,
                'security_score': found,
                'timestamp': datetime.now().isoformat()
            }
            
            self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - وب سایت آنالیز شد: {url}")
            Menu.success("عملیات با موفقیت انجام شد!")
            
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def dns_analyze(self):
        """تحلیل DNS"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"📊 تحلیل DNS: {self.target}")
        
        try:
            domain = self.target
            if domain.startswith(('http://', 'https://')):
                domain = urlparse(domain).netloc
            
            Menu.info(f"دریافت رکوردهای DNS برای {domain}...")
            
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5
            
            print(f"{Colors.BOLD}🌐 رکوردهای DNS:{Colors.END}")
            
            # A Records
            try:
                answers = resolver.resolve(domain, 'A')
                print(f"\n  {Colors.GREEN}A Records:{Colors.END}")
                for rdata in answers:
                    print(f"    └ {rdata.to_text()}")
            except:
                print(f"\n  {Colors.RED}A Records: یافت نشد{Colors.END}")
            
            # AAAA Records (IPv6)
            try:
                answers = resolver.resolve(domain, 'AAAA')
                print(f"\n  {Colors.GREEN}AAAA Records:{Colors.END}")
                for rdata in answers:
                    print(f"    └ {rdata.to_text()}")
            except:
                print(f"\n  {Colors.YELLOW}AAAA Records: یافت نشد{Colors.END}")
            
            # MX Records
            try:
                answers = resolver.resolve(domain, 'MX')
                print(f"\n  {Colors.GREEN}MX Records:{Colors.END}")
                for rdata in answers:
                    print(f"    └ {rdata.preference} {rdata.exchange}")
            except:
                print(f"\n  {Colors.YELLOW}MX Records: یافت نشد{Colors.END}")
            
            # NS Records
            try:
                answers = resolver.resolve(domain, 'NS')
                print(f"\n  {Colors.GREEN}NS Records:{Colors.END}")
                for rdata in answers:
                    print(f"    └ {rdata.to_text()}")
            except:
                print(f"\n  {Colors.RED}NS Records: یافت نشد{Colors.END}")
            
            # TXT Records
            try:
                answers = resolver.resolve(domain, 'TXT')
                print(f"\n  {Colors.GREEN}TXT Records:{Colors.END}")
                for rdata in answers:
                    print(f"    └ {rdata.to_text()[:50]}..." if len(str(rdata)) > 50 else f"    └ {rdata.to_text()}")
            except:
                print(f"\n  {Colors.YELLOW}TXT Records: یافت نشد{Colors.END}")
            
            # بررسی امنیت DNS
            print(f"\n{Colors.BOLD}🛡️  امنیت DNS:{Colors.END}")
            
            # SPF
            try:
                answers = resolver.resolve(domain, 'TXT')
                has_spf = False
                for rdata in answers:
                    if 'v=spf1' in rdata.to_text():
                        has_spf = True
                        break
                
                if has_spf:
                    print(f"  {Colors.GREEN}SPF: فعال ✓{Colors.END}")
                else:
                    print(f"  {Colors.RED}SPF: غیرفعال ✗{Colors.END}")
            except:
                print(f"  {Colors.RED}SPF: بررسی ناموفق{Colors.END}")
            
            # DMARC
            try:
                answers = resolver.resolve(f'_dmarc.{domain}', 'TXT')
                has_dmarc = False
                for rdata in answers:
                    if 'v=DMARC1' in rdata.to_text():
                        has_dmarc = True
                        break
                
                if has_dmarc:
                    print(f"  {Colors.GREEN}DMARC: فعال ✓{Colors.END}")
                else:
                    print(f"  {Colors.RED}DMARC: غیرفعال ✗{Colors.END}")
            except:
                print(f"  {Colors.RED}DMARC: بررسی ناموفق{Colors.END}")
            
            # ذخیره نتایج
            self.results['dns'] = {
                'domain': domain,
                'timestamp': datetime.now().isoformat()
            }
            
            self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - DNS آنالیز شد برای {domain}")
            Menu.success("عملیات با موفقیت انجام شد!")
            
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def phishing_check(self):
        """تشخیص فیشینگ"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"🎭 تشخیص فیشینگ: {self.target}")
        
        url = self.target
        score = 0
        warnings = []
        
        print(f"{Colors.BOLD}🔍 آنالیز URL:{Colors.END}")
        print(f"  URL: {url}")
        
        # 1. بررسی طول URL
        if len(url) > 75:
            score += 1
            warnings.append("URL بسیار طولانی است")
            print(f"  {Colors.YELLOW}[!] طول URL: {len(url)} کاراکتر{Colors.END}")
        
        # 2. بررسی وجود @
        if '@' in url:
            score += 2
            warnings.append("کاراکتر @ در URL وجود دارد (مشکوک)")
            print(f"  {Colors.RED}[!] کاراکتر @ در URL{Colors.END}")
        
        # 3. بررسی IP مستقیم
        try:
            clean_url = url.replace('http://', '').replace('https://', '').split('/')[0]
            ipaddress.ip_address(clean_url)
            score += 2
            warnings.append("استفاده مستقیم از IP به جای دامنه")
            print(f"  {Colors.RED}[!] استفاده از IP مستقیم{Colors.END}")
        except:
            pass
        
        # 4. بررسی تعداد دات‌ها
        domain = url.replace('http://', '').replace('https://', '').split('/')[0]
        dot_count = domain.count('.')
        if dot_count > 3:
            score += 1
            warnings.append(f"تعداد دات‌ها زیاد است ({dot_count})")
            print(f"  {Colors.YELLOW}[!] تعداد دات‌ها: {dot_count}{Colors.END}")
        
        # 5. بررسی کوتاه‌کننده‌ها
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'shorturl', 'is.gd']
        for shortener in shorteners:
            if shortener in url:
                score += 1
                warnings.append(f"استفاده از سرویس کوتاه‌کننده: {shortener}")
                print(f"  {Colors.YELLOW}[!] کوتاه‌کننده URL: {shortener}{Colors.END}")
                break
        
        # 6. کلمات کلیدی فیشینگ
        phishing_keywords = ['login', 'signin', 'verify', 'account', 'secure', 'banking',
                           'update', 'confirm', 'password', 'credential', 'paypal']
        
        found_keywords = []
        for keyword in phishing_keywords:
            if keyword in url.lower():
                score += 1
                found_keywords.append(keyword)
        
        if found_keywords:
            warnings.append(f"کلمات کلیدی مشکوک: {', '.join(found_keywords)}")
            print(f"  {Colors.YELLOW}[!] کلمات کلیدی مشکوک: {', '.join(found_keywords)}{Colors.END}")
        
        # 7. بررسی HTTPS
        if url.startswith('http://') and not url.startswith('https://'):
            score += 1
            warnings.append("استفاده از HTTP به جای HTTPS")
            print(f"  {Colors.YELLOW}[!] استفاده از HTTP (ناامن){Colors.END}")
        
        # نمایش نتیجه
        print(f"\n{Colors.BOLD}📊 نتیجه تشخیص:{Colors.END}")
        print(f"  امتیاز خطر: {score}/10")
        
        if score >= 7:
            risk = "🚨 بسیار خطرناک"
            color = Colors.RED
        elif score >= 4:
            risk = "⚠️  خطرناک"
            color = Colors.YELLOW
        elif score >= 2:
            risk = "🔶 متوسط"
            color = Colors.CYAN
        else:
            risk = "✅ ایمن"
            color = Colors.GREEN
        
        print(f"  سطح خطر: {color}{risk}{Colors.END}")
        
        # نمایش هشدارها
        if warnings:
            print(f"\n{Colors.BOLD}🚨 هشدارها:{Colors.END}")
            for warning in warnings:
                print(f"  └ {warning}")
        
        # ذخیره نتایج
        self.results['phishing'] = {
            'url': url,
            'score': score,
            'risk_level': risk,
            'warnings': warnings,
            'timestamp': datetime.now().isoformat()
        }
        
        self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - فیشینگ بررسی شد: {url}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def network_test(self):
        """تست شبکه"""
        if not self.target:
            Menu.error("لطفاً ابتدا هدف را تعیین کنید!")
            time.sleep(1.5)
            return
        
        Menu.clear_screen()
        Menu.header(f"📡 تست شبکه: {self.target}")
        
        # تشخیص IP
        try:
            try:
                ipaddress.ip_address(self.target)
                ip = self.target
            except:
                ip = socket.gethostbyname(self.target)
        except:
            Menu.error("نامعتبر!")
            input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
            return
        
        print(f"{Colors.WHITE}🎯 IP هدف: {Colors.GREEN}{ip}{Colors.END}")
        
        print(f"\n{Colors.CYAN}نوع تست:{Colors.END}")
        print("  1. Ping ساده")
        print("  2. Ping پیشرفته")
        print("  3. Traceroute (اگر در دسترس)")
        
        try:
            test_type = input(f"{Colors.GREEN}➜ انتخاب [1-3]: {Colors.END}")
            
            if test_type == "1":
                self.simple_ping(ip)
            elif test_type == "2":
                self.advanced_ping(ip)
            elif test_type == "3":
                self.traceroute(ip)
            else:
                Menu.error("انتخاب نامعتبر!")
                return
        except:
            return
    
    def simple_ping(self, ip):
        """Ping ساده"""
        print(f"\n{Colors.YELLOW}[!] در حال Ping...{Colors.END}")
        
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            count = '4'
            
            result = subprocess.run(
                ['ping', param, count, ip],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            print(f"\n{Colors.GREEN}✅ نتیجه Ping:{Colors.END}")
            print(result.stdout)
            
            # تحلیل نتیجه
            if 'ttl=' in result.stdout.lower() or 'ttl' in result.stdout.lower():
                print(f"\n{Colors.GREEN}🎯 هدف قابل دسترس است{Colors.END}")
            else:
                print(f"\n{Colors.RED}🎯 هدف غیرقابل دسترس است{Colors.END}")
                
        except subprocess.TimeoutExpired:
            Menu.error("زمان Ping به پایان رسید")
        except Exception as e:
            Menu.error(f"خطا در Ping: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def advanced_ping(self, ip):
        """Ping پیشرفته"""
        print(f"\n{Colors.YELLOW}[!] در حال Ping پیشرفته...{Colors.END}")
        
        success_count = 0
        total_pings = 10
        
        for i in range(total_pings):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                start_time = time.time()
                result = sock.connect_ex((ip, 80))
                end_time = time.time()
                
                if result == 0:
                    latency = (end_time - start_time) * 1000
                    print(f"{Colors.GREEN}  پکت {i+1}: پاسخ در {latency:.2f}ms{Colors.END}")
                    success_count += 1
                else:
                    print(f"{Colors.RED}  پکت {i+1}: از دست رفته{Colors.END}")
                
                sock.close()
                time.sleep(0.5)
                
            except Exception as e:
                print(f"{Colors.RED}  پکت {i+1}: خطا - {str(e)}{Colors.END}")
        
        # نتیجه
        success_rate = (success_count / total_pings) * 100
        print(f"\n{Colors.BOLD}📊 نتیجه:{Colors.END}")
        print(f"  ارسال شده: {total_pings}")
        print(f"  دریافت شده: {success_count}")
        print(f"  درصد موفقیت: {success_rate:.1f}%")
        
        if success_rate >= 90:
            status = f"{Colors.GREEN}عالی{Colors.END}"
        elif success_rate >= 70:
            status = f"{Colors.YELLOW}متوسط{Colors.END}"
        else:
            status = f"{Colors.RED}ضعیف{Colors.END}"
        
        print(f"  وضعیت اتصال: {status}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def traceroute(self, ip):
        """Traceroute"""
        print(f"\n{Colors.YELLOW}[!] در حال Traceroute... (ممکن است زمان‌بر باشد){Colors.END}")
        
        try:
            if platform.system().lower() == 'windows':
                result = subprocess.run(['tracert', '-h', '15', ip], 
                                      capture_output=True, text=True, timeout=30)
            else:
                result = subprocess.run(['traceroute', '-m', '15', ip], 
                                      capture_output=True, text=True, timeout=30)
            
            print(f"\n{Colors.GREEN}✅ نتیجه Traceroute:{Colors.END}")
            print(result.stdout[:2000])  # محدود کردن خروجی
            
        except FileNotFoundError:
            Menu.error("دستور traceroute/tracert یافت نشد!")
        except subprocess.TimeoutExpired:
            Menu.error("زمان Traceroute به پایان رسید")
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def show_history(self):
        """نمایش تاریخچه"""
        Menu.clear_screen()
        Menu.header("📝 تاریخچه عملیات")
        
        if not self.history:
            print(f"{Colors.YELLOW}تاریخچه‌ای وجود ندارد.{Colors.END}")
        else:
            for i, entry in enumerate(reversed(self.history[-20:]), 1):
                print(f"{i:2}. {entry}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def save_report(self):
        """ذخیره گزارش"""
        Menu.clear_screen()
        Menu.header("💾 ذخیره گزارش")
        
        if not self.results:
            Menu.error("هیچ نتیجه‌ای برای ذخیره وجود ندارد!")
            time.sleep(1.5)
            return
        
        print(f"{Colors.CYAN}فرمت گزارش:{Colors.END}")
        print("  1. فایل متنی (.txt)")
        print("  2. فایل JSON (.json)")
        print("  3. فایل HTML (.html)")
        
        try:
            choice = input(f"{Colors.GREEN}➜ انتخاب [1-3]: {Colors.END}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pentest_report_{timestamp}"
            
            if choice == "1":
                filename += ".txt"
                self.save_text_report(filename)
            elif choice == "2":
                filename += ".json"
                self.save_json_report(filename)
            elif choice == "3":
                filename += ".html"
                self.save_html_report(filename)
            else:
                Menu.error("انتخاب نامعتبر!")
                return
                
        except Exception as e:
            Menu.error(f"خطا: {str(e)}")
        
        input(f"\n{Colors.YELLOW}برای ادامه Enter بزنید...{Colors.END}")
    
    def save_text_report(self, filename):
        """ذخیره گزارش متنی"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("🔐 PENETRATION TESTING REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"تاریخ تولید: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
                f.write(f"هدف: {self.target}\n\n")
                
                f.write("📝 تاریخچه:\n")
                f.write("-" * 40 + "\n")
                for entry in self.history:
                    f.write(f"{entry}\n")
                
                f.write("\n📊 نتایج:\n")
                f.write("-" * 40 + "\n")
                for key, value in self.results.items():
                    f.write(f"\n{key.upper()}:\n")
                    f.write(json.dumps(value, indent=2, ensure_ascii=False))
                    f.write("\n")
            
            Menu.success(f"گزارش در {filename} ذخیره شد.")
            
        except Exception as e:
            Menu.error(f"خطا در ذخیره‌سازی: {str(e)}")
    
    def save_json_report(self, filename):
        """ذخیره گزارش JSON"""
        try:
            report_data = {
                "metadata": {
                    "tool": "PenTest Toolkit Terminal",
                    "timestamp": datetime.now().isoformat(),
                    "target": self.target
                },
                "results": self.results,
                "history": self.history
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            Menu.success(f"گزارش JSON در {filename} ذخیره شد.")
            
        except Exception as e:
            Menu.error(f"خطا در ذخیره‌سازی: {str(e)}")
    
    def save_html_report(self, filename):
        """ذخیره گزارش HTML"""
        try:
            html = f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <title>گزارش PenTest</title>
    <style>
        body {{ font-family: Tahoma, Arial; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: auto; padding: 20px; }}
        .header {{ background: #007acc; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 5px; }}
        .success {{ color: green; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 گزارش Penetration Testing</h1>
            <p>تاریخ: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}</p>
            <p>هدف: {self.target}</p>
        </div>
"""
            
            for key, value in self.results.items():
                html += f"""
        <div class="section">
            <h2>{key}</h2>
            <pre>{json.dumps(value, indent=2, ensure_ascii=False)}</pre>
        </div>
"""
            
            html += """
    </div>
</body>
</html>
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            Menu.success(f"گزارش HTML در {filename} ذخیره شد.")
            
        except Exception as e:
            Menu.error(f"خطا در ذخیره‌سازی: {str(e)}")
    
    def clear_results(self):
        """پاک کردن نتایج"""
        Menu.clear_screen()
        Menu.header("🗑️ پاک کردن نتایج")
        
        print(f"{Colors.YELLOW}آیا از پاک کردن تمام نتایج و تاریخچه اطمینان دارید؟{Colors.END}")
        print(f"{Colors.RED}این عمل غیرقابل بازگشت است!{Colors.END}")
        
        confirm = input(f"{Colors.GREEN}تایید [y/N]: {Colors.END}").lower()
        
        if confirm == 'y' or confirm == 'yes':
            self.results = {}
            self.history = []
            Menu.success("تمامی نتایج پاک شدند.")
        else:
            Menu.info("عملیات لغو شد.")
        
        time.sleep(1)

# ============================================================================
# اجرای برنامه
# ============================================================================

def main():
    """تابع اصلی"""
    # بررسی وابستگی‌ها
    try:
        import requests
        import bs4
        import whois
        import dns.resolver
    except ImportError as e:
        print(f"{Colors.RED}خطا: کتابخانه مورد نیاز نصب نیست.{Colors.END}")
        print(f"{Colors.YELLOW}لطفاً نصب کنید:{Colors.END}")
        print("pip install requests beautifulsoup4 python-whois dnspython")
        sys.exit(1)
    
    # ایجاد نمونه برنامه
    app = TerminalPenTest()
    
    # اجرای منوی اصلی
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}برنامه خاتمه یافت.{Colors.END}")

if __name__ == "__main__":
    main()
