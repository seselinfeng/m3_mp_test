from pages.basepage import BasePage


class HotelScheduled(BasePage):
    """酒店预订页"""

    def save_order(self, name, phone):
        """
        预订订单
        :return:
        """
        self._params["name"] = name
        self._params["phone"] = phone
        self.step('../data/hotel_scheduled.yaml')
        self.app.restart()
        return HotelScheduled(self._mini)
