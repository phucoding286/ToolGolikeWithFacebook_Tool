from modules import *
from scroll_facebook import scroll_facebook, continue_scroll

def facebook_login(driver):
    driver.get("https://facebook.com/")
    input(system_color("[?] Hãy nhập username và mật khẩu của bạn và nhấn đăng nhập\n-> "))

def like(driver):
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
                driver.close()
                return {"error": "like thất bại"}

            time.sleep(1)

        except:
            driver.close()
            return {"error": "like thất bại"}
        
        driver.close()
        return {"success": "like thành công"}
    
    except:
        driver.close()
        return {"error": "like thất bại"}
    
if __name__ == "__main__":
    driver = driver_init()
    input(">>> ")
    print(like(driver))
    input(">>> ")