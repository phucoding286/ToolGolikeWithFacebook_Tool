from modules import *
from facebook import like
from golike import get_job, verify_job, drop_job
from simulation import simulator

sessions_manager_file = "sessions.json"
if not os.path.exists(sessions_manager_file):
    with open(sessions_manager_file, "w", encoding="utf-8") as file:
        json.dump({"data": {}}, file)


def add_new_session():
    global sessions_manager_file
    # nhập đường dẫn lưu trữ phiên trình duyệt chưa thông tin đã thiết lập
    path = input(system_color("[?] nhập đường dẫn đến phiên của bạn\n-> "))
    data = json.load(open(sessions_manager_file))
    # nhập tên phiên
    while True:
        session_name = input(system_color("[?] Nhập tên phiên của bạn\n-> "))
        if session_name in data['data']:
            print(error_color(f"[!] tên phiên {session_name} đã tồn tại vui lòng nhập tên phiên mới!"))
            continue
        else:
            break
    # mở trình duyệt và yêu cầu nhập thông tin thiết lập
    driver = driver_init(path + "\\" + session_name)
    facebook_login(driver)
    golike_login(driver)
    golike_job_setup(driver)
    # lưu lại tên phiên và phiên đã thiết lập
    data["data"][session_name] = path + "\\" + session_name
    json.dump(data, open(sessions_manager_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    # thông báo hoàn tất
    input(success_color("[#] Đã hoàn tất quy trình thêm phiên của bạn, nhấn enter để thoát\n->"))
    storage_cookies(driver, cookie_f_name=session_name)
    try:
        driver.quit()
    except:
        pass


def add_golike_auth(filename="auth.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào auth golike của bạn\n-> "))

        if len(inp) < 10:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập auth hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu auth golike thành công!"))
        waiting_ui(4, "4s...")
        break


def add_golike_t(filename="t.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào t golike của bạn\n-> "))

        if len(inp) < 4:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập t hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu t golike thành công!"))
        waiting_ui(4, "4s...")
        break


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


def __run(driver: webdriver.Chrome):
    try:
        # đi đến trang chủ facebook và thực hiện mô phỏng
        driver.get("https://www.facebook.com/")
        simulator(driver)
    except:
        pass

    # mở tab mới để làm nhiệm vụ
    driver.execute_script("window.open();")
    handles = driver.window_handles
    driver.switch_to.window(handles[1])

    rgj = get_job(driver) # nhận job
    # check job lỗi
    if "error" in rgj:
        return "job_err"
    link = rgj['success'] # lấy link job
    print(purple_color(f"[>] Mục tiêu: {link}"))
    handles = driver.window_handles
    driver.switch_to.window(handles[2])

    # đi đến bài viết và like
    rlk = like(driver, link)
    # trở về trang nhận job ban đầu
    driver.close()
    handles = driver.window_handles
    driver.switch_to.window(handles[1])

    if "error" in rlk:
        try: [drop_job(driver), print(success_color("[*] Đã bỏ job thành công"))]
        except: print(success_color("[!] Đã bỏ job thất bại"))
        return "like_err"
    else:
        print(success_color("[*] Like thành công"))
        rvj = verify_job(driver)
        if "error" in rvj:
            try: [drop_job(driver), print(success_color("[*] Đã bỏ job thành công"))]
            except: print(success_color("[!] Đã bỏ job thất bại"))
            return "verify_err"
        else:
            return "success"
    

def __main(hide_chrome, delay):
    data = json.load(open(sessions_manager_file))['data']
    for ss_name, ss_path in data.items():
        try:
            print(system_color(f"[>] Phiên đang chạy là: {ss_name}"))
            driver = driver_init(ss_path, hide_chrome)
            response = __run(driver)
            if response == "job_err":
                print(error_color("[!] Lỗi khi nhận job"))
            elif response == "like_err":
                print(error_color("[!] Lỗi khi like"))
            elif response == "verify_err":
                print(error_color("[!] Lỗi khi xác minh job"))
            elif response == "success":
                from golike import prices
                print(success_color("[*] Đã xác minh job thành công"))
                print(success_color(f"[$] Tổng tiền: {prices}đ"))
            else:
                print(error_color("[!!] Lỗi không xác định"))
            driver.quit()
            waiting_ui(delay, f"Đợi {delay}s để tiếp tục")
        except:
            try:
                driver.quit()
            except:
                pass
            waiting_ui(delay, f"[!!] Có lỗi không xác định hãy đợi {delay}s để tiếp tục")
            try:
                r = requests.get("https://www.google.com/")
            except:
                print(error_color("\n[!!] Không có mạng!"))
                input(system_color("[!!] Phát hiện không có mạng, chương trình tạm dừng, chờ can thiệp, enter để tiếp tục chạy\n-> "))

def main_program():
    delay = int(input(system_color("[?] Nhập delay: ")))
    hide_chrome = True if input(system_color("[?] Ẩn chrome y/n?: ")).lower().strip() == "y" else False
    print()
    while True:
        __main(hide_chrome, delay)


if __name__ == "__main__":
    while True:
        print(system_color(" ----------------------------------------------------"))
        print(system_color("| Tool Golike Facebook By PhuTech (Programing-Sama)  |"))
        print(system_color("|     Công cụ được xây dựng dựa trên UC - Sel        |"))
        print(system_color(" ----------------------------------------------------"))
        print(system_color("| # Các nguồn tài nguyên phụ thuộc                |"))
        print(system_color("|  $ undetected-chromedriver (python package)     |"))
        print(system_color("|  $ selenium (python package)                    |"))
        print(system_color(" -------------------------------------------------"))
        print(system_color("| ? Các lựa chọn theo index                       |"))
        print(system_color("| [0] Thêm golike authorization                   |"))
        print(system_color("| [1] Thêm golike t                               |"))
        print(system_color("| [2] Thêm phiên                                  |"))
        print(system_color("| [3] Chạy tool                                   |"))
        print(system_color(" -------------------------------------------------"))
        print()

        inp = int(input(system_color("[?] Nhập lựa chọn của bạn\n-> ")))
        print()

        if inp == 0:
            add_golike_auth()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 1:
            add_golike_t()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 2:
            add_new_session()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 3:
            main_program()