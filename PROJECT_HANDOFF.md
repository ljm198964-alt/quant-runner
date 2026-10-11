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

## 2026-10-12 共享中文名称库收敛与当前状态
- **本节状态被 2026-10-12 全量复核结果更新：** 共享库最新提交 `d353f4a`；12,172 个 team ID 的英文身份全部恢复，canonical 简体中文名 3,475（28.55%），8,697 条仍无唯一可核验中文名。771 个 league ID 中 329 个有 canonical 中文名。M1 历史覆盖 1,855/3,880（47.81%），MR1 历史覆盖 3,410/11,916（28.62%）。旧段落数字仅为当时快照。
- 最近一次 `Shared Football Identity Recovery` 已在 run `38178789455` 成功结束；持久化检查点记录 58/58 个待查联赛完成、0 个失败、1,374 次累计 TotalCorner API 请求，恢复 295 个英文身份。没有重新 dispatch 已完成的身份采集。
- 在唯一未映射队名上追加了 Reep/Wikidata 严格交叉：仅 exact English name 且 Reep QID、TotalCorner team ID 均唯一；622 个候选中 64 个有简体中文标签并新增，558 个无简体标签，24 个同名交叉歧义排除。没有模糊匹配或按 team ID 猜名。其余 8,697 条及逐条原因保存在 `results/football_chinese_bulk_report.json`。
- M1 与 MR1/MR1 AI 继续读取 `totalcorner-research-bridge/data/football_display_names/`。MR1 AI browser-forward/reconcile 已停止读取其旧 registry snapshot（快照保留为历史证据），改用 workflow checkout 的同一共享库；MR1 代码提交 `c9a6ccc`。解析/隔离测试通过，未改模型、策略、账本或通知规则。
- 主要报告：`results/football_chinese_bulk_report.md`、`data/football_display_names/coverage.json`；名称源分布和 ID 来源见报告与 `teams.json` 的每行 `source`。
- 唯一共享库仍为 M1 仓库 `data/football_display_names/`。M1 formatter 按 team/league ID 读它；M1 scan preflight 只报告展示映射缺口，不阻塞正式锁单。MR1 AH、MR1 AI browser-forward/reconcile 与 MR1 Telegram formatter 从 `external/football-display-registry` 读取同一库，运行 workflow checkout 主仓 master。名称只影响展示，不进入模型字段。
- `totalcorner-research-bridge` 以 `52fe40d9164560caf3232740762b035ed70391af` 为基础的原统计属于历史快照，现由顶部 `d353f4a` 结果替代。英文身份与中文覆盖数字请以顶部新结果为准。
- 最新已保存 M1 scan `results/latest.json`：88 场、176 个唯一 team ID；175 个有 canonical 中文展示名（99.43%），39 个 league ID 全部覆盖。唯一未确认中文名为 `FC Livyi Bereh`（ID 86544）；不以猜译补齐。扫描报告 `results/m1_telegram_display_unresolved.json` 已重算。
- 当前扫描池补充名使用 7M、500彩票网、Sofascore、Titan007、FootballAnt、公开中文球队资料等逐条链接的来源；未改既有正确映射。近期重点包含施利马流浪、格兹拉联、波德布雷佐瓦、斯拉文贝鲁波、维京古尔、利雅得青年人、布赖代合作、阿根廷青年人、塔勒瑞斯、纽维尔老男孩等。来源 URL 写在每个 curation row 的 `source.reference`。
- 已验证共享读取：MR1 `src/football-display-names.js` 实际加载本次 M1 共享库，并对测试 fixture 渲染中文；MR1 AI browser-forward/reconcile、Telegram formatter 均使用该 resolver。`615542b96` 的 MR1 对接测试通过；直接挂载本次共享目录的只读测试 2/2 通过。M1 formatter/coverage/recovery 测试 12/12 通过。
- `Football display identity recovery` 的早期尝试曾遇到 push/rebase 和报告 staging 失败；后续恢复机制已修复并由 run `38178789455` 成功完成，当前不得重复采集。quant-runner 的手动 workflow 保留；只有新增且可核验的身份数据时才考虑再次运行。
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
