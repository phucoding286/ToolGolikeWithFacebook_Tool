from modules import *
from scroll_facebook import scroll_facebook, continue_scroll
import random

def facebook_login(driver):
    driver.get("https://facebook.com/")
    input(system_color("[?] Hãy nhập username và mật khẩu của bạn và nhấn đăng nhập\n-> "))

def change_vpn(driver: webdriver.Chrome):
    driver.get("chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/popup/index.html")
    
    check_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='timer main-page__timer']")))
    if check_time.text != "00 : 00 : 00":
        stop_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='play-button play-button--pause']")))
        stop_btn.click()

    server_vpn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class='select-location__input']")))
    server_vpn.click()

    server_list_rdn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//p[@class='locations__item-name']")
    ))
    server_list_rdn[random.randrange(0, 4)].click()
    
    for _ in range(10):
        check_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='timer main-page__timer']")))
        if check_time.text == "00 : 00 : 00":
            time.sleep(1)
            continue
        else:
            break
    return "timeout_connect"

def disconnect_vpn(driver):
    driver.get("chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/popup/index.html")
    check_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='timer main-page__timer']")))
    if check_time.text != "00 : 00 : 00":
        stop_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='play-button play-button--pause']")))
        stop_btn.click()

def like(driver):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    
    driver.execute_script("window.open();")
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    try:
        r = change_vpn(driver)
        driver.close()
    except:
        driver.close()

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    try:

        try:
            link = driver.current_url
            print(purple_color(f"[>] Link bài viết -> {link}"))
            
            if link.split("/")[3].startswith("permalink")\
                or link.split("/")[4].startswith("post"):

                check_tt_cell = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa']")
                    )
                )
                print(system_color(f"[>] Số lượng phần tử tương tác trong ô -> {len(check_tt_cell)}"))
                if len(check_tt_cell) < 7:
                    try:
                        disconnect_vpn(driver)
                    except:
                        pass
                    driver.close()
                    return {"error": "like thất bại"}
                
                try:
                    continue_scroll(driver, 0, 250)
                    time.sleep(1)
                    continue_scroll(driver, 250, 500)
                except:
                    pass
                
                time.sleep(2)
                
                try:
                    like_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//span[text()='Thích']")
                        )
                    )
                except:
                    like_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//span[text()='Like']")
                        )
                    )

                time.sleep(1)
                
                if len(like_btn) > 1:
                    # driver.execute_script("arguments[0].click()", like_btn[1])
                    like_btn[1].click()
                else:
                    # driver.execute_script("arguments[0].click()", like_btn[0])
                    like_btn[0].click()

            elif link.split("/")[3].startswith("watch"):

                try:
                    continue_scroll(driver, 0, 250)
                    time.sleep(1)
                    continue_scroll(driver, 250, 500)
                except:
                    pass

                time.sleep(2)
                
                try:
                    like_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//span[text()='Thích']")
                        )
                    )
                except:
                    like_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//span[text()='Like']")
                        )
                    )

                time.sleep(1)

                driver.execute_script("arguments[0].click()", like_btn[0])

            else:
                try:
                    disconnect_vpn(driver)
                except:
                    pass
                driver.close()
                return {"error": "like thất bại"}

            time.sleep(1)

        except:
            try:
                disconnect_vpn(driver)
            except:
                pass
            driver.close()
            return {"error": "like thất bại"}
        
        try:
            disconnect_vpn(driver)
        except:
            pass
        driver.close()
        return {"success": "like thành công"}
    
    except:
        try:
            disconnect_vpn(driver)
        except:
            pass
        driver.close()
        return {"error": "like thất bại"}
    
if __name__ == "__main__":
    driver = driver_init(r"E:\MySRC\golike-tools\golike-facebook-selenium\acc1")
    input(">>> ")
    print(like(driver))
    input(">>> ")