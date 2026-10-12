# 量化亚洲盘｜跨会话工作交接记录

更新日期：2026-10-11（北京时间）
性质：项目事实与工作进度快照。**不是新增策略规则或验收 Gate。** 每次引用成绩必须核对账本的 generated_at，不得把本文件历史快照冒充实时值。

## 用户已经明确的要求
- 正式实战 = 实际向 Telegram 发送的正式策略订单；测试消息、影子测试、研究回测均不得算实战。
- 盘口来源严格使用 Crown；不允许以其他公司盘口替代。
- M1 AH、M1 OU 旧线、M1 OU R1、MR1 AH、MR1 AI、对手分别统计，MR1 AH 与 MR1 AI **绝非同一模型**。
- 用户目标：M1 OU R1 **完全恢复**自动扫描、真实 TG 派单、正式账本回写和后续结算；不接受仅代码修复或 TG 测试成功就宣布恢复。
- 新工作优先公开仓库；用户此前要求停止使用私有运行链路并最终移除不再需要的私有仓库。当前运行链路仍依赖私有仓库，属于尚未解决的工程遗留问题，不得误报已经迁移。
- 不得擅自新增数量门槛、Gate、策略参数、测试/发布阻塞条件。未确认的建议不得当作已冻结规则。

## 仓库与关键路径
- 公开 Runner：`ljm198964-alt/quant-runner`，`.github/workflows/m1-free-runtime.yml`。
- M1 当前代码和数据仍在 `ljm198964-alt/totalcorner-research-bridge`：`m1_formal_runtime.py`、`m1_notification.py`、`results/m1_formal_ledger.json`（约3 MB）、`results/m1_formal_report.json`。
- MR1 AH：`ljm198964-alt/mr1-shadow/data/mr1-v6-cross-market/formal/performance.json`。
- MR1 AI：`ljm198964-alt/mr1-shadow/data/mr1-ai-browser-forward/formal-performance/summary.json`。
- 对手：`ljm198964-alt/totalcorner-research-bridge/results/opponent_settlement_latest.json`。
- GitHub 连接器读取大文件可能返回空内容；已经验证可经授权 Mac 的 GitHub CLI `gh api` 读取，**不得把空内容解释为没有账本**。

## M1 OU R1 恢复进展（2026-10-11）
- `m1_formal_runtime.py` 已是 `PAUSED_FORMAL_MARKETS = ()`。
- 已从 `m1_notification.py` 删除旧的 OU 暂停抑制函数及 claim 调用，提交 `cc676b6359b924b97c4dadfabc4bfaa18d008e0c`。
- 公开 Runner 增加恢复触发路径，提交 `b50253136b489b6eee7e7f67dfe1471db4308f35`。
- 创建触发文件，提交 `42250752eaaea82e5e080caa60c9bbf1b9da7ff4`。
- 实际 GitHub Actions 运行：`38148601775`（最后一次检查 in_progress，正在扫描），`38148606525`（最后一次检查 pending）。链接：https://github.com/ljm198964-alt/quant-runner/actions/workflows/m1-free-runtime.yml
- **尚未确认完整恢复**：必须继续查询这两次运行的最终步骤、真实 TG 正式回执和账本回写。不要把“已触发”说成“已成功”。
- 公开 Runner 目前仍 checkout 私有 M1 并使用 `PRIVATE_REPO_TOKEN`；未完成公开独立迁移。
- 旧 `SKIPPED_MARKET_PAUSED` 通知不会因删除代码自动恢复，不能盲目补发历史单。

## 已核对的正式实战成绩快照（各自生成时间不同）
| 链路 | 报告 generated_at (UTC) | 已结算 | 待结算 | PnL U | ROI |
|---|---|---:|---:|---:|---:|
| M1 AH | 2026-10-11 11:06:23 | 79 | 21 | +4.295 | +5.44% |
| M1 OU 旧线 | 2026-10-11 11:06:23 | 69 | 5 | -0.425 | -0.62% |
| M1 总账 | 2026-10-11 11:06:23 | 148 | 26 | +3.870 | +2.61% |
| MR1 AH | 2026-10-11 14:38:15 | 56 | 56 | +1.475 | +2.63% |
| MR1 AI | 2026-10-11 14:22:56 | 17 | 1 | -5.750 | -33.82% |
| 对手（非我方 TG） | 2026-10-10 06:28:02 | 179 | 48 条未解决 | +0.185 | +0.10% |

- M1 总账已发送 174 单（AH 100、OU 74），结算 148 单；M1 OU R1 新恢复线未取得独立已结算结果。
- MR1 AI 报告 formal_receipts=18，研究回填和事故恢复消息排除；不可与 MR1 AH 混用。
- 对手 AH：98 单，+2.325 U，ROI +2.37%；OU：81 单，-2.140 U，ROI -2.64%。对手来源不是 Crown 验证报价，不可冒充 Crown 盘口。
- 所有数字仅代表对应文件时间点，后续要读取新报告重算。

## 下一次会话直接接续
1. **优先**读取公开 Runner 运行 `38148601775`、`38148606525` 的最终状态和具体日志，检查正式派单与账本回写；失败则按日志修复，不修改策略。
2. 获取 M1、MR1 AH、MR1 AI、对手各自最新结算报告，按实际生成时间展示；不要重复使用本文件旧数字。
3. 确认 M1 OU R1 的真实 TG 正式订单与回执（若当轮没有符合策略的信号，明确写无新信号，不得伪造）。
4. 继续解决公开 Runner 对私有仓库的代码与账本依赖，但不能在迁移时丢失既有账本、造成重复发单。

## 已确认的 M1 OU R1 策略身份（2026-10-11 用户明确确认）
- **M1-OU R1 = `M1_SELECTION_20260924_EARLY_ROBUST`**。这是用户明确确认的版本映射，不得与 V2 混淆。
- 核查生产订单时必须检查实际执行的策略逻辑与版本，不得仅凭 `M1-OU-R1` 字符串或共用函数名断言策略正确。
- 用户要求正式 OU 使用 R1，移除 V2 的正式派单逻辑；历史账本与研究资料不可被误删。

## 2026-10-11 新增生产核查（本节优先于上方旧运行快照）
- M1 OU R1 用户确认版本：`M1_SELECTION_20260924_EARLY_ROBUST`；原始策略代码可从 `totalcorner-research-bridge` 历史提交 `e1be5eb5d8` 找到。
- 对照原始版本，当前 `gate_candidate()` 核心 EV/edge、时间窗口、盘口逆向变动规则一致；当前 OU 另遵循后来确认的顶级俱乐部赛事范围。
- `m1_live_scan.py` 的 OU 评估结果策略身份已修正，提交 `e26b1df52f9a78d881eac14bd2705cb1bd944eff`。**该提交的后续运行验证尚未完成，不得误报已验证。**
- 正式 M1 账本经 `gh api` raw 方式读取成功；OU 已确认 TG 正式发送 100 单，最新消息回执含 594—601。旧 OU 与新 R1 必须按真实策略身份/时间分开统计。
- GitHub Actions `38148601775` 已成功：扫描 `COMPLETE`、28 条新信号、45 条候选、0 扫描错误、0 即时派单错误；后续 `telegram_sent=1`、`telegram_unknown=0`、正式账本回写成功（提交 `24a694e`）。该运行早于 `e26b1df`。
- GitHub Actions `38148606525` 最新检查仍 `in_progress`，扫描步骤已成功，锁单/派单/账本回写尚待完成。继续检查，不得当作失败或成功。
- 生产工作流仍从私有仓库 checkout，公开 Runner 尚未完全独立。

## 2026-10-12 实战统计更新（以源文件 generated_at 为准）
- M1 正式报告 `results/m1_formal_report.json`，生成 UTC `2026-10-11T15:37:30.556621`：AH 已发105、结算79、待结26、+4.295U、ROI+5.44%；OU含旧线已发100、结算69、待结31、-0.425U、ROI-0.62%；总计已发205、结算148、待结57、+3.870U、ROI+2.61%。R1 新线不得与旧线混算。
- MR1 AH 正式报告 `data/mr1-v6-cross-market/formal/performance.json`，生成 UTC `2026-10-11T17:29:17.266Z`：结算81、待结36、-1.155U、ROI-1.43%，状态全赢33/半赢6/走水6/半输4/全输32；此前盈利快照已过时。
- MR1 AI 正式报告 `data/mr1-ai-browser-forward/formal-performance/summary.json`，生成 UTC `2026-10-11T14:22:56.677Z`：正式TG回执18、结算17、待结1、-5.750U、ROI-33.82%。不得与 MR1 AH 混用。
- 对手报告 `results/opponent_settlement_latest.json`，生成 UTC `2026-10-10T06:28:02`：来源227、结算179、未解决48、+0.185U、ROI+0.10%；AH 98单+2.325U，OU 81单-2.140U。该数据明显较旧。
- 本节是历史核查快照，下一次必须重新读取生产报告，不能冒充实时数据。

## 2026-10-12 GitHub Actions 工程清理
- 用户明确要求由 GPT 直接清理，不交 Codex；目标减少废弃和重复工作流，不影响正式模型生产。
- 已盘点公开 `quant-runner`：清理前 42 个工作流文件。
- 第一批已删除 4 个完成用途的一次性工作流：`m1-ou-r1-tg-test.yml` (`d180fdbb`)、`mr1-model-sign-audit-once.yml` (`41885c1f`)、`mr1-universe-coverage-once.yml` (`2a939b99`)、`mr1-row-schema-audit-once.yml` (`f9af4af9`)。
- 第一批清理后预计 38 个工作流文件，仍需复核最新仓库树及运行状态。未删除任何正式账本、TG 回执、研究结果或生产定时工作流。
- 其他旧研究/临时工作流尚未确认实际依赖，不得把它们写成已清理；后续继续盘点触发、依赖、最近运行及历史用途后处理。

## 2026-10-12 GitHub Actions 第二批清理
- 在第一批 4 个之外，又删除 7 个一次性/固定批次入口：`mr1-defense-sign-audit-once.yml` (`1d9fa015`)、`mr1-target-ou-audit-once.yml` (`10e44153`)、`mr1-totalcorner-zh-probe.yml` (`eb604f5d`)、`mr1-target-history-backfill-b1.yml` (`f68bb040`)、`mr1-target-history-backfill-b2.yml` (`1136d920`)、`mr1-target-history-backfill-b3.yml` (`d5940918`)、`mr1-target-history-deepen-1.yml` (`04d9ef06`)。
- 公开仓库工作流文件数经最新 GitHub 树核实：原 42，累计删除 11，剩余 31。
- 未删除正式 M1、MR1、MR1 AI、对手结算生产入口；MR1 Free Runtime 在最近运行列表中继续执行。未删除任何正式账本、研究数据、TG 回执。
- `Football display identity recovery` 最新运行列表出现 cancelled，尚未确认取消原因；中文库工作由 Codex 重构中，不得将其视为已完成。
- 剩余工作流需要逐项判断生产/研究依赖，不得为了压低数量擅自删除。

## 2026-10-12 GitHub Actions 第三批清理
- 已删除硬编码六条历史消息的 `mr1-v6-current-display-fix.yml`（提交 `9b90b713`）和被现有正式 M1 派单链路替代的 `m1-immediate-delivery-integrate.yml`（提交 `846ba034`）。
- GitHub 仓库树已重新核实：初始 42 个工作流，累计删除 13 个，剩余 29 个。
- 最新 MR1 Free Runtime 仍在运行；未删除正式 M1、MR1、MR1 AI、对手结算生产入口。对中文库恢复工作流的取消原因尚未核实。

## 2026-10-12 共享中文名称库历史恢复快照（运行方式已被下方新节取代）
- **本节状态被 2026-10-12 全量复核结果更新：** 共享库当前提交 `11f978103e09393573a635911d3fa9ff14c9036f`；12,172 个 team ID 的英文身份全部恢复，canonical 简体中文名 3,640（29.90%），8,532 条仍无唯一可核验中文名。771 个 league ID 中 329 个有 canonical 中文名。M1 历史覆盖 1,933/3,880（49.82%），MR1 历史覆盖 3,562/11,916（29.89%）。旧段落数字仅为当时快照。
- 最近一次 `Shared Football Identity Recovery` 已在 run `38178789455` 成功结束；持久化检查点记录 58/58 个待查联赛完成、0 个失败、1,374 次累计 TotalCorner API 请求，恢复 295 个英文身份。没有重新 dispatch 已完成的身份采集。
- 在唯一未映射队名上追加 Reep/Wikidata 严格交叉：仅用主队名/英文别名，做大小写、重音和标点标准化；要求 Reep QID、TotalCorner team ID 均唯一，不做模糊拼写匹配。两轮累计候选中 229 个获得简体中文标签并新增；最近一轮 1,049 个双端唯一候选中 884 个没有简体标签，43 个交叉歧义被排除。其余 8,532 条及逐条原因保存在 `results/football_chinese_bulk_report.json`。
- M1 与 MR1/MR1 AI 继续读取 `totalcorner-research-bridge/data/football_display_names/`。MR1 AI browser-forward/reconcile 已停止读取其旧 registry snapshot（快照保留为历史证据），改用 workflow checkout 的同一共享库；MR1 代码提交 `c9a6ccc`。解析/隔离测试通过，未改模型、策略、账本或通知规则。
- 历史报告：`results/football_chinese_bulk_report.md`、`data/football_display_names/coverage.json`；其多文件结构仅作为历史审计，不是现行映射入口。
- 唯一共享库仍为 M1 仓库 `data/football_display_names/`。M1 formatter 按 team/league ID 读它；M1 scan preflight 只报告展示映射缺口，不阻塞正式锁单。MR1 AH、MR1 AI browser-forward/reconcile 与 MR1 Telegram formatter 从 `external/football-display-registry` 读取同一库，运行 workflow checkout 主仓 master。名称只影响展示，不进入模型字段。
- `totalcorner-research-bridge` 以 `52fe40d9164560caf3232740762b035ed70391af` 为基础的原统计属于历史快照，现由顶部本轮提交结果替代。英文身份与中文覆盖数字请以顶部新结果为准。
- 最新已保存 M1 scan `results/latest.json`：88 场、176 个唯一 team ID；175 个有 canonical 中文展示名（99.43%），39 个 league ID 全部覆盖。唯一未确认中文名为 `FC Livyi Bereh`（ID 86544）；不以猜译补齐。扫描报告 `results/m1_telegram_display_unresolved.json` 已重算。
- 当前扫描池补充名使用 7M、500彩票网、Sofascore、Titan007、FootballAnt、公开中文球队资料等逐条链接的来源；未改既有正确映射。近期重点包含施利马流浪、格兹拉联、波德布雷佐瓦、斯拉文贝鲁波、维京古尔、利雅得青年人、布赖代合作、阿根廷青年人、塔勒瑞斯、纽维尔老男孩等。来源 URL 写在每个 curation row 的 `source.reference`。
- 已验证共享读取：MR1 `src/football-display-names.js` 实际加载本次 M1 共享库，并对测试 fixture 渲染中文；MR1 AI browser-forward/reconcile、Telegram formatter 均使用该 resolver。`615542b96` 的 MR1 对接测试通过；直接挂载本次共享目录的只读测试 2/2 通过。M1 formatter/coverage/recovery 测试 12/12 通过。
- run `38178789455` 是已完成的历史身份恢复；旧手动 workflow 已在本次重构中退役，不再重复采集。
- 公开中文名称来源已使用现成映射库 `qqyg000/lottery-football`（英文别名到中国体育彩票规范名）；精确、唯一的 ID 映射可自动导入，多候选不自动裁决。7M/中文体育彩票及主流中文比分来源的核验链接见执行对话/共享库每条 `source.reference`；继续以 ID 和来源为依据，不按名字近似合并。
- MR1 代码已有历史显示修正器 `src/v6-ah-formal-display-repair.js`，但目前没有 workflow 调用它；M1 与 MR1 AI 仍缺历史消息批量 edit 的独立部署/回执。不得把未来 formatter 测试说成历史 Telegram 已修复，也不得重发历史正式单。
- 本轮未改 M1/MR1 策略、模型、阈值、scope、订单/结算账本或正式 Telegram 新单规则。历史 Telegram 仍未批量 edit：MR1 现有 repairer 尚未接入受控流程；M1/MR1 AI 也需要独立、可审计的 edit 任务。任何修复都只能按原 message ID 调 `editMessageText`，不得重发或更改盘口、价格、方向、时间、结算字段。

## 2026-10-12 用户明确要求持续跟踪的非正式研究线索
用户要求：保留以下亮眼方向持续跟踪，不得跨会话遗忘。**这不是批准实战发单，也不是新增自动晋级 Gate、数量门槛或策略规则。** 正式 TG 统计与研究样本必须隔离。

1. **MR1 OU T1 小球反买大球**：历史模拟 56 场，反向 +6.575 U、ROI +11.74%；LOCKED_EVALUATION 16 场，+0.8125 U、ROI +5.08%。反向平均 CLV -0.0404，正 CLV 比率约 7.4%，需同步跟踪这一不利信号。来源 `mr1-shadow/data/mr1-v6-cross-market/ou-t1-reverse-validation/summary.json`。
2. **M1 俱乐部 OU 强残差与市场确认**：先期 12 场开发样本冻结残差阈值 0.683，后段 7 场 +2.425 U、ROI +34.64%；其中强残差 3 场 +2.025 U、ROI +67.5%，强残差且市场确认 2 场 +1.65 U、ROI +82.5%。小样本、子集重叠，不得重复计算独立样本。来源 `totalcorner-research-bridge/research/m1-ou-challenger-v1/summary.json`；前瞻跟踪 `research/m1-ou-challenger-v1/forward-shadow-report.json`（最新 38 条俱乐部诊断，11 已结算）。
3. **MR1 AH 连续盘口确认/P75 噪声确认**：开发样本 4 场 +2.65 U、ROI +66.25%；尚不能视为锁定评估成功。来源 `mr1-shadow/data/mr1-v6-cross-market/ah-stable-edge-combined-research/summary.json`。
4. **M1 国家队 OU 反买**：历史 25 场反向 +4.05 U、ROI +16.20%；独立 Crown 前瞻截至该快照 0 条合格触发/0 条结算，不得将历史成绩冒充前瞻。来源 `totalcorner-research-bridge/research/m1-ou-challenger-v1/summary.json` 和 `research/m1-national-ou-reverse-v1/forward/summary.json`。

后续研究会话应读取上述原始文件最新生成时间，继续更新样本、结算、ROI、回撤、CLV 和独立前瞻证据；不改变已确认的正式模型运行，不擅自将研究线索升级为 TG 实战。

## 2026-10-12 共享中文名称运行源收敛（本节优先于旧多文件说明）
- 唯一运行时映射文件为 `ljm198964-alt/totalcorner-research-bridge/data/football_display_names/display_names.json`。它将既有 teams、competitions、aliases、curation、auto-curation、provider overrides 等层精确合并；旧映射层校验等价后退役，历史审计/覆盖证据保留。
- M1、MR1 AH、MR1 AI 的展示及名称核验读取器统一消费该单文件；映射只用于展示/名称身份文本核验，不进入模型计算。M1 每轮 Wikidata 自动补名步骤已移除，preflight 仅报告展示缺口且不阻塞锁单。
- 全历史批量身份恢复 workflow 与一次性 harvest 工具已退役，避免重复全库查询。旧报告里的全历史覆盖率仅为历史快照，不代表当前正式赛事范围覆盖率。
- 后续正式范围统计按 M1 当前范围/正式池、MR1 AH 当前范围/前瞻池、MR1 AI 正式镜像范围实际计算；不得通过猜译补全。不要建立 MR1 私有映射副本或第二个中文名称库。
- 本次只调整展示数据源和名称恢复工程入口，不修改模型、策略、赛事范围、阈值、账本、结算或正式通知规则。
- 部署提交：共享库/M1 `b6520ab1d563d2537c312a54897b878dfb874d51`；MR1 reader `7ac52fb7f737b50a25264f65dd3efd09bbbd9bd6`；quant-runner workflow/handoff `39d6602a0d61c41999532e99fb4261eb23e06550`。
- 共享库 README/覆盖报告说明最后更新于 `d64eb4b43fbd78dd0e9d186882b40c82c027ded1`；其中补录 M1 OU R1 的实测覆盖为 52/52。
- 本机验收：M1 显示与正式运行相关单测 20/20；MR1 共享名称/AI 前瞻/历史显示修复专项测试 5/5，`npm test` 通过。只读云端 smoke run `38182821814` 在 runner 启动前被 GitHub 账户支付/支出限制拦截，零代码步骤执行；因此云端 runner 验收未通过，不能记作 PASS。

## 2026-10-12 中文名称库补充核验（最新）
- 共享库/M1 当前提交：`e514a86240f9029c2ad447a07a62517c96ffa274`。复用既有 team IDs，仅增加带逐项来源的映射；全库 12,172 个 ID 均有 provider 英文身份，canonical 中文 3,651（30.00%），全库尚未映射 8,521。正式 M1/MR1 union 2,468 ID 中 canonical 1,639（66.41%），829 未映射；M1 1,202/1,576（76.27%），MR1 AH 1,283/1,921（66.79%），M1 OU-R1 52/52。MR1 AH 当前 prospective fixture 池 1,529/1,934 名称槽可展示（79.06%）。
- 新增校验项含布拉格杜克拉、斯塔泽舒夫、卢多戈雷茨B队、瓦赫达麦加、亚达禾、阿尔纳泽马、阿尔泰伊、奥斯特拉瓦巴尼克B队、蒙塔纳、斯梅代雷沃、PAOK沙朗历基B队；源链接保存在 registry 行内。未能找到可靠主流中文名的仍保持 unresolved，不以机器翻译填充。
- 最新提交只改共享 registry 与正式范围统计；M1 单测 20/20 通过，MR1 共享 registry/browser-forward 定向测试 5/5、`npm test` 通过。其余本机未提交更改属于既有用户文件，未纳入提交。
- 云端 smoke run `38182821814` 仍是 runner 启动前遭账户支付/支出限制拦截，不能据此宣称云端部署验证通过；本轮没有触发生产扫描、Telegram 或账本写入。

## 2026-10-12 中文名称库全量身份/来源复核
- 最新共享库提交：`2a607c9acedd07adfc91b6c0a55294221623e0ee`；唯一库仍是 M1 仓库 `data/football_display_names/display_names.json`。本轮精确复核已保存的 24,888 行 `lottery-football` 名称表及其全部 TotalCorner 身份别名，新增 team_id `1407` / `T.N.S.` → `新圣徒`（Sporttery 明确 English alias `The New Saints`），没有按 ID 猜名，也没有合并球队 ID。
- 最终全库 12,172/12,172 英文身份可恢复；canonical_zh 3,652（30.00%），未映射 8,520；已记录身份冲突 0、译名冲突 0。115 条旧 `curated_transliteration` 保留但单独标识，不计入可追溯来源数（3,537）。未映射逐条及原因写入共享库旁审计清单，不是第二份名称库。
- 更新后的正式范围：M1 1,203/1,576（76.33%），MR1 AH 1,283/1,921（66.79%），M1+MR1 去重并集 1,640/2,468（66.45%），M1 OU-R1 52/52。MR1 AI 与 M1 共享同一展示登记读取路径。
- M1 单测 20/20，MR1 shared registry/browser-forward 5/5；本地同一 canonical 文件在 M1、MR1 两个 formatter 中都把 `T.N.S.` 渲染为「新圣徒」。
- 远端 MR1 只读 registry smoke `38185225540` 及历史批量恢复 run `38138357332` 均在 runner 启动前失败；GitHub annotation 的具体原因是账户近期付款失败或支出限制，两个 job 均无执行 steps/log。不能记为云端 PASS；共享库 Git push 本身已成功。未触发任何策略运行、Telegram 或账本写入。

## 2026-10-12 全量身份恢复续核（最终）
- 共享库最新提交：`ae67d2f4075de83006b5ba03612294fae81ec168`。只读扫描当前 MR1 master `a2997be5f8e8a9418b21ac2c64cd9437fb08a525` 的 124,392 个存档文件，712,870 次身份观察；将此前共享库缺失的 104 个 MR1 team ID 和原文证据路径加入唯一运行时登记。104 个均有唯一英文 provider identity，未用 ID 猜队名；其中 4 个新增来源核验的中文名。MR1 旧样本有 2 个仅大小写/女足标记差异，存为 aliases。4 个新增中文名均保留独立 identity_source 与 canonical 中文名来源。
- 最终共享库 12,276 个 team ID，provider 英文身份 12,276/12,276；canonical 中文 3,656，未匹配 8,620，覆盖 29.78%。其中 3,541 条有可追溯来源或引用；115 条旧 `curated_transliteration` 保留但不计为已核验主流译名。身份冲突 0，已标注译名冲突 0，精确英文 alias 歧义 4；771 个 league ID 中 329 个有 canonical 中文名。
- 正式范围快照：M1 1,203/1,576（76.33%）；MR1 AH 1,283/1,921（66.79%）；M1+MR1 union 1,640/2,468（66.45%）；M1 OU-R1 52/52。104 个新存档 ID 没有 league_id 证据，不纳入正式范围分母。
- 本地验证：M1 20/20 tests；MR1 shared-display/browser-forward 5/5 tests。共享数据新增 7M/中文来源核验：FC Jazz→爵士FC、Hougang United FC→后港联、Balestier Khalsa FC→马里士他卡沙、Newcastle Jets→纽卡斯尔喷气机。没有改 M1/MR1/MR1 AI 模型、策略、阈值、账本、结算、通知或调度。
- GitHub Actions 只读 smoke 的已知结果仍是 runner 启动前被账户付款/支出限制拦截；无步骤日志，云端 smoke 不可记 PASS。本次只推共享名称库数据和审计，不触发生产扫描或 Telegram。

## 2026-10-12 共享足球中文名正式范围补齐（最新）
- M1/共享库最新提交：`e66ae3c958dbb7f043cc1a4f97baa91cf919a7d5`，已 push 到 `totalcorner-research-bridge/master`。唯一运行时库仍为 `data/football_display_names/display_names.json`；没有新增 MR1 私有名称库。
- 在正式未匹配清单上新增 88 个 team ID：13 个有中文足球来源的逐队名称、70 个由唯一已映射基础球队名加 TotalCorner 明示的 U 年龄/二队/B队/女足/奥运/预备队标记形成的稳定展示名、3 个唯一共享库别名复用、2 个 Sporttery/中文数据别名映射。所有来源和 identity/base ID 记录在 registry 对应行。
- 最终实际文件统计：球队 ID 12,276；英文 provider identity 12,276/12,276；canonical 中文 3,744；全库 unresolved 8,532；全库覆盖 30.50%。现有英文身份冲突 0、标记译名冲突 0；4 个新增重复 canonical label 组经核对属于同队 provider 别名或国家队拼写变体，ID 均保留独立；全库重复 canonical 名称 review signal 共 43 组。771 个赛事 ID 中 329 个有中文名。
- 正式范围：M1 1,287/1,576（81.66%）；MR1 AH 1,323/1,921（68.87%）；M1+MR1 去重并集 1,728/2,468（70.02%）；MR1 AI 声明范围镜像 M1，为 1,287/1,576；M1 OU-R1 52/52。MR1 AI confidence>=50 的 91-entry/182-team 子队列按历史快照保留为 181/182，本批没有重建其单独成员资格；不要把它和声明镜像范围混算。
- 最新已保存 M1 scan `M1_20261012T011531Z` 有 32 场/64 个唯一 team ID，63 个已映射（98.44%），唯一 unresolved 为 FC Livyi Bereh（ID 86544）；经本轮检索仍缺可靠主流简体中文队名，保留 unresolved。正式范围剩余 740 条逐 ID 留在 `formal_scope_coverage.json` 与 `curated_batch_report_20261012.json`，reason_detail 均说明本轮没有建立唯一、有来源的 canonical 名称；不得猜译。
- 中国体育彩票映射源 `qqyg000/lottery-football` 本次按 24,888 行 CSV 全表精确/规范化唯一匹配；formal unresolved 中新增 2 个可验证命中（PK-35、Ankaragucu）。本轮亦检查现有共享英文 alias 命中；无其他可唯一复用项。没有重跑全历史身份恢复、调用 TotalCorner API 或猜 ID。
- Reader/接入：M1 formatter、M1 non-blocking preflight；MR1 AH、MR1 AI browser-forward/reconcile、Telegram formatters 均读取同一共享文件。MR1 workflow checkout `totalcorner-research-bridge/master`。本批无需修改 MR1 生产代码。
- 本地验收：M1 display/formal-runtime 相关测试 20/20 通过；MR1 shared registry/AI forward 定向测试 5/5 通过，完整 `npm test` 通过。两边直接读取最终 registry 的中文渲染 smoke 通过；当前 pool preflight `strategy_gate=false`。没有运行生产 workflow、发送 Telegram 或改写 ledger。
- GitHub Actions 本轮未能做云端 smoke；已知当前账户付款/支出限制会使 runner 启动前拦截，不能登记云端 PASS。Git 数据 push 成功。
- 本机 M1 仓库保留未提交的既有用户修改 `.gitignore`、`package-lock.json`、`__pycache__/`、`results/competitor_zou/`，未纳入本次提交。策略、模型、Crown 来源、scope、账本、结算及通知规则均未修改。

## 2026-10-12 正式范围中文名称续补（本轮）
- 共享库最新提交：`8098ed2dcc3e2ab141344270187fe8cc766f29ae`，已 push 到 `totalcorner-research-bridge/master`。只修改唯一共享 `display_names.json`、正式范围覆盖/批次审计，以及可重复校验并导入国家/地区代表队中文名的 `ops/curate_formal_scope_national_teams.py`；未新增第二份名称库。
- 基于最新正式清单核对后，新增 22 个具有可核验中文来源的 team ID（含中华台北、缅甸、佛得角、安提瓜和巴布达、文莱、老挝、尼泊尔、巴斯克、加泰罗尼亚、不丹、蒙古、关岛、阿富汗、毛里求斯、土库曼斯坦、吉布提、乍得、中国澳门、桑给巴尔、美属维尔京群岛、斯威士兰等）。名称及逐条 source/reference 保存在共享 registry 和 `curated_batch_report_20261012.json`。未映射项没有猜译；准确性优先。
- 最新正式范围统计：M1+MR1 去重 union 2,468 个 team ID，已映射 1,750、未映射 718，覆盖 70.91%；M1 1,309/1,576（83.06%）；MR1 AH 1,324/1,921（68.92%）；MR1 AI 声明镜像范围 1,309/1,576（83.06%）；M1 OU-R1 52/52（100%）。全共享库 12,276 个 team ID，canonical 中文 3,766，provider 英文身份 12,276/12,276；全库中文覆盖 30.68%。各口径均由最新文件计算，不能与此前快照混用。
- 来源复用/核验：本轮检查已有体育彩票映射、QiuXiaoCe/公开映射及 Wikidata 中文标签；精确匹配没有产生可安全新增的球队结果。额外补充的 22 项来源分布：7 项成熟中文足球资料页、3 项 7M、1 项 Sofascore、11 项 Wikidata 国家/地区简体标签并结合 International Match 代表队身份。疑似同名或无法证明是目标球队的候选均保留 unresolved。完整 718 条清单和逐条原因见共享库 `data/football_display_names/formal_scope_coverage.json`。
- 中文显示本地验收：M1 formatter/preflight 及相关回归测试 20/20 通过；MR1 共享 registry/AI forward 定向测试 5/5 通过，完整 `npm test` 通过。M1 与 MR1 resolver 均直接读取该唯一共享文件；新增国家队/地区队样例隔离渲染为中文。MR1 仓库本轮未修改。
- 已发送消息审计（没有发送新消息）：M1 AH 与 M1 OU-R1 共用的历史修复 dry-run 仍有 37 条候选，但 Telegram 对既有 37 条返回 `ALREADY_MATCHING`，本轮没有新 edit；另有 99 条缺原消息文本、70 条名称仍未映射。MR1 AH 既有修复累计实际编辑 6 条，后续 123 条已处理/无新变化，本轮没有新 edit。MR1 AI 9 条旧消息的历史 edit 曾全部返回 `400: message to edit not found`，当前仍不可编辑；另 192 条仍缺可确认修复资料。没有重发任何历史订单，没有改变盘口、方向、水位、账本或结算。
- 云端正式链没有触发生产扫描或 Telegram。共享文件已推送，未来 checkout master 的格式器可读到新名称；但本轮未取得新的云端 runtime 回执，因此仅记本地 PASS，不宣称云端运行验证完成。历史消息中的 Telegram message-id/chat 目标限制仍需有可编辑的原始消息证据才能处理。
- 未修改 M1/MR1/MR1 AI 模型、策略、赛事范围、阈值、皇冠来源、正式订单、结算、通知规则或调度。quant-runner 的本 handoff 需随本节单独提交。

## 2026-10-12 正式范围中文名称续补（二）
- 共享库最新提交 `c4d58b1d2d81e721ee1e8669b28bc22fd5f20e88` 已推送并核对 `totalcorner-research-bridge/master`。唯一 registry 保持不变；本次新增 23 个正式 scope team IDs，来自中文维基洲际顶级联赛表中中文队名与英文队名同一行的精确对应，涉及欧洲、亚洲和南美页面。来源 URL 与精确英文行记录在 registry 和批次报告；脚本 `ops/curate_formal_scope_public_club_tables.py` 在写入前检查 ID 仍 unresolved、不覆盖已有 canonical 名，并校验英文身份的重音/俱乐部后缀规范化精确相等。
- 本次覆盖变化：正式 union 2,468 中 canonical 1,773、unresolved 695（71.84%）；M1 1,332/1,576（84.52%）；MR1 AH 1,338/1,921（69.65%）；MR1 AI 声明镜像 1,332/1,576（84.52%）；M1 OU-R1 52/52。共享库 12,276 IDs、canonical 3,789（30.87%），provider English identity 12,276/12,276。逐条余项见 `data/football_display_names/formal_scope_coverage.json` 的 `unresolved_records`。
- 来源页面：欧洲顶级足球俱乐部列表、亚洲足球俱乐部列表、南美洲足球俱乐部列表；只取带中文名和英文/外文名列的球队行，未把城市列或荣誉字段误当队名，也未做模糊拼写匹配。候选确认包括迪纳摩城、埃斯卡尔德斯体育俱乐部、加巴拉、索菲亚火车头、内姆梅卡柳、青岛西海岸、艾费哈、石油联盟等；英文注释括号已从来源展示标签清理，底层身份原文及 ID 不变。
- M1 回归测试 20/20 通过；MR1 shared registry/AI-forward 测试 5/5 通过，完整 `npm test` 通过。测试期间第一次从 MR1 目录误启动 M1 Python 测试，因测试模块不在该目录而导入失败；随即在 M1 仓库正确重跑并 20/20 通过。没有生产 workflow、TG 或账本操作。
- MR1 AH/MR1 AI/M1 TG formatter 继续消费唯一共享 registry；历史 TG 消息本轮未编辑或重发。新映射只进入展示 registry，不改模型、策略、scope、阈值、账本、结算或 Telegram 投递规则。

## 2026-10-12 正式范围中文名称续补（三）
- 共享 registry 最新提交 `c4d58b1d2d81e721ee1e8669b28bc22fd5f20e88` 已推送至 `totalcorner-research-bridge/master`。本次从中文维基洲际顶级联赛表中精确匹配 23 个 formal-scope ID 的英文/中文同表球队行；没有使用 fuzzy match。新增映射数据及审计清单在共享库，采集/验证程序 `ops/curate_formal_scope_public_club_tables.py`。
- 最新实算：formal union 2,468 中已匹配 1,773、未匹配 695（71.84%）；M1 1,332/1,576（84.52%）；MR1 AH 1,338/1,921（69.65%）；MR1 AI 镜像 1,332/1,576（84.52%）；M1 OU-R1 52/52。全共享库 12,276 IDs、canonical 3,789（30.87%）、英文身份 12,276/12,276。
- M1 测试 20/20；MR1 shared registry/AI-forward 5/5，`npm test` 通过。只验证展示解析，本轮无生产 runtime、TG、订单或结算操作。M1/MR1/MR1 AI 策略和范围均未改变。

## 2026-10-12 正式范围中文名称续补（四）
- 共享库最新提交 `1bdc1263a5ad5878a33500239efc622df764af36` 已推送到 `totalcorner-research-bridge/master`。本轮新增 11 个正式范围 team ID，来源包括中文洲际/威尔士球队名表、7M、雷速及球探资料；脚本 `ops/curate_formal_scope_club_tables_batch2.py` 仅允许未映射正式 ID，通过重音、F.C./A.F.C. 写法及 Utd→United 明确缩写规范化后的精确身份匹配，不使用模糊拼写，也拒绝覆盖已有 canonical。
- 新增名称：图兹拉自由、恩维加多、帕特里奥坦斯、纽约城、西雅图海湾者、费罗尔竞技、邓迪联、卡纳芬镇、普雷斯塔廷城、拉内利、斯芬杜特斯。逐项来源写在 registry `source.reference` 和批次报告；西雅图海湾人、博亚卡爱国者、费罗尔竞赛会等作为别名保存。
- 最新统计：formal union 2,468 中 canonical 1,784、unresolved 684（72.29%）；M1 1,343/1,576（85.22%）；MR1 AH 1,345/1,921（70.02%）；MR1 AI 声明镜像 1,343/1,576（85.22%）；M1 OU-R1 52/52。全共享库 12,276 IDs、canonical 3,800（30.95%）、provider English identity 12,276/12,276。余项逐条见 `formal_scope_coverage.json` 的 `unresolved_records`。
- 本轮 M1 display/formal-runtime 测试 20/20 通过；MR1 shared registry/AI-forward 5/5，完整 `npm test` 通过。仅更新展示名称与审计数据；未运行生产扫描、发送/编辑 TG，未改模型、策略、范围、阈值、账本、结算或通知规则。

## 2026-10-12 正式范围中文名称续补（五）
- 共享 registry 最新提交 `8a31f0a9e066c475516874f1840f7f9034c2d253` 已推送到 `totalcorner-research-bridge/master`。本轮根据 7M 中文球队档案新增 7 个精确匹配 team ID：克拉科维亚、涅波沃米采、尤尼史洛波西亚、哥利亚布沙、辛迪亚泰哥维斯特、梅塔洛格布斯、CS布加勒斯特迪纳摩。每条保存 7M 页面来源和原 TotalCorner identity；名称库及 scope coverage 均从最新提交数据更新。
- 最新实算：formal union 2,468 中 canonical 1,791、unresolved 677（72.57%）；M1 1,350/1,576（85.66%）；MR1 AH 1,351/1,921（70.33%）；MR1 AI 声明镜像 1,350/1,576（85.66%）；M1 OU-R1 52/52。全共享库 12,276 IDs、canonical 3,807（31.01%），provider English identity 12,276/12,276。未匹配条目及原因见共享 `formal_scope_coverage.json`。
- 新增脚本 `ops/curate_formal_scope_7m_batch3.py` 在写入前校验 ID 仍属正式 unresolved 集、拒绝覆盖已有 canonical，并以可核验 7M 英文/中文球队档案作为来源。M1 display/formal-runtime 测试 20/20；MR1 shared registry/AI-forward 5/5，完整 `npm test` 通过。没有触发生产运行或 Telegram 发送/编辑，也未改模型、策略、赛事范围、阈值、账本或结算。

## 2026-10-12 正式范围中文名称续补（六）
- 在 7M 档案批次之后再补 3 个正式 ID：敖德萨黑海人、普莱斯堤纳、哈尔科夫冶金1925。共享提交 `899c06492f96816c12de18a546e14a35b9536710` 已推送；来源分别为雷速球队档案及 7M 对应球队档案，并保留原 provider identity。两个近似但可能有不同实体历史的 Metalurh Zaporizhya ID 暂不合并，继续列为 unresolved。
- 当前正式 union 2,468 中 canonical 1,794、unresolved 674（72.69%）；M1 1,350/1,576（85.66%）；MR1 AH 1,354/1,921（70.48%）；MR1 AI 声明镜像 1,350/1,576（85.66%）；M1 OU-R1 52/52。全共享库 12,276 IDs、canonical 3,810（31.04%）。逐条余项仍以 `formal_scope_coverage.json` 为准。
- M1 tests 20/20、MR1 focused 5/5 和完整 `npm test` 再次通过。只更新名称展示数据/审计，未触发 production/TG，未修改任何模型、策略或账本。

## 2026-10-12 正式范围中文名称续补（七）
- 共享 registry 提交 `c654c317d5e0c427231582e8c92a2a91cb7c0cb8` 已推送到 `totalcorner-research-bridge/master`。仍使用唯一 `data/football_display_names/display_names.json`，新增 8 个有公开中文球队资料来源、并与正式 TotalCorner team ID 直接交叉核实的名称：艾玛卡沙、艾尔明亚、法尤姆FC、艾尔扎尔夸、卡夫尔、阿拉布达曼豪尔、阿斯旺FC、埃及电信。来源和 ID 均保存在 registry 与批次审计。
- 最新文件实算：正式并集 2,468，已映射 1,802、未映射 666（73.01%）；M1 1,360/1,576（86.29%）；MR1 AH 1,361/1,921（70.85%）；MR1 AI 声明镜像 M1 1,360/1,576（86.29%）；M1 OU-R1 52/52。全共享库 12,276 IDs、canonical 3,818（31.10%）。
- 对拼写相近但身份交叉不足的 Abo Qir Semad 暂不补名，继续 unresolved，避免仅凭联赛或音译相似合并。批处理脚本为 `ops/curate_formal_scope_footystats_batch.py`，拒绝覆盖已有 canonical，并在写入前校验正式范围身份。
- M1 display/formal-runtime 相关测试 20/20 通过。此次只改展示 registry/审计文件；没有生产扫描、Telegram 发送或编辑，也未改模型、策略、赛事范围、阈值、正式账本或结算。待办：继续处理 formal unresolved 清单；分别审计 M1、M1 OU-R1、MR1 AH、MR1 AI 现有 TG 消息的可编辑原始 message ID，并仅对可确认的历史消息执行获授权的文字替换；尚无本轮实际编辑回执。

## 2026-10-12 正式范围中文名称续补（八）
- 最新共享 registry 提交 `70f237cf2ec134ec455dd43cc89298bf15dcf223` 已 push 到 `totalcorner-research-bridge/master`。相较上一节又新增 4 个正式 ID：南蒂罗尔、阿特罗米托斯、索菲亚斯拉维亚、帕提萨尼；各项保留原 TotalCorner ID/英文身份、中文资料来源及别名，不建立第二份名称库。
- 最新文件实算：formal union 2,468，已匹配 1,806，未匹配 662，覆盖 73.18%；M1 1,365/1,576（86.61%）；MR1 AH 1,366/1,921（71.11%）；MR1 AI 声明镜像 1,365/1,576（86.61%）；M1 OU-R1 52/52；共享库 12,276 IDs、canonical 3,822（31.13%）。全量 unresolved 逐条原因以共享文件 `data/football_display_names/formal_scope_coverage.json` 为准。
- 验收：M1 display/formal-runtime 测试 20/20；MR1 `npm test` 通过。隔离渲染证明新 ID 经 MR1 `football-display-names.js` 及 M1 formatter 输出 canonical 中文，M1 AH/OU-R1 共用 `m1_notification.py` 的 formatter；MR1 runtime 从 M1 仓库 master checkout 同一 shared registry。M1历史编辑 dry-run 37 条具备原文的候选、99 条缺保存原文、70 条名称未匹配；本机没有 M1 TG 凭据，未执行任何编辑。MR1 AH 现有 v5 审计为 123 条跳过/无变化；MR1 AI 最近 9 条编辑失败、192 条未解决，本轮不重试或重发。尚无本轮实际 TG 历史编辑回执。
- GitHub Actions 云端 smoke 未启动；本轮没有触发生产 runtime 或测试消息。仅名称/显示层变更，没有修改任何模型、策略、范围、投注/结算账本或 TG 派单规则。下一步继续处理剩余 662 个 ID，并在拥有安全 Telegram 运行环境和可编辑原始消息时处理历史展示文本。

## 2026-10-12 正式范围中文名称续补（九）
- 共享 registry 最新提交 `bff46c865c2c6223e98f2672dc12982b778b7de6` 已推送至 `totalcorner-research-bridge/master`，新增 4 个正式 team ID：墨西哥美洲队、蒂华纳、札幌冈萨多、埃斯比约；名称均附对应球队中文资料和英文 identity source。复用同一 shared registry，不新增库。
- 最新统计：正式并集 2,468，已匹配 1,810，未匹配 658（73.34%）；M1 1,369/1,576（86.87%）；MR1 AH 1,369/1,921（71.26%）；MR1 AI 声明镜像 1,369/1,576（86.87%）；M1 OU-R1 52/52；全共享库 12,276 IDs、canonical 3,826（31.17%）。逐项未匹配原因由 `formal_scope_coverage.json` 提供。
- M1 display/formal-runtime 测试 20/20 通过。名称变更仍只限展示层；没有生产运行、TG 派单/编辑或账本/模型/策略修改。剩余 unresolved 继续按联赛分组核证，不作机器猜译。

## 2026-10-12 正式范围中文名称续补（十）
- 共享 registry 提交 `fd619093348d06c6caf99bfed9bb6a3eccffc5b0` 已推送；本轮新增华雷斯（ID 14139）和马萨特兰（ID 68824），均来自 7M 对应球队资料页并与正式英文 identity 核验。
- 最新统计：formal union 2,468，已匹配 1,812、未匹配 656（73.42%）；M1 1,371/1,576（86.99%）；MR1 AH 1,370/1,921（71.32%）；MR1 AI 镜像 1,371/1,576（86.99%）；M1 OU-R1 52/52；共享库 12,276 IDs、canonical 3,828（31.18%）。完整未匹配表与 reason_detail 仍在同一 `formal_scope_coverage.json`。
- M1 display/formal-runtime 测试 20/20 通过；本次只改展示库及其审计。未触发生产任务、TG 编辑/发送或模型、策略、范围、正式账本改动。

## 2026-10-12 正式范围中文名称续补（十一）
- 共享 registry 新提交 `abb06d2b45a030c843d91d8512cf1be9e2c04c40` 已推送至 `totalcorner-research-bridge/master`。在保留原有数据的基础上新增 14 个来源核验映射：哈森姆、利雅得体育、达曼协作、吉达联合、波德戈里察未来、瓜达拉哈拉、苏杜瓦、奥达巴斯、多瑙斯特雷达、阿什杜德、斯科普里冶金、查洛摩亚，以及此前同批已并入的华雷斯、马萨特兰。每条带 team_id、原始英文名、别名和来源链接；不改模型身份字段。
- 以当前 `formal_scope_coverage.json` 实算：正式并集 2,468，canonical 中文 1,824，未匹配 644，覆盖 73.91%；M1 1,383/1,576（87.75%）；MR1 AH 1,381/1,921（71.89%）；MR1 AI 声明镜像 M1 1,383/1,576（87.75%）；M1 OU-R1 52/52；共享库 12,276 IDs、canonical 3,840（31.28%）。未匹配逐项和原因继续以共享覆盖文件为准。
- M1 formatter (`m1_telegram_display.py`) 和已有消息编辑脚本都读取该唯一 registry；MR1 AH/AI 运行工作流通过私有只读 checkout 拉取相同共享库。隔离验证没有更改 Telegram。历史 TG 编辑尚未执行：本机未配置 M1 bot credentials；不使用其它系统凭据，也不重发历史订单。MR1 runtime 未触发，云端因既有 GitHub 支出限制暂不可验收。
- 本地 `python3 -m pytest -q test_m1_telegram_display.py test_m1_telegram_display_repair.py test_m1_formal_runtime.py`：20 passed；三个 JSON 文件解析通过，`git diff --check` 通过。根 package 未定义 `npm test`，因此不把该命令错误视为失败，也未声称 MR1 云端验收通过。
- 下一步按正式 unresolved 清单继续逐项核验；不要对身份不确定的队伍猜译。Telegram 历史编辑须在安全提供对应 M1/M1 OU-R1/MR1 AH/MR1 AI 专用凭据、确认原始消息 ID/原文和对应可编辑通道后逐条执行，仅替换球队/赛事显示名称，不改订单内容或结算。

## 2026-10-12 正式范围中文名称续补（十二）
- 共享 registry 已推送提交 `98ce58cb6fd39449a3f957b706899c6d63621525`。本轮追加 10 条带公开资料引用的正式映射：加斯梅登、乌利斯、格林达维克、泛亚加亚、哈尼亚、科特布斯、瑟兰、斯米尔尼阿波罗、特里耐克、普塔达韦城。原 provider identity/team ID 均保留；异体/旧名仅放 aliases。
- 当前文件重新统计：formal union 2,468，mapped 1,834、unresolved 634（74.31%）；M1 1,393/1,576（88.39%）；MR1 AH 1,388/1,921（72.25%）；MR1 AI mirror 1,393/1,576（88.39%）；M1 OU-R1 52/52；共享 registry 12,276 IDs、canonical 3,850（31.36%）。最新未匹配球队和逐项 reason 以 `data/football_display_names/formal_scope_coverage.json` 为准。
- M1 展示、消息编辑脚本读取同一共享 registry，MR1 Actions runtime 通过只读 checkout 加载；formatter/repair/runtime 定向测试 20/20 通过，JSON 校验及 `git diff --check` 通过。`package.json` 未定义 npm test script。
- 本轮未运行生产 scan、未发送/编辑 Telegram，也未修改策略/账本。历史消息编辑仍受本机无 M1 Telegram 专用凭据阻挡；不得借用 MR1 凭据或重新发送旧 Pick。GitHub Actions runner 既有支出限制尚未解除，云端 smoke 不宣称通过。

## 2026-10-12 正式范围中文名称续补（十三）
- 共享库最新提交 `956bc9aefcda146684971d87a9fd268a305fea05` 已推送。继续按公开中文球队档案及区域联赛中英对照表的精确英文身份配对新增 27 项，涵盖查洛里、莫达伦、阿伯里斯特威斯、阿费查尔丁、IR雷克查域克、塞尔福斯、斯洛图尔、富佐尼、苏博蒂察、尼什工人、纳尔瓦特兰斯、伊万尼察枫树、邦加、科马尔诺、穆拉、纳夫塔1903、久加斯、格罗比纳、贝尔格莱德红星、赫尔曼施泰特、捷迪苏、第聂伯罗第一、迪克维斯、阿尔西米、奥博隆、特泰克斯、诺尔比。每项保留正式 team_id、原 provider name、别名及来源；未确认名称继续不映射。
- 当前 formal union 2,468，mapped 1,861、unresolved 607（75.41%）；M1 1,420/1,576（90.10%）；MR1 AH 1,414/1,921（73.61%）；MR1 AI 镜像 1,420/1,576（90.10%）；M1 OU-R1 52/52；shared registry 12,276 IDs、canonical 3,877（31.58%）。完整未匹配清单及原因以 `formal_scope_coverage.json` 为准。
- M1 formatter 已用真实共享库隔离渲染新增 team_id，显示为中文队名与方向；MR1 AH formatter 亦读取同一 registry 并渲染中文。M1 display/repair/formal runtime tests 20/20；MR1 `npm test` passed；JSON/diff 检查通过。M1 历史 TG dry-run：37 条有可替换原文、99 条缺原文、70 条仍缺名称映射。dry-run 未发消息；本机没有 M1 专用 Telegram credentials，所以历史 TG 实际 edits=0。没有生产扫描、订单/结算写入或策略更改。
- Runner 尚受账户级支出限制，云端 smoke 未运行；不要将本机 formatter 测试说成生产 TG live PASS。继续剩余 607 项来源核验，并在安全可用的 M1/MR1 各自凭据及原始 editable message 证据后才执行历史文字编辑。

## 2026-10-12 正式范围中文名称续补（十四）
- 共享 registry 提交 `132183e27c916ed2c276c61807d65a7bbb3a4e9d` 已 push 至 totalcorner-research-bridge/master。本轮在唯一 `display_names.json` 新增 3 个已核验 formal IDs：MFK Chrudim（ID 1899）→赫鲁迪姆（Sofascore 简中球队页）；Fylkir Reykjavik（ID 3170）→费基亚（7M 球队页）；Gornik Leczna（ID 524）→莱茨纳（球探/Titan007 球队页）。来源、英文 identity、ID、aliases 同存于 registry；已确认 canonical 未覆盖。
- 最新实算 formal union 2,468：mapped 1,864，unresolved 604，覆盖 75.53%；M1 1,423/1,576（90.29%）；M1 OU-R1 52/52（100%）；MR1 AH 1,417/1,921（73.76%）；MR1 AI 声明镜像 M1 为 1,423/1,576（90.29%）。共享库 12,276 IDs、3,880 canonical。完整未匹配项与逐条原因见共享库 `data/football_display_names/formal_scope_coverage.json`。
- Telegram 显示接入复核：M1 AH 与 M1 OU-R1 通过 `m1_notification.py` 共用 `m1_telegram_display.py`，读取共享 registry；MR1 AH formatter、MR1 AI forward notify 通过 `football-display-names.js` 读取同一 registry。三个新增队名已用两侧 formatter 隔离渲染为中文；MR1 样本联赛 ID 114 尚无 canonical，展示层仍按现有 fallback 输出原名，尚不能宣称赛事名全中文。
- 测试：M1 定向 pytest 20/20；MR1 `npm test` 全量通过；JSON 解析及 `git diff --check` 通过。没有运行生产 Actions、策略、账本、结算、TG。
- 历史 M1 TG names-only dry-run 更新后：37 条具备原文及可映射字段；99 条缺 ledger 保存的原始消息文本；70 条仍缺映射；dry-run failed=0。当前进程环境不存在 M1/MR1 Telegram bot credentials，未编辑任何消息（成功0、失败0）；不借用另一系统 credentials、不重发订单。后续真实编辑需各系统各自可用 bot credentials 和 Telegram 可编辑原消息。
- 云端 Actions 仍受账户付款/支出限制，未触发或记为 PASS。所有更名仅展示层数据，不改 M1/MR1/MR1 AI 策略、模型、盘口、赛事范围、通知条件或账本。

## 2026-10-12 正式范围中文名称续补（十五）
- 接续时先 fetch 核对远端 master，确认共享仓库当前仍在上一提交 `132183e27c916ed2c276c61807d65a7bbb3a4e9d`；任务消息所说“718”与该最新正式范围文件不一致，覆盖 JSON 当时实际是 604 unresolved。本轮新增 2 个准确配对：Pietà Hotspurs（ID 502）→佩塔（中文百科明确配英文队名）；Carmarthen Town（TotalCorner provider 简写 Carmarthen，ID 1459）→卡马森城（中文维基俱乐部条目）。
- 共享库新提交 `cee1e57` 已 push。最新 authoritative `formal_scope_coverage.json`：正式 union 2,468，canonical 1,866、unresolved 602、coverage 75.61%；M1 1,425/1,576（90.42%）；M1 OU-R1 52/52；MR1 AH 1,419/1,921（73.87%）；MR1 AI declared mirror 1,425/1,576（90.42%）。
- M1 展示 formatter 对 ID 502、1459 隔离渲染分别得到「佩塔」「卡马森城」。M1 定向测试 20/20 通过；共享 JSON、覆盖与审计数据重新生成并校验。中文维基欧洲顶级联赛全量表交叉尝试未产生严格英文身份命中，未按近似字符串自动导入。
- 本轮没有配置 M1/MR1 Telegram credentials，未进行消息编辑或发送；此前干跑仍为 37 eligible、99 条无原文、70 条未映射。正式 TG live 修复未完成。生产 Actions 未触发。

## 2026-10-12 正式范围中文名称续补（十六）
- 共享 registry 提交 `fbc712b90d10676951ff72cf39bebd88e5634049` 已推送至 `totalcorner-research-bridge/master`。基于最新共享库实际文件继续处理；交接旧快照的 718 unresolved 已过时，本轮开始前正式清单为 600。本轮新增 3 个有可核验来源的 canonical：Middelfart（ID 2890）→米德法特、HB Køge（ID 750）→赫福尔格（均为 7M 球队页）；Al Taawon（ID 6300）→布赖代合作（FootyStats 简中球队档案，TotalCorner ID 页面确认对应 Al Taawon）。provider identity、team ID、aliases 和 source URL 均写入唯一共享 `display_names.json`。
- 最新正式范围实算：union 2,468，中文已匹配 1,869，未匹配 599，覆盖 75.73%；M1 1,428/1,576（90.61%）；M1 OU-R1 52/52（100%）；MR1 AH 1,421/1,921（73.97%）；MR1 AI 声明镜像 1,428/1,576（90.61%）。共享库 12,276 IDs、3,885 canonical。完整 599 条未匹配及逐条原因见共享 `data/football_display_names/formal_scope_coverage.json`。
- 本地显示验收：M1 formatter 对 Middelfart/HB Køge 输出「米德法特 vs 赫福尔格」，对 Al Taawon/Al Ittihad 输出「布赖代合作 vs 吉达联合」；M1 formatter/display-repair/formal-runtime 测试 20/20 通过。MR1 通过 `external/football-display-registry` 只读 checkout 读取唯一共享库；加载共享文件后的两组 fixture 中文渲染通过，MR1 `npm test` 通过。没有修改两边 formatter 或策略。
- 历史 Telegram：本轮未编辑或重发既有消息。安全环境没有可用于各自 provider 的已授权凭据及完整原始可编辑消息证据，历史 live edit=0；不能把本地渲染记为 TG 实际修复。未触发生产 workflow；账户级 Actions 支出限制仍阻止云端 smoke。
- 本批不覆盖任何既有 canonical；未确认名称继续保留 provider identity 并标记 `NO_VERIFIED_CANONICAL_ZH`。

## 2026-10-12 正式范围中文名称续补（二十一）
- 接续共享库 `c0580d75351d07bcac6fc302d16955bddc24a78b`，当前唯一库已推送提交 `701ef84`（完整 SHA 见 `totalcorner-research-bridge/master`）。用现有精确 ID 防覆盖脚本新增4条：Abo Qir Semad（5987）→艾柏卡尔瑟梅德（7M）；Wuxi Wugou（83267）→无锡吴钩（新浪体育）；Shanghai Jiading Huilong（83468）→上海嘉定汇龙（新浪体育）；Dalian Young Boy（143714）→大连英博（懂球帝官方更名报道）。来源及 provider identity/aliases 均写入唯一 `display_names.json`；未确认条目继续保留未匹配，不做临时音译。
- 最新 authoritative 统计：formal union 2,468，canonical 1,879、unresolved 589（76.13%）；M1 1,438/1,576（91.24%）；M1 OU-R1 52/52（100%）；MR1 AH 1,431/1,921（74.49%）；MR1 AI declared mirror 1,438/1,576（91.24%）；MR1 AI observed confidence≥50 cohort 181/182（99.45%，该分组仍是旧快照）。共享库 12,276 team IDs、3,895 canonical。未匹配原因/逐队清单以 `formal_scope_coverage.json` 为准。
- M1 formatter 隔离渲染四队名称成功；M1 定向 pytest 20/20 通过。MR1 通过 `FOOTBALL_DISPLAY_REGISTRY_DIR` 直接读取当前共享库；MR1 display tests 2/2 通过，两个 fixture 均输出中文。MR1 正式 workflow 在运行时 checkout 共享仓库 `master`，本地验证证明新库可消费；生产 Action 未触发。
- 本轮未编辑或重发任何历史 Telegram 消息。当前执行环境未配置 M1/MR1 Bot 凭据，且未取得可供本轮确认的账本 message-id ↔ 原文完整快照；历史实发修复仍未完成。不得将 formatter/本地测试说成 TG 实际修复。各模型策略、账本、结算及通知规则未改；Actions 仍受账户支出限制，不重复触发。

## 2026-10-12 正式范围中文名称续补（二十二）
- 在共享库提交 `701ef84ea281f822179d574a611a8f8337711cb8` 后，继续用7M简体中文球队页核实 Termalica BB Nieciecza（team_id 540）→特马利卡，资料页展示“特马利卡 (Bruk Bet Termalica Nieciecza)”。新增记录连同官方英文变体 alias 写入唯一共享 `display_names.json`，提交 `421208f` 已推送到 master。
- 最新实算：formal union 2,468，canonical 1,880，unresolved 588（76.18%）；M1 1,439/1,576（91.31%）；M1 OU-R1 52/52；MR1 AH 1,432/1,921（74.55%）；MR1 AI declared mirror 1,439/1,576（91.31%）。共享 registry 12,276 IDs、3,896 canonical；588 条均因 `NO_VERIFIED_CANONICAL_ZH` 暂未匹配，具体清单见共享 `formal_scope_coverage.json`。
- M1 formatter 隔离渲染“特马利卡”，M1 定向测试 20/20 通过；MR1 对共享注册表的测试/解析保持通过。无模型、策略、账本、结算或 Telegram 行为变化。历史 TG 仍未编辑：环境没有系统专用 Bot 凭据，也没有本轮逐条可编辑原文证据；生产 workflow 未触发。

## 2026-10-12 正式范围中文名称续补（二十三）
- 接续共享库 `421208fef14e01504dff8cd7864eda113029b8b7`，新增 Hamilton（ID 2376）→汉密尔顿学院；其 scope leagues 是苏格兰 Premiership/Championship/League One，中文俱乐部资料将 Hamilton 对应到 Hamilton Academical。新增 Viktoria Zizkov（ID 3560）→日热科夫胜利；中文俱乐部条目明确列出 FK Viktoria Žižkov 全名。新 mappings/aliases/source 均进入唯一共享库，提交 `d6bbe732bae671136f7db5087e1733bd521f193d` 已推送 master。
- 最新实际覆盖：formal union 2,468，canonical 1,882、unresolved 586（76.26%）；M1 1,441/1,576（91.43%）；M1 OU-R1 52/52；MR1 AH 1,434/1,921（74.65%）；MR1 AI declared mirror 1,441/1,576（91.43%）；置信度≥50 observed cohort 181/182（旧 cohort 快照）。共享库 12,276 IDs、3,898 canonical。未匹配逐项均在共享 `formal_scope_coverage.json`，本次未映射条目继续为 NO_VERIFIED_CANONICAL_ZH。
- M1 formatter 隔离渲染新增名称，定向测试 20/20 通过；MR1 通过运行时共享库目录测试 2/2 通过。生产 workflow 未触发、历史 Telegram 未编辑或重发；系统专用 Bot 凭据和可核对 message-id/evidence 仍不可用。没有策略或正式账本修改。

## 2026-10-12 正式范围中文名称续补（二十四）
- 继续核验 Hamilton（2376）和 Viktoria Zizkov（3560）的来源、队名与正式赛事身份。Viktoria 的中文条目列出全名 FK Viktoria Žižkov，并在简体内容中用“日热科夫胜利足球俱乐部”；Hamilton 的正式范围仅涉及苏格兰联赛，中文球队资料将 Hamilton 识别为 Hamilton Academical。两项均添加到共享库并随 `d6bbe732bae671136f7db5087e1733bd521f193d` 推送。
- 当前 authoritative 统计：formal union 2,468；canonical 1,882；unresolved 586（76.26%）；M1 1,441/1,576（91.43%）；M1 OU-R1 52/52；MR1 AH 1,434/1,921（74.65%）；MR1 AI declared mirror 1,441/1,576（91.43%）。共享库 12,276 IDs、3,898 canonical。此数字基于共享 JSON 实算，不再使用旧的718作为当前未匹配数。
- 本地 formatter 对两队渲染通过；M1 定向测试20/20、MR1共享库读取测试2/2。额外交叉比对 legacy M1显示报告未发现可直接复用的正式未匹配ID中文名；exact alias 命中 Jeddah Club（42718）但现有同名 alias关联到吉达联合（3397），联赛ID显示它们不是同一队，因此保留 unresolved，没有错误合并。
- 没有修改任何策略/账本/结算或发送条件；生产 workflow、历史 Telegram 编辑/重发均未执行。继续按来源证据补齐其余队名。

## 2026-10-12 正式范围中文名称续补（二十五）
- 共享 registry 提交 `53938b00c91806ce07653d3e384abe4ebc8b20cf` 已推送。本轮依据 Tips.GG 简中 El Shams 球队页新增 ID 3887 →“埃尔夏姆队”，对应正式 provider identity `El Shams`，原 ID/英文名及来源链接保留在唯一共享 `display_names.json`；未覆盖既有名称。
- 最新 coverage 文件实算：formal union 2,468，canonical 1,883、unresolved 585（76.30%）；M1 1,442/1,576（91.50%）；M1 OU-R1 52/52（100%）；MR1 AH 1,435/1,921（74.70%）；MR1 AI declared mirror 1,442/1,576（91.50%）。MR1 AI confidence≥50 保留的历史 cohort 是 181/182（99.45%），未重建 cohort membership。共享库 12,276 team IDs、3,899 canonical。完整 unresolved 清单及原因仍以 `data/football_display_names/formal_scope_coverage.json` 为准。
- M1 display/formal-runtime 定向测试 20/20 通过，`git diff --check` 通过。名称数据仍由 M1 formatter 和 MR1 shared-registry loader 共用；本轮未改 formatter、生产模型、策略、账本、结算、调度或 Telegram 派单逻辑。
- 本轮未运行生产 workflow，未发送或编辑 Telegram。历史 TG 实际 edits=0：没有可用的专用凭据/可编辑原消息证据，不能声称历史消息已修复。继续逐条来源核验剩余 585 个正式范围 ID，不以机器音译填充。

## 2026-10-12 正式范围中文名称续补（二十六）
- 共享库提交 `e3e5314e09af62981157d6de30981f8e57f25160` 已推送到 `totalcorner-research-bridge/master`。依据中文球队资料新增 Lamia（ID 2803）→拉米亚（Tips.GG 中文球队页、球天下球队页）及 Skeid（ID 4189）→斯凯德（FootyStats 简中球队档案、Tips.GG 对阵页）；精确英文身份、ID、别名及来源写入唯一 registry，没有覆盖现有 canonical。来源链接分别为 `https://tips.gg/cn/team/lamia-football/`、`https://footystats.org/cn/clubs/skeid-fotball-7729`。
- 最新 coverage 实算：formal union 2,468，canonical 1,885、unresolved 583（76.38%）；M1 1,444/1,576（91.62%）；M1 OU-R1 52/52（100%）；MR1 AH 1,437/1,921（74.80%）；MR1 AI declared mirror 1,444/1,576（91.62%）。旧 observed confidence≥50 cohort 181/182（99.45%，历史 cohort 未重建）；共享 registry 12,276 team IDs、3,901 canonical。逐项 unresolved 原因和完整清单以共享 `formal_scope_coverage.json` 为准。
- M1 display/formal-runtime pytest 20/20 通过，`git diff --check` 通过；MR1 针对共享 registry 的读取/展示测试 2/2 通过。本轮仅处理展示名称数据和审计，不改模型、策略、范围、正式账本、结算、通知规则。
- 没有运行生产 workflow、发送或编辑 Telegram。历史 TG 实际编辑仍为 0；系统专用凭据及逐条可编辑原消息证据不在当前安全执行环境。继续 source-backed 核验剩余 583 个正式范围球队。

## 2026-10-12 正式范围中文名称续补（二十七）
- 共享 registry 提交 `19ac5f3291551fe19635231b1d095b3ba7c25a4a` 已推送。本轮新增 3 个精确 ID：Iwaki SC（41151）→磐城FC（7M 简中球队页；与已映射的 Iwaki FC 统一）；FK Zalgiris Vilnius（33136）→维尔纽斯扎尔吉里斯（简中俱乐部条目，避免与 Kauno Žalgiris“考纳斯扎尔吉里斯”混淆）；Rigas FS（11336）→里加足球学校（Sofascore 简中球队页）。来源、英文名、aliases 和 team_id 均保存在唯一共享 registry。
- 最新正式范围实算：2,468 IDs，canonical 1,888，unresolved 580（76.50%）；M1 1,447/1,576（91.81%）；M1 OU-R1 52/52；MR1 AH 1,440/1,921（74.96%）；MR1 AI declared mirror 1,447/1,576（91.81%）。MR1 AI observed confidence≥50 历史 cohort 仍为 181/182；共享库 12,276 IDs、3,904 canonical。完整 unresolved 名单及原因见共享 `formal_scope_coverage.json`。
- M1 display/formal-runtime 测试 20/20 通过，`git diff --check` 通过。此变更仅为展示名称；生产 workflow 未运行、Telegram 未发送或编辑，模型、策略、赛事范围、账本、结算未改。继续核实余下 580 项，不对含混身份猜译。

## 2026-10-12 正式范围中文名称续补（二十八）
- 共享库提交 `ebc49567eb9ca3267de4a1125c246a2bf9fd460f` 已推送至 master。本轮新增 Hillerød（ID 15189）→希勒罗（7M 简中/繁中球队档案）及 Etar 1924 Veliko Tarnovo（ID 41501）→伊塔尔（7M 球队资料页）；provider IDs、英文原名、别名和来源均保存在共享 registry。
- 最新实际范围：2,468 个 formal IDs，canonical 1,890、unresolved 578（76.58%）；M1 1,449/1,576（91.94%）；M1 OU-R1 52/52；MR1 AH 1,442/1,921（75.07%）；MR1 AI declared mirror 1,449/1,576（91.94%）。历史 observed confidence≥50 cohort 181/182；共享库 12,276 IDs、3,906 canonical。具体 unresolved 清单仍以共享 `formal_scope_coverage.json` 为准。
- M1 display/formal-runtime 测试 20/20，MR1 shared-registry 测试 2/2；MR1 对本轮及前批新 ID 的 formatter 隔离渲染均输出中文。没有生产 workflow/TG 操作；策略、正式账本、结算、派单规则均未修改。继续核证剩余 578 项。

## 2026-10-12 正式范围中文名称续补（二十九）
- 本轮继续增加两次来源核验并推送到共享库：`19ac5f3291551fe19635231b1d095b3ba7c25a4a` 增加 Iwaki SC（41151）→磐城FC、FK Žalgiris Vilnius（33136）→维尔纽斯扎尔吉里斯、Rigas FS（11336）→里加足球学校；`ebc49567eb9ca3267de4a1125c246a2bf9fd460f` 增加 Hillerød（15189）→希勒罗、Etar 1924 Veliko Tarnovo（41501）→伊塔尔；`0ac9f75952c8ec2a9ec7f9684059063bafb4c065` 增加 Al Fayhaa（53649）→费哈、Ballkani（106837）→巴尔干尼。来源包含 7M、Sofascore、中文维基条目和球迷屋球队档案；ID、provider identity、aliases/source 保留于唯一共享 registry。
- 当前正式范围实算：2,468 个 ID，canonical 1,892、unresolved 576（76.66%）；M1 1,451/1,576（92.07%）；M1 OU-R1 52/52；MR1 AH 1,443/1,921（75.12%）；MR1 AI declared mirror 1,451/1,576（92.07%）。共享 registry 12,276 个 team IDs、3,908 canonical；MR1 AI confidence≥50 的保留 cohort 为 181/182（历史分组）。逐条 unresolved 和原因见共享 `formal_scope_coverage.json`。
- M1 formatter/formal-runtime 定向测试 20/20 通过；MR1 共享库显示读取测试 2/2 通过，并对本轮相关新增 ID 做过隔离 formatter 渲染。没有生产 workflow、Telegram 发送或编辑；未改模型、策略、正式账本、结算、派单条件。剩余 576 项继续逐一核证，不对不清晰身份猜译。

## 2026-10-12 正式范围中文名称续补（三十）
- 共享 registry 已推送提交 `2798c0ae914a884043887821bd2a504148260589`。本轮新增 Al Orubah（4428）→欧鲁巴赫（球迷屋中文队档）、KF Shkupi Skopje（4605）→斯库皮（雷速中文资料，来源使用球队简称并核对 provider 主体）、Hapoel Ironi Kiryat Shmona（5956）→基尔史莫纳夏普尔（中文联赛参赛表列出英文全名及对应中文队名）。对应原始 ID、provider 英文名、aliases、reference 写入唯一共享库。
- 最新 authoritative coverage：formal union 2,468，canonical 1,895、unresolved 573（76.78%）；M1 1,454/1,576（92.26%）；M1 OU-R1 52/52；MR1 AH 1,446/1,921（75.27%）；MR1 AI declared mirror 1,454/1,576（92.26%）。历史 AI observed confidence≥50 cohort 181/182；全共享库 12,276 team IDs、3,911 canonical。完整 unresolved 清单与逐条原因见共享 `formal_scope_coverage.json`。
- M1 定向 pytest 20/20 通过；MR1 shared-registry 测试2/2通过，三条新增名称隔离渲染正确。只改展示映射和审计，不运行生产 workflow/TG，也不修改模型、策略、范围、账本、结算或通知条件；继续处理余下573项。

## 2026-10-12 正式范围中文名称续补（三十一）
- 共享 registry 提交 `4bcbeb64c174223ab82cd5cf1f039374ea6043e7` 已推送。本轮新增 Hajer（2706）→哈哲尔（球天下球队资料）、Enosis Paralimni（6227）→伊诺西斯（FootyStats 简中赛程/杯赛资料）、MOL Fehervar FC（53149）→维迪奥顿（中文俱乐部资料将 Fehérvár FC 与 MOL Vidi 名称联系到该俱乐部，且与共享库既有 Videoton/Fehervar IDs 使用同一稳定中文名）。全部 team ID、provider name、aliases 和 reference 写入同一 `display_names.json`。
- 当前实际统计：正式范围 2,468，canonical 1,898，unresolved 570（76.90%）；M1 1,456/1,576（92.39%）；M1 OU-R1 52/52；MR1 AH 1,448/1,921（75.38%）；MR1 AI declared mirror 1,456/1,576（92.39%）。MR1 AI 历史 observed confidence≥50 cohort 181/182；共享库 12,276 team IDs、3,914 canonical。完整 unresolved 和 reason 以共享 `formal_scope_coverage.json` 为准。
- M1 display/formal-runtime 定向测试20/20，MR1 shared-registry tests 2/2；本轮三队均经 MR1 formatter 只读隔离渲染为中文。未运行生产 Actions、未发/编辑 Telegram；模型、策略、正式订单、结算及通知规则未修改。继续来源核验剩余570项。

## 2026-10-12 正式范围中文名称续补（三十二）
- 共享库 `totalcorner-research-bridge/master` 新提交 `f6c5855f5b6847ad1d4cd7b0746312e1e428a679`。新增3条来源核验映射：Banants Yerevan（ID 4142）→乌拉尔图（中文球队条目说明 FC Banants 更名为 FC Urartu）；FC Kryvbas Kriviy Rih（15199）→克里沃罗格克里夫巴斯（Sofascore 简中队页）；Arsenal Kiev（14919）→基辅兵工厂（中文球队条目以 Arsenal Kyiv 对照）。provider identity、ID、别名和来源保存在唯一 `display_names.json`。
- 最新 coverage 实算：正式范围 2,468，canonical 1,901，unresolved 567（77.03%）；M1 1,459/1,576（92.58%）；M1 OU-R1 52/52；MR1 AH 1,449/1,921（75.43%）；MR1 AI declared mirror 1,459/1,576（92.58%）。共享 registry 12,276 IDs、3,917 canonical。逐项 unresolved 及原因以共享 `formal_scope_coverage.json` 为准。
- M1 display/formal-runtime 定向测试 20/20 通过；MR1 shared-registry tests 2/2 通过，新三 ID 共享库读取正常。本轮没有触碰生产链或历史 TG；未运行/修改 Telegram。其余策略、账本、结算及派单逻辑未变。继续逐条核验剩余567项。

## 2026-10-12 正式范围中文名称续补（三十三）
- 共享库 `totalcorner-research-bridge/master` 新提交 `4037f447a4dd4aec38f20398df9b18ee22e5bb8f`。本轮新增 Bregalnica Stip（ID 489）→什蒂普布雷加尔尼察（中文维基俱乐部条目）；Belenenses（561）→贝伦人（中文俱乐部资料）；Batman Petrolspor（3682）→巴特曼石油体育俱乐部（Tips.GG 简中对阵资料）。ID、provider identity、aliases、来源均入唯一 registry。
- authoritative formal coverage：2,468 个 ID，canonical 1,904，unresolved 564（77.15%）；M1 1,462/1,576（92.77%）；M1 OU-R1 52/52（100%）；MR1 AH 1,451/1,921（75.53%）；MR1 AI declared mirror 1,462/1,576（92.77%）。共享库 12,276 IDs、3,920 canonical。完整 unresolved 列表/原因见共享 coverage JSON。
- M1 定向 pytest 20/20 通过。未运行生产 workflow、未编辑或发送历史 TG；无策略/模型/正式账本变更。继续核验剩余564项。

## 2026-10-12 正式范围中文名称续补（三十四）
- 共享库 `totalcorner-research-bridge/master` 已推送 `b83a312e1324add4e4bd46b90522d144ab0db580`。新增 Patro Eisden Maasmechelen（ID 1171）→马斯梅赫伦、Cheonan City（ID 6049）→天安，两项分别来自 Sofascore 简中队页并保留 provider identity、ID、aliases 与来源。
- 最新正式范围统计：2,468 IDs，canonical 1,906，unresolved 562（77.23%）；M1 1,464/1,576（92.89%）；M1 OU-R1 52/52；MR1 AH 1,453/1,921（75.64%）；MR1 AI declared mirror 1,464/1,576（92.89%）。共享库 12,276 IDs、3,922 canonical。逐项待核清单见共享 `formal_scope_coverage.json`。
- M1 定向测试 20/20 通过；未触发生产 workflow 或 Telegram，不涉及策略、订单/结算账本变动。继续补齐余下562项。

## 2026-10-12 正式范围中文名称续补（三十五）
- 共享库 `totalcorner-research-bridge/master` 已推送 `d898fab92cc1425ee913a6c8e7a879ff703bc8d7`。新增 FK Skendija 79（ID 3742）→斯肯迪亚（球天下中文球队页，将 Shkendija Tetovo 对应为斯肯迪亚）；FK Gostivar（ID 3744）→戈斯蒂瓦尔（Sofascore 简中球员资料中的现役球队显示名）。canonical、精确 team ID/provider 名、alias 和来源留在唯一共享 registry。
- 当前范围实算：formal union 2,468，canonical 1,908，unresolved 560（77.31%）；M1 1,466/1,576（93.02%）；M1 OU-R1 52/52；MR1 AH 1,453/1,921（75.64%）；MR1 AI mirror 1,466/1,576（93.02%）。共享 registry 12,276 IDs、3,924 canonical；未匹配清单/原因见 formal_scope_coverage.json。
- M1 定向 pytest 20/20 通过。无生产 workflow/TG 操作，无模型、策略、正式账本/结算改动；剩余560项继续逐条核验。

## 2026-10-12 正式范围中文名称续补（三十六）
- 共享库 `totalcorner-research-bridge/master` 已推送 `023cf148ee60a95f2a1af540606ded6c67925503`。新增 Thor Akureyri（ID 8635）→托尔（7M 简中队页）；Hapoel Petach Tikva（ID 7713）→佩塔提克瓦工人，复用共享 registry 中已核验的 Hapoel Petah Tikva Wikidata 简中标签（Q1130537），保留第二个 provider ID、拼写 alias，未覆盖/合并原有 team row。
- 最新正式范围统计：2,468 IDs，canonical 1,910，unresolved 558（77.39%）；M1 1,468/1,576（93.15%）；M1 OU-R1 52/52；MR1 AH 1,455/1,921（75.74%）；MR1 AI declared mirror 1,468/1,576（93.15%）。共享库 12,276 IDs、3,926 canonical；未匹配明细见 `formal_scope_coverage.json`。
- M1 定向测试20/20，MR1 shared-registry读取测试2/2通过。未触发生产workflow、未发或编辑TG；策略、模型、账本、结算未改。继续处理剩余558项。

## 2026-10-12 正式范围中文名称续补（三十七）
- 共享库 `totalcorner-research-bridge/master` 推送 `fe5abfe9b74ae82f8639765a9e5588ff94641c88`。新增 Zira IK（ID 3855）→兹拉（球迷屋简中球队资料）；FK Sumqayit（4309）→萨姆加耶特（Sofascore 简中球队页）；Lokomotiv Tbilisi（7661）→第比利斯火车头（7M 简中球队页）。来源、Team ID/provider 原名与 aliases 均在唯一 registry。
- 最新正式覆盖：union 2,468，canonical 1,913，unresolved 555（77.51%）；M1 1,471/1,576（93.34%）；M1 OU-R1 52/52；MR1 AH 1,458/1,921（75.90%）；MR1 AI declared mirror 1,471/1,576（93.34%）。共享库 12,276 IDs、3,929 canonical。完整未匹配列表及 reason 见 coverage JSON。
- M1 定向 pytest 20/20、MR1 shared-registry测试2/2通过；新增三队 MR1 读取渲染为中文。未运行生产 Actions/TG，无模型、策略、账本、结算变化；剩余555项持续处理。

## 2026-10-12 正式范围中文名称续补（三十八）
- 共享库 `totalcorner-research-bridge/master` 已推送 `2c03fce421583aad15435dda296bd9777464823f`。新增 Landskrona（ID 9492）→兰斯科罗纳（7M 简中）；Leotar（9349）→莱奥塔尔（球天下简中）；FC Luka Koper（9303）→科佩尔（7M 简中，沿用共享 registry 对同俱乐部既有标准中文名）；Aluminij Kidricevo（7202）→亚穆尼基（Sofascore 简中）。ID、英文 provider identity、aliases 和来源入唯一 `display_names.json`。
- 最新正式范围：2,468 IDs，canonical 1,917，unresolved 551（77.67%）；M1 1,475/1,576（93.59%）；M1 OU-R1 52/52；MR1 AH 1,461/1,921（76.05%）；MR1 AI declared mirror 1,475/1,576（93.59%）。共享库 12,276 IDs、3,933 canonical。逐项 unresolved/reason 以共享 coverage JSON 为准。
- M1 定向 tests 20/20、MR1 shared-registry tests 2/2 通过，四 ID 均可被 MR1 共享 registry 正确读出。本轮未触发生产 Actions/TG，无策略、模型、正式账本或结算改动；继续处理剩余551项。

## 2026-10-12 正式范围中文名称续补（十七）
- 共享 registry 提交 `29a8dcd6e953fd04be232fe46310ec3ce31378d3` 已推送至 `totalcorner-research-bridge/master`。在续补（十六）基础上新增 2 条精确身份映射：B93 Copenhagen（ID 3622）→哥本哈根B93，Sofascore 简中球队页；Dukla Banska Bystrica（ID 3460）→班斯卡比斯特里察杜克拉，Sofascore 简中球队页。两条均属于 M1 与 MR1 AH 范围，原英文 provider identity、ID、别名及来源保留在共享 registry。
- 最新范围：formal union 2,468，canonical 中文 1,871，unresolved 597（75.81%）；M1 1,430/1,576（90.74%）；M1 OU-R1 52/52；MR1 AH 1,423/1,921（74.08%）；MR1 AI mirror 1,430/1,576（90.74%）。未匹配完整清单仍位于共享 `formal_scope_coverage.json`，当前 597 条均为 `NO_VERIFIED_CANONICAL_ZH`。
- M1 display/runtime 定向测试 20/20 通过；新 ID formatter 渲染待随共享库提交后复核。未发送或编辑 Telegram；未触发生产 scan 或 GitHub Actions。策略、账本、通知条件不变。

## 2026-10-12 正式范围中文名称续补（十八）
- 共享 registry 提交 `f0018c7d1d1a1b861f3799d406db46dff791b585` 已推送至 `totalcorner-research-bridge/master`。本轮继续从公开中文足球资料核验并新增 Mgarr United（ID 1798）→姆加尔联，来源为 FootyStats 简中球队档案；该条处于 M1+MR1 AH 范围。对应来源和 aliases 写入共享 registry，不将音译猜测作为补库依据。
- 最新 formal union 2,468：canonical 1,872，unresolved 596，覆盖 75.85%；M1 1,431/1,576（90.80%）；M1 OU-R1 52/52；MR1 AH 1,424/1,921（74.13%）；MR1 AI mirror 1,431/1,576（90.80%）。完整未匹配及原因以共享 `formal_scope_coverage.json` 为准。
- M1 display/runtime 定向测试 20/20 通过；Telegram 未编辑/重发，未触发生产 workflow。策略、账本、阈值、正式通知条件未改。
- 共享库提交 SHA 待本轮推送后填入。

## 2026-10-12 正式范围中文名称续补（十九）
- 共享 registry 提交 `40065138bdad4574b229e813323cb9e6efd8549f` 已推送至 `totalcorner-research-bridge/master`。本轮新增 2 条经 7M 球队页核对的正式映射：Talaea El Geish（ID 4547）→塔拉雅；Al Khaleej Saihat（ID 4412）→卡赫利塞哈特。前者另将中文百科译名放入 aliases。provider 英文名、ID 与来源链接保留在唯一共享 registry。
- 最新正式范围 union 2,468：已匹配 1,874，未匹配 594（75.93%）；M1 1,433/1,576（90.93%）；M1 OU-R1 52/52；MR1 AH 1,426/1,921（74.23%）；MR1 AI mirror 1,433/1,576（90.93%）。未匹配明细及原因见共享 `formal_scope_coverage.json`。
- M1 display/runtime 定向测试 20/20 通过；未触发生产 scan、未发或编辑 TG。策略及实战状态未改。

## 2026-10-12 正式范围中文名称续补（二十）
- 共享 registry 提交 `c0580d75351d07bcac6fc302d16955bddc24a78b` 已推送至 `totalcorner-research-bridge/master`。在公开中文资料中核实 Hamrun Spartans（ID 7652）→阿姆伦斯巴达，采用球迷屋中文球队档案的简体常用名称，并保留英文/带附加符号名称别名。该 ID 属于 M1+MR1 AH 范围。
- 最新正式范围 union 2,468：已匹配 1,875，未匹配 593（75.97%）；M1 1,434/1,576（90.99%）；M1 OU-R1 52/52；MR1 AH 1,427/1,921（74.28%）；MR1 AI mirror 1,434/1,576（90.99%）。逐队未匹配及原因留在共享 `formal_scope_coverage.json`。
- M1 display/runtime 定向测试 20/20 通过；Telegram 未编辑/发送，生产 workflow 未触发。策略与账本未变。

## 2026-10-12 正式范围中文名称续补（三十九）
- 共享 registry 提交 `0901a5dd1a080e23293a364cb524276cda0f6407` 已推送至 `totalcorner-research-bridge/master`。本轮新增 4 个有公开中文足球记录支持的映射：Mezokovesd Zsory（1537）→迈泽克韦什德；Soroksar（1543）→索罗克萨尔；Energetik Mingechevir（2126）→明盖恰乌尔能量；Apollon Kalamarias（2205）→阿波罗卡拉马里亚。各行保留 provider ID/name、aliases、来源与核验时间。
- 当前覆盖：正式范围 2,468，canonical 1,921，unresolved 547（77.84%）；M1 1,479/1,576（93.85%）；M1 OU-R1 52/52；MR1 AH 1,465/1,921（76.26%）；MR1 AI declared mirror 1,479/1,576（93.85%）。共享库 12,276 IDs、3,937 canonical。剩余逐队清单及 reason 见共享 `data/football_display_names/formal_scope_coverage.json`。
- M1 formatter/runtime pytest 20/20、MR1 shared-registry 测试 2/2 通过。未运行生产 workflow，未编辑/发送 Telegram；当前本机无 M1 Telegram 凭据，故不声称完成历史消息编辑。未改模型、策略、范围、正式账本或结算。

## 2026-10-12 正式范围中文名称续补（四十）
- 共享 registry 提交 `bcd3c0de3f88adea28bea18e80804aaaf858d591` 已推送至 `totalcorner-research-bridge/master`。在续补（三十九）后新增 CS Tunari（ID 2907）→图纳里（Sofascore 简中球队页）及 Laçi（ID 8736）→拉奇（中文足球俱乐部条目）；均保留原 provider identity、ID、别名及来源。
- 最新正式范围：2,468 IDs，canonical 1,923、unresolved 545（77.92%）；M1 1,481/1,576（93.97%）；M1 OU-R1 52/52；MR1 AH 1,467/1,921（76.37%）；MR1 AI declared mirror 1,481/1,576（93.97%）。共享库 12,276 IDs、3,939 canonical。未匹配全量清单及逐项原因见共享 `formal_scope_coverage.json`。
- M1 定向 pytest 20/20、MR1 registry 读取测试 2/2 通过，六条本轮/上一批映射隔离渲染成功。未运行生产 workflow，未发/编辑历史 Telegram；生产 TG 凭据不可用。未修改模型、策略、正式账本或结算。

## 2026-10-12 正式范围中文名称续补（四十一）
- 共享 registry 提交 `49b8952dfc64d78f0070560669c58882181607a0` 已推送至 `totalcorner-research-bridge/master`。新增 Altay（3794）→阿尔泰体育俱乐部（雷速简中）；LKS Lodz（9392）→LKS洛迪兹（雷速简中）；FC Elva（9416）→埃尔瓦FC（Sofascore简中）；Suwon FMC (W)（10243）→水原FMC女足（7M简中）；Hwacheon KSPO (W)（10710）→华川KSPO女足（7M简中）；FCV Dender EH（17871）→FCV丹达（7M中文页面）。保留身份与别名，女足身份未与男队合并。
- 最新正式范围：2,468 IDs，canonical 1,929、unresolved 539（78.16%）；M1 1,487/1,576（94.35%）；M1 OU-R1 52/52；MR1 AH 1,473/1,921（76.68%）；MR1 AI declared mirror 1,487/1,576（94.35%）。共享库 12,276 IDs、3,945 canonical。完整剩余列表及逐项原因见共享 `formal_scope_coverage.json`。
- M1 定向 pytest 20/20、MR1 shared-registry tests 2/2 通过；六条名称隔离渲染通过。未触发生产任务或 TG；未修改任何模型、策略、正式订单或结算。

## 2026-10-12 正式范围中文名称续补（四十二）
- 共享 registry 提交 `cec5affae7c131f31099db502885f96d5db9f646` 已推送。新增 WSG Swarovski Wattens（ID 3704）→WSG蒂罗尔，奥地利 Bundesliga 官方资料核对 2021 更名，复用共享库 WSG Tirol（85219）的标准中文名；Odra Opole（7038）→奥波莱（球天下中文资料）；HK Kópavogur（8685）→HK科帕沃格（球天下中文资料）。
- 最新范围：formal 2,468，canonical 1,932，unresolved 536（78.28%）；M1 1,490/1,576（94.54%）；M1 OU-R1 52/52；MR1 AH 1,475/1,921（76.78%）；MR1 AI mirror 1,490/1,576（94.54%）。共享库 12,276 IDs、3,948 canonical。完整待补清单及每条原因在共享 `formal_scope_coverage.json`。
- M1 定向测试 20/20、MR1 registry 测试 2/2 和三条新增名称 formatter 隔离渲染通过。未触发生产 workflow/TG，模型、策略、账本和结算未改。

## 2026-10-12 正式范围中文名称续补（四十三）
- 共享 registry 提交 `209d318d5a4c0e854de9fdcd7c1c234ecce3dc29` 已推送至 `totalcorner-research-bridge/master`。新增 Giannina（ID 2746）→吉安尼纳（雷速简中球队资料）及 Kavala（ID 7802）→卡瓦拉（360百科球队资料）；ID、provider 原名、别名、来源和核验时间保存在唯一 `display_names.json`。
- 最新正式范围：2,468 IDs，canonical 1,934、unresolved 534（78.36%）；M1 1,492/1,576（94.67%）；M1 OU-R1 52/52（100%）；MR1 AH 1,477/1,921（76.89%）；MR1 AI declared mirror 1,492/1,576（94.67%）。共享 registry 12,276 IDs、3,950 canonical。完整未匹配及逐项原因见共享 `data/football_display_names/formal_scope_coverage.json`。
- M1 formatter/runtime 定向 pytest 20/20、MR1 shared-registry tests 2/2 通过；无生产 Actions/TG 发送或编辑。本轮未改模型、策略、正式订单、结算或通知规则。历史 Telegram 编辑仍未完成：当前回合未调用生产 Telegram API；不得将 formatter 测试视为历史消息修复。

## 2026-10-12 正式范围中文名称续补（四十四）
- 共享 registry 新提交 `4e07b4ecb2c9338df3bbf24d01a08b3430da3741` 已推送。新增 OFK Igalo（ID 2569）→伊高洛（球天下中文球队资料）和 Zurrieq FC（ID 3347）→祖里耶克（雷速中文球队资料）。未将仅有外文身份资料的其他候选猜译入库。
- 最新实际 coverage：正式范围 2,468，canonical 1,936、unresolved 532（78.44%）；M1 1,494/1,576（94.80%）；M1 OU-R1 52/52；MR1 AH 1,479/1,921（76.99%）；MR1 AI declared mirror 1,494/1,576（94.80%）。共享 registry 12,276 IDs、3,952 canonical。剩余逐项清单及原因见共享 `formal_scope_coverage.json`。
- 历史 Telegram 未编辑/重发，生产 TG/API 未触发；不能把共享 formatter 测试视为正式消息修复。模型、策略、账本、结算和派单条件保持不变。

## 2026-10-12 正式范围中文名称续补（四十五）
- 共享 registry 提交 `5f5b13098533a140a00634fdfb9afdfdaab9d6ea` 已推送。新增 FK Indija（ID 3746）→因吉亚，来源为中文球队资料页；英文身份、ID、拼写别名、来源和核验时间已写入共享库。
- 最新实算：formal union 2,468，canonical 1,937、unresolved 531（78.48%）；M1 1,495/1,576（94.86%）；M1 OU-R1 52/52；MR1 AH 1,480/1,921（77.04%）；MR1 AI declared mirror 1,495/1,576（94.86%）。共享 registry 12,276 IDs、3,953 canonical。逐项 unresolved/reason 在 `formal_scope_coverage.json`。
- 当前回合仅本地验证与 registry 数据提交；未编辑/发送正式 Telegram，未改模型、策略、正式账本/结算。

## 2026-10-12 正式范围中文名称续补（四十六）
- 共享 registry 提交 `2665893a59debbb10b3037cee2ec655d34d3cbeb` 已推送。新增 FC Bihor Oradea（ID 1967）→比霍尔奥拉迪亚（中文比赛预览明确使用“FC 比霍尔奥拉迪亚”）和 Felgueiras 1932（ID 6094）→费尔盖拉什（Sofascore 简中球队页），均保留精确 provider identity/ID 与别名。
- 最新实际 coverage：formal union 2,468，canonical 1,939、unresolved 529（78.57%）；M1 1,497/1,576（94.99%）；M1 OU-R1 52/52；MR1 AH 1,481/1,921（77.10%）；MR1 AI declared mirror 1,497/1,576（94.99%）。共享 registry 12,276 IDs、3,955 canonical。其余清单和逐项原因见 `formal_scope_coverage.json`。
- 本批为展示映射数据更新；未触发生产 Actions/TG 或历史消息编辑；模型、策略、账本、结算和通知规则未变。

## 2026-10-12 正式范围中文名称续补（四十七）
- 共享 registry 提交 `4f779e4910d9a1f616efe7deb3ce83d7a88d303c` 已推送。新增 Kolkheti Poti（ID 7324）→克尔赫提（7M 中文球队页）；Marek Dupnitsa（7810）→马历克（中文俱乐部条目）；Skenderbeu Korce（8420）→科尔察斯克得比鲁（中文球队页）。每条保留来源、英文 provider identity、ID 和 aliases。
- 最新实算：正式范围 2,468，canonical 1,942、unresolved 526（78.69%）；M1 1,500/1,576（95.18%）；M1 OU-R1 52/52；MR1 AH 1,484/1,921（77.25%）；MR1 AI declared mirror 1,500/1,576（95.18%）。共享 registry 12,276 IDs、3,958 canonical。剩余详细列表及原因见共享 `formal_scope_coverage.json`。
- 只更新共享展示映射和交接记录；生产 Telegram 未发送或编辑，模型、策略、订单、结算未修改。

## 2026-10-12 正式范围中文名称续补（四十八）
- 共享 registry 新提交 `92ad545f7564ab34a7a2042b7a5652c2114c90f8` 已推送。新增 Makedonija Gj. P.（ID 4606）→乔尔切彼得罗夫马其顿尼亚，采用中文俱乐部条目所列全名，保留 provider 缩写及英文全名 aliases。
- 最新覆盖：正式范围 2,468，canonical 1,943、unresolved 525（78.73%）；M1 1,501/1,576（95.24%）；M1 OU-R1 52/52；MR1 AH 1,485/1,921（77.30%）；MR1 AI declared mirror 1,501/1,576（95.24%）。共享 registry 12,276 IDs、3,959 canonical。完整剩余项及原因见共享 `formal_scope_coverage.json`。
- M1 display/runtime 定向测试 20/20、MR1 shared-registry 测试 2/2 通过。仅更新显示层数据，没有生产 TG 编辑/发送或策略、账本、结算变更。

## 2026-10-12 正式范围中文名称续补（四十九）
- 共享 registry 新提交 `3984a22790eed66856ea381f4e1377c8b606163a` 已推送。新增 Admira Wacker Mödling（ID 8740）→阿德米拉华卡默德林（百度百科球队资料）；Borac Čačak（9162）→查查克博拉克（百度百科球队资料）；PAEEK（9752）→佩伊克（乐彩网中文球队概述）。
- 最新 coverage：formal union 2,468，canonical 1,946、unresolved 522（78.85%）；M1 1,504/1,576（95.43%）；M1 OU-R1 52/52；MR1 AH 1,487/1,921（77.41%）；MR1 AI declared mirror 1,504/1,576（95.43%）。共享 registry 12,276 IDs、3,962 canonical。剩余逐项清单及 reason 见 `formal_scope_coverage.json`。
- 更新限于共享显示名称库与交接文档；生产 Telegram 未发送/编辑，模型、策略、账本和结算未改。

## 2026-10-12 正式范围中文名称续补（五十）
- 共享库提交 `2860dfd190aefb3594eabc9dfd7f4092653e8f9d` 已推送到 `totalcorner-research-bridge/master`。新增 Hrvace（ID 6452）→贺瓦斯（雷速简中球队资料）、FK Csikszereda Miercurea Ciuc（4886）→米耶尔库雷亚丘克（Sofascore 简中球队页）、Al Jeel（5403）→阿尔吉尔（Sofascore 简中球队页）。三个映射均有可核验中文来源，provider identity/ID、别名、来源与时间写入唯一 `display_names.json`；没有把本批只找到外文来源的候选猜译入库。
- 最新正式范围：union 2,468，canonical 1,949，unresolved 519（78.97%）；M1 1,506/1,576（95.56%）；M1 OU-R1 52/52（100%）；MR1 AH 1,490/1,921（77.56%）；MR1 AI declared mirror 1,506/1,576（95.56%）。共享库 12,276 IDs、3,965 canonical。完整 unresolved 清单和逐项原因见共享 `data/football_display_names/formal_scope_coverage.json`。
- 验证：M1 formatter/runtime pytest 20/20 通过；MR1 共用 registry 读取测试 2/2 通过。MR1 测试命令为 `FOOTBALL_DISPLAY_REGISTRY_DIR=/Users/mac/Documents/totalcorner-research-bridge/data/football_display_names node --test test-football-display-names.js`。未调用 Telegram API，因此没有历史消息编辑成功；当前终端环境无 M1/MR1 Telegram 环境变量，生产编辑需通过现有安全凭据运行链执行。未改模型、策略、赛事范围、正式账本或结算。

## 2026-10-12 Telegram 中文历史显示被动验收（五十一）
- 使用现有 quant-runner 工作流分别运行 M1 `38208422182`、MR1 formal `38208422303`、MR1 AI `38208422297`；三者均以 success 结束。没有发新消息/订单。
- M1 修复回执：37 条具备原始文案且映射可计算的既有通知均由 Telegram 返回 `ALREADY_MATCHING`（实际编辑 0、失败 0）；99 条缺少已持久化原文被安全跳过；70 条仍未命中映射。账本包含 AH/OU 通知，故该执行也覆盖已有 M1 OU-R1 通知。
- MR1 formal：124 条检查结果均跳过、edited 0、failed 0、display unresolved 0；现有报告未细分跳过原因，因此不将其表述为实际编辑。
- MR1 AI：检查 201 条；9 条有映射变更候选，Telegram 对 9 条均返回 `400 Bad Request: message to edit not found`（edited 0）；192 条保持未解析/没有可用中文替换。错误及逐条回执已由运行器提交 `584a07145675cdc6dd40ffd42effb7905159f8d3` 持久化。
- 本轮新增映射提交为 `2860dfd190aefb3594eabc9dfd7f4092653e8f9d`；最新正式范围 union 2,468，mapped 1,949、unresolved 519（78.97%）。完整剩余队伍和 reason 保存在共享 `data/football_display_names/formal_scope_coverage.json`。M1 测试 20/20、MR1 shared display 测试 2/2 通过。策略、模型、账本、结算和通知条件未改。

## 2026-10-12 正式范围中文名称续补（五十二）
- 共享库新增 4 条正式范围映射并推送，提交 `50776476904b8b5c8c205ca6bb4b48e4de84f404`：Mladost Podgorica（511）→迪托格特（Titan007中文赛程名，结合UEFA更名资料确认为OFK Titograd；未与其他Mladost合并）；Rad Belgrade（2851）→拉德足球俱乐部（Wikidata/中文维基标签）；FK Baku（4031）→巴库足球俱乐部（中文维基）；UAE U23（4391）→阿联酋U23（懂球帝球队页）。
- 最新 formal union 2,468：canonical 1,953、unresolved 515、覆盖79.13%；M1 1,510/1,576（95.81%）；M1 OU-R1 52/52；MR1 AH 1,490/1,921（77.56%）；MR1 AI declared mirror 1,510/1,576（95.81%）。完整剩余 ID/英文名/联赛/系统/reason 仍在共享 `formal_scope_coverage.json`。
- formatter按ID隔离渲染本批与上一批共7条正确；M1定向 pytest 20/20、MR1共享 registry 读取测试2/2通过。未运行新生产TG编辑。模型、策略、账本、结算未改；继续处理剩余515项。

## 2026-10-12 正式范围中文名称续补（五十三）
- 共享库已推送提交 `220da8659498af924e44ac02291ca40a4b4f7201`，新增 Egyptian/Cypriot 四队：Eastern Company（7819）→东方公司（智博埃及足球数据表）；Al Majd（7705）→阿尔马吉德（Tips.GG中文埃及比赛页）；Karmiotissa（8497）→卡尔米奥提萨（Tips.GG中文赛程/球队页）；Suez Montakhab（7568）→苏伊士蒙塔哈布（雷速中文赛果页）。英文 identity、team_id、别名及来源保留于唯一共享库。
- 最新 formal union 2,468：canonical 1,957、unresolved 511（79.29%）；M1 1,514/1,576（96.07%）；M1 OU-R1 52/52；MR1 AH 1,494/1,921（77.77%）；MR1 AI declared mirror 1,514/1,576（96.07%）。完整剩余清单及逐项 reason 见共享 `formal_scope_coverage.json`。
- 四个新增 ID formatter 验证通过；M1定向 pytest 20/20、MR1共享名称测试2/2通过。没有编辑或重发 Telegram，也没有改模型、策略、账本、结算；继续处理剩余511项。

## 2026-10-12 正式范围中文名称续补（五十四）
- 共享库本轮新增 3 条来源可核验映射：Fgura United（4265）→富格拉联队、Gudja United（4267）→古德加联合（Tips.GG 中文马耳他杯赛资料明确显示对应名称）；Taffs Well（3989）→塔夫斯韦尔（Tips.GG 中文球队页）。唯一 `display_names.json` 保留 team_id、原 provider 英文名、aliases、source 与核验时间。
- 当前正式范围 union 2,468：canonical 1,960、unresolved 508（79.42%）；M1 1,517/1,576（96.26%）；M1 OU-R1 52/52；MR1 AH 1,497/1,921（77.93%）；MR1 AI declared mirror 1,517/1,576（96.26%）。完整未匹配条目与逐项原因以共享 `formal_scope_coverage.json` 为准。
- M1 定向 pytest 20/20、MR1 shared registry tests 2/2 通过。只更新共享名称数据及交接记录；未触发生产 Telegram 或历史消息修改，未修改模型、策略、正式账本或结算；继续处理剩余 508 项。

## 2026-10-12 正式范围中文名称续补（五十五）
- 共享库再新增 2 条正式范围中文映射：Melita FC Saint Julian（3342）→梅利塔圣朱利安队（Tips.GG 中文马耳他赛事实录）；Bekescsabai Elore SE（3492）→贝克什巴（Tips.GG 中文匈牙利比赛记录，并以匈牙利俱乐部资料核对 Békéscsaba 1912 Előre 身份）。原 provider 名、ID、aliases、来源均留在唯一 registry。
- 最新 formal union 2,468：canonical 1,962、unresolved 506（79.50%）；M1 1,519/1,576（96.38%）；M1 OU-R1 52/52；MR1 AH 1,499/1,921（78.03%）；MR1 AI declared mirror 1,519/1,576（96.38%）。完整 unresolved 明细仍以共享 `formal_scope_coverage.json` 为准。
- M1 pytest 20/20、MR1 shared-registry 测试 2/2 通过。仅更新显示名称映射/交接，无 Telegram API 调用，无模型、策略、账本、结算改动；继续处理剩余 506 项。

## 2026-10-12 正式范围中文名称续补（五十六）
- 共享 registry 新增 5 条有中文赛事/球队页支持的映射：Ionikos（6120）→伊奥尼科斯；Zakynthos（5780）→扎金索斯；Bijelo Brdo（3662）→白山；Chernomorets Burgas（28530）→黑海堡尔加斯；FK Metalac GM（6365）→梅塔拉茨队。来源均为 Tips.GG 简中球队/比赛页，provider identity、ID、别名和引用保留。
- 最新正式范围 union 2,468：canonical 1,967、unresolved 501（79.70%）；M1 1,524/1,576（96.70%）；M1 OU-R1 52/52；MR1 AH 1,503/1,921（78.24%）；MR1 AI declared mirror 1,524/1,576（96.70%）。完整逐项未匹配及原因保存在共享 `formal_scope_coverage.json`。
- M1 formatter/runtime pytest 20/20、MR1 shared registry tests 2/2 通过。仅改显示名数据/交接；未编辑或发送 TG，也未改模型、策略、正式账本或结算；继续处理剩余 501 项。

## 2026-10-12 正式范围中文名称续补（五十七）
- 共享 registry 新增 3 个来源可核验的正式队名：FK Kukesi（13481）→库克西队；Bodrumspor（15286）→博德鲁姆体育；FK Graficar Beograd（29414）→贝尔格莱德制图师队。分别由 Tips.GG 中文阿尔巴尼亚比赛、土耳其球队页和塞尔维亚比赛页明确配对，ID/provider identity/aliases/source 保留。
- 最新正式范围 union 2,468：canonical 1,970、unresolved 498（79.82%）；M1 1,527/1,576（96.89%）；M1 OU-R1 52/52；MR1 AH 1,505/1,921（78.34%）；MR1 AI declared mirror 1,527/1,576（96.89%）。完整 unresolved 清单与原因仍以共享 `formal_scope_coverage.json` 为准。
- M1 定向 pytest 20/20、MR1 registry tests 2/2 通过。未调用 Telegram API，未修改模型/策略/正式账本/结算；继续处理剩余 498 项。

## 2026-10-12 正式范围中文名称续补（五十八）
- 共享 registry 新增 2 条经中文足球资料核验的球队：Hasselt（30173）→哈瑟尔特队（Tips.GG 简中球队页）；FK Backa Topola（30089）→巴奇卡托波拉（7M 中文球队档案）。保留原英文 provider identity、ID、别名及来源。
- 最新正式范围 union 2,468：canonical 1,972、unresolved 496（79.90%）；M1 1,529/1,576（97.02%）；M1 OU-R1 52/52；MR1 AH 1,506/1,921（78.40%）；MR1 AI declared mirror 1,529/1,576（97.02%）。完整 unresolved 项及 reason 见共享 `formal_scope_coverage.json`。
- M1 tests 20/20、MR1 shared-registry tests 2/2 通过。只更新名称映射和交接；未触发 Telegram 或生产任务，未改模型、策略、账本、结算；继续处理剩余 496 项。

## 2026-10-12 正式范围中文名称续补（五十九）
- 共享 registry 新增 Dhamk（team_id 22197）→达马克，来源为 7M 中文球队档案（https://team.7m.com.cn/5282/index_gb.shtml）；原 provider name、ID、别名、来源及核验时间写入唯一 `display_names.json`。本轮其他检索到的低级别队伍没有找到足以确认常用中文队名的中文来源，仍保留 unresolved，不做机器音译。
- 最新正式范围 union 2,468：canonical 1,973、unresolved 495（79.94%）；M1 1,530/1,576（97.08%）；M1 OU-R1 52/52（100%）；MR1 AH 1,506/1,921（78.40%）；MR1 AI declared mirror 1,530/1,576（97.08%）。逐项未匹配原因见共享 `data/football_display_names/formal_scope_coverage.json`。
- 验证：M1 Telegram display/runtime 定向 pytest 20/20；MR1 shared-registry tests 2/2。仅更改展示映射/审计数据/本交接，未调用生产 Telegram API或编辑历史消息，未改策略、模型、账本或结算。未匹配条目尚有 495 个，继续按可核验中文来源补齐。

## 2026-10-12 正式范围中文名称续补（六十）
- 共享库新增 Olympic El Qanah（team_id 10778）→艾尔夸纳尔奥林匹克，来源为 FootyStats 简中球队页（https://footystats.org/cn/clubs/olympic-el-qanah-17841）。本范围另有 provider 名 Olympic El Qanal 的不同 ID；没有强行合并，待取得可确认其身份等同的证据。
- 当前 formal union 2,468：canonical 1,974、unresolved 494（79.98%）；M1 1,531/1,576（97.14%）；M1 OU-R1 52/52；MR1 AH 1,507/1,921（78.45%）；MR1 AI declared mirror 1,531/1,576（97.14%）。完整剩余明细与 reason 见共享 `formal_scope_coverage.json`。
- 验证：M1 display/runtime pytest 20/20；MR1 shared-registry tests 2/2。仅更新共享名称库、审计报告及本交接；没有执行 Telegram API编辑/发送，模型、策略、订单和结算未改；继续处理剩余 494 项。

## 2026-10-12 正式范围中文名称续补（六十一）
- 共享库新增 SC Poltava（team_id 53034）→SC波尔塔瓦；新球体育（Titan007）中文球队档案明确以“SC波尔塔瓦”配对英文名 SC Poltava（https://info.titan007.com/cn/team/Summary.aspx?TeamID=43904）。
- 最新 formal union 2,468：canonical 1,975、unresolved 493（80.02%）；M1 1,532/1,576（97.21%）；M1 OU-R1 52/52；MR1 AH 1,508/1,921（78.50%）；MR1 AI declared mirror 1,532/1,576（97.21%）。剩余项详见共享 coverage JSON。
- M1 display/runtime pytest 20/20、MR1 shared registry tests 2/2 通过。仅更改名称展示基础设施及交接；无 Telegram API 操作，无策略/模型/账本/结算改动，继续补其余 493 个正式范围未匹配项。

## 2026-10-12 正式范围中文名称续补（六十二）
- 共享库新增 Gyeongju (W)（team_id 41028）→庆州女足；Tips.GG 中文女足球队页以“庆州 (女子)”标识 Gyeongju (w)（https://tips.gg/cn/team/gyeongju-fc-w-football/）。保留女子队身份和原英文名，不与男子队 ID 6048 合并。
- 最新 formal union 2,468：canonical 1,976、unresolved 492（80.06%）；M1 1,533/1,576（97.27%）；M1 OU-R1 52/52；MR1 AH 1,509/1,921（78.55%）；MR1 AI declared mirror 1,533/1,576（97.27%）。剩余逐项 reason 见共享 `formal_scope_coverage.json`。
- M1 display/runtime pytest 20/20，MR1 shared-registry tests 2/2。只更新共享展示映射/审计/交接，不触发 Telegram，未改模型、策略、账本或结算；继续处理 492 条未匹配。

## 2026-10-12 正式范围中文名称续补（六十三）
- 共享库新增两条：Gyeongju (W)（41028）→庆州女足（Tips.GG 中文女足档案）；FC Petrzalka（41471）→柏沙卡（7M 中文球队档案）。另新增 Jeddah Club（42718）→阿尔拉比亚（FootyStats 简中球队档案）。
- 审计并修复一处旧别名冲突：删除 team_id 3397（吉达联合）的错误/歧义别名“Jeddah Club”，因为该名对应独立 Saudi First Division 队 team_id 42718；以 FootyStats 的 Jeddah Club/阿尔拉比亚球队页交叉确认。其他正确 canonical、team ID 和交易数据未动。
- 最新 formal union 2,468：canonical 1,978、unresolved 490（80.15%）；M1 1,535/1,576（97.40%）；M1 OU-R1 52/52；MR1 AH 1,511/1,921（78.66%）；MR1 AI declared mirror 1,535/1,576（97.40%）。剩余明细及逐项 reason 在共享 `formal_scope_coverage.json`。
- M1 display/runtime pytest 20/20，MR1 shared registry tests 2/2 通过。未编辑或发送 Telegram；只改共享显示名/别名冲突与交接，模型、策略、订单、结算不变。继续处理剩余 490 项。

## 2026-10-12 正式范围中文名称续补（六十四）
- 共享库新增 JK Nõmme United（team_id 29759）→诺梅联队，来源为 Tips.GG 简体中文球队页（https://tips.gg/cn/team/fc-nomme-united-football/）；原始 provider identity、拉丁字母拼写别名和精确 ID 保留。
- 最新 formal union 2,468：canonical 1,979、unresolved 489（80.19%）；M1 1,536/1,576（97.46%）；M1 OU-R1 52/52；MR1 AH 1,512/1,921（78.71%）；MR1 AI declared mirror 1,536/1,576（97.46%）。未匹配详单见共享 coverage JSON。
- M1 display/runtime pytest 20/20、MR1 shared registry tests 2/2 通过。未改生产 Telegram、模型、策略、正式 ledger 或 settlement；继续补齐剩余 489 项。

## 2026-10-12 正式范围中文名称续补（六十五）
- 共享库新增 Ethnikos Achna（team_id 14056）→艾治拿斯，来源为 7M 中文球队档案（https://team.7m.com.cn/553/index.shtml），页面列出 Ethnikos Achna FC 与中文队名；provider 原名及常见拼写别名保留在唯一 registry。
- 最新正式范围 union 2,468：canonical 1,980、unresolved 488（80.23%）；M1 1,537/1,576（97.53%）；M1 OU-R1 52/52（100%）；MR1 AH 1,513/1,921（78.76%）；MR1 AI declared mirror 1,537/1,576（97.53%）。未匹配明细及逐项原因以共享 `formal_scope_coverage.json` 为准。
- M1 display/runtime pytest 20/20、MR1 shared-registry tests 2/2 通过。只更新共享展示映射/审计与交接；未编辑或发送 Telegram，未改模型、策略、正式账本或结算；继续处理剩余 488 项。

## 2026-10-12 正式范围中文名称续补（六十六）
- 共享库新增 Sektzia Nes Tziona（team_id 5450）→耐斯茨奥纳，来源为 7M 中文球队档案（https://team.7m.com.cn/10048/index.shtml）；采用该来源中文名的简体字规范形式，保留来源繁体名“耐斯茨奧納”及 provider 英文身份/ID。
- 最新 formal union 2,468：canonical 1,981、unresolved 487（80.27%）；M1 1,538/1,576（97.59%）；M1 OU-R1 52/52；MR1 AH 1,514/1,921（78.81%）；MR1 AI declared mirror 1,538/1,576（97.59%）。完整 unresolved 列表及原因见共享 `formal_scope_coverage.json`。
- 验证：M1 定向 pytest 20/20、MR1 shared registry tests 2/2。未触发 Telegram、未修改交易模型/策略/账本/结算；仅更新共享名称、审计与交接，继续处理剩余 487 项。

## 2026-10-12 正式范围中文名称续补与历史 TG 核验（六十七）
- 共享名称库已推送至 `totalcorner-research-bridge` master `0a390db`；Runner 记录共享库 batch 66，并追加本次真实历史通知修复回执。
- 三条既有、专用于名称编辑的 workflow 均完成：M1 `38211696706`（成功）；MR1 AH `38211700043`（成功）；MR1 AI `38211703325`（成功）。均只调用原消息 edit API/保存各系统自己的修复状态，没有重新发送策略消息、触发扫描或新建 Pick。
- 实际结果：M1 AH 与 M1 OU-R1 共用 ledger/formatter，37 条已保存原文候选全部 `ALREADY_MATCHING`，新编辑 0、失败 0；另 99 条没有 ledger 原文、70 条仍无可替换的已确认名称。MR1 AH 0 条需要编辑，124 条已处理/跳过，unresolved 0、failed 0。MR1 AI 新编辑 0；9 条候选均因 Telegram 返回 `400 message to edit not found` 失败，另 192 条仍 unresolved；未重发。完整 status/report 分别保存在 M1 ledger repair artifact 和 MR1 自己的 `telegram-edit-repair.json` / formal repair status 中。
- 当前共享正式范围：2,468 个 ID，canonical 1,981、unresolved 487、覆盖 80.27%；M1 1,538/1,576（97.59%）；M1 OU-R1 52/52（100%）；MR1 AH 1,514/1,921（78.81%）；MR1 AI declared mirror 1,538/1,576（97.59%）。逐项 unresolved 及原因见共享 `formal_scope_coverage.json`。
- 定向验证：M1 pytest 20/20；MR1 共用库与 AI formatter/parser 测试 8/8。单独 V6 formal runtime 集成测试未计入通过数：其断言价格为 `@0.93`，实际格式文本仍为原 fixture 锁定水位 `@0.90`，此项与中文映射无关，本轮未改交易字段/策略。
- 不曾修改 M1/MR1 策略、模型、盘口、交易账本或结算。后续继续只为剩余 487 个正式范围 ID 寻找有来源的 canonical 中文名；Telegram 尚未编辑的限制与回执如上，不以重发替代。

## 2026-10-12 正式范围中文名称续补（六十八）
- 共享库新增 Ravan Baku（team_id 2716）→拉万巴库；Sofascore 中文资料使用“拉万巴库”，与中文维基条目“拉雲巴古”交叉核验，保留繁体别名及原 provider 英文身份/ID。
- 当前 formal union 2,468：canonical 1,982、unresolved 486（80.31%）；M1 1,539/1,576（97.65%）；M1 OU-R1 52/52（100%）；MR1 AH 1,514/1,921（78.81%）；MR1 AI declared mirror 1,539/1,576（97.65%）。逐项 unresolved 及原因以共享 `formal_scope_coverage.json` 为准。
- M1 定向 pytest 20/20、MR1 registry tests 2/2 通过。该映射在三条 TG 历史修复 workflow 完成后才新增，故需再运行 M1/MR1 AI 各自现有名称编辑流程确认是否有新增可修复原消息；不发送新通知。模型、策略、正式账本和结算保持不变。

## 2026-10-12 正式范围中文名称续补（六十九）
- 在共享库 `0cb06d0` 推送 Ravan Baku 映射后，复跑既有 M1 与 MR1 AI 名称修复：M1 workflow `38212009365` 成功，结果仍为 eligible 37 / already matching 37 / edited 0 / missing original text 99 / unmapped 70 / failed 0；MR1 AI workflow `38212013783` 成功，仍为 9 条候选、编辑 0、9 条 `400 message to edit not found`、192 条 unresolved。新映射没有产生新的历史可编辑消息。
- 故历史 Telegram 最终实际编辑成功数仍为 0；M1 现有可核实消息已是目标名称，MR1 AH 全部 124 条状态已处理且无待改文本，MR1 AI 的 9 条失败因消息不在目标 Bot 可编辑范围内无法修复。没有重发或改变投注内容。
- 最新共享正式覆盖维持 batch 68 数字：union 2,468 / 1,982 canonical / 486 unresolved（80.31%）；M1 1,539/1,576（97.65%）；M1 OU-R1 52/52；MR1 AH 1,514/1,921（78.81%）；MR1 AI declared mirror 1,539/1,576（97.65%）。本地共享 registry 与 formatter 测试通过；未修改策略、模型、正式 ledger 或 settlement。

## 2026-10-12 正式范围中文名称续补（七十）
- 共享库新增 TotalCorner team_id 2101（provider `MP`）→米凯利。其唯一正式范围联赛 ID 122 已在同一 registry 对应芬兰 Ykkösliiga；Sofascore 中文 MP 球队页对应城市 Mikkeli，并列出 Ykkösliiga，故身份匹配由 provider 缩写、联赛与中文来源交叉确认；附加 MP Mikkeli/Mikkelin Palloilijat 别名。
- 最新正式范围 union 2,468：canonical 1,983、unresolved 485（80.35%）；M1 1,540/1,576（97.72%）；M1 OU-R1 52/52（100%）；MR1 AH 1,515/1,921（78.87%）；MR1 AI declared mirror 1,540/1,576（97.72%）。逐项未匹配及原因见共享 `formal_scope_coverage.json`。
- 本地 M1 display/runtime pytest 20/20、MR1 registry tests 2/2 通过。此 ID 同属 M1/MR1 正式范围，映射推送后将再运行相关既有历史名称编辑工作流；只尝试原消息改字，不发新策略消息，不改交易规则/记录。

## 2026-10-12 正式范围中文名称续补与 Telegram 复核（七十一）
- 将 team_id 2101→米凯利推送后，M1 历史名称工作流 `38212342672` 完成：仍 37 条目标文本已在 Telegram 中、edited 0、already matching 37、缺原始文本 99、无映射 70、失败 0。
- MR1 AH 工作流初次 `38212345596` 的 Telegram 编辑步骤成功（eligible 0、skip 124、unresolved 0、failed 0），但状态提交遇并发 push 冲突；串行重跑 `38212531699` 成功，status 已持久化：eligible 0、edited 0、skipped 125、unresolved 0、failed 0。
- MR1 AI 工作流初次 `38212348400` 的消息编辑结果为 9 条 Telegram 400 `message to edit not found`、192 unresolved，回执 push 遇同类并发冲突；串行重跑 `38212591122` 成功并持久化同样结果。没有新增编辑、没有重发。
- 最新正式范围：union 2,468、canonical 1,983、unresolved 485（80.35%）；M1 1,540/1,576（97.72%）；M1 OU-R1 52/52；MR1 AH 1,515/1,921（78.87%）；MR1 AI declared mirror 1,540/1,576（97.72%）。全量 unresolved 明细与逐项原因在共享 coverage JSON。
- 验证仍为 M1 formatter/runtime pytest 20/20，MR1 共享 registry tests 2/2。无模型/策略/盘口/ledger/settlement 改动；当前已确认的 TG 历史可修复消息均已是中文，剩余限制为缺失原文、无已确认映射以及 Telegram 原消息不存在。

## 2026-10-12 正式范围中文名称续补（七十二）
- 共享 registry 新增 Estudiantes Rio Cuarto（team_id 30795）→里奥夸尔托学生队，来源 Tips.GG 简中球队页；TotalCorner provider 原名与页面队名对应，球队 ID、别名及引用留存。
- 最新 formal union 2,468：canonical 1,984、unresolved 484（80.39%）；M1 1,541/1,576（97.78%）；M1 OU-R1 52/52；MR1 AH 1,516/1,921（78.92%）；MR1 AI declared mirror 1,541/1,576（97.78%）。完整 unresolved 及原因以共享 coverage JSON 为准。
- M1 display/runtime pytest 20/20、MR1 registry tests 2/2 通过。该映射更新后待复核已有 M1/MR1 AH/MR1 AI 历史名称编辑流程；只操作原消息，不发送新的策略消息。

## 2026-10-12 正式范围中文名称续补与 TG 复核（七十三）
- 在新增 Estudiantes Rio Cuarto 映射后，重跑已有名称编辑流程：M1 `38212825405` 成功，eligible 37、already_matching 37、edited 0、缺 ledger 原文 99、unmapped 70、failed 0；M1 AH 与 OU-R1 共用此账本/formatter。
- MR1 AH `38212829492` 成功：eligible 0、edited 0、skipped 125、display unresolved 0、failed 0；回执提交成功。MR1 AI `38212833318` 成功：total 201、9 candidates、edited 0、9 failed（Telegram 400 `message to edit not found`）、192 unresolved；结果已持久化到 MR1 自有修复报告。
- 历史 TG 此轮及此前各轮实际编辑成功仍为 0：已经是中文的原消息均不改；M1 99 条缺保存原文、70 条无确认映射；MR1 AI 九条 Telegram 目标 Bot 无法找到原消息、192 条 unresolved。未重发任何 Pick，未改交易字段/账本/结算。
- 最新共享 registry `9203628`：正式范围 union 2,468，canonical 1,984，unresolved 484（80.39%）；M1 1,541/1,576（97.78%）；M1 OU-R1 52/52；MR1 AH 1,516/1,921（78.92%）；MR1 AI declared mirror 1,541/1,576（97.78%）。M1 定向测试 20/20，MR1 registry 测试 2/2。
