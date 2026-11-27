"""册·链式哈希账本单测：只追加、页页相衔、篡改现形。"""
import unittest

from xuanhengce.ce import Ce, GENESIS


class TestCe(unittest.TestCase):
    def test_append_links_chain(self):
        ce = Ce()
        e1 = ce.append({"n": 1})
        e2 = ce.append({"n": 2})
        self.assertEqual(e1["seq"], 1)
        self.assertEqual(e2["seq"], 2)
        self.assertEqual(e1["prev"], GENESIS)
        self.assertEqual(e2["prev"], e1["hash"])

    def test_verify_clean(self):
        ce = Ce()
        for n in range(5):
            ce.append({"n": n})
        self.assertEqual(ce.verify(), (True, None))
        self.assertEqual(len(ce), 5)

    def test_tamper_detected(self):
        ce = Ce()
        for n in range(5):
            ce.append({"n": n})
        # 篡改第二页记录，其后全链现形
        ce.entries[1]["record"]["n"] = 999
        ok, bad_seq = ce.verify()
        self.assertFalse(ok)
        self.assertEqual(bad_seq, 2)

    def test_tamper_hash_detected(self):
        ce = Ce()
        ce.append({"n": 1})
        ce.append({"n": 2})
        ce.entries[0]["hash"] = "f" * 64
        ok, bad_seq = ce.verify()
        self.assertFalse(ok)
        self.assertEqual(bad_seq, 1)

    def test_delete_detected(self):
        ce = Ce()
        for n in range(4):
            ce.append({"n": n})
        del ce.entries[1]
        ok, bad_seq = ce.verify()
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
