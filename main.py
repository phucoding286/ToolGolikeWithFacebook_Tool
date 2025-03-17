from modules import *
from facebook import facebook_login, like
from golike import check_and_get_job, golike_login, verify_job, drop_job
from scroll_facebook import scroll_facebook, continue_scroll
from random_wait import rdn_wait, rdn_do
from backup_cookies import storage_cookies, load_cookies

# --------------------------------------------------------------------

sessions_manager_file = "sessions.json"
sessions_limit_times = "times_limit.json"
sessions_times_count = "times_count.json"
day_json_file = "day.json"
count_times = 0
max_limit_sum_error = 5
max_times_error_unknown = 4
error_unknown_counter = 0
sum_errors_count = {}

# ----------------------------------------------------------------------

if not os.path.exists(sessions_manager_file):
    with open(sessions_manager_file, "w", encoding="utf-8") as file:
        json.dump({"data": {}}, file)

if not os.path.exists(sessions_limit_times):
    with open(sessions_limit_times, "w", encoding="utf-8") as file:
        json.dump({}, file)

if not os.path.exists(sessions_times_count):
    with open(sessions_times_count, "w", encoding="utf-8") as file:
        json.dump({}, file)

hist_day = json.load(open(day_json_file))
if hist_day['day'] == 0:
    json.dump({"day": datetime.datetime.today().day}, open(day_json_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

# -----------------------------------------------------------------------------------------------------------------------------

def __main(driver, wait, session_name, max_times_for_interaction=10):
    global sum_errors_count
    interaction_count = 0
    while True:

        if interaction_count >= max_times_for_interaction:
            return "giới hạn số lần tương tác mỗi phiên"
        
        time.sleep(1)

        r = check_and_get_job(driver)
        if r == "giới hạn job":
            return "giới hạn job"
        
        time.sleep(1)
        lk_out = like(driver)
    
        if "error" in lk_out:
            print(error_color("[!] Like thất bại"))

            if "error" in drop_job(driver):
                print(wait_color(f"[!] Lỗi khi bỏ job {wait}s ... "))

                waiting_ui(wait, f"[#] Vui lòng đợi {wait}s")

                driver.execute_script("window.open();")
                time.sleep(1)
                driver.close()
                time.sleep(1)
                continue

            else:
                print(success_color("[#] Đã bỏ job."))

            print(error_color(f"[!] Lỗi khi like 2s ... "))
            waiting_ui(2, "Vui lòng đợi 2s")

            driver.execute_script("window.open();")
            time.sleep(1)
            driver.close()
            time.sleep(1)
            continue
    
        else:
            print(success_color("[$] Like thành công"))
            waiting_ui(5, f"[#] Vui lòng đợi 5s để xác minh job")

            if "error" in verify_job(driver):
                interaction_count += 1
                drop_job(driver)
                print(error_color(f"[!] Lỗi khi xác minh job {wait}s ... "))
                
                if session_name not in sum_errors_count:
                    sum_errors_count[session_name] = 1
                else:
                    sum_errors_count[session_name] += 1

                waiting_ui(wait, f"[#] Vui lòng đợi {wait}s")

                driver.execute_script("window.open();")
                time.sleep(1)
                driver.close()
                time.sleep(1)
                continue
            
            if session_name in sum_errors_count:
                sum_errors_count[session_name] = 1

            print(success_color(f"[$] Đã xác minh job {wait}s ... "))
            waiting_ui(wait, f"[#] Vui lòng đợi {wait}s")

            driver.execute_script("window.open();")
            time.sleep(1)
            driver.close()
            time.sleep(1)
            
            interaction_count += 1

# ------------------------------------------------------------------------------------

def __run(data, wait, max_times_for_interaction):
    global count_times
    global sum_errors_count
    global max_limit_sum_error
    session_limit_times = json.load(open(sessions_limit_times))
    hist_day = json.load(open(day_json_file))

    for session_name, user_data_path in data['data'].items():
        
        if session_name in sum_errors_count\
            and sum_errors_count[session_name] >= max_limit_sum_error\
            and datetime.datetime.today().day != hist_day['day']:
                sum_errors_count = {}

        elif session_name in sum_errors_count\
            and sum_errors_count[session_name] >= max_limit_sum_error:
                print(error_color(f"[!] Phiên '{session_name}' lỗi xác minh job quá nhiều trong ngày, bỏ qua."))
                continue

        ss_times_count = json.load(open(sessions_times_count))
        ss_times_count[session_name] = count_times
        json.dump(
            ss_times_count,
            open(sessions_times_count, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
        )

        if session_name in session_limit_times:
            if session_limit_times[session_name] <= ss_times_count[session_name]\
                and datetime.datetime.today().day == hist_day['day']:
                    print(error_color(f"[>] Phiên '{session_name}' đã đạt giới hạn quy định, đổi phiên..."))
                    continue
            else:
                if datetime.datetime.today().day != hist_day['day']:
                    count_times = 0
                    
                    json.dump(
                        {"day": datetime.datetime.today().day},
                        open(day_json_file, "w", encoding="utf-8"),
                        ensure_ascii=False,
                        indent=4
                    )
                
                    for ss_key, _ in ss_times_count.items():
                        ss_times_count[ss_key] = 0

                    json.dump(
                        ss_times_count,
                        open(sessions_times_count, "w", encoding="utf-8"),
                        ensure_ascii=False,
                        indent=4
                    )
        
        try:
            print(system_color(f"[#] Phiên đang chạy hiện tại là -> {session_name}"))
            driver = driver_init(user_data_path)
            load_cookies(driver, session_name)

            r = __main(driver, wait, session_name, max_times_for_interaction)
            error_unknown_counter = 0
            if r == "giới hạn số lần tương tác mỗi phiên":
                print(success_color("[#] Đã đến giới hạn tương tác, thực hiện đổi phiên..."))
                storage_cookies(driver, cookie_f_name=session_name)
                try:
                    window_handles = driver.window_handles
                    for i in range(len(window_handles)):
                        try:
                            driver.switch_to.window(window_handles[i])
                            driver.close()
                        except:
                            continue
                    driver.quit()
                except:
                    pass
                continue

            elif r == "giới hạn job":
                print(error_color("[!] Đã bị giới hạn job, thực hiện đổi phiên..."))
                storage_cookies(driver, cookie_f_name=session_name)
                try:
                    window_handles = driver.window_handles
                    for i in range(len(window_handles)):
                        try:
                            driver.switch_to.window(window_handles[i])
                            driver.close()
                        except:
                            continue
                    driver.quit()
                except:
                    pass
                continue

            else:
                storage_cookies(driver, cookie_f_name=session_name)
                try:
                    window_handles = driver.window_handles
                    for i in range(len(window_handles)):
                        try:
                            driver.switch_to.window(window_handles[i])
                            driver.close()
                        except:
                            continue
                    driver.quit()
                except:
                    pass
                continue

        except:
            print(error_color("[!] Lỗi không xác định, thử lại..."))
            error_unknown_counter += 1
            if error_unknown_counter >= max_times_error_unknown:
                input(error_color("[!] Lỗi không xác định nhiều lần, tạm dừng chương trình, enter để tiếp tục\n-> "))
                error_unknown_counter = 0
            try:
                driver.quit()
            except:
                pass
            continue

# ---------------------------------------------------------------------------------------

def add_session_limit_times():
    data = json.load(open(sessions_limit_times))
    s = json.load(open(sessions_manager_file))

    while True:
        session_name = input(system_color("[?] Nhập tên phiên của bạn\n-> "))
        if session_name not in s['data']:
            print(error_color(f"[!] Tên phiên '{session_name}' chưa tồn tại."))
        else:
            break

    times_limit = input(system_color("[?] Nhập số lần giới hạn cho phiên\n-> "))
    data[session_name] = int(times_limit)
    json.dump(data, open(sessions_limit_times, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    input(success_color("[#] Đã hoàn tất quy trình thêm giới hạn cho phiên, nhấn enter để thoát\n->"))

# ----------------------------------------------------------------------------------------------------
    
def add_new_session():
    global sessions_manager_file
    path = input(system_color("[?] nhập đường dẫn đến phiên của bạn\n-> "))
    data = json.load(open(sessions_manager_file))

    while True:
        session_name = input(system_color("[?] Nhập tên phiên của bạn\n-> "))
        if session_name in data['data']:
            print(error_color(f"[!] Tên phiên {session_name} đã tồn tại vui lòng nhập tên session mới!"))
            continue
        else:
            break

    driver = driver_init(path + "\\" + session_name)

    facebook_login(driver)
    golike_login(driver)
    
    data["data"][session_name] = path + "\\" + session_name
    json.dump(data, open(sessions_manager_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

    input(success_color("[#] Đã hoàn tất quy trình thêm phiên của bạn, nhấn enter để thoát\n->"))

    try:
        driver.quit()
    except:
        pass


if __name__ == "__main__":
    while True:
        print(error_color(" -----------------------------------------------------"))
        print(error_color("| Tool Golike facebook By PhuTech (Programing sama)   |"))
        print(error_color("| Mục tiêu -> Kiếm tiền thông qua tự động hóa         |"))
        print(error_color(" -----------------------------------------------------"))
        print(error_color("| Công cụ được xây dựng trên các nguồn tài nguyên sau |"))
        print(error_color("| -> undetected-chromedriver                          |"))
        print(error_color("| -> selenium                                         |"))
        print(error_color(" -----------------------------------------------------"))
        print(error_color("|                  Các lựa chọn                       |"))
        print(error_color("| 1. thêm phiên                                       |"))
        print(error_color("| 2. chạy tool                                        |"))
        print(error_color("| 3. thêm giới hạn cho phiên                          |"))
        print(error_color(" -----------------------------------------------------"))
        print()

        ch = int(input(system_color("[?] Nhập lựa chọn của bạn\n-> ")))
    
        if ch == 1:
            add_new_session()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
            continue

        elif ch == 2:
            data = json.load(open(sessions_manager_file))
            wait = int(input(system_color("[?] Nhập số thời gian chờ giữa mỗi lần tương tác\n-> ")))
            max_times_for_interaction = int(input(system_color("[?] Nhập số lần tối đa tương tác trên mỗi account\n-> ")))
            print()

            while True:
                count_times += 1
                try:
                    __run(data, wait, max_times_for_interaction)
                except:
                    print(error_color("[!] Lỗi chương trình chính! thử lại..."))
                    continue

        elif ch == 3:
            add_session_limit_times()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
            continue