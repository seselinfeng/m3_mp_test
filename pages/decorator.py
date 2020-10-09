import time
import datetime

import allure
from common.log import Log

log = Log()


def handle_black(func):
    """
    黑名单处理
    :param func:
    :return:
    """

    def handle(*args, **kwargs):
        from pages.basepage import BasePage
        # 首次进入隐私协议黑名单
        _black_list = [
        ]
        # 最大重试次数
        _max_error_count = 3
        # 失败次数初始化
        _error_count = 0
        # 拿到BasePage实例对象
        instance: BasePage = args[0]
        log.info("run " + func.__name__ + "\n args: \n" + repr(args) + "\n" + repr(kwargs))
        element = func(*args, **kwargs)
        # 重置失败次数
        _error_count = 0
        time.sleep(5)
        if element:
            return element
        else:
            # 错误日志
            log.info("element not found, handle black list")
            # 错误截图
            filename = "%s.png" % datetime.datetime.now().strftime("%H%M%S%f")
            instance._mini.app.screen_shot(save_path=f"../screenshot/{filename}")
            with open(f"{filename}", "rb") as f:
                content = f.read()
            allure.attach(content, attachment_type=allure.attachment_type.PNG)
            # 缩短隐式等待时间，优化速度
            time.sleep(2)
            # 如果超出最大处理次数，抛出异常
            if _error_count > _max_error_count:
                raise Exception
            _error_count += 1
            # 判断获取到的元素是否属于黑名单
            for ele in _black_list:
                # 找出元素
                elementlist = instance.finds(*ele)
                # 如果黑名单元素存在，获取该元素并点击处理
                if len(elementlist) > 0:
                    elementlist[0].click()
                    return handle(*args, **kwargs)
            raise Exception

    return handle
