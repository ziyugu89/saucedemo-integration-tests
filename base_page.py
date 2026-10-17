from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    # 使用 Edge 浏览器的配置
    options = webdriver.EdgeOptions()
    # options.add_argument("--headless") # 可选，静默运行
    
    # 自动下载并安装 EdgeDriver
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

def login(driver, username, pwd):
    # 传参：浏览器对象、用户名、密码
    driver.get("https://www.saucedemo.com")
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(pwd)
    driver.find_element(By.ID, "login-button").click()

def get_error_message(driver):
    try:
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        )
        return error_element.text
    except:
        return None
