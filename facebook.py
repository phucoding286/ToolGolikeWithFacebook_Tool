from modules import *
from scroll_facebook import scroll_facebook, continue_scroll
import random

def facebook_login(driver):
    driver.get("https://facebook.com/")
    input(system_color("[?] Hãy nhập username và mật khẩu của bạn và nhấn đăng nhập\n-> "))

def like_permalink_post(driver, link, like_type="like"): #like type (tim, haha, sad..vv)
    check_tt_cell = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa']")
        )
    )
    print(system_color(f"[>] Số lượng phần tử tương tác trong ô -> {len(check_tt_cell)}"))
    if len(check_tt_cell) < 7:
        return {"error": "like thất bại"}
                
    try:
        continue_scroll(driver, 0, 250)
        time.sleep(1)
        continue_scroll(driver, 250, 500)
    except:
        pass

    time.sleep(1)
    driver.get(link)
                
    try:
        like_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Thích']")))
    except:
        like_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Like']")))

    time.sleep(1)
                
    if len(like_btn) > 1:
        like_btn[1].click()
    else:
        like_btn[0].click()

def check_permalink_post(link):
    return link.split("/")[3].startswith("permalink") or link.split("/")[4].startswith("post")

def like_watch(driver, link):
    try:
        continue_scroll(driver, 0, 250)
        time.sleep(1)
        continue_scroll(driver, 250, 500)
    except:
        pass

    time.sleep(1)
    driver.get(link)
                
    try:
        like_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Thích']")))
    except:
        like_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Like']")))
        time.sleep(1)
        driver.execute_script("arguments[0].click()", like_btn[0])

def check_watch(link):
    return link.split("/")[3].startswith("watch")

def like_photo(driver, link):
    try:
        continue_scroll(driver, 0, 250)
        time.sleep(1)
        continue_scroll(driver, 250, 500)
    except:
        pass

    time.sleep(1)
    driver.get(link)
                
    like_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz x5ve5x3']")
    ))
    like_btn.click()

def check_photo(link):
    return link.split("/")[3].startswith("photo")

def like_video(driver, link):
    check_tt_cell = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa']")
        )
    )
    print(system_color(f"[>] Số lượng phần tử tương tác trong ô -> {len(check_tt_cell)}"))
    if len(check_tt_cell) < 5:
        return {"error": "like thất bại"}
                
    try:
        continue_scroll(driver, 0, 250)
        time.sleep(1)
        continue_scroll(driver, 250, 500)
    except:
        pass

    time.sleep(1)
    driver.get(link)
                
    try:
        like_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Thích']")))
    except:
        like_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Like']")))

    time.sleep(1)
                
    if len(like_btn) > 1:
        like_btn[1].click()
    else:
        like_btn[0].click()

def check_video(link):
    return link.split("/")[4].startswith("videos")

def like(driver):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    try:

        try:
            link = driver.current_url
            print(purple_color(f"[>] Link bài viết -> {link}"))
            
            if check_permalink_post(link):
                r = like_permalink_post(driver, link)
                if isinstance(r, dict) and "error" in r:
                    driver.close()
                    return {"error": "like thất bại"}

            elif check_watch(link):
                like_watch(driver, link)

            elif check_photo(link):
                like_photo(driver, link)

            elif check_video(link):
                r = like_video(driver, link)
                if isinstance(r, dict) and "error" in r:
                    driver.close()
                    return {"error": "like thất bại"}

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
    driver = driver_init(r"E:\MySRC\golike-tools\golike-facebook-selenium\acc1")
    input(">>> ")
    print(like(driver))
    input(">>> ")