from pages.basepage import BasePage
from pages.hotellist import HotelList


class Main(BasePage):
    """首页"""

    def goto_day_hotel_list(self):
        """
        跳转到酒店列表页
        :return:
        """
        self.step('../data/main.yaml')
        return HotelList(self._mini)

    def goto_hour_hotel_list(self):
        """
        选择时租房后，跳转到酒店列表页
        :return:
        """
        self.step('../data/main.yaml')
        return HotelList(self._mini)

    def goto_night_hotel_list(self):
        """
        选择时租房后，跳转到酒店列表页
        :return:
        """
        self.step('../data/main.yaml')
        return HotelList(self._mini)

    def set_day_date(self, start_date, end_date):
        """
         打开时间选择器，设置日租房预定时间
        :param start_date: 开始日期  ex 1
        :param end_date: 结束时间  ex 3
        :return:
        """
        self._params['start_date'] = start_date
        self._params['end_date'] = end_date
        self.step('../data/main.yaml')
        return Main(self._mini)