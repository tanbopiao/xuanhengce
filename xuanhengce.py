"""玄衡册（XUANHENGCE）· 全链路审计溯源账本

道统出处：元极恒一·道统构件定名册 V1.0 全量编译补录（代号避璇衡撞码取全拼） ｜ 第五批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：全链路审计溯源账本。

边界：本件为算子 v1——骨架桩已按命名映射补齐实现；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Xuanhengce:
    """玄衡册（XUANHENGCE）算子 v1。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "XUANHENGCE"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕
        self.chain = []
        self._seq = 0

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "xuanhengce",
            "cn": "玄衡册",
            "code": self.CODE,
            "duty": "全链路审计溯源账本",
            "mingwen": "玄衡录事，链上可溯",
            "anchor": self.ANCHOR,
        }

    def append(self, event):
        """玄衡录事：事件入链，只增不覆盖。"""
        import hashlib, json
        self._seq += 1
        prev = self.chain[-1]["hash"] if self.chain else "GENESIS"
        payload = json.dumps(event, sort_keys=True, ensure_ascii=False)
        entry = {"seq": self._seq, "event": event, "prev": prev,
                 "hash": hashlib.sha256(("%s|%s" % (prev, payload)).encode()).hexdigest()[:32]}
        self.chain.append(entry)
        self.events.append({"event": "append", "seq": entry["seq"]})
        return entry["seq"]

    def trace(self, seq):
        """链上可溯：按序取证。"""
        if seq < 1 or seq > len(self.chain):
            raise KeyError("链上无此序： %s" % seq)
        entry = self.chain[seq - 1]
        self.events.append({"event": "trace", "seq": seq})
        return entry
