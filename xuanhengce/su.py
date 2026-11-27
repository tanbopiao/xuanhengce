"""溯·回放追踪

「溯」＝顺流讨源。册已留痕，溯以三把筛子取证：
按主体（谁做的）、按时间窗（何时做的）、按衡级（事情多大）。
筛子可单用可合用，合用取交集。
"""


class Su:
    """溯：回放追踪算子。"""

    @staticmethod
    def replay(entries, subject=None, start=None, end=None, grade=None):
        """从册页中回放：返回满足全部筛选条件的册页列表（保持页序）。

        subject：按记录主体取；
        start / end：按记录时间窗取（含端点；无时间戳的页不入选）；
        grade：按衡级（常/要/重）取。
        """
        out = []
        for entry in entries:
            record = entry["record"]
            if subject is not None and record.get("subject") != subject:
                continue
            if grade is not None and record.get("grade") != grade:
                continue
            ts = record.get("ts")
            if start is not None and (ts is None or ts < start):
                continue
            if end is not None and (ts is None or ts > end):
                continue
            out.append(entry)
        return out
