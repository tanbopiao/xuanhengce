"""璇衡策（XUANHENGCE）算子单测：名帖完整、行为达标、只增不覆盖。"""
import unittest

from xuanhengce import Xuanhengce


class TestXuanhengce(unittest.TestCase):
    def setUp(self):
        self.op = Xuanhengce()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "xuanhengce")
        self.assertEqual(d["code"], "XUANHENGCE")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_append_trace(self):
        s1 = self.op.append({"act": "一"})
        s2 = self.op.append({"act": "二"})
        self.assertEqual(s2, s1 + 1)
        entry = self.op.trace(s2)
        self.assertEqual(entry["prev"], self.op.trace(s1)["hash"])
        with self.assertRaises(KeyError):
            self.op.trace(99)


if __name__ == "__main__":
    unittest.main()
