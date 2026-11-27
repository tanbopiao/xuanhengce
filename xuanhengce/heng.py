"""衡·事件称量

「玄衡」＝玄色天平，称量裁断。凡入册之事，先过衡：
分级（常/要/重）、加权、签名（HMAC-SHA256），有衡方可入册。

边界：签名密钥由调用方注入，缺省键仅用于演示与自测，生产使用必须自带密钥；
凭据不入档。
"""

import hashlib
import hmac
import json

# 衡制三等：常（例行）、要（须留意的）、重（须追责的）
GRADES = ("常", "要", "重")


class Heng:
    """衡：事件称量算子——分级、加权、签名。"""

    def __init__(self, key=None):
        # 缺省键只保证开箱可跑；生产场景必须传入自有密钥。
        self._key = key if key is not None else b"xuanhengce-default-key"

    def weigh(self, event, weight=None, subject=None, ts=None):
        """称一事件：定权重、定衡级、出签名，返回待入册的记录。"""
        if weight is None:
            weight = 1
        weight = int(weight)
        if weight < 1:
            raise ValueError("权重至少为一，收到：%s" % weight)
        payload = json.dumps(event, sort_keys=True, ensure_ascii=False)
        signature = hmac.new(self._key, payload.encode("utf-8"),
                             hashlib.sha256).hexdigest()
        return {
            "event": event,
            "subject": subject,
            "ts": ts,
            "weight": weight,
            "grade": self.grade_of(weight),
            "signature": signature,
        }

    @staticmethod
    def grade_of(weight):
        """衡级：一至二为常，三至六为要，七及以上为重。"""
        if weight >= 7:
            return "重"
        if weight >= 3:
            return "要"
        return "常"
