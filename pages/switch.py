from pages.basepage import BasePage


class Switch(BasePage):
    """选择游戏机页面"""

    def select_switch(self):
        """
        选择游戏机
        """
        from pages.hotelscheduled import HotelScheduled
        self.step("../data/switch.yaml")
        return HotelScheduled(self._mini)
