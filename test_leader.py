import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base_page import get_driver, login, get_error_message

class TestLeader:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = get_driver()
        yield
        self.driver.quit()

    def test_login_module(self):
        # 1. 登录模块 - 成功
        login(self.driver, "standard_user", "secret_sauce")
        assert "inventory.html" in self.driver.current_url

        # 2. 登录模块 - 锁定验证
        login(self.driver, "locked_out_user", "secret_sauce")
        error_msg = get_error_message(self.driver)
        assert "Locked out" in error_msg

    def test_user_status_validation(self):
        # 传入不同账号判断跳转
        users = [
            ("standard_user", True),
            ("locked_out_user", False),
            ("problem_user", True)
        ]
        for user, should_succeed in users:
            login(self.driver, user, "secret_sauce")
            if should_succeed:
                assert "inventory.html" in self.driver.current_url
                # 登出以便下次测试
                self.driver.find_element(By.ID, "react-burger-menu-btn").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "logout_sidebar_link").click()
            else:
                assert get_error_message(self.driver) is not None

    def test_integration_path_1(self):
        # 路径 1（深度 3）：登录 -> 筛选 -> 加入购物车
        login(self.driver, "standard_user", "secret_sauce")
        
        # 筛选 (Price low to high)
        select = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        select.select_by_value("lohi")
        
        # 加入购物车
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert badge == "1"

    def test_integration_path_2(self):
        # 路径 2（深度 4）：登录 -> 商品详情 -> 加入购物车 -> 购物车确认
        login(self.driver, "standard_user", "secret_sauce")
        
        # 进入详情
        self.driver.find_element(By.ID, "item_4_title_link").click()
        assert "inventory-item.html" in self.driver.current_url
        
        # 加入购物车
        self.driver.find_element(By.ID, "add-to-cart").click()
        
        # 进入购物车
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        assert "cart.html" in self.driver.current_url
        assert self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"

    def test_data_combination(self):
        # 数据组合测试
        user_list = ["standard_user", "locked_out_user", "problem_user"]
        results = []
        for user in user_list:
            login(self.driver, user, "secret_sauce")
            success = "inventory.html" in self.driver.current_url
            results.append((user, success))
            # 重置环境
            self.driver.get("https://www.saucedemo.com")
        
        print("\nData Combination Results:", results)
        assert len(results) == 3
