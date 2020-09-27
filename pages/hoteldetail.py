from pages.basepage import BasePage
from pages.hotelscheduled import HotelScheduled


class HotelDetail(BasePage):
    """酒店列表页"""

    def goto_hotel_scheduled(self, room_type):
        """
        跳转到酒店预订页
        :return:
        """
        self._params['room_type'] = room_type
        self.step('../data/hotel_detail.yaml')
        return HotelScheduled(self._mini)
