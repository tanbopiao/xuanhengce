"""溯·回放追踪单测：按主体、时间窗、衡级取交集。"""
import unittest

from xuanhengce.ce import Ce
from xuanhengce.heng import Heng
from xuanhengce.su import Su


def build_entries():
    ce = Ce()
    heng = Heng(key=b"test-key")
    ce.append(heng.weigh({"act": "登录"}, subject="甲", ts=10.0))
    ce.append(heng.weigh({"act": "删库"}, subject="乙", ts=20.0, weight=9))
    ce.append(heng.weigh({"act": "导出"}, subject="甲", ts=30.0, weight=3))
    return ce.entries


class TestSu(unittest.TestCase):
    def setUp(self):
        self.entries = build_entries()
        self.su = Su()

    def test_no_filter_returns_all(self):
        self.assertEqual(len(self.su.replay(self.entries)), 3)

    def test_by_subject(self):
        pages = self.su.replay(self.entries, subject="甲")
        self.assertEqual([p["seq"] for p in pages], [1, 3])

    def test_by_time_window(self):
        pages = self.su.replay(self.entries, start=15.0, end=25.0)
        self.assertEqual([p["seq"] for p in pages], [2])

    def test_window_excludes_untimestamped(self):
        entries = build_entries()
        entries[1]["record"]["ts"] = None
        pages = self.su.replay(entries, start=0, end=100)
        self.assertEqual([p["seq"] for p in pages], [1, 3])

    def test_by_grade(self):
        pages = self.su.replay(self.entries, grade="重")
        self.assertEqual([p["seq"] for p in pages], [2])

    def test_combined_filters_intersect(self):
        pages = self.su.replay(self.entries, subject="甲", grade="要")
        self.assertEqual([p["seq"] for p in pages], [3])


if __name__ == "__main__":
    unittest.main()
