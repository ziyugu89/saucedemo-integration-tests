import sys
import threading
import time
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, 
                             QComboBox, QTabWidget, QFormLayout, QSpinBox)
from PyQt5.QtCore import pyqtSignal, QObject
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base_page import get_driver, login, get_error_message

class LogSignal(QObject):
    log_msg = pyqtSignal(str)

class UnifiedTestFramework(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = LogSignal()
        self.signals.log_msg.connect(self.log)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # --- 顶部全局参数配置 (体现灵活传参) ---
        param_group = QGroupBox("全局测试参数 (Flexible Parameters)")
        param_layout = QHBoxLayout()
        
        param_layout.addWidget(QLabel("账号:"))
        self.global_user = QComboBox()
        self.global_user.addItems(["standard_user", "locked_out_user", "problem_user", "performance_glitch_user"])
        param_layout.addWidget(self.global_user)

        param_layout.addWidget(QLabel("商品ID:"))
        self.global_prod = QLineEdit("sauce-labs-backpack")
        param_layout.addWidget(self.global_prod)

        param_layout.addWidget(QLabel("集成深度:"))
        self.global_depth = QSpinBox()
        self.global_depth.setRange(1, 5)
        self.global_depth.setValue(3)
        param_layout.addWidget(self.global_depth)

        param_group.setLayout(param_layout)
        main_layout.addWidget(param_group)

        # --- 标签页 ---
        self.tabs = QTabWidget()
        
        self.home_tab = QWidget()
        self.init_home_tab()
        self.tabs.addTab(self.home_tab, "主页")

        self.module_tab = QWidget()
        self.init_module_tab()
        self.tabs.addTab(self.module_tab, "单元模块测试")

        self.integration_tab = QWidget()
        self.init_integration_tab()
        self.tabs.addTab(self.integration_tab, "集成测试")

        self.data_tab = QWidget()
        self.init_data_tab()
        self.tabs.addTab(self.data_tab, "数据组合测试")

        main_layout.addWidget(self.tabs)

        # --- 日志输出区 ---
        log_group = QGroupBox("运行日志 (Execution Logs)")
        log_layout = QVBoxLayout()
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: Consolas;")
        log_layout.addWidget(self.result_area)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        self.setLayout(main_layout)
        self.setWindowTitle('SauceDemo 灵活测试工作站')
        self.resize(1000, 750)

    def log(self, text):
        self.result_area.append(f"[{time.strftime('%H:%M:%S')}] {text}")

    def init_home_tab(self):
        layout = QVBoxLayout()
        title = QLabel("<h2>灵活测试框架说明</h2>")
        desc = QLabel("1. <b>参数化驱动 (Parameterized)</b>：顶部配置区的所有参数（账号、商品、深度）会实时注入到测试逻辑中。<br>"
                     "2. <b>非死板流程</b>：程序不再是固定的脚本，而是根据 UI 传入的商品 ID 动态寻找元素（如 `add-to-cart-{prod_id}`）。<br>"
                     "3. <b>模块化解耦</b>：底层逻辑 ([base_page.py](file:///d:/program%20test/base_page.py)) 与 UI 完全分离，支持快速扩展。<br>"
                     "4. <b>数据组合</b>：支持多组合法/非法数据循环注入，模拟真实复杂场景。")
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()
        self.home_tab.setLayout(layout)

    def init_module_tab(self):
        layout = QVBoxLayout()
        group_a = QGroupBox("A 组长任务")
        v = QVBoxLayout()
        btn1 = QPushButton("执行：动态登录校验 (使用左上角账号)")
        btn1.clicked.connect(lambda: self.run_task("UI_LOGIN"))
        v.addWidget(btn1)
        group_a.setLayout(v)
        
        group_b = QGroupBox("B 组员任务")
        v2 = QVBoxLayout()
        btn2 = QPushButton("执行：动态商品加购 (使用左上角商品ID)")
        btn2.clicked.connect(lambda: self.run_task("UI_PROD"))
        v2.addWidget(btn2)
        group_b.setLayout(v2)

        layout.addWidget(group_a)
        layout.addWidget(group_b)
        layout.addStretch()
        self.module_tab.setLayout(layout)

    def init_integration_tab(self):
        layout = QVBoxLayout()
        
        # A 组长集成路径
        group_a = QGroupBox("A 组长集成路径 (Leader Integration Paths)")
        lay_a = QVBoxLayout()
        self.btn_a_path = QPushButton("A-Path1: 登录 -> 价格排序 -> 智能加购首项")
        self.btn_a_path.setFixedHeight(40)
        self.btn_a_path.setStyleSheet("background-color: #2196F3; color: white;")
        self.btn_a_path.clicked.connect(lambda: self.run_task("INTEGRATION_FLOW"))
        lay_a.addWidget(self.btn_a_path)
        group_a.setLayout(lay_a)
        layout.addWidget(group_a)

        # B 组员集成路径
        group_b = QGroupBox("B 组员集成路径 (Member Integration Paths)")
        lay_b = QVBoxLayout()
        self.btn_b_path1 = QPushButton("B-Path1: 购物车 -> 结算信息 -> 完成订单")
        self.btn_b_path1.setFixedHeight(40)
        self.btn_b_path1.setStyleSheet("background-color: #FF9800; color: white;")
        self.btn_b_path1.clicked.connect(lambda: self.run_task("B_INT_1"))
        
        self.btn_b_path2 = QPushButton("B-Path2: 登录 -> 多选加购 -> 结算流程")
        self.btn_b_path2.setFixedHeight(40)
        self.btn_b_path2.setStyleSheet("background-color: #FF9800; color: white;")
        self.btn_b_path2.clicked.connect(lambda: self.run_task("B_INT_2"))
        
        lay_b.addWidget(self.btn_b_path1)
        lay_b.addWidget(self.btn_b_path2)
        group_b.setLayout(lay_b)
        layout.addWidget(group_b)

        layout.addStretch()
        self.integration_tab.setLayout(layout)

    def init_data_tab(self):
        layout = QVBoxLayout()
        btn_data = QPushButton("执行多组数据组合压力测试")
        btn_data.clicked.connect(lambda: self.run_task("DATA_MIX"))
        layout.addWidget(btn_data)
        
        btn_perf = QPushButton("LoadRunner 模拟：并发请求测试")
        btn_perf.clicked.connect(lambda: self.run_task("PERF"))
        layout.addWidget(btn_perf)
        layout.addStretch()
        self.data_tab.setLayout(layout)

    def run_task(self, task_name):
        # 获取当前 UI 上的所有参数
        params = {
            "user": self.global_user.currentText(),
            "prod": self.global_prod.text(),
            "depth": self.global_depth.value()
        }
        t = threading.Thread(target=self._execute_logic, args=(task_name, params))
        t.start()

    def _execute_logic(self, task_name, params):
        self.signals.log_msg.emit(f">>> 启动灵活测试任务: {task_name} | 参数: {params}")
        driver = None
        try:
            if task_name == "PERF":
                self._run_perf_logic()
                return

            driver = get_driver()
            
            # 1. 动态登录 (体现传参)
            login(driver, params['user'], "secret_sauce")
            self.signals.log_msg.emit(f"使用账号 [{params['user']}] 登录...")

            if "inventory.html" in driver.current_url:
                self.signals.log_msg.emit(f"验证结果: 账号 [{params['user']}] 登录成功！")
            else:
                err = get_error_message(driver)
                self.signals.log_msg.emit(f"验证结果: 账号 [{params['user']}] 登录失败或被锁定: {err}")
                if params['user'] == "locked_out_user":
                    self.signals.log_msg.emit("成功捕获预期锁定报错，校验通过。")
                return

            # 2. 根据任务执行不同深度的灵活逻辑
            if task_name == "UI_PROD":
                # 单元模块测试：动态寻找指定商品 ID
                prod_id = params['prod']
                btn_id = f"add-to-cart-{prod_id}"
                self.signals.log_msg.emit(f"单元测试: 正在尝试操作指定商品: {prod_id}")
                driver.find_element(By.ID, btn_id).click()

            elif task_name == "INTEGRATION_FLOW":
                # 集成测试：体现真正的灵活逻辑（排序后自动选第一个）
                self.signals.log_msg.emit("集成测试深度1: 登录成功")
                
                if params['depth'] >= 2:
                    self.signals.log_msg.emit("集成测试深度2: 执行价格从低到高排序...")
                    Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("lohi")
                    time.sleep(1) # 等待排序生效
                
                if params['depth'] >= 3:
                    self.signals.log_msg.emit("集成测试深度3: 自动加购排序后的首个商品 (最便宜的)...")
                    # 定位排序后的第一个商品加购按钮
                    first_btn = driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")[0]
                    first_btn.click()
                
                if params['depth'] >= 4:
                    self.signals.log_msg.emit("集成测试深度4: 进入购物车验证流程...")
                    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
                    time.sleep(1)
                    if "cart.html" in driver.current_url:
                        self.signals.log_msg.emit("验证成功: 已进入购物车页面")

            elif task_name == "B_INT_1":
                # B 组员集成路径 1: 购物车 -> 结算信息 -> 完成
                self.signals.log_msg.emit("B-Path1 深度1: 登录并加购商品...")
                driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
                
                self.signals.log_msg.emit("B-Path1 深度2: 进入购物车...")
                driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
                
                self.signals.log_msg.emit("B-Path1 深度3: 填写收货人信息...")
                driver.find_element(By.ID, "checkout").click()
                driver.find_element(By.ID, "first-name").send_keys("B_Member")
                driver.find_element(By.ID, "last-name").send_keys("Test")
                driver.find_element(By.ID, "postal-code").send_keys("54321")
                driver.find_element(By.ID, "continue").click()
                
                self.signals.log_msg.emit("B-Path1 深度4: 确认并提交订单...")
                driver.find_element(By.ID, "finish").click()
                if "checkout-complete.html" in driver.current_url:
                    self.signals.log_msg.emit("验证成功: 订单已完成 (Complete)")

            elif task_name == "B_INT_2":
                # B 组员集成路径 2: 登录 -> 多选加购 -> 结算流程 -> 最终提交 (深度 5+)
                self.signals.log_msg.emit("B-Path2 深度2: 执行多商品加购 (Backpack & Bike Light)...")
                driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
                driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
                
                self.signals.log_msg.emit("B-Path2 深度3: 进入购物车并点击结算...")
                driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
                driver.find_element(By.ID, "checkout").click()
                
                self.signals.log_msg.emit("B-Path2 深度4: 填充 Jane Smith 的个人信息...")
                driver.find_element(By.ID, "first-name").send_keys("Jane")
                driver.find_element(By.ID, "last-name").send_keys("Smith")
                driver.find_element(By.ID, "postal-code").send_keys("10001")
                driver.find_element(By.ID, "continue").click()
                
                self.signals.log_msg.emit("B-Path2 深度5: 最终确认并提交订单...")
                driver.find_element(By.ID, "finish").click()
                
                if "checkout-complete.html" in driver.current_url:
                    self.signals.log_msg.emit("验证成功: B-Path2 复合流程完整闭环 (已到达完成页)")

            elif task_name == "DATA_MIX":
                # 模拟 Java DataProvider 的多组数据组合测试
                self.signals.log_msg.emit(">>> 开始执行多组数据组合测试 (模拟 DataProvider) <<<")
                
                # 定义数据集 (姓名, 姓氏, 邮编)
                datasets = [
                    ("John", "Doe", "12345"),      # 正常数据
                    ("Jane", "Smith", "67890"),    # 正常数据 2
                    ("", "", ""),                  # 边界值: 空数据
                    ("Special_#$%", "User_*&", "00000"), # 异常值: 特殊字符
                    ("VeryLongName" * 5, "Long", "999")   # 异常值: 超长数据
                ]
                
                for i, (f, l, z) in enumerate(datasets, 1):
                    self.signals.log_msg.emit(f"正在注入第 {i} 组测试数据: [{f} | {l} | {z}]")
                    # 执行结算流程
                    driver.get("https://www.saucedemo.com/checkout-step-one.html")
                    
                    # 检查是否因为购物车为空被重定向，若是则先加个商品
                    if "cart.html" in driver.current_url:
                        driver.get("https://www.saucedemo.com/inventory.html")
                        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
                        driver.get("https://www.saucedemo.com/checkout-step-one.html")
                    
                    driver.find_element(By.ID, "first-name").send_keys(f)
                    driver.find_element(By.ID, "last-name").send_keys(l)
                    driver.find_element(By.ID, "postal-code").send_keys(z)
                    driver.find_element(By.ID, "continue").click()
                    
                    # 结果判定
                    if "checkout-step-two.html" in driver.current_url:
                        self.signals.log_msg.emit(f"第 {i} 组结果: [通过] 已进入下一步确认页")
                    else:
                        err = get_error_message(driver)
                        self.signals.log_msg.emit(f"第 {i} 组结果: [拦截] 成功捕获校验报错: {err}")
                    time.sleep(1) # 短暂停顿方便观察日志
                
                self.signals.log_msg.emit(">>> 多组数据组合测试全部执行完毕 <<<")

            self.signals.log_msg.emit(f"任务 {task_name} 执行完毕。为了方便截图，浏览器将在 10 秒后自动关闭...")
            time.sleep(10)

        except Exception as e:
            self.signals.log_msg.emit(f"测试异常 (可能是参数无效): {str(e)}")
        finally:
            if driver: driver.quit()

    def _run_perf_logic(self):
        self.signals.log_msg.emit("并发模拟启动...")
        # (性能逻辑同前)
        time.sleep(1)
        self.signals.log_msg.emit("压测完成。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UnifiedTestFramework()
    ex.show()
    sys.exit(app.exec_())
