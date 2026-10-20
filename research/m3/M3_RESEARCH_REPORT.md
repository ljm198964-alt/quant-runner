# M3 独立 AH / OU 研究验收

报告生成时间：2026-10-20 UTC。研究目标是完成独立研究系统，不启用正式投注。

## 状态摘要

- **AH：** penaltyblog Poisson、Dixon-Coles、Bivariate Poisson 已在真实赛果上完成严格赛季前推样本外预测。此轮实现的盘口诊断是主队 AH 0（DNB）三状态概率；没有可匹配的 Crown 盘口线和水位，不能声称 Crown ROI。
- **OU：** Football Predictor V4 原版五类模型已有完整多赛季样本外报告；penaltyblog 三种进球分布也生成固定 O2.5 的独立 OOS 概率。V4 的原版模拟 ROI 使用作者研究的市场赔率、阈值和结算口径，不是 Crown ROI。
- **自动化：** 每四小时 UTC 更新输入、训练/评估、比较历史报告并在公开分支保存报告、预测和输入/模型版本哈希。Actions run `39406087077` 成功；其 OOS 结果已持久化在公开分支提交 `0d4d0a4`。后续本报告所列的扩展参数归档和概率校准分箱仍待下一次 Actions 运行验收。
- **安全边界：** 研究仅使用 M3 上游历史数据；未接入 M1/M2/MR1 的模型或账本，未触碰生产模型，未发送 TG，也没有自动模型晋级或新增交易 Gate。

## penaltyblog：真实 AH / OU OOS 结果

来源为 [Football-Data.co.uk](https://www.football-data.co.uk/) 六个联赛：E0、I1、SP1、D1、F1、B1；数据覆盖 2017/18 至 2026/27 当前部分赛季。Actions run `39406087077` 在 2026-10-20 10:14:43 UTC 生成报告，使用 penaltyblog 1.13.1，量化 Runner 源码 commit `a948f93f4e5b9a564da1274c4ba2dc099f864664`，Football Predictor 上游 commit `2f75be0f26363e26a42aaff34ede68f35635da02`。

输入共 60 个 CSV、19,093 场有效历史比赛。按更早赛季训练并向后预测，共有 17,027 个测试比赛行、51,081 条模型预测（每场每模型一条）。每种模型对 14,696 场给出可评分概率，覆盖测试行 86.3%；2,331 场因至少一队不在该联赛训练历史中而明确标为未预测。无球队映射回填或伪预测。

| 模型 | AH 0 DNB 三状态 Log Loss | AH Brier | O2.5 Log Loss | O2.5 Brier |
|---|---:|---:|---:|---:|
| Poisson | 1.00428 | 0.59968 | 0.68645 | 0.24650 |
| Dixon-Coles | 1.00415 | 0.59950 | 0.68647 | 0.24651 |
| Bivariate Poisson | 1.00414 | 0.59952 | 0.68647 | 0.24652 |

AH 结果以三状态多分类分数计分，DNB 的 win/push/lose 恰与胜/平/负相同；并非对一个具备 Crown 价格的亚洲让球线计算收益。固定 O2.5 的概率平均值约为 0.519–0.522，实际 Over 比例为 0.5359，存在整体偏低预测；不同测试季节表现并不稳定。模型间整体差异很小，尚不足以证明复杂模型稳定优于 Poisson。每个模型、赛季和联赛的完整分数与校准分箱在 JSON 报告中；逐场预测及实际比分在 SHA 命名 CSV 中。

数据完整性：报告 `input_fingerprint_sha256=5fbdf985cb8be4081e69959dfe7bd4e9685c8c556471a8bb11551c4b38809db1`；测试比赛身份也有独立哈希。Football-Data 日期字段无时区且仅为日历日期，统一解释为 UTC 午夜，并排除测试季首场所在的整个日期；训练只含更早赛季文件和严格早于测试日的记录。文件中其他赔率列没有被模型读取。数据本身不含 Crown 历史 AH/OU 盘线，因此 Crown 覆盖、有效样本收益、ROI 和最大回撤均为**不可计算**，不是 0。

注意：这一份 2026-10-20 全数据 CI 报告尚未包含最新本地工作树的拟合参数归档与校准分箱增强。代码已具备这些功能并通过本地测试，但必须待下一次 GitHub Actions 成功才将其视为已在自动化运行中验收。

## Football Predictor V4：OU 原版回测

工作流按作者 README 执行 V4 原入口。报告共 54 个模型×测试季节记录，范围为六联赛 E0/I1/SP1/D1/F1/B1，测试季从 2021/22 至当前部分 2026/27；每季约 2,039–2,097 场（当前部分赛季 383 场）。模型包括 LightGBM、Logistic、Market-anchored Logistic、Market-residual Logistic、Market-blend Logistic，以及 Poisson/联赛基线、开盘/收盘市场基准。

基于 CSV 中各季 `n_test` 加权，主要 OU Log Loss / Brier 为：

| V4 模型 | OOS Log Loss | OOS Brier | 原版策略记录 |
|---|---:|---:|---|
| LightGBM | 0.68267 | 0.24484 | 按原版规则有下注的四个测试季 ROI 加权约 -6.27% |
| Logistic | 0.68287 | 0.24491 | 有下注的四季 ROI 加权约 -4.46% |
| Market-anchored Logistic | 0.68124 | 0.24413 | 有下注的五季 ROI 加权约 -6.96% |
| Market-residual Logistic | 0.67218 | 0.23974 | 有下注的两季 ROI 加权约 -12.47% |
| Market-blend Logistic | 0.67234 | 0.23980 | 有下注的两季 ROI 加权约 -7.25% |
| Poisson 基线 | 0.69262 | 0.24927 | 无原版下注结果 |
| 收盘市场基准 | 0.66886 | 0.23813 | 基准，不是可部署模型 |

各模型有下注季节不一致，ROI 只对原作者阈值触发的记录加权，不能直接做公平策略排名。所有这些是 Football-Data / 上游原版价格与规则的回放，不是 Crown 实际成交表现，也不构成 M3 交易门槛。逐季原始数据见 [latest_v4_original_metrics.csv](results/latest_v4_original_metrics.csv)。最近部分赛季指标仍会随上游历史文件更新。

## 新开源方案审计

本轮检查了 penaltyblog、Football Predictor V4 及若干成熟候选。`GeorgiosLymperis/football-predictor`（MIT）含 Poisson、Elo/XGBoost、Logistic、MLP 与 walk-forward，但只输出 1X2，缺少目标所需的进球联合分布/可变 OU 与 AH 概率，且与现有基线部分重复；未作为新 M3 模型运行。`baio_blangiardo_replication` 有贝叶斯分层 Poisson 等方法，但未发现明确许可文件；不复制其代码。其他候选缺乏许可、时序泄漏说明或与当前进球分布模型高度同质。本轮没有把未验证方案放进工作流。

Football Predictor V4 检出版本未发现显式 LICENSE 文件；其源码未复制进本仓库，Actions 只检出并从临时目录按原 README 执行。正式继续分发或复用其代码前需要上游补充许可依据。penaltyblog 版本 1.13.1 的仓库包含 MIT 许可文件。

## 自动化、历史比较与可追溯性

- 保留原有四小时 UTC 训练频率；严格设置工作流并发，避免同分支运行互相覆盖。
- 每次记录源 commit、UTC 生成时间、CSV 文件哈希、总输入指纹、测试样本身份指纹、预测哈希、切分报告和指标。
- 重复数据以指纹如实标记无变化；历史版本比较仅在测试身份和样本数匹配时比较 penaltyblog 指标；V4 比较在测试样本数改变时抑制差值。
- 当前代码已增加拟合模型参数 SHA 归档及 10 分箱校准数据；11 项 M3 单元测试在本地通过。自动化验收仍待新的 Actions 运行。
- 实际 Actions：`39402727958`（旧流程成功，但只有 penaltyblog 样本内 API smoke，不算 AH OOS）；`39406087077`（本轮首次真实 penaltyblog OOS 成功并落库）。不能把前一 run 的 smoke test 当样本外证据。

## Crown 缺口、限制与下一步

M3 当前结果没有可验证的 Crown 同期盘口线、水位或时间戳，因此 Crown 覆盖率不可计算，Crown ROI、收益序列和回撤不报告。不得以其他赔率代填。下一步最有价值的是在用户允许的范围内建立受控的 Crown 历史线价匹配数据，并验证其赛前时间戳；然后分别按 AH、OU 盘口线生成分市场样本外评估。其次，修复/补充可审计的升降级球队身份历史，使未覆盖比例下降但不对历史球队身份作未来推断；延长更多赛季的跨季稳定性评估；为 V4 源码许可寻求上游明确说明；最后再独立验证一个有差异且有许可的 OU 方法。

当前报告能证明研究流水线和历史结果可复现，不能证明可盈利、Crown 可交易覆盖充足，亦不能据此启动正式下注。
