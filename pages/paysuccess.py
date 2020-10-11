from pages.basepage import BasePage
from pages.orderdetail import OrderDetail


class PaySuccess(BasePage):
    """订单支付成功页面"""

    def goto_order_detail(self):
        self.step('../data/pay_success.yaml')
        return OrderDetail(self._mini)
