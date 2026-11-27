"""衡·事件称量单测：分级、加权、签名。"""
import unittest

from xuanhengce.heng import Heng, GRADES


class TestHeng(unittest.TestCase):
    def setUp(self):
        self.heng = Heng(key=b"test-key")

    def test_default_weight_is_one(self):
        record = self.heng.weigh({"act": "读"})
        self.assertEqual(record["weight"], 1)
        self.assertEqual(record["grade"], "常")

    def test_grades(self):
        self.assertEqual(GRADES, ("常", "要", "重"))
        self.assertEqual(Heng.grade_of(1), "常")
        self.assertEqual(Heng.grade_of(2), "常")
        self.assertEqual(Heng.grade_of(3), "要")
        self.assertEqual(Heng.grade_of(6), "要")
        self.assertEqual(Heng.grade_of(7), "重")
        self.assertEqual(Heng.grade_of(99), "重")

    def test_weight_must_be_positive(self):
        with self.assertRaises(ValueError):
            self.heng.weigh({"act": "x"}, weight=0)

    def test_signature_deterministic_and_key_bound(self):
        a = Heng(key=b"k1").weigh({"act": "写"})["signature"]
        b = Heng(key=b"k1").weigh({"act": "写"})["signature"]
        c = Heng(key=b"k2").weigh({"act": "写"})["signature"]
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(len(a), 64)

    def test_subject_and_ts_carried(self):
        record = self.heng.weigh({"act": "删"}, subject="甲", ts=100.0)
        self.assertEqual(record["subject"], "甲")
        self.assertEqual(record["ts"], 100.0)


if __name__ == "__main__":
    unittest.main()
