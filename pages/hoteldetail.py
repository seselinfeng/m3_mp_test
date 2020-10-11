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

    def get_root_status(self, room_type):
        """
        获取当前房型的房态
        """
        self._params['room_type'] = room_type
        result = self.step('../data/hotel_detail.yaml')
        return result
