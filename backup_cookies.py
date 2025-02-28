from modules import *

def storage_cookies(driver, cookie_f_name="session_name.pkl"):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    driver.get("https://www.facebook.com")
    pickle.dump(driver.get_cookies(), open("facebook_cookie_" + cookie_f_name + ".pkl", "wb"))
    print(success_color("[#] Đã lưu cookie thành công."))

def load_cookies(driver, cookie_f_name="session_name"):
    if not os.path.exists("facebook_cookie_" + cookie_f_name + ".pkl"):
        print(error_color("[!] File cookie chưa tồn lại"))
        return 0
    driver.get("https://www.facebook.com")
    cookies = pickle.load(open("facebook_cookie_" + cookie_f_name + ".pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    print(success_color("[#] Đã load cookie thành công."))

if __name__ == "__main__":
    driver = driver_init(r"E:\MySRC\golike-tools\golike-facebook-selenium\acc1")
    load_cookies(driver, "acc1")
    input()