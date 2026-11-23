"""玄衡册（XUANHENGCE）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
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

    def test_append_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.append(None)

    def test_trace_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.trace(None)


if __name__ == "__main__":
    unittest.main()
