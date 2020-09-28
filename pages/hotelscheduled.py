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
        self.step('../data/hotel_scheduled.yaml')

    def goto_pay(self):
        """
        去支付
        :return: HotelScheduled
        """
        self.step('../data/hotel_scheduled.yaml')
        return HotelScheduled(self._mini)
