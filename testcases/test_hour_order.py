import time
import allure
import pytest

from common.processingdata import get_data
from pages.app import App


@allure.feature("时租房预定订单模块")
class TestHourOrder:
    def setup(self):
        self.app = App()
        self.main = self.app.start().main()
        self.my = self.app.start().my()
        self.routing = self.app.start().routing()
        self.order_list = self.app.start().order_list()
        self.order_detail = self.app.start().order_detail()

    @allure.title("时租房预定流程测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "except_result"),
                             get_data('test_hour_order', '../data/test_hour_order.yaml'))
    def test_hour_order(self, name, phone, room_type, except_result):
        """日租房预定当日酒店流程测试"""
        with allure.step(f"{room_type}-时租房下单流程"):
            hotel_scheduled = self.main.goto_hour_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone)
        with allure.step("校验时租房费是否正确"):
            fee_result = hotel_scheduled.get_fee()
            room_rate = except_result.get("expect_result")[0].get("房费总额")
            amount_paid = except_result.get("expect_result")[1].get("实付金额")
            assert fee_result == f'房费总额:\n{room_rate}\n实付金额:\n{amount_paid}', f'当前返回实际值为: {fee_result}'
        with allure.step("支付房费"):
            pay_success = hotel_scheduled.goto_pay()
        with allure.step("跳转到订单详情"):
            time.sleep(4)
            pay_success.goto_order_detail()
        with allure.step("获取订单详情页面数据，并校验"):
            paid_result = self.order_detail.get_amount_paid()
            username_result = self.order_detail.get_username()
            totel_paid = except_result.get("expect_result")[2].get("总价")
            room_user = except_result.get("expect_result")[3].get("入住人")
            assert paid_result == f"总价：{totel_paid}", f'当前返回的实际值为: {paid_result}'
            assert username_result == f"入住人：{room_user}", f'当前返回的实际值为:{username_result}'
        with allure.step("取消订单，释放房态"):
            self.order_detail.cancel_order()

    @allure.title("时租房预定流程（带游戏机）测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "except_result"),
                             get_data('test_switch_hour_order', '../data/test_hour_order.yaml'))
    def test_switch_hour_order(self, name, phone, room_type, except_result):
        """
        租赁游戏机订单
        """
        with allure.step("时租房下单流程"):
            hotel_scheduled = self.main.goto_hour_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone).equipment_rental().select_switch()
        with allure.step("断言时租房费"):
            fee_result = hotel_scheduled.get_fee()
            room_rate = except_result.get("expect_result")[0].get("房费总额")
            value_added_services = except_result.get("expect_result")[1].get("增值服务")
            amount_paid = except_result.get("expect_result")[2].get("实付金额")
            assert fee_result == f'房费总额:\n{room_rate}\n增值服务:\n{value_added_services}\n实付金额:\n{amount_paid}', f'当前返回实际值为: {fee_result}'
        with allure.step("去支付"):
            pay_success = hotel_scheduled.goto_pay()
        with allure.step("跳转到订单详情"):
            time.sleep(4)
            pay_success.goto_order_detail()
        with allure.step("获取订单详情页面数据，并断言"):
            paid_result = self.order_detail.get_amount_paid()
            username_result = self.order_detail.get_username()
            switch_result = self.order_detail.get_switch()
            totel_paid = except_result.get("expect_result")[3].get("总价")
            room_user = except_result.get("expect_result")[4].get("入住人")
            assert paid_result == f"总价：{totel_paid}", f'当前返回的实际值为: {paid_result}'
            assert username_result == f"入住人：{room_user}", f'当前返回的实际值为:{username_result}'
            assert switch_result == f"(含游戏机租金30元)", f'当前返回的实际值为:{switch_result}'
        with allure.step("取消订单，释放房态"):
            self.order_detail.cancel_order()

    def teardown(self):
        self.routing.goto_main()
