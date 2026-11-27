"""册·链式哈希账本

「册」＝账册留痕。页页相衔：每页哈希罩住前页哈希与本页记录，
只追加、不改不删，篡改一页则其后全链现形。

边界：内存账本，落盘持久化留待后续版本；本版只保证链式完整可验。
"""

import hashlib
import json

GENESIS = "GENESIS"


class Ce:
    """册：链式哈希账本——只追加，篡改现形。"""

    def __init__(self):
        self.entries = []

    def append(self, record):
        """录一页：页序、前页哈希、本页哈希、记录。返回该页。"""
        prev = self.entries[-1]["hash"] if self.entries else GENESIS
        payload = json.dumps(record, sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(("%s|%s" % (prev, payload)).encode("utf-8")).hexdigest()
        entry = {"seq": len(self.entries) + 1, "prev": prev,
                 "hash": digest, "record": record}
        self.entries.append(entry)
        return entry

    def verify(self):
        """验册：逐页重算哈希。完整返回 (True, None)；
        被篡改返回 (False, 首处破页序号)。"""
        prev = GENESIS
        for entry in self.entries:
            payload = json.dumps(entry["record"], sort_keys=True, ensure_ascii=False)
            expect = hashlib.sha256(
                ("%s|%s" % (prev, payload)).encode("utf-8")).hexdigest()
            if entry["prev"] != prev or entry["hash"] != expect:
                return False, entry["seq"]
            prev = entry["hash"]
        return True, None

    def __len__(self):
        return len(self.entries)
