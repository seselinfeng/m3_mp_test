from pages.basepage import BasePage
from pages.orderlist import OrderList


class My(BasePage):
    """我的"""
    def goto_order_list(self):
        self.step('../data/my.yaml')
        return OrderList(self._mini)
