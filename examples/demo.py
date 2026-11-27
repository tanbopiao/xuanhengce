"""玄衡册演示：一次登录审计的全链路——衡→册→溯。

运行：python3 examples/demo.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xuanhengce import XuanhengceLedger


def main():
    ledger = XuanhengceLedger(key=b"demo-key", clock=lambda: 1700000000.0)

    # 衡→册：录三件事，权重不同、衡级不同
    ledger.record({"act": "登录", "by": "甲"}, subject="甲")
    ledger.record({"act": "批量导出", "rows": 5000}, subject="甲", weight=4)
    ledger.record({"act": "删除账户", "target": "乙"}, subject="丙", weight=9)

    # 册：验册——只追加、篡改现形
    ok, bad = ledger.verify()
    print("验册：", "完整" if ok else "第 %s 页被篡改" % bad)
    print("册页数：", len(ledger.ce))

    # 溯：按主体回放
    print("\n按主体「甲」回放：")
    for page in ledger.replay(subject="甲"):
        r = page["record"]
        print("  第%s页 [%s] %s" % (page["seq"], r["grade"], r["event"]))

    # 溯：按衡级回放重事
    print("\n按衡级「重」回放：")
    for page in ledger.replay(grade="重"):
        r = page["record"]
        print("  第%s页 %s（主体：%s）" % (page["seq"], r["event"], r["subject"]))


if __name__ == "__main__":
    main()
