from pages.basepage import BasePage
from pages.paysuccess import PaySuccess
from pages.switch import Switch


class HotelScheduled(BasePage):
    """酒店预订页"""

    def save_order(self, name, phone):
        """
        预订订单
        :return:HotelScheduled
        """
        self._params["name"] = name
        self._params["phone"] = phone
        self.step('../data/hotel_scheduled.yaml')
        return HotelScheduled(self._mini)

    def equipment_rental(self):
        """
        设备租赁
        """
        self.step('../data/hotel_scheduled.yaml')
        return Switch(self._mini)

    def get_fee(self):
        """
        获取费用明细
        """
        result = {}
        result = self.step('../data/hotel_scheduled.yaml')
        return result

    def goto_pay(self):
        """
        去支付
        :return: HotelScheduled
        """
        self.step('../data/hotel_scheduled.yaml')
        # mock 支付接口
        mock_location = {"errMsg": "requestPayment:ok"}
        self._mini.app.mock_wx_method("requestPayment", result=mock_location)
        return PaySuccess(self._mini)

    def goto_pay_fail(self):
        """
        支付失败
        """
        return self.call_js_method("checkSubmitOrder")

    def get_switch(self):
        """
        判断是否存在switch机租赁模块
        """
        result = self.step('../data/hotel_scheduled.yaml')
        return result
