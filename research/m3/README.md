# M3 独立 AH / OU 研究

M3 是独立研究模型，不读取 M1、M2、MR1 的预测、订单、参数或账本。当前流程不产生正式交易信号、不发 Telegram、不自动提升模型，也没有增加交易 Gate。

## 研究入口与结果

- [完整研究验收报告](M3_RESEARCH_REPORT.md)
- [Crown 存档线级审计](M3_CROWN_STAGE_A_B_AUDIT.md)
- [Crown 离线证据录入契约](crown_evidence_contract.md)
- [最新 penaltyblog OOS 报告](results/latest_penaltyblog_oos_report.json)
- [最新时间切分清单](results/latest_penaltyblog_oos_splits.json)
- [最新 V4 原版指标](results/latest_v4_original_metrics.csv)
- [OpenFootball 无盘口影子 OOS 报告](results/openfootball/latest_oos_report.json)
- [OpenFootball 配对样本跨季稳定性审计](results/openfootball/latest_oos_stability.json)
- [稳定性审计复算器](openfootball_stability.py)
- [无重训稳定性 Actions 工作流](../../.github/workflows/m3-oos-stability.yml)
- [OpenFootball 影子运行收据](results/openfootball/latest_shadow_run.json)
- [OpenFootball 预测/结算追加式账本](results/openfootball/shadow_ledger.jsonl)
- 历史报告、预测 CSV 与参数快照在 `results/history/`、`results/predictions/`、`results/model_parameters/`。

稳定性工作流在 PR 分支完成 Actions run [39419131182](https://github.com/ljm198964-alt/quant-runner/actions/runs/39419131182) 与 [39419363464](https://github.com/ljm198964-alt/quant-runner/actions/runs/39419363464)：两次均运行现有产物分析和完整 M3 单元测试，不执行模型拟合；结果按 SHA 变化持久化。定时每四小时 UTC；PR 合并前 schedule 尚不在默认分支执行。

GitHub Actions 工作流 `.github/workflows/m3-independent-research.yml` 保持每 4 小时 UTC 运行，下载开源 Football Predictor V4 数据，按原项目流程执行 OU 模型，并对 penaltyblog 的 Poisson、Dixon-Coles、Bivariate Poisson 执行严格赛季前推 AH / OU 评估。每次运行记录输入文件 SHA-256、来源 commit、模型参数、预测文件哈希、时间切分、分数与前次报告比较；输入哈希相同会明确记录没有新增数据变化。

独立工作流 `.github/workflows/m3-openfootball-shadow.yml` 也配置为每 4 小时、手动和代码变更触发，使用 OpenFootball CC0 赛果/赛程分别运行三种 penaltyblog 进球模型，持久化严格赛季前推预测、逐次模型参数快照、运行历史与无盘口影子账本。它不下载或读取 Crown 报价，也不写正式账本。OpenFootball 日期没有文档化时区：具体开赛时间被忽略，影子预测只接纳源日历日期至少晚于运行 UTC 日期 3 天的 fixture。B1 在此数据源缺席。工作流已在 PR 分支经 Actions 验收；定时 schedule 只有在进入默认分支后才会生效。

## 重要口径

Football-Data.co.uk 历史赛果仅提供日期（无精确开赛时间），训练集排除测试赛季首场比赛所在的整个 UTC 日期；训练仅使用更早赛季文件且比赛日期严格早于测试截止。该数据源文件中的赔率列不会被 penaltyblog 流程读取。未知训练球队不生成伪预测，而记录为未覆盖。

penaltyblog 目前的 AH 评价为 AH 0.0（主队 DNB）三状态概率；OU 评价为固定 O2.5。由于当前没有 Crown 的同期有效盘线和双边水位，二者只是模型概率诊断，不是具体 Crown 下注结果，ROI、收益和回撤均为空。其他来源的赔率不能代替 Crown。

Football Predictor V4 的 ROI 列只还原其上游研究阈值和原数据赔率，不能称作 Crown ROI，也不能作为 M3 正式交易规则。该上游仓库当前检出版本未发现显式许可证文件；M3 不复制其源代码，工作流按原项目入口运行，并将许可限制记录在报告中。

OpenFootball 评估的 AH 只报告 AH0/DNB 三状态概率，OU 报告固定 O2.5；目前影子账本尚无 Crown 盘口、EV、ROI 或可计算回撤。原始 OpenFootball 日期键不代表精确 kickoff UTC。

稳定性 JSON 对同一 OOS 集按模型、赛季、联赛和联赛×赛季列出 AH0 三类与 O2.5 的 `(预测均值−实际发生率)`，用于观察概率误差集中在哪些子组。当前 O2.5 全量低估约 2.09–2.40 pp；D1 低估 5.15–5.35 pp，I1 与 SP1 接近零。2026/27 部分赛季 n=199 时低估约 10 pp，样本不足以支持稳定结论。此诊断不进行事后概率修正或交易筛选。

逐组误差扩展在 Actions run [39420905826](https://github.com/ljm198964-alt/quant-runner/actions/runs/39420905826) 验收成功，33 项测试通过并将 JSON 保存到公开分支提交 `a28d0b0`。原输入 fingerprint 与 source OOS report 时间未变，workflow 只复算保存的预测，没有重新拟合。

账本 append-only，保留了首次版本身份实现造成的重复预测历史行；随后 4,215 条以 `FORECAST_DUPLICATE_SUPERSEDED` 标记为重复。报告按唯一 forecast key 计有效预测，账本不会把 superseded 行再次计分/结算。修复后的重复 Actions run 已验证新预测、结算、重复修正均为 0，ledger SHA 不变；详情见完整验收报告。

`openfootball_shadow_audit.py` 在不拟合、不结算的情况下校验逻辑 forecast 键唯一、supersession 引用、UTC 预测时间和日期 guard、概率归一化、无 Crown 时 EV/ROI 为空及无正式单/TG。当前 ledger 有 8,430 条原始 FORECAST 行，其中 4,215 条明确 superseded，折为 4,215 条有效逻辑预测；零结算、零 Crown 快照、零 EV/ROI。该审计随 Saved OOS Stability 工作流每四小时运行并持久化 `results/openfootball/latest_shadow_ledger_audit.json`，且验证 ledger SHA 与当时账本一致。Actions run [39420305676](https://github.com/ljm198964-alt/quant-runner/actions/runs/39420305676) 于 2026-10-20 SUCCESS，33 项测试通过，上传 artifact 与仓库审计 JSON 一致。该 workflow 只读既存 OOS 产物及 ledger，不重新训练。

如获得书面授权，可用 `crown_totalcorner_import.py` 在本地离线读取既存 TotalCorner Crown API 响应；它要求 IANA 时区证据、精确队伍身份与独立 UTC kickoff、过滤所有不满足赛前条件的移动记录，并且拒绝 DST 歧义及未定义复合线。该 adapter 不联网、不打印或落库价格、不计算 EV/ROI；合成测试只验证转换逻辑，并不增加真实 Crown 覆盖。当前未提供书面授权，因此未执行任何新 Crown 请求。 本适配器提交 `feb6f4dfabb19653bbedaaba2a212644e86a85d0` 已由 Actions [39421816343](https://github.com/ljm198964-alt/quant-runner/actions/runs/39421816343) 真实验收，40 项 M3 tests 通过；该 workflow 是无重训审计，未新增数据或 Crown 覆盖。

运行单元测试：

```bash
python -m unittest discover -s research/m3 -p 'test_*.py' -v
```
