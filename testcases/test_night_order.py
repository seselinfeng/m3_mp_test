import time
import allure
import pytest

from common.processingdata import get_data
from pages.app import App


@allure.feature("整夜房预定订单模块")
class TestNightOrder:
    def setup(self):
        self.app = App()
        self.main = self.app.start().main()
        self.my = self.app.start().my()
        self.routing = self.app.start().routing()
        self.order_list = self.app.start().order_list()
        self.order_detail = self.app.start().order_detail()

    @allure.title("整夜房当日预定流程测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "except_result"),
                             get_data('test_night_order', '../data/pro_data/test_overnight_order.yaml'))
    def test_night_order(self, name, phone, room_type, except_result):
        """
        整夜房预定当日酒店流程测试
        :param name: 入住人
        :param phone: 电话号码
        :param room_type: 房型名称
        :param except_result: 期望结果集
        :return: None
        """
        with allure.step(f"{room_type}-整夜房下单流程"):
            hotel_scheduled = self.main.goto_night_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone)
        with allure.step("校验整夜房费是否正确"):
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

    @allure.title("整夜房预定流程（带游戏机）测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "except_result"),
                             get_data('test_switch_night_order', '../data/pro_data/test_overnight_order.yaml'))
    def test_switch_night_order(self, name, phone, room_type, except_result):
        """
        租赁游戏机订单
        :param name: 入住人
        :param phone: 电话号码
        :param room_type: 房型名称
        :param except_result: 期望结果集
        :return: None
        """
        with allure.step("整夜房下单流程"):
            hotel_scheduled = self.main.goto_night_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone).equipment_rental().select_switch()
        with allure.step("断言整夜房费"):
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

    @allure.title("整夜房房态已满测试")
    @pytest.mark.skip
    @pytest.mark.parametrize(("name", "phone", "room_type", "room_code", "except_result"),
                             get_data('test_night_nh_order', '../data/pro_data/test_overnight_order.yaml'))
    def test_night_nh_order(self, name, phone, room_type, room_code, except_result):
        """
        整夜房房态已满测试
        :param name: 入住人
        :param phone: 电话号码
        :param room_type: 房型名称
        :param room_code: 房型编码
        :param except_result: 期望结果集
        :return: None
        """
        with allure.step(f"{room_type}-整夜下单流程"):
            hotel_scheduled = self.main.goto_night_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone)
        with allure.step("校验整夜房费是否正确"):
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
            result = self.main.tap_night().tap_search_hotels().goto_hotel_detail().get_root_status(room_code)
            assert result == '满房', f"当前实际返回值为{result}"

    @allure.title("整夜房选择前一天预定测试")
    @pytest.mark.parametrize(("yesterday_date", "except_result"),
                             get_data('test_yesterday_order', '../data/pro_data/test_overnight_order.yaml'))
    def test_yesterday_order(self, yesterday_date, except_result):
        """
        测试前一天是否可选
        :param yesterday_date: 昨天日期
        :param except_result: 期望结果集
        :return: None
        """
        with allure.step(f"{yesterday_date[0]} 日：整夜房下单流程"):
            self.main.tap_night()
            self.main.tap_night_time_select()
            result = self.main.get_night_yesterday_date(yesterday_date[0])
        assert except_result == result[0]

    @allure.title("整夜房远期预定流程测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "start_date", "end_date", "except_result"),
                             get_data('test_forward_night_order', '../data/pro_data/test_overnight_order.yaml'))
    def test_forward_night_order(self, name, phone, room_type, start_date, end_date, except_result):
        """
        远期预定流程
        :param name: 入住人
        :param phone: 电话号码
        :param room_type: 房型名称
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param except_result: 期望结果集
        :return: None
        """
        with allure.step(f"{start_date}日：{room_type}-整夜房下单流程"):
            hotel_scheduled = self.main.set_night_date(
                start_date, end_date).tap_search_hotels().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name,
                                      phone)
        with allure.step("校验整夜房费是否正确"):
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

    @allure.title("整夜房远期预定游戏机选择测试")
    @pytest.mark.parametrize(("name", "phone", "room_type", "start_date", "end_date", "except_result"),
                             get_data('test_switch_forward_night_order', '../data/pro_data/test_overnight_order.yaml'))
    def test_switch_forward_night_order(self, name, phone, room_type, start_date, end_date, except_result):
        """
        选择远期、选择游戏机测试
        :param name: 入住人
        :param phone: 电话号码
        :param room_type: 房型名称
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param except_result: 期望结果集
        :return: None
        """
        with allure.step(f"{start_date}日：{room_type}-整夜房下单流程"):
            hotel_scheduled = self.main.set_night_date(
                start_date, end_date).tap_search_hotels().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name,
                                      phone).equipment_rental().select_switch()
        with allure.step("断言整夜房费"):
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
        time.sleep(1)
