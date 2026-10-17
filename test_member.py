import pytest
import time
from selenium.webdriver.common.by import By
from base_page import get_driver, login

class TestMember:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = get_driver()
        yield
        self.driver.quit()

    def add_product_by_index(self, index=0):
        # 封装：传入商品序号，打开详情并加入购物车
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        items[index].click()
        self.driver.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart']").click()

    def fill_checkout_info(self, first_name, last_name, zip_code):
        # 封装：填充结算信息
        self.driver.find_element(By.ID, "first-name").send_keys(first_name)
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(zip_code)
        self.driver.find_element(By.ID, "continue").click()

    def test_product_module(self):
        login(self.driver, "standard_user", "secret_sauce")
        self.add_product_by_index(0)
        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert badge == "1"

    def test_checkout_module(self):
        login(self.driver, "standard_user", "secret_sauce")
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.fill_checkout_info("Test", "User", "12345")
        assert "checkout-step-two.html" in self.driver.current_url

    def test_integration_path_1(self):
        # 路径 1（深度 3）：购物车 -> 传入信息 -> 提交结算
        login(self.driver, "standard_user", "secret_sauce")
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        self.driver.find_element(By.ID, "checkout").click()
        self.fill_checkout_info("John", "Doe", "67890")
        self.driver.find_element(By.ID, "finish").click()
        assert "checkout-complete.html" in self.driver.current_url

    def test_integration_path_2(self):
        # 路径 2（深度 4）：登录 -> 多选商品 -> 填写地址 -> 完成
        login(self.driver, "standard_user", "secret_sauce")
        
        # 多选
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
        
        # 流程
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.fill_checkout_info("Jane", "Smith", "54321")
        self.driver.find_element(By.ID, "finish").click()
        assert "checkout-complete.html" in self.driver.current_url

    def test_data_combination_address(self):
        # 数据组合：合法、空值、特殊字符
        address_data = [
            ("John", "Doe", "12345"),
            ("", "", ""),
            ("!@#", "$%^", "&*(")
        ]
        login(self.driver, "standard_user", "secret_sauce")
        
        for f, l, z in address_data:
            self.driver.get("https://www.saucedemo.com/checkout-step-one.html")
            # 如果没加入商品，页面会自动跳转回 cart，先加一个
            if "cart.html" in self.driver.current_url:
                self.driver.get("https://www.saucedemo.com/inventory.html")
                self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
                self.driver.get("https://www.saucedemo.com/checkout-step-one.html")
                
            self.fill_checkout_info(f, l, z)
            if f == "":
                error = self.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
                assert "Error" in error
            else:
                assert "checkout-step-two.html" in self.driver.current_url
