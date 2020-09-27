import time
import allure
import pytest

from common.processingdata import get_data
from pages.app import App


class TestOrder:
    def setup(self):
        self.app = App()
        self.main = self.app.start().main()
        self.routing = self.app.start().routing()
        self.order_list = self.app.start().order_list()

    @allure.title("日租房当日预定流程")
    @pytest.mark.parametrize(("name", "phone", "room_type"), get_data('test_day_order', '../data/test_order.yaml'))
    def test_day_order(self, name, phone, room_type):
        with allure.step("日租房下单流程"):
            self.main.goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(room_type).save_order(name, phone)
        time.sleep(10)
        # 去订单列表页
        with allure.step("跳转到订单列表页面"):
            self.routing.goto_order_list()
        time.sleep(10)
        with allure.step("获取当前页面第一个订单,并点击"):
            self.order_list.get_order_list()[0].click()
        time.sleep(10)
        with allure.step("获取订单详情页面数据，并断言"):
            pass

    @allure.title("时租房预定流程")
    @pytest.mark.parametrize(("name", "phone", "room_type"), get_data('test_hour_order', '../data/test_order.yaml'))
    def test_hour_order(self, name, phone, room_type):
        with allure.step("时租房下单流程"):
            self.main.goto_hour_hotel_list().goto_hotel_detail().goto_hotel_scheduled(room_type).save_order(name, phone)
        time.sleep(10)
        # 去订单列表页
        with allure.step("跳转到订单列表页面"):
            self.routing.goto_order_list()
        time.sleep(10)
        with allure.step("获取当前页面第一个订单,并点击"):
            self.order_list.get_order_list()[0].click()
        time.sleep(10)
        with allure.step("获取订单详情页面数据，并断言"):
            pass

    @allure.title("整夜房当日预定流程")
    @pytest.mark.parametrize(("name", "phone", "room_type"), get_data('test_night_order', '../data/test_order.yaml'))
    def test_night_order(self, name, phone, room_type):
        with allure.step("整夜房下单流程"):
            self.main.goto_night_hotel_list().goto_hotel_detail().goto_hotel_scheduled(room_type).save_order(name,
                                                                                                             phone)
        time.sleep(10)
        # 去订单列表页
        with allure.step("跳转到订单列表页面"):
            self.routing.goto_order_list()
        time.sleep(10)
        with allure.step("获取当前页面第一个订单,并点击"):
            self.order_list.get_order_list()[0].click()
        time.sleep(10)
        with allure.step("获取订单详情页面数据，并断言"):
            pass

    @allure.title("日租房远期预定流程")
    @pytest.mark.parametrize(("name", "phone", "room_type", "start_date", "end_date"),
                             get_data('test_forward_day_order', '../data/test_order.yaml'))
    def test_forward_day_order(self, name, phone, room_type, start_date, end_date):
        with allure.step("日租房下单流程"):
            self.main.set_day_date(start_date, end_date).goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name,
                                      phone)
        time.sleep(10)
        # 去订单列表页
        with allure.step("跳转到订单列表页面"):
            self.routing.goto_order_list()
        time.sleep(10)
        with allure.step("获取当前页面第一个订单,并点击"):
            self.order_list.get_order_list()[0].click()
        time.sleep(10)
        with allure.step("获取订单详情页面数据，并断言"):
            pass

    @allure.title("测试demo")
    @pytest.mark.parametrize(("start_date", "end_date"), get_data('test_demo', '../data/test_order.yaml'))
    def test_demo(self, start_date, end_date):
        self.main.set_day_date(start_date, end_date)

    def teardown(self):
        # self.app.stop()
        pass
