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
