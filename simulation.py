from modules import *

def scroll_to_down(driver: webdriver.Chrome):
    rdn_times_scroll = random.randint(2, 10) # random scroll
    for i in range(rdn_times_scroll):
        driver.execute_script(f"window.scrollTo({i*600}, {(i+1)*600});")
        waiting_ui(random.randint(1, 3), "Đợi để tiếp tục scroll") # random wait
        print(system_color(f"[>] Đã scroll, số lần {i+1}/{rdn_times_scroll}"))
    return ""

def scroll_to_up(driver: webdriver.Chrome):
    rdn_times_scroll = random.randint(2, 10)
    for i in range(rdn_times_scroll):
        driver.execute_script(f"window.scrollTo({i*-100}, {(i+1)*-100});")
        waiting_ui(random.randint(1, 3), "Đợi để tiếp tục scroll") # random wait
        print(system_color(f"[>] Đã scroll, số lần {i+1}/{rdn_times_scroll}"))
    return ""

def random_scroll(driver: webdriver.Chrome):
    total_scroll = random.randint(1, 3)
    for i in range(total_scroll):
        is_scroll_down = random.choice([True, False])
        scroll_out = scroll_to_down(driver) if is_scroll_down or i == 0 else scroll_to_up(driver)
        if "error" in scroll_out: return scroll_out
        print(system_color(f"[>] Số lần tổng scroll {i+1}/{total_scroll}"))
    return ""

def post_scroll(driver: webdriver.Chrome):
    print(purple_color("Đang scroll bên post feed"))
    home_btn = WebDriverWait(driver, 10).until( EC.presence_of_element_located(
        (By.XPATH, "//a[@aria-label='Home']"))
    )
    home_btn.click()
    random_scroll(driver)

def video_scroll(driver: webdriver.Chrome):
    print(purple_color("Đang scroll bên video feed"))
    home_btn = WebDriverWait(driver, 10).until( EC.presence_of_element_located(
        (By.XPATH, "//a[@aria-label='Video']"))
    )
    home_btn.click()
    random_scroll(driver)

def simulator(driver: webdriver.Chrome):
    try: post_scroll(driver) if random.choice([True, False]) else video_scroll(driver)
    except: return {"error": "Lỗi khi scroll"}
    return {"success": "Thành công"}


if __name__ == "__main__":
    driver = driver_init(chrome_user_data=r"E:\MySRC\golike-tools\golike_facebook_selenium\data", hide_chrome=False)
    driver.get("https://www.facebook.com/")
    input(">>> ")
    r = simulator(driver)
    print(r)
    input("-> ")