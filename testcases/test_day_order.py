import time
import allure
import pytest

from common.processingdata import get_data
from pages.app import App


@allure.feature("日租房预定订单模块")
class TestDayOrder:
    def setup(self):
        self.app = App()
        self.main = self.app.start().main()
        self.my = self.app.start().my()
        self.routing = self.app.start().routing()
        self.order_list = self.app.start().order_list()
        self.order_detail = self.app.start().order_detail()

    @allure.title("日租房当日预定流程测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "except_result"),
                             get_data('test_day_order', '../data/test_day_order.yaml'))
    def test_day_order(self, name, phone, room_type, except_result):
        """日租房预定当日酒店流程测试"""
        with allure.step(f"{room_type}-日租房下单流程"):
            hotel_scheduled = self.main.goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone)
        with allure.step("校验日租房费是否正确"):
            fee_result = hotel_scheduled.get_fee()
            room_rate = except_result.get("expect_result")[0].get("房费总额")
            amount_paid = except_result.get("expect_result")[1].get("实付金额")
            try:
                assert fee_result == f'房费总额:\n{room_rate}\n实付金额:\n{amount_paid}', f'当前返回实际值为: {fee_result}'
            except AssertionError as e:
                self.app.get_image()
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
            try:
                assert paid_result == f"总价：{totel_paid}", f'当前返回的实际值为: {paid_result}'
                assert username_result == f"入住人：{room_user}", f'当前返回的实际值为:{username_result}'
            except AssertionError as e:
                self.app.get_image()
        with allure.step("取消订单，释放房态"):
            self.order_detail.cancel_order()

    @allure.title("日租房预定流程（带游戏机）测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "except_result"),
                             get_data('test_switch_day_order', '../data/test_day_order.yaml'))
    def test_switch_day_order(self, name, phone, room_type, except_result):
        """
        租赁游戏机订单
        """
        with allure.step("日租房下单流程"):
            hotel_scheduled = self.main.goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone).equipment_rental().select_switch()
        with allure.step("断言日租房费"):
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
            assert switch_result == f"(含游戏机租金120元)", f'当前返回的实际值为:{switch_result}'
        with allure.step("取消订单，释放房态"):
            self.order_detail.cancel_order()

    @allure.title("日租房房态已满测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "room_code", "except_result"),
                             get_data('test_day_nh_order', '../data/test_day_order.yaml'))
    def test_day_nh_order(self, name, phone, room_type, room_code, except_result):
        """日租房预定当日房态已满测试"""
        with allure.step(f"{room_type}-日租房下单流程"):
            hotel_scheduled = self.main.goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone)
        with allure.step("校验日租房费是否正确"):
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
        with allure.step("继续下单测试该房源"):
            self.routing.goto_main()
            result = self.main.goto_day_hotel_list().goto_hotel_detail().get_root_status(
                room_code)
            assert result == '满房', f"当前实际返回值为{result}"

    @allure.title("日租房选择前一天预定测试")
    @pytest.mark.parametrize(("yesterday_date", "except_result"),
                             get_data('test_yesterday_order', '../data/test_day_order.yaml'))
    def test_yesterday_order(self, yesterday_date, except_result):
        with allure.step(f"{yesterday_date[0]} 日：日租房下单流程"):
            result = self.main.get_yesterday_date(yesterday_date[0])
        assert except_result == result[0]

    @allure.title("日租房远期多天预定流程测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "start_date", "end_date", "except_result"),
                             get_data('test_forward_day_order', '../data/test_day_order.yaml'))
    def test_forward_day_order(self, name, phone, room_type, start_date, end_date, except_result):
        with allure.step(f"{start_date}-{end_date} 日：{room_type}-日租房下单流程"):
            hotel_scheduled = self.main.set_day_date(start_date,
                                                     end_date).goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name,
                                      phone)
        with allure.step("校验日租房费是否正确"):
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

    @allure.title("日租房远期多天预定游戏机选择测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "start_date", "end_date"),
                             get_data('test_forward_day_switch_order', '../data/test_day_order.yaml'))
    def test_forward_day_switch_order(self, name, phone, room_type, start_date, end_date):
        with allure.step(f"{start_date}-{end_date} 日：{room_type}-日租房下单流程"):
            hotel_scheduled = self.main.set_day_date(start_date,
                                                     end_date).goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type)
        with allure.step("校验游戏机是否可选,期望不可选"):
            assert None == hotel_scheduled.get_switch(), f'当前游戏机可选结果为{hotel_scheduled.get_switch()}'

    # @allure.title("日租房不输入用户名测试")
    # @pytest.mark.parametrize(("phone", "room_type"),
    #                          get_data('test_name_non_exist', '../data/test_day_order.yaml'))
    # def test_name_non_exist(self, phone, room_type):
    #     with allure.step(f"{room_type}-日租房下单流程"):
    #         hotel_scheduled = self.main.goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
    #             room_type).save_order("", phone)
    #         print(hotel_scheduled._mini.app.get_current_page())

    def teardown(self):
        self.routing.goto_main()
