from modules import *
prices = 0

list_task_avaible = ["TĂNG LIKE CHO BÀI VIẾT"]


def drop_job(driver: webdriver.Chrome):
    cancel_job = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h6[text()='Báo lỗi cho hệ thống khi làm việc thất bại']"))
    )
    # scroll đến nút
    driver.execute_script("arguments[0].scrollIntoView(true);", cancel_job)
    cancel_job.click()
    # gửi báo cáo
    report_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Gửi báo cáo']"))
    )
    # scroll đến nút
    driver.execute_script("arguments[0].scrollIntoView(true);", report_btn)
    # nhấn nút
    report_btn.click()

    check = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='Đã gửi báo cáo lên hệ thống']"))
    )


def check_avaible_job(driver: webdriver.Chrome):
    driver.get("https://app.golike.net/jobs/facebook?load_job=true")
    # nút job
    job_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='card mb-2 hand']"))
    )
    job_btn[0].click()
    # lấy text nhiệm vụ
    task_label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='font-18 font-bold b200 block-text']"))
    )

    # kiểm tra task có avaible không
    if task_label.text not in list_task_avaible:
        try: [drop_job(driver), print(success_color("Bỏ job thành công"))]
        except: print(error_color("Bỏ job thất bại"))
        return {"unavaible_job": "Job không thuộc danh sách avaible"}
    else:
        return {"avaible_job": "Job thuộc danh sách avaible"}
    

def get_job(driver: webdriver.Chrome):
    try:
        # kiểm tra job có hợp lệ không
        check_job = check_avaible_job(driver)
        while "unavaible_job" in check_job:
            check_job = check_avaible_job(driver)
            print(error_color(check_job["unavaible_job"])) if "unavaible_job" in check_job else print(success_color(check_job["avaible_job"]))
        # lấy link đối tượng của job cần làm
        link_job = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@class='row align-items-center']"))
        )
        # scroll đến nút
        driver.execute_script("arguments[0].scrollIntoView(true);", link_job[0])
        link_job = link_job[0].get_attribute("href")
        
        job_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Làm việc bằng trình duyệt Web trên điện thoại.']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", job_btn)
        job_btn.click()

        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        driver.close()
        handles = driver.window_handles
        driver.switch_to.window(handles[0])

        return {"success": link_job}
    except:
        return {"error": "Lỗi khi nhận job"}


def __verify_job(driver: webdriver.Chrome):
    global prices
    waiting_ui(4, "Đợi 4s để xác minh")
    verify_job_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h6[text()='Bấm hoàn thành để nhận tiền sau khi làm việc xong.']"))
    )
    # scroll đến nút
    driver.execute_script("arguments[0].scrollIntoView(true);", verify_job_btn)
    verify_job_btn.click()
    
    try:
        error_text = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Lỗi']"))
        )
        waiting_ui(2, "Lỗi xác minh job")
        ok_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='OK']"))
        )
        # scroll đến nút
        driver.execute_script("arguments[0].scrollIntoView(true);", ok_btn)
        ok_btn.click()
        return {"error": "Xác minh job thất bại"}
    except:
        prices += 35
        return {"success": "Đã xác minh job thành công.", "prices": prices}
    

def verify_job(driver: webdriver.Chrome, max_try=5):
    response = None
    for _ in range(max_try):
        response = __verify_job(driver)
        if "success" in response:
            return response
        else:
            print(error_color(f"Lỗi xác minh job, thử lại lần {_+1}/{max_try}"))
            continue
    else:
        return response


if __name__ == "__main__":
    driver = driver_init(chrome_user_data=r"E:\MySRC\golike-tools\golike_facebook_selenium\data", hide_chrome=False)
    input(">>> ")
    r = get_job(driver)
    print(r)
    input(">>> ")
    print(verify_job(driver))
    input(">>> ")