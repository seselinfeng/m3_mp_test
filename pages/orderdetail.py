from pages.basepage import BasePage


class OrderDetail(BasePage):
    """订单详情页"""

    def get_amount_paid(self):
        """
        获取总价
        """
        result = self.step('../data/order_detail.yaml')
        return result

    def get_username(self):
        """
        获取入住人
        """
        result = self.step('../data/order_detail.yaml')
        return result

    def get_switch(self):
        """
        获取游戏机信息
        """
        result = self.step('../data/order_detail.yaml')
        return result
