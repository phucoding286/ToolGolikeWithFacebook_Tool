from modules import *

def scroll_facebook(driver, times=10):
    driver.get("https://www.facebook.com/")
    try:
        i, j = 0, 250
        for _ in range(times):
            driver.execute_script(f"window.scroll({i}, {j})")
            time.sleep(1)
            i += 250
            j += 250
    except:
        pass
    i+= 250
    j += 250
    return i, j

def continue_scroll(driver, i, j):
    try:
        driver.execute_script(f"window.scroll({i}, {j})")
        time.sleep(1)
    except:
        print(error_color("[!] Scroll thất bại."))
    i += 250
    j += 250
    return i, j