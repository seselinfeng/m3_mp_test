import time
import unittest
import allure
import minium

from pages.app import App


class MainTest(minium.MiniTest):
    def setUp(self):
        self.app = App()
        self.main = self.app.start().main()
        self.routing = self.app.start().routing()
        self.order_list = self.app.start().order_list()

    def test_order(self):
        # 下单
        self.main.goto_hotel_list().goto_hotel_detail().goto_hotel_scheduled().save_order()
        # 去订单列表页
        self.routing.goto_order_list()

    def test_order_list(self):
        # 回到首页
        self.routing.goto_main()
        # 下单
        self.main.goto_hotel_list().goto_hotel_detail().goto_hotel_scheduled().save_order()

    # @allure.title("测试demo")
    def test_demo(self):
        with allure.step("跳转到订单列表页"):
            self.routing.goto_order_list()
        time.sleep(3)
        with allure.step("获取当前页面第一个订单,并点击"):
            self.order_list.get_order_list()[0].click()

    def test_demo1(self):
        self.main.set_day_date(29, 30)

    def tearDown(self):
        # 回到首页
        time.sleep(3)
        # self.routing.goto_main()


if __name__ == '__main__':
    # 构造测试集
    suit = unittest.TestSuite()
    suit.addTest(MainTest("test_demo"))  # 把这个类中需要执行的测试用例加进去，有多条再加即可
    runner = unittest.TextTestRunner()
    runner.run(suit)  # 运行测试用例
