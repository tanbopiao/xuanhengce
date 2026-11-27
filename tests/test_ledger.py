"""玄衡册全链路门面单测：衡→册→溯一条道，兼容算子 v1。"""
import unittest

from xuanhengce import Xuanhengce, XuanhengceLedger


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        self.now += 10.0
        return self.now


class TestXuanhengceLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = XuanhengceLedger(key=b"test-key", clock=FakeClock())

    def test_full_flow(self):
        self.ledger.record({"act": "登录"}, subject="甲")
        page = self.ledger.record({"act": "删库"}, subject="乙", weight=9)
        self.assertEqual(page["seq"], 2)
        self.assertEqual(page["record"]["grade"], "重")
        self.assertTrue(page["record"]["ts"] > 0)

    def test_verify_and_replay(self):
        self.ledger.record({"act": "一"}, subject="甲")
        self.ledger.record({"act": "二"}, subject="乙", weight=5)
        self.assertEqual(self.ledger.verify(), (True, None))
        pages = self.ledger.replay(subject="乙")
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]["record"]["event"], {"act": "二"})

    def test_tamper_surface_through_facade(self):
        self.ledger.record({"act": "一"})
        self.ledger.record({"act": "二"})
        self.ledger.ce.entries[0]["record"]["event"] = {"act": "改"}
        ok, bad_seq = self.ledger.verify()
        self.assertFalse(ok)
        self.assertEqual(bad_seq, 1)


class TestV1Compat(unittest.TestCase):
    """算子 v1 行为保持：只增不覆盖。"""

    def test_v1_untouched(self):
        op = Xuanhengce()
        d = op.describe()
        self.assertEqual(d["repo"], "xuanhengce")
        s1 = op.append({"act": "一"})
        s2 = op.append({"act": "二"})
        self.assertEqual(s2, s1 + 1)
        self.assertEqual(op.trace(s2)["prev"], op.trace(s1)["hash"])
        with self.assertRaises(KeyError):
            op.trace(99)


if __name__ == "__main__":
    unittest.main()
