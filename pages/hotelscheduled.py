from pages.basepage import BasePage


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

    def get_fee(self):
        """
        获取费用明细
        """
        result = {}
        self.step('../data/hotel_scheduled.yaml')

    def goto_pay(self):
        """
        去支付
        :return: HotelScheduled
        """
        self.step('../data/hotel_scheduled.yaml')
        # mock 支付接口
        mock_location = {"appId": None}
        self._mini.app.mock_wx_method("requestPayment", result=mock_location)
        return HotelScheduled(self._mini)
