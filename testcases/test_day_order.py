import time
import allure
import pytest

from common.processingdata import get_data
from pages.app import App


class TestDayOrder:
    def setup(self):
        self.app = App()
        self.main = self.app.start().main()
        self.my = self.app.start().my()
        self.routing = self.app.start().routing()
        self.order_list = self.app.start().order_list()
        self.order_detail = self.app.start().order_detail()

    @allure.title("日租房当日预定流程")
    @pytest.mark.parametrize(("name", "phone", "room_type"), get_data('test_day_order', '../data/test_order.yaml'))
    def test_day_order(self, name, phone, room_type):
        with allure.step("日租房下单流程"):
            hotel_scheduled = self.main.goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name, phone)
        with allure.step("断言日租房费"):
            fee_result = hotel_scheduled.get_fee()
            room_rate = '1.00'
            preferential_amount = '0.00'
            amount_paid = '1.00'
            assert fee_result == f'房费总额：¥{room_rate}\n优惠金额： ¥{preferential_amount}\n实付金额：¥{amount_paid}', f'当前返回实际值为: 房费总额：¥{room_rate}\n优惠金额： ¥{preferential_amount}\n实付金额：¥{amount_paid}'
        with allure.step("去支付"):
            hotel_scheduled.goto_pay()
        time.sleep(5)
        with allure.step("跳转到订单详情"):
            hotel_scheduled.goto_order_detail()
        with allure.step("获取订单详情页面数据，并断言"):
            paid_result = self.order_detail.get_amount_paid()
            username_result = self.order_detail.get_username()
            assert paid_result == f"总价：¥{amount_paid}", f'当前返回的实际值为: 总价：¥{amount_paid}'
            assert username_result == f"入住人：{name}", f'当前返回的实际值为:入住人：{name} '

    @allure.title("日租房远期预定流程")
    @pytest.mark.parametrize(("name", "phone", "room_type", "start_date", "end_date"),
                             get_data('test_forward_day_order', '../data/test_order.yaml'))
    def test_forward_day_order(self, name, phone, room_type, start_date, end_date):
        with allure.step("日租房下单流程"):
            hotel_scheduled = self.main.set_day_date(start_date,
                                                     end_date).goto_day_hotel_list().goto_hotel_detail().goto_hotel_scheduled(
                room_type).save_order(name,
                                      phone)
        with allure.step("断言日租房费"):
            fee_result = hotel_scheduled.get_fee()
            room_rate = '1.00'
            preferential_amount = '0.00'
            amount_paid = '2.00'
            assert fee_result == f'房费总额：¥{room_rate}\n优惠金额： ¥{preferential_amount}\n实付金额：¥{amount_paid}', f'当前返回实际值为: 房费总额：¥{room_rate}\n优惠金额： ¥{preferential_amount}\n实付金额：¥{amount_paid}'
        with allure.step("去支付"):
            hotel_scheduled.goto_pay()
        time.sleep(10)
        with allure.step("跳转到订单详情"):
            hotel_scheduled.goto_order_detail()
        with allure.step("获取订单详情页面数据，并断言"):
            paid_result = self.order_detail.get_amount_paid()
            username_result = self.order_detail.get_username()
            assert paid_result == f"总价：¥{amount_paid}", f'当前返回的实际值为: 总价：¥{amount_paid}'
            assert username_result == f"入住人：{name}", f'当前返回的实际值为:入住人：{name} '

    def teardown(self):
        self.routing.goto_my()
