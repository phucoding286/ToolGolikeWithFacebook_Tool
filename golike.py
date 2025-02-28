from modules import *

def golike_login(driver):
    driver.get("https://app.golike.net/")
    input(system_color("[?] Hãy nhập username và mật khẩu của bạn và nhấn đăng nhập\n-> "))


def __get_job(driver):
    try:

        gj = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[@class='row align-items-center']")
            )
        )

        driver.execute_script("arguments[0].click()", gj[1])
        time.sleep(1)
        return ""
    
    except:
        return {"error": "lỗi nhận job"}


def drop_job(driver):
    try:

        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[0])

        list_report = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='card card-job-detail mt-2']")
            )
        )

        driver.execute_script("arguments[0].setAttribute('style', '')", list_report)

        send_drop_job = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='Gửi báo cáo']")
            )
        )

        driver.execute_script("arguments[0].click()", send_drop_job)
        time.sleep(1)
        return ""
    
    except:
        return {"error": "Lỗi khi bỏ job"}


def verify_job(driver):
    try:

        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[0])

        verify_job = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='row align-items-center']")
            )
        )
    
        driver.execute_script("arguments[0].click()", verify_job[0])
        time.sleep(2)

        try:
            if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[@class='swal2-title']"))).text == "Lỗi":
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='swal2-confirm swal2-styled']"))).click()
                return {"error": "Lỗi khi xác minh job"}
        except:
            pass

        return {"success": "xác minh job thành công."}
    
    except:
        return {"error": "Lỗi khi xác minh job"}
    
def __check_and_get_job(driver):
    try:

        driver.get("https://app.golike.net/jobs/facebook/")

        check_jobs = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[@class='font-14 block-text-2']")
            )
        )

        if len(check_jobs) == 0:
            print(error_color("[!] hết job 10s ... "))
            time.sleep(10)
            return "continue"
        
        task = copy.copy(check_jobs[0]).text

        if task == "":
            print(system_color("[!] Chưa phát hiện job..."))
            return "continue"

        time.sleep(1)
        driver.execute_script("arguments[0].click()", copy.copy(check_jobs[0]))
        
        time.sleep(1)

        if task == "LIKE cho bài viết:":
            __get_job(driver)
            print(success_color("[$] Đã nhận job thành công!"))
            return "success"
        else:
            drop_job(driver)
            print(success_color("[#] Đã bỏ job."))
        
        return ""

    except:
        return {"error": "Bị giới hạn jobs"}

def check_and_get_job(driver):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[0])
    max_times_try_limit_job = 1

    while True:
        
        if max_times_try_limit_job >= 2+1:
            return "giới hạn job"

        check = __check_and_get_job(driver)
        if "error" in check:
            print(error_color(f"[!] Bị giới hạn jobs. giới hạn lần thử lại là {max_times_try_limit_job}/2"))
            max_times_try_limit_job += 1
            continue

        if check == "continue":
            continue
        
        if check == "success":
            return ""
        
if __name__ == "__main__":
    driver = driver_init()
    # r = check_and_get_job(driver)
    # print(r)
    input(">>> ")
    r = verify_job(driver)
    print(r)
    input()