# M3 独立 AH / OU 研究验收

报告生成时间：2026-10-20 UTC。研究目标是完成独立研究系统，不启用正式投注。

最新前瞻 shadow 复验：PR #51 head `f95a23d028924dbad918f1c5d201829906a460e6` 对应 Actions [39430049592](https://github.com/ljm198964-alt/quant-runner/actions/runs/39430049592)，UTC `13:23:58Z`–`13:25:19Z` 全步骤 SUCCESS，M3 单元测试通过。运行产物 UTC `2026-10-20T13:24:32.579566Z`，OpenFootball 源 commit `e6744429ee395bc86f247348c6184bb08d4eb361`。14,384 场 OOS 测试、43,152 条模型预测，其中各模型11,254条已评分；训练结果和未来赛程输入均未变化，故本次新增学习信息、预测、修订和结算均为0。Shadow 保留4,215个唯一 forecast keys、Crown quote=0，EV/ROI=N/A；B1来源文件仍缺失。此 run 只上传研究 artifact，没有新结果 commit。它验证了 PR 分支 no-market 流程，没有验证 Crown 行情链路。

最新复验：commit `6737a07bad4568a031551c8dfa256dc30cd55c22` 对应的 GitHub Actions run [39426586706](https://github.com/ljm198964-alt/quant-runner/actions/runs/39426586706) 于 2026-10-20T12:59:11Z–13:00:04Z SUCCESS。40/40 M3 单元测试和保存结果的稳定性/账本审计均通过；严格 UTC cutoff 复核 33,762 行，三模型各 11,254 个配对评分样本，输入 fingerprint 未变，Crown quotes used=false，账本 4,215 个 canonical forecast、0 settlement。报告输入没有变化，Actions 正确记录 `M3_STABILITY_REPORT_UNCHANGED`，没有伪报新增学习或盘口结果。源码与输出详情见 `latest_oos_stability.json` 和 `latest_shadow_ledger_audit.json`。

阶段 B 结算工具在 PR HEAD `906bd21bc6e9051725448699e10556c4f83a6f3f` 对应的 Actions [39427250600](https://github.com/ljm198964-alt/quant-runner/actions/runs/39427250600) 中完成云端验收：45/45 tests PASS，OOS stability/ledger audit SUCCESS；workflow 于 `2026-10-20T13:03:57Z`–`13:04:51Z` 运行。输入数据没有变化，Crown quotes used=false，报告未产生新 shadow/OOS 数据或结果提交。真实单场 Crown hindcast 的 EV 与结算复算见 [Stage A/B audit](M3_CROWN_STAGE_A_B_AUDIT.md)。

随后将新增结算 API 合并回既有 `probabilities.py`，避免复制原有 quarter-line 计算。本次 PR HEAD `86e2e9eaf25e8b3896df39f4d62650afa24aa71a` 的 Actions [39427828868](https://github.com/ljm198964-alt/quant-runner/actions/runs/39427828868) 于 `2026-10-20T13:08:07Z`–`13:09:01Z` SUCCESS：43/43 M3 tests PASS，OOS stability 与影子账本 audit PASS，记录 `M3_STABILITY_REPORT_UNCHANGED`。模型输入与 shadow ledger 未变化，没有新训练结果、预测、Crown 报价或结算写入。

## OpenFootball：独立真实 OOS 与前瞻无盘口影子

GitHub Actions [39415198829](https://github.com/ljm198964-alt/quant-runner/actions/runs/39415198829) 于 2026-10-20T11:30:25Z 全步骤 SUCCESS。研究代码提交 `8c011d68ecbd51ff5a7fa90c3cb88178656e30ce`；结果与影子账本由 Actions 落库提交 `7613522`。报告生成 UTC 为 `2026-10-20T11:30:06.224625+00:00`，影子运行 UTC 为 `2026-10-20T11:29:18.057086Z`。源为 CC0-1.0 的 `openfootball/football.json` commit `e6744429ee395bc86f247348c6184bb08d4eb361`，penaltyblog 固定 1.13.1。

源中 50 个赛季×联赛文件（2017/18–2026/27），五个可用联赛 E0/D1/SP1/I1/F1，共 16,210 场完赛赛果；B1 文件缺失，明确不补造。严格逐联赛逐赛季前推 45 个测试切分全部有早期训练数据，测试共 14,384 场，三模型共 43,152 条预测；每种模型有 11,254 条已评分预测，未覆盖的升班/新队不生成假概率。每个测试季都只用更早赛季且比赛日严格早于该季首个测试日期的记录训练。完整切分、逐场赛果/概率和来源文件 SHA 保存在本目录 `results/openfootball/`。

| 模型 | AH0/DNB 三状态 Log Loss | AH0/DNB Brier | OU O2.5 Log Loss | OU O2.5 Brier |
|---|---:|---:|---:|---:|
| Poisson | 1.00076 | 0.59739 | 0.68634 | 0.24638 |
| Dixon-Coles | 1.00104 | 0.59744 | 0.68633 | 0.24638 |
| Bivariate Poisson | 1.00090 | 0.59737 | 0.68649 | 0.24648 |

AH0 的胜/和/负与 DNB win/push/lose 三状态分数一致，但不是任意 Crown 让球线评价；OU 仅固定 O2.5。模型总体分数很接近，未证明复杂模型稳健胜过 Poisson；详细逐测试赛季指标和校准分箱见 `latest_oos_report.json`。这是五联赛 CC0 数据上的独立口径，与 Football-Data 六联赛 OOS 不能直接做性能优劣比较。

同一 run 使用源中的 1,405 个日期至少领先 3 天的 fixture，形成 4,215 个逻辑前瞻预测（3 模型×每场），记录在 append-only `shadow_ledger.jsonl`。历史上因预测身份曾包含仓库 commit，账本实际保留了 8,430 条原始 `FORECAST` 行；随后 4,215 条重复版本均通过 `FORECAST_DUPLICATE_SUPERSEDED` 显式标记，唯一 canonical 预测为 4,215 条，模型各 1,405。该历史没有删除或覆盖。生成时间、训练输入 hash、模型版本/参数、fixture 和赛果身份均记录；首次持久化运行的前次数据/赛程指纹为 null；没有已结算影子样本，结算指标、ROI 和最大回撤均为 null。当前不抓 Crown，不记录 EV、下注或 Telegram。源 fixture 的具体时间字段无文档化时区，本协议完全忽略时刻，只使用日历日期并标注“时区未指定”；因此不能声称精确 UTC 开赛窗口。

### 固定样本跨季模型稳定性审计（不重训）

对已保存的 `latest_oos_report.json` 与逐场 OOS CSV 运行 `openfootball_stability.py`，生成 [latest_oos_stability.json](results/openfootball/latest_oos_stability.json)。审计确认三模型在 AH0/DNB 与 O2.5 都共享同一组 11,254 场可评分 OOS 比赛；45 个联赛×赛季单元上每个模型样本数一致，共复核 33,762 条模型预测，训练 cutoff 对每条预测严格早于源日历日期。另 3,130 个测试 fixture 没有预测，主要因测试球队未出现于训练历史；它们保留在测试分母，不做补造。

| 盘口概率目标 | 模型 | Log Loss | Brier | 45 个配对联赛×赛季单元中最佳数（Log Loss / Brier） |
|---|---|---:|---:|---:|
| AH0/DNB 三状态 | Poisson | 1.000761 | 0.597390 | 21 / 18 |
| AH0/DNB 三状态 | Dixon-Coles | 1.001044 | 0.597438 | 15 / 19 |
| AH0/DNB 三状态 | Bivariate Poisson | 1.000898 | 0.597370 | 9 / 8 |
| 固定 O2.5 | Poisson | 0.686342 | 0.246385 | 14 / 13 |
| 固定 O2.5 | Dixon-Coles | 0.686333 | 0.246382 | 13 / 14 |
| 固定 O2.5 | Bivariate Poisson | 0.686490 | 0.246475 | 18 / 18 |

这是同一赛果、同一测试身份的配对比较，不能从很小的汇总差异推导稳定模型胜者。OU 上 Dixon-Coles 与 Poisson 的 Log Loss 差仅约 0.000010；两者 Brier 差约 0.000003。不同模型在 45 个联赛×赛季单元里轮流领先。2026/27 当前部分赛季只有199个可评分样本，不能当成稳定结论。未做预先设定的假设检验、投注策略筛选或 Crown 收益计算。

另按 45 个联赛×赛季块执行 10,000 次固定种子（20261020）配对区块 bootstrap，比较每个非基准模型的逐场 Log Loss/Brier 相对 Poisson 差值；全部未调整 95% 区间都跨过 0。下列每项先给全样本加权点差，再给区块 bootstrap 区间。AH 的 Dixon-Coles 点差：Log Loss +0.000283 `[-0.000472, 0.001070]`，Brier +0.000048 `[-0.000372, 0.000497]`；Bivariate Poisson 为 +0.000137 `[-0.000551, 0.000834]` 与 -0.000021 `[-0.000368, 0.000325]`。OU Dixon-Coles 为 -0.000010 `[-0.000043, 0.000021]` 与 -0.000003 `[-0.000017, 0.000010]`；Bivariate Poisson 为 +0.000148 `[-0.000293, 0.000658]` 与 +0.000090 `[-0.000118, 0.000335]`。这只是跨联赛×赛季块的描述性不确定区间；45 个块仍有限，比较未做多重检验调整，也不等同策略检验。数据没有支持复杂分布稳定胜过 Poisson 的证据。

三种模型在这 11,254 个 O2.5 预测上的平均概率分别为 Poisson 0.51786、Dixon-Coles 0.51780、Bivariate Poisson 0.51469；Over 实际比例为 0.53874，平均预测低约 2.09、2.09、2.40 个百分点。该偏差是全量描述性校准，不是皇冠线价概率优势；不能对概率做事后修正后再用同一 OOS 集合声称改进。AH 评价仍仅为 DNB 三状态结果，不等价任意 AH 线。

最新 `latest_oos_stability.json` 的 `probability_bias` 从相同逐场 OOS 行计算 `(平均预测概率−实际发生率)`，按模型、赛季、联赛和联赛×赛季拆分；AH0 分别报告 win/push/lose，OU 仅固定 O2.5。它是边际频率误差描述，不是概率分箱检验、显著性检验或策略筛选；没有拟合修正器，也没有改预测。

该扩展由 GitHub Actions [39420905826](https://github.com/ljm198964-alt/quant-runner/actions/runs/39420905826) 于 2026-10-20 12:15:36–12:16:20 UTC 实际运行，33/33 测试通过。输入 fingerprint 保持 `93e0b8b91722f9c967e608ad63ae88d4c8d8b4c466de92948673404697c8e`，source OOS report UTC 仍为 `2026-10-20T11:38:35.164608+00:00`；没有训练，只刷新误差拆分 JSON。Actions 结果由 commit `a28d0b0411d79f09709b2a0e58fe3104b98df053` 持久化。

| O2.5 子样本 | n | Poisson 偏差 | Dixon-Coles 偏差 | Bivariate Poisson 偏差 |
|---|---:|---:|---:|---:|
| 全部 OOS | 11,254 | -2.09 pp | -2.09 pp | -2.40 pp |
| D1 | 1,962 | -5.15 pp | -5.18 pp | -5.35 pp |
| E0 | 2,274 | -3.23 pp | -3.24 pp | -3.46 pp |
| F1 | 2,211 | -2.69 pp | -2.68 pp | -2.88 pp |
| I1 | 2,373 | +0.29 pp | +0.29 pp | -0.37 pp |
| SP1 | 2,434 | -0.32 pp | -0.32 pp | -0.61 pp |
| 2025/26 | 1,507 | -4.34 pp | -4.35 pp | -4.65 pp |
| 2026/27 部分赛季 | 199 | -10.07 pp | -10.07 pp | -10.41 pp |

三个模型对 O2.5 的误差方向在 D1/E0 及若干赛季较集中，但联赛差异明显；2026/27 只有 199 场，不能外推。Poisson 的 AH0 边际偏差为 win +0.67 pp、push -1.14 pp、lose +0.46 pp；Dixon-Coles 约 +0.10、+0.03、-0.13 pp；Bivariate Poisson 约 +0.43、-0.46、+0.03 pp。边际发生率不能说明每个预测概率区间都已校准，也不能说明相对 Crown 价格有优势；没有据此事后校准或筛选投注。

### 无重训影子账本结构审计

`openfootball_shadow_audit.py` 对 append-only ledger 做只读检查，并已接入 `.github/workflows/m3-oos-stability.yml` 的四小时任务。它复核 forecast ID 与逻辑键一对一 canonical、supersession 引用及理由结构、预测 UTC 时间及日历日期 guard、概率范围/归一化、无 Crown quote 时 EV/ROI 必须为空、无正式单与 Telegram 标记；不训练、不结算、不访问 Crown。首次审计报告见 `latest_shadow_ledger_audit.json`：原始 forecast 8,430、逻辑/有效 forecast 4,215、superseded 4,215、settlement/Crown/EV/ROI/订单/Telegram 均为 0。报告内 ledger SHA 必须等于账本当前 SHA，避免在分支同步竞态下保存过期审计。GitHub Actions [39420305676](https://github.com/ljm198964-alt/quant-runner/actions/runs/39420305676) 于 2026-10-20 12:10:49–12:11:32 UTC SUCCESS，33/33 测试通过；下载的 shadow audit artifact 与仓库 JSON 字节一致（SHA-256 `9cb01056753bf50fd15e59b8281ceea0fa034b8be16597cfbb6d69377a98dd90`），workflow 确认报告未变，故没有生成虚假结果提交。新增概率误差拆分同样只复算这些 OOS 预测，不拟合或修改模型。

后续 no-market 前瞻 shadow run [39421816230](https://github.com/ljm198964-alt/quant-runner/actions/runs/39421816230) 于 UTC `2026-10-20T12:23:02Z`–`12:25:08Z` 实际成功，40/40 测试通过。运行时结果输入 fingerprint `93e0b8b91722f9c967e608ad63ae88d4c8d8b4c466de92948673438704697c8e`、赛程 fingerprint `2db32fe59ae637841be2d3ad7abc1d410e0aa5ea543bca2fe7af61096322f526` 均未变化；符合 3 日日期保护条件的赛程身份仍有1,405个，但全部已有逻辑 forecast key，因此新增 forecast=0、settlement=0、重复修正=0。公开 artifact 中生成 UTC 为 `2026-10-20T12:23:44.220002Z`；canonical forecast key=4,215，ledger SHA 保持 `0645da41b79bbec056081188ba6fb52b4b4a40b077f743eccc7e6645fefbc21e`。Crown quote=0、EV/ROI/最大回撤=N/A、正式订单=0、Telegram=未发送；状态未变，结果持久化步骤按设计跳过。高频重复运行并没有产生新赛果或新学习信息。

当前分支随后再次手动运行 [OpenFootball shadow Actions 39423160751](https://github.com/ljm198964-alt/quant-runner/actions/runs/39423160751)（UTC 12:33:20–12:35:26，40/40 tests PASS；artifact `generated_utc=2026-10-20T12:34:05.833328Z`）和 [saved OOS stability Actions 39423493743](https://github.com/ljm198964-alt/quant-runner/actions/runs/39423493743)（UTC 12:35:56–12:36:33，40/40 tests PASS）。影子任务重跑真实 walk-forward 拟合与 no-market 账本校验；OpenFootball 源 commit `e6744429ee395bc86f247348c6184bb08d4eb361` 不变，结果/训练 fingerprint 为 `93e0b8b91722f9c967e608ad63ae88d4c8d8b4c466de92948673438704697c8e`、赛程 fingerprint 为 `2db32fe59ae637841be2d3ad7abc1d410e0aa5ea543bca2fe7af61096322f526`。仍有 1,405 个日期保护范围内 fixture、4,215 canonical forecast keys；本次 forecast、settlement、supersession 均新增 0，账本 SHA 仍为 `0645da41b79bbec056081188ba6fb52b4b4a40b077f743eccc7e6645fefbc21e`。稳定性复核对每模型 11,254 个配对评分样本、33,762 条训练 cutoff 再验证；Crown quotes used=false。artifact 与公开 JSON 逐字节一致，SHA-256 分别为 `a727f8b75241eef9becb4fbb85b5f7b5ee4dbdebef9b238095471129c299c304`、`9cb01056753bf50fd15e59b8281ceea0fa034b8be16597cfbb6d69377a98dd90`；persist step 确认 `M3_STABILITY_REPORT_UNCHANGED`，未生成新报告提交。Crown、EV、ROI、回撤仍不可计算；正式单/TG 均为0。这是无盘口前瞻基础设施的重复运行验收，不是新预测或新增 OOS 学习证据。

可复算命令（只读现存 OOS 产物，不重新训练）：

```bash
python -m research.m3.openfootball_stability \
  --report research/m3/results/openfootball/latest_oos_report.json \
  --predictions research/m3/results/openfootball/latest_oos_predictions.csv \
  --output research/m3/results/openfootball/latest_oos_stability.json
```

### 影子账本幂等性修复及二次 Actions 验收

首次 Actions run 后的手动重复 run `39415593340` 暴露出 ID 设计缺陷：forecast/model version ID 将整个 quant-runner commit 纳入身份，文档 commit 使同一数据上的4,215条预测被重复追加；该 run 全绿但不能作为“无变化不追加”的验收。复核后没有删除、覆盖或隐瞒旧账本行。修复提交 `88091ba` 将预测身份改为 fixture/赛程 revision + 模型语义版本 + 训练输入指纹 + penaltyblog 版本，并让 OOS 快照按研究代码内容哈希与赛果指纹归档，不随文档或 Actions 结果 commit 变化。对同语义重复记录只选一条进入评分/结算，其余通过 append-only `FORECAST_DUPLICATE_SUPERSEDED` 事件明确标记。

修复后的真实 Actions run [39416174708](https://github.com/ljm198964-alt/quant-runner/actions/runs/39416174708) SUCCESS，结果落库 commit `8ab0434`：输入及赛程指纹分别未变化；新预测0、结算0、追加重复修正4,215。原始 forecast 行8,430、唯一逻辑预测键4,215、被 superseded 行4,215，账本 SHA-256 为 `0645da41b79bbec056081188ba6fb52b4b4a40b077f743eccc7e6645fefbc21e`。随后手动 Actions [39416501773](https://github.com/ljm198964-alt/quant-runner/actions/runs/39416501773) SUCCESS，状态确认无赛果/赛程变化、无新 forecast、无新 settlement、无新重复修正；账本 SHA 保持不变，结果持久化步骤按预期跳过。两个 run 都重新执行了真实 OOS，OOS 数据输入 fingerprint 保持 `93e0b8b91722f9c967e608ad63ae88d4c8d8b4c466de92948673438704697c8e`；修复后代码评估 fingerprint 固定为 `c6bdb7edeb213005b7770219b7572b8b6b809cf962f835311a37bf21675ae631`。这证明本源快照没有新增学习信息，也没有被报告成成绩改善。

工作流 `.github/workflows/m3-openfootball-shadow.yml` 配置每 4 小时、手动和指定文件变更触发，并在数据/赛程/账本有变化时把历史报告和账本提交回研究分支；本次 PR 分支 push 验证证明代码、测试、实际拟合、结果落库均成功。GitHub 定时事件只对默认分支生效，PR 合并前不能称该新工作流已在默认分支持续定时运行。原 Football-Data 工作流维持现状。OpenFootball 本身每日更新，四小时触发不会制造新增赛果；本次之后须以指纹判断实际是否有新信息。

## 状态摘要

- **AH：** penaltyblog Poisson、Dixon-Coles、Bivariate Poisson 已在真实赛果上完成严格赛季前推样本外预测。此轮实现的盘口诊断是主队 AH 0（DNB）三状态概率；没有可匹配的 Crown 盘口线和水位，不能声称 Crown ROI。
- **OU：** Football Predictor V4 原版五类模型已有完整多赛季样本外报告；penaltyblog 三种进球分布也生成固定 O2.5 的独立 OOS 概率。V4 的原版模拟 ROI 使用作者研究的市场赔率、阈值和结算口径，不是 Crown ROI。
- **自动化：** 每四小时 UTC 更新输入、训练/评估、比较历史报告并在公开分支保存报告、预测和输入/模型版本哈希。首次 OOS run `39406087077` 成功；增强验收 run `39407478152` 也 SUCCESS，最新结果已持久化在公开分支提交 `67680e4`。
- **安全边界：** 研究仅使用 M3 上游历史数据；未接入 M1/M2/MR1 的模型或账本，未触碰生产模型，未发送 TG，也没有自动模型晋级或新增交易 Gate。

## penaltyblog：真实 AH / OU OOS 结果

来源为 [Football-Data.co.uk](https://www.football-data.co.uk/) 六个联赛：E0、I1、SP1、D1、F1、B1；数据覆盖 2017/18 至 2026/27 当前部分赛季。增强验收 Actions run `39407478152` 在 2026-10-20 10:27:00 UTC 生成报告，使用 penaltyblog 1.13.1，量化 Runner 源码 commit `0aa1514`，Football Predictor 上游 commit `2f75be0f26363e26a42aaff34ede68f35635da02`。

输入共 60 个 CSV、19,093 场有效历史比赛。按更早赛季训练并向后预测，共有 17,027 个测试比赛行、51,081 条模型预测（每场每模型一条）。每种模型对 14,696 场给出可评分概率，覆盖测试行 86.3%；2,331 场因至少一队不在该联赛训练历史中而明确标为未预测。无球队映射回填或伪预测。

| 模型 | AH 0 DNB 三状态 Log Loss | AH Brier | O2.5 Log Loss | O2.5 Brier |
|---|---:|---:|---:|---:|
| Poisson | 1.00428 | 0.59968 | 0.68645 | 0.24650 |
| Dixon-Coles | 1.00415 | 0.59950 | 0.68647 | 0.24651 |
| Bivariate Poisson | 1.00414 | 0.59952 | 0.68647 | 0.24652 |

AH 结果以三状态多分类分数计分，DNB 的 win/push/lose 恰与胜/平/负相同；并非对一个具备 Crown 价格的亚洲让球线计算收益。固定 O2.5 的概率平均值约为 0.519–0.522，实际 Over 比例为 0.5359，存在整体偏低预测；不同测试季节表现并不稳定。模型间整体差异很小，尚不足以证明复杂模型稳定优于 Poisson。每个模型、赛季和联赛的完整分数与校准分箱在 JSON 报告中；逐场预测及实际比分在 SHA 命名 CSV 中。

数据完整性：报告 `input_fingerprint_sha256=5fbdf985cb8be4081e69959dfe7bd4e9685c8c556471a8bb11551c4b38809db1`；测试比赛身份也有独立哈希。Football-Data 日期字段无时区且仅为日历日期，统一解释为 UTC 午夜，并排除测试季首场所在的整个日期；训练只含更早赛季文件和严格早于测试日的记录。文件中其他赔率列没有被模型读取。数据本身不含 Crown 历史 AH/OU 盘线，因此 Crown 覆盖、有效样本收益、ROI 和最大回撤均为**不可计算**，不是 0。

报告记录 162 次实际拟合参数，参数快照已公开落库为 SHA 命名 JSON；其文件 SHA-256 与报告字段一致。逐场预测 CSV 的文件 SHA-256 也与报告一致。输入指纹与上一轮相同，`data_changed_vs_previous_snapshot=false`，本次运行没有新增比赛信息。逐场预测覆盖 51,081 模型×比赛记录，参数文件 505,365 字节。

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
- 当前工作流已验证拟合参数 SHA 归档及 10 分箱校准数据，11 项 M3 单元测试本地通过；54 个 league×season 时间切分均满足训练结束早于测试开始。
- 实际 Actions：`39402727958`（旧流程成功，但只有 penaltyblog 样本内 API smoke，不算 AH OOS）；`39406087077`（首次真实 penaltyblog OOS）；`39406828896`（模型参数文件首次报告但因工作流遗漏未落库）；`39407478152`（修复后 SUCCESS，参数、预测、报告、切分和 V4 指标均持久化，receipt 正确记录 AH 训练状态）。最新输入指纹与预测哈希可在 `latest_penaltyblog_oos_report.json` 查验。
- 新增独立 `.github/workflows/m3-oos-stability.yml`，每四小时 UTC 读取已存 OpenFootball OOS 报告/逐场预测并做 M3 单测与稳定性复算，不运行拟合器；仅结果指纹变化时同步持久化 JSON。设置为在保存 OOS 文件更新后自动触发，并与模型 OOS 工作流分开并发。实际 PR 分支 Actions [39419131182](https://github.com/ljm198964-alt/quant-runner/actions/runs/39419131182) 和 [39419363464](https://github.com/ljm198964-alt/quant-runner/actions/runs/39419363464) 均 SUCCESS，26/26 测试及分析/持久化通过；JSON 已落库提交 `2442713`。PR 尚未合并前 schedule 不在默认分支生效。

## Crown 缺口、限制与下一步

离线 Crown evidence contract 提交 `3136522bbdc559e48bb26b651dd59db929f8e857` 已在 Actions [39417655093](https://github.com/ljm198964-alt/quant-runner/actions/runs/39417655093) 上验收：22/22 M3 tests PASS；OpenFootball OOS/shadow step SUCCESS；run 生成 UTC `2026-10-20T11:49:48.243037Z`。输入/结果指纹均为 `93e0b8b91722f9c967e608ad63ae88d4c8d8b4c466de92948673404697c8e`，fixture 指纹也未变；本次新增预测、结算及重复修正均为0，持久化步骤按预期跳过，没有产生新的学习样本或成绩变化。完整 receipt 在 Actions artifact，当前 ledger SHA 保持 `0645da41b79bbec056081188fb6ba52b4b4a40b077f743eccc7e6645fefbc21e`。

本轮对已有 Crown artifact 的逐线复核与覆盖边界见 [M3 Crown Stage A/B audit](M3_CROWN_STAGE_A_B_AUDIT.md)。单场结果不提供 ROI；后续只有在取得书面许可并提供独立授权的数据后，才按 [离线 M3 Crown evidence contract](crown_evidence_contract.md) 校验时间和身份；该契约不执行抓取。

M3 原始预测产物没有 Crown 盘口。但对已有公开 Actions 存档作只读身份审计后，在 `Crown Bet365 Paired Research` run [37765506416](https://github.com/ljm198964-alt/quant-runner/actions/runs/37765506416) 中发现 1 场与 D1 2026/27 M3 OOS 测试身份相符的 fixture；该场在 M3 测试表 17,027 场中占 1 场（0.0059%），并有 1 个 Crown AH 与 1 个 Crown OU 报价记录。Crown 来源响应摘要 SHA-256 为 `2b60bd3ff46828451f1d1b06514020bbf52531571155108f6a3749905bd46c52`；配对审计报告标记 `bookmaker_execution_verified=false`。该 run 的其他 15 场不属于 M3 的六联赛测试范围。匹配只代表留存 artifact 中找到的下限，不代表对 Crown 全部历史覆盖作了穷尽统计。

该场已有 Crown AH 线为主队 -1.5（主/客水位1.93/1.95），OU 线为3.5（大/小水位2.04/1.84）；报价时刻及样本来源、概率和逐方向 EV 见 [Crown Stage A/B audit](M3_CROWN_STAGE_A_B_AUDIT.md)。对同一逐场线级概率与水位计算后，三种 penaltyblog 模型在 AH、OU 的四个方向每单位理论 EV 都为负，范围约 -0.0589 至 -0.0009。比赛赛果为2–2：该线下 AH 主队方向全输、客队方向全赢，OU 大球全赢、小球全输。按每方向单独1单位描述性结算，净收益分别为 -1.00/+0.95/+1.04/-1.00；它们是四种互斥方向的反事实结果，不构成同一策略的收益序列。没有预先规定选边策略、真实下单或重复样本，因此策略 ROI、累计收益和最大回撤均仍为 **N/A**。这一行是赛后生成的严格 walk-forward hindcast，不是同期记录预测，也不能证明盈利。

既有 `probabilities.py` 已实现 AH/OU quarter-line 比分网格结算和单位 EV；本轮将 exact-score AH/OU 结算与从五类结算概率计算单位 EV 的 API 补充到该模块，避免重复建立第二套结算器。新增测试覆盖观察到的2–2线级结算及 quarter-line 五类状态。接口不抓取、不校验授权、不选择下注方向；真实输入必须先通过 Crown 证据与时间校验。合成测试不计入实绩。V4 原版只有 O2.5 支持，本场 Crown 总进球线为3.5，故其五种模型方案仍是0条有效 Crown 评估样本。

影子账本成熟度复核：当前保留 4,215 个 canonical forecast，fixture 日历日期为 `2026-10-23` 至 `2027-05-30`。以 `2026-10-20 UTC` 审核时这些比赛均未到期，故当前无可结算前瞻样本；账本有 0 Crown snapshot、0 settlement。该字段是源日历日期且没有文档化时区，本复核只得出“无已成熟条目”，不推算实际 kickoff UTC。原始事件、重复 forecast 与显式 supersession 均保留不变。

后续 Crown 数据工作的授权范围尚未核实。TotalCorner 官方 API 文档面向 VIP 开发者，提供 `bookmaker=crown`、AH/goal-line movements、curl/Python 请求示例和限速；当前条款则把 APIs 纳入 Service，并要求自动化提取事先书面同意，未明确说明已文档化的 API 客户端调用是否豁免，也未明授公开保留/分发 Crown 价线。因此本轮不新增自动 Crown 请求、镜像原始响应或把新逐价数据写进公开仓库：[TotalCorner Terms](https://www.totalcorner.com/page/terms)、[TotalCorner API](https://www.totalcorner.com/page/api)。这不等于接口不存在，也不把既有 token 视作权限范围证明。OddsPapi 的 `singbet` 是供应商自称“Crown in Asia”的未核实 alias，另一供应商将 SingBet 与 Crown 分列；没有操作方一手来源确认前不计为 Crown。后续只有可追溯的既有授权范围明确覆盖自动采集/留存/发布，且开赛 UTC、赛队身份可独立核验时，才建立独立采集配对；在此之前不能宣称有可估计的 Crown ROI。

本轮依据该 API 文档新增离线适配器 `crown_totalcorner_import.py`：只读用户已在授权环境保存的原始 JSON，不联网。适配器要求书面授权编号、match ID 精确命中、源队名精确映射、账户 IANA 时区证据、API kickoff 与独立核实 UTC kickoff 完全一致；只归一化开赛前、未暂停的 AH/goal-line movement 行，且拒绝 DST 歧义和未定义复合线。CLI 只输出原始响应 hash、引用行计数和 UTC 时间范围，不输出价格、不保存规范化 quote。专项测试使用合成样本，确认转换与失败路径，不是 Crown 真实观察，未改变前述有效覆盖数。接口说明见 [`crown_totalcorner_import_contract.md`](crown_totalcorner_import_contract.md)。

该适配器以提交 `feb6f4dfabb19653bbedaaba2a212644e86a85d0` 和 Actions [39421816343](https://github.com/ljm198964-alt/quant-runner/actions/runs/39421816343) 完成真实云端验收：UTC `2026-10-20T12:23:01Z`–`12:23:40Z`，40/40 M3 tests 通过；同一 run 对已存 OOS/shadow 文件完成无重训审计，3 模型各11,254个评分样本，逐行复核33,762条训练 cutoff，Crown quotes used=false，结果无变化。该 run 不重新拟合，也没有新增样本或 Crown 数据。

V4 的单场 Crown 适用性也已按原版市场范围核验：run `39407478152` 的暂存 artifact `walk_forward_predictions.csv` 有10,687行，SHA-256 `b612c1158cefe014676d56e4cf7fce2c9137f3b9b9ce3f7be78d524d16a9a921`，其中存在 Dortmund–Werder D1 2026/27 同日预测；但归档 Crown OU 盘口线不等于 V4 原版 O2.5 目标，因此 V4 的五种方案在此场均不计 Crown 盘口评估样本。该 CSV 还含上游来源市场字段，保留在 90 天 Actions artifact（到期 UTC `2027-01-18T10:22:29Z`），未复制进公开 M3 仓库；公开版本继续只保存按模型/赛季聚合的指标。详情见 [Crown 审计](M3_CROWN_STAGE_A_B_AUDIT.md)。

另一项局限是 M3 当前逐场产物只保存 AH 0 与 O2.5 概率；除上述单场临时重算外，没有整套 Crown 市场线对应的历史概率面板，故不能对这 17,027 场统一计算 Crown 线级 Log Loss、Brier、收益或回撤。不得用无时区的 Football-Data 日历日去伪造 Crown 精确开赛匹配。

其次，修复/补充可审计的升降级球队身份历史，使未覆盖比例下降但不对历史球队身份作未来推断；延长更多赛季的跨季稳定性评估；为 V4 源码许可寻求上游明确说明；最后再独立验证一个有差异且有许可的 OU 方法。

当前报告能证明研究流水线和历史结果可复现，不能证明可盈利、Crown 可交易覆盖充足，亦不能据此启动正式下注。
