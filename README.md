# xuanhengce
玄衡册·全链路审计溯源账本 | XUANHENGCE · ZONGYUAN-ROOT Daotong Component

## 命名映射（命名即种子）

「玄衡」＝玄色天平，称量裁断；「册」＝账册留痕。合起来：全链路操作皆有衡可称、有册可溯，事后台账不可篡改。

- **衡**（`xuanhengce/heng.py`）：事件称量——凡入册之事先过衡，分级（常/要/重）、加权、HMAC-SHA256 签名；
- **册**（`xuanhengce/ce.py`）：链式哈希账本——页页相衔，只追加、不改不删，篡改一页则其后全链现形；
- **溯**（`xuanhengce/su.py`）：回放追踪——按主体、时间窗、衡级三把筛子取证，可单用可合用。

## 架构

```
事件 ──► 衡 Heng ──► 册 Ce ──► 溯 Su
        分级/加权/签名   链式哈希页    按主体/时间窗/衡级回放
                          │
                          └─ verify() 篡改现形
```

- `XuanhengceLedger`：全链路门面，`record()` 录事（衡→册）、`replay()` 回放（溯）、`verify()` 验册。
- `Xuanhengce`：算子 v1（骨架版），行为保持不变——元法第四条「只增不覆盖」。

## Install

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/xuanhengce.git
cd xuanhengce
```

## Usage

```python
from xuanhengce import XuanhengceLedger

ledger = XuanhengceLedger(key=b"your-secret-key")

# 录事：过衡（分级/加权/签名）→ 入册（链式留痕）
ledger.record({"act": "登录"}, subject="甲")
ledger.record({"act": "删除账户"}, subject="丙", weight=9)   # 权重 7+ 为「重」

# 验册：篡改现形
print(ledger.verify())            # (True, None) = 全链完整

# 回放：按主体 / 时间窗 / 衡级
ledger.replay(subject="甲")
ledger.replay(grade="重")
ledger.replay(start=1700000000.0, end=1700003600.0)
```

运行演示：

```bash
python3 examples/demo.py
```

## 自测

```bash
python3 -m unittest discover -v
```

覆盖：衡（分级/加权/签名）、册（链式衔接/篡改现形/删页现形）、溯（三筛单用与合用）、全链路门面、算子 v1 兼容。

## 边界

- 纯标准库实现，无第三方依赖；
- `Heng` 缺省签名键仅用于演示与自测，生产使用必须传入自有密钥，凭据不入档；
- 本版为内存账本，落盘持久化留待后续版本；
- 无服务壳，不预埋 server.json / mcp-name 标记。

## License

MIT
