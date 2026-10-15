# 量化亚洲盘｜跨会话工作交接记录

## 2026-10-15 正式范围球队中文续补（batch 123）
- 从共享库 master `0883dd065eb53307f41f8b31508f410e19d1df28` 继续，对剩余正式未匹配项做定向身份核查；没有重跑历史身份恢复。新增 TotalCorner `team_id=2442`：provider 原名仍为 `CS Stefanesti`，canonical 简中名 `斯特凡内什蒂林达布队`，别名保留 `Lindab Stefanesti`。Tips.GG 简中球队页以 `斯特凡内什蒂林达布队` 标注 Lindab Stefanesti；罗马尼亚县足协及俱乐部历史资料证明 `CS/FC Stefanesti` 与 `Lindab Stefanesti` 为同一俱乐部名称沿革；TotalCorner 比赛历史核对罗马尼亚赛事身份。证据链接及说明写入唯一共享 registry 的 source 字段。
- 共享库 PR [#26](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/26) 已合并，merge SHA `58f338d89e69be7ce0f3facbd11fa0fcc144bfed`。formal union 当前 2,468 IDs / 2,357 canonical / 111 unresolved（95.50%）；M1 1,539/1,553（99.10%），M1 OU-R1 52/52（100%），MR1 AH 1,837/1,921（95.63%），MR1 AI 声明镜像 M1 1,539/1,553（99.10%）。剩余身份和原因以共享库 `formal_scope_coverage.json#unresolved_records` 为准；无可靠来源项继续 unresolved，不做猜译。
- M1 formatter 与 display-repair 本地测试 13/13 PASS，新增测试通过 ID 2442 确认中英别名均按 team ID 渲染，不改盘口、方向数据或正式 pick。可读取的 M1/M1 OU-R1 正式账本和 MR1 AI browser prospective ledger 未找到该 team ID 的既有 Pick。
- 合并后重新运行了既有 name-only 历史修复：M1 [run 38660715684](https://github.com/ljm198964-alt/quant-runner/actions/runs/38660715684) PASS，eligible 41、edited 0、already matching 41、缺原发送文本 99、unmapped 100、failed 0；MR1 AH [run 38661008930](https://github.com/ljm198964-alt/quant-runner/actions/runs/38661008930) PASS，edited 0、skipped/already processed 125、unresolved 0、failed 0；MR1 AI [run 38661130525](https://github.com/ljm198964-alt/quant-runner/actions/runs/38661130525) workflow PASS，total 201、candidate 9、edited 0、unresolved 192、failed 9，9 条都因 Telegram 返回 `400 message to edit not found`。因此本轮历史消息实际编辑 0；没有重发或测试 TG。未来消息依赖正式 runtime 读取已合并共享 registry。
- 本轮只更新共享展示名称、来源/coverage、独立 formatter 测试及本交接；未改 M1、M1 OU-R1、MR1 AH、MR1 AI 模型/策略、scope、阈值、盘口源、账本、结算或发送规则。

## 2026-10-15 剩余正式范围缺名定向复核（batch 122）
- 先以共享 master `0883dd065eb53307f41f8b31508f410e19d1df28` 的实际 `formal_scope_coverage.json` 为准：仍为 2,468 个正式范围球队 ID，2,356 有 canonical，112 未匹配；未沿用旧“740/718”快照。
- 对共享库全部历史 JSON 身份/中文证据档案做了按 unresolved provider identity 的精确交叉检查，没有发现此前未登记的同 ID 中文别名。对埃及低级别、科索沃、马耳他、北马其顿、威尔士及波罗的海候选做了中文来源定向检索；找到的官方/权威球队资料多数只保留英文/本地品牌，不能据此造中文名。
- 特别保留身份隔离：埃及城市/球队 Ghazl El Mahalla 的中文“马哈拉/加斯马哈拉”资料不能证明另一 provider identity `El Mahalla El Kobra` 是同队；阿尔巴尼亚 Vllaznia 的中文资料也不能转给科索沃 `Vllaznia`（league_id 8293）。这些仍不写入 canonical。无新增 mapping；正式覆盖率与各模型计数不变。完整逐队余项、league_ids 与 reason 见共享库 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 本轮只做证据复核及交接记录，不改共享库、模型、策略、TG、账本或工作流。后续从 remaining 112 中继续逐队找带精确身份对应的简中球队资料；无可靠资料的保留 unresolved。

## 2026-10-15 中文 Telegram 显示纠偏（batch 121）
- 在最新共享 master `f6328b064869a5e838edf426d8383ecab72d0164` 上继续，仅修 display 层。修正 `team_id=82622`：LiveScore 简中页明确显示“立陶宛Be1 Nfa”，此前 canonical 仅为拉丁字母 `Be1 NFA`，被 M1 formatter 判作未中文化；现 canonical 为“立陶宛Be1 Nfa”，保留 Be1 NFA 官方品牌和 ID。`league_id=514` Greece Super League 2 更新为 FootyStats 简中赛事名“希腊超级联赛2”，旧通称留在 aliases。来源分别见共享 registry 的 source reference 和 `competition_curation_20261015.json`。
- 共享库 PR [#25](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/25) 已合并，merge SHA `0883dd065eb53307f41f8b31508f410e19d1df28`。formal scope 仍是 2,468 IDs / 2,356 canonical / 112 unresolved（95.46%）；M1 与声明镜像 MR1 AI 1,538/1,553，M1 OU-R1 52/52，MR1 AH 1,836/1,921。映射数不变；修正了一个此前登记为 canonical 但不能通过 M1 中文字符判定的显示标签。完整余项及逐项原因仍以共享 `formal_scope_coverage.json#unresolved_records` 为准（111 条无可核验中文名，team_id 4931 的 provider identity 为无效字面 `0`）。
- M1 formatter 测试 10/10 PASS，包含 Be1 球队/让球方向、Greece SL2 和 Lithuania 1 Lyga 的 ID 渲染；M1 curation 二次运行幂等。MR1 reader/formatter 2/2 PASS；直接用共享 registry 验证得到“立陶宛1 Lyga / 立陶宛Be1 Nfa / 希腊锡罗斯”及“希腊超级联赛2”。M1 AH、M1 OU-R1、MR1 AH、MR1 AI 仍读取同一共享名称库；未改变消息格式、策略字段、模型、scope、账本、结算或通知规则。
- 更新后触发了现有名称修复 workflow（不扫描赛事、不发送新消息）：M1/M1 OU-R1 [run 38659182499](https://github.com/ljm198964-alt/quant-runner/actions/runs/38659182499) PASS，eligible 41、edited 0、already matching 41、缺保存原文 99、unmapped 97、failed 0；MR1 AH [run 38659182779](https://github.com/ljm198964-alt/quant-runner/actions/runs/38659182779) PASS，eligible/edit 0、skipped 125、unresolved/failed 0；MR1 AI [run 38659182628](https://github.com/ljm198964-alt/quant-runner/actions/runs/38659182628) PASS，201 条中 9 个改名候选、edited 0、unresolved 192、failed 9，均因 Telegram 返回 `400 message to edit not found`。因此本轮历史消息实际编辑 0；M1 原有 41 条可编辑记录均已与 formatter 文本相同。没有历史重发或测试推送。
- 真实后续新 Pick 的 TG 显示尚未自然发生，不能宣称已由新生产 Pick 回执验收。新增名称在合并后可由现有 runtime 通过共享 registry 读取。没有因 Actions 支出限制而新增或重构工作流。

## 2026-10-15 正式范围中文名称续补（batch 120）
- 继续 PR #23 后，补入 TotalCorner `team_id=135539` / `Hellas Syrou → 希腊锡罗斯`。来源为球天下体育中文赛事页及多个中文赛程页对同一 Hellas Syrou 对阵的稳定用名；ID 和原英文身份保持不变。共享库 PR [#24](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/24) 已合并，master merge SHA `f6328b064869a5e838edf426d8383ecab72d0164`。
- 当前唯一正式范围统计：2,468 个队 ID，2,356 有 canonical display 名称，112 unresolved（95.46%）。M1 1,538/1,553（99.03%）；M1 OU-R1 52/52（100%）；MR1 AH 1,836/1,921（95.58%）；MR1 AI 镜像 M1 1,538/1,553（99.03%）。剩余完整队名/原因请读取 M1 master `data/football_display_names/formal_scope_coverage.json#unresolved_records`：111 个 `NO_VERIFIED_CANONICAL_ZH`，1 个 `PROVIDER_IDENTITY_INVALID`（ID 4931 的原始队名为字面 `0`）。本轮对候选名称做了定向核验，没有把无中文来源的球队音译后冒充主流规范名。
- 本地展示验收：M1 display tests 9/9 PASS；MR1 shared registry reader/formatter 2/2 PASS，测试通过 `FOOTBALL_DISPLAY_REGISTRY_DIR` 直接读取共享 registry。四条正式展示链仍共享唯一 registry；未改 Telegram 版式、签名或策略字段。对本轮映射涉及的历史 M1 ledger/TG repair 状态没有找到可编辑已发送订单，因此本轮真实编辑 0；无测试发送、无历史重发。没有启动生产 workflow，云端新 Telegram 展示回执未验证。
- 本 runner handoff 随 PR #7 同步。模型、策略、阈值、赛事范围、盘口、正式订单、账本、结算和发送规则未改。

## 2026-10-15 正式范围中文名称续补（batch 119）
- 从共享库 master `533c2765` 继续。新增 3 个带公开中文赛事数据来源的正式范围映射：`109103 NK Stupcanica Olovo → 斯图普卡尼察`（Tips.GG 简中球队页，并以波黑联赛赛程核对）、`82622 BE1 NFA → Be1 NFA`（LiveScore 简中站使用“立陶宛Be1 Nfa”，品牌名保留）、`110165 Attard → 阿塔德`（Tips.GG 简中球队页）。ID、provider identity 和赛事归属均未改；未合并重复 provider ID。
- 更新后唯一共享库正式范围实算：2,468 IDs，2,355 canonical，113 unresolved，95.42%。M1 1,537/1,553（98.97%）；M1 OU-R1 52/52（100%）；MR1 AH 1,835/1,921（95.52%）；MR1 AI 声明镜像 M1 1,537/1,553（98.97%）。完整剩余队名和逐项原因以 `data/football_display_names/formal_scope_coverage.json#unresolved_records` 为准；其中 112 个目前无经核实 canonical 中文名，1 个 `team_id=4931` 的 provider identity 是无效字面 `0`，均未猜译。
- 本地展示验证：M1 display + formal runtime 21/21 PASS；MR1 shared registry reader/formatter 2/2 PASS，MR1 测试直接读取本批共享 JSON。涵盖的 M1 AH、M1 OU-R1、MR1 AH、MR1 AI formatter 代码均读取唯一共享 registry；未改消息格式或策略字段。没有新可编辑历史 Telegram 目标，本批历史实际编辑 0；没有发送测试或历史重发。云端运行/Telegram 实际回执未验证。
- 本批共享库 PR [#23](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/23) 已合并；分支提交 `dd3ac8c16e7bf032c803be3beb3ac6394c5098a4`，master merge SHA `1b0120dd7d2efb29ae1ec6afc5fa13671775fe92`。本 runner handoff 随后提交更新。未更改模型、策略、赛事范围、赔率、账本、结算或正式派单规则。

## 2026-10-15 正式范围中文名称续补（batch 118）
- 从共享库 `totalcorner-research-bridge/master` 的 PR #21 merge `daa5b066ae00d6c89705d8e0b22a651354fcc907` 继续。本批唯一可靠新增为 TotalCorner `team_id=113064`，`Ittihad Nabarouh → 纳巴鲁伊蒂哈德`；来源是 Sofascore 简体中文球队档案（https://www.sofascore.com/zh/football/team/ittihad-nabarouh/275010），同页英文队名和埃及 Second Division B 背景核对一致。原 provider identity、ID 和策略数据未改。
- 共享库 PR [#22](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/22) 已合并，master commit `533c2765`（本批分支提交 `de2fd662f989477863804b47cd812d219439ccc2`）。本批使用既有精确 ID curation 脚本，二次运行幂等（新增 0）。
- 合并后文件实算：formal union 2,468 个 team ID，2,352 有 canonical 中文名，116 unresolved，覆盖 95.30%；M1 1,534/1,553（98.78%）；M1 OU-R1 52/52（100%）；MR1 AH 1,832/1,921（95.37%）；MR1 AI 声明镜像 M1 1,534/1,553（98.78%）。完整余项和逐项原因以唯一共享文件 `data/football_display_names/formal_scope_coverage.json#unresolved_records` 为准。其余 115 项缺少经核验的中文名，1 项 `team_id=4931` 的 provider identity 仍是无效字面 `0`；未用临时音译填充。
- 展示验证：M1 formatter 与历史名称修复测试 11/11 PASS；MR1 AI 共享 registry/Telegram formatter 测试 4/4 PASS。之前批次已验证 M1 OU-R1 和 MR1 AH 使用唯一共享库；本批新增名称在四模型共用文件可读。测试是隔离代码验证，不代表云端真实发送。
- 历史 TG：本批没有可因 `team_id=113064` 新映射而编辑的已发送消息：当前 M1 formal ledger 无此 ID；MR1 AH 的 repair status 和 MR1 AI 的 edit-repair report 也无此 ID。最近既有正式修复回执可复核为：M1 workflow [38651673155](https://github.com/ljm198964-alt/quant-runner/actions/runs/38651673155) 的报告附件为 41 eligible、0 edited、41 already matching、99 缺原发送正文、97 unmapped、0 failed；MR1 AH workflow [38651677750](https://github.com/ljm198964-alt/quant-runner/actions/runs/38651677750) 的持久状态为 0 eligible/edited、125 skipped/already processed、0 unresolved/failed；MR1 AI workflow [38650382575](https://github.com/ljm198964-alt/quant-runner/actions/runs/38650382575) 为 201 total、9 candidates、0 edited、192 unresolved、9 failed，9 条均是 Telegram `400: message to edit not found`。这些回执都早于本批 merge；未为没有新目标的映射重复触发修复工作流，也未重发历史单或发送测试消息。
- GitHub Actions 未因本次共享库 PR 触发；最近生产运行仍受账户运行限制影响。没有更改 M1 AH、M1 OU-R1、MR1 AH 或 MR1 AI 策略、范围、阈值、订单、账本、结算或通知规则。

## 2026-10-15 正式范围中文名称续补（batch 117）
- 从最新共享库 `master` `7aadf155ba382c45c22b379d7e6521c99fe844c5` 继续；当前正式范围并集 2,468 个 team ID，原 unresolved 121。本批新增 4 个可核实名称，结果为 canonical 2,351、unresolved 117、覆盖率 95.26%；M1 1,533/1,553（98.71%）、M1 OU-R1 52/52、MR1 AH 1,831/1,921（95.31%）、MR1 AI 声明范围镜像 M1 1,533/1,553（98.71%）。
- 新增：`45722 KF Kosova Prishtine → KF科索沃布利斯丁`、`45930 KF Ramiz Sadiku → KF拉米兹萨迪库`、`141371 KF Dinamo Ferizaj → 费里扎戴拿模`、`169513 FC Prizreni → 普里兹雷尼`。来源均为 FootballAnt 简体中文队页，并以 TotalCorner 对应 team 页面及科索沃联赛上下文交叉核验。只新增展示名/来源记录，不改 provider identity 或模型数据。
- 共享库 PR [#21](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/21) 已合并，merge SHA `daa5b066ae00d6c89705d8e0b22a651354fcc907`。可复现 curation 入口：`ops/curate_formal_scope_public_club_tables.py`，二次运行验证幂等（新增 0、余项仍 117）。当前完整余项应始终读取 `data/football_display_names/formal_scope_coverage.json#unresolved_records`，不要沿用旧的 718/740 计数。
- 本批只核对并增补共享名称数据，没有编辑或重发历史 TG，没有运行生产链。121 项起始余项中其余 117 项继续逐项寻找有来源的中文名；上游无效身份 `team_id=4931` 不猜测。

## 2026-10-15 中文展示库续补（batch 116）
- 共享库 PR [#20](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/20) 已合并，master SHA `7aadf155ba382c45c22b379d7e6521c99fe844c5`。唯一库仍为 `data/football_display_names/display_names.json`。
- 新增 TotalCorner `team_id=114375` Victoria Hotspurs → `维多利亚热刺`；来源为 Sofascore 简体中文关联俱乐部显示，TotalCorner 队页核对其马耳他联赛身份。新增 `league_id=15795` Malta Challenge League → `马耳他挑战联赛`，来源为中文赛事页并以 TotalCorner 队页赛区交叉核对。provider 原名、ID、联赛身份均未改写。审计及可重复的精确 ID curation 脚本保存在共享仓库对应数据目录和 `ops/`。
- 合并后从 `formal_scope_coverage.json` 实算：正式范围并集 2,468，canonical 2,347，未匹配 121，覆盖 95.10%；M1 1,529/1,553（98.45%）；M1 OU-R1 52/52；MR1 AH 1,827/1,921（95.11%）；MR1 AI 声明镜像 M1 1,529/1,553（98.45%）。剩余项及原因见唯一共享文件 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；不将“Al Magd/Al Majd”混为同队（TotalCorner 分别标注埃及与叙利亚联赛），其余无可靠中文来源者继续 unresolved。
- 展示验收：M1 Telegram 专项本地测试 6/6 PASS；使用最新共享文件的隔离 M1 formatter 渲染为 `【M1】2026-10-15 20:00 马耳他挑战联赛 维多利亚热刺 vs 泽巴格流浪 全场让球 维多利亚热刺 -0.25@0.95`。MR1 共享 registry reader/formatter 定向测试 2/2 PASS，并验证读取相同共享 JSON。未运行生产策略或发送测试 Telegram。
- 本轮未执行历史 Telegram 编辑，因此本轮真实编辑成功数为 0；历史编辑仍不得重发。最近既有修复回执仍记录于 batch 115：M1/M1 OU-R1 run `38651673155` 编辑 0（缺正文/映射限制），MR1 AH run `38651677750` 编辑 0（125 already processed）；MR1 AI 历史 9 条 Telegram edit 返回 `400 message to edit not found`。没有新的生产回执，不能宣称历史消息已修复。GitHub Actions 未因本轮名称提交而触发；云端正式链未做新运行验证。
- 本次仅增加 display mapping/source/coverage/audit 与本 handoff；模型、策略、阈值、赛事范围、盘口、账本、结算和通知规则均未修改。

### Batch 116 后续：MR1 AI formatter 接线修复
- 真实隔离检查发现 MR1 AI formatter 接收共享解析器 `{league, match}`，却只读取 `{league, home, away}`，导致球队字段退回英文。修复已合并到 `mr1-shadow/master`，PR [#1](https://github.com/ljm198964-alt/mr1-shadow/pull/1)，merge SHA `0a8e90025550d103c4b2c431d31b67e131a22eb0`。
- 修复只在展示层从共享 `match` 字符串提取主客队；新增回归测试。MR1 AI Telegram formatter + shared reader 共 5/5 PASS；使用共享 JSON 的隔离输出为 `【MR1 AI】2026-10-15 20:00 马耳他挑战联赛 维多利亚热刺 vs 泽巴格流浪 全场让球 维多利亚热刺 -0.25@0.95`。没有真实发送 TG；云端下一轮运行与频道回执未被动验收。
- 本次核对的 M1 formal ledger、MR1 AH formal data 与 MR1 AI sent ledger 中未找到 team_id 114375 的既有发送记录，因此在这些已检查账本中没有可编辑的历史消息；未检查独立 M1 OU-R1 发送账本，也不重发历史单。其他历史修复数仍按 batch 115 已有真实回执记录。

## 2026-10-15 中文展示/正式 Telegram 尾项复核（batch 115）
- 从已合并共享库 `master` `3db198e7e38514efbff692d837a2c4adc1f03e24` 快进复核；覆盖统计仍为正式并集 2,468 IDs、canonical 2,346、unresolved 122（95.06%）；M1 1,528/1,553（98.39%）、M1 OU-R1 52/52、MR1 AH 1,826/1,921（95.05%）、MR1 AI 声明镜像 1,528/1,553（98.39%）。本轮对剩余项作定向来源核验，未发现可安全加入的新 canonical。例：KF Kika 的中文站资料仍显示拉丁字母队名，不据此编造音译。完整 unresolved 名单及逐项原因仍以唯一共享文件 `data/football_display_names/formal_scope_coverage.json#unresolved_records` 为准（121 条无经核实中文名，1 条 team_id 4931 provider identity 为无效字面 `0`）。
- 四条正式展示链（M1 AH、M1 OU-R1、MR1 AH、MR1 AI）继续读取唯一共享 `display_names.json`；M1 11/11、MR1 registry/AI formatter 4/4 定向测试通过。隔离格式验收通过；没有触发生产策略、发送测试单或改动账本。
- 已完成的历史 TG 名称修复回执仍是：M1/M1 OU-R1 run `38651673155` edited 0（41 已匹配、99 缺原消息正文、97 无映射、0 failed）；MR1 AH run `38651677750` edited 0（125 already processed）；MR1 AI 没有本轮新增可编辑目标，既有 9 条失败原因为 Telegram `400 message to edit not found`。不重发任何旧订单；不能宣称历史消息已修复。
- 无新增可靠映射，故共享 registry 无新提交；本条仅记录最终尾项核验。M1/M1 OU-R1/MR1 AH/MR1 AI 的模型、策略、阈值、范围、盘口来源、通知条件、账本及结算保持不变。

## 2026-10-15 formal-scope 中文名称续补（batch 114，最新）
- 从共享库 `totalcorner-research-bridge/master` 最新 `f9b33f3c3cfb4187979facee37db8849b1cb6d55` 继续，新增两条经中文足球资料核验的正式 ID：`109052 FK Famos Vojkovici → 法莫斯·沃季科维基`（SportScore 中文球队页）及 `43182 KF Iliria Fushe-Kruje → 伊利里亚富谢-Kruje`（Tips.GG 中文对阵页）。第二条另用中文地名资料核实 Fushë-Krujë=富舍克鲁亚，将最终显示规范为全中文 `伊利里亚富舍克鲁亚`；旧混合写法保留 alias。英文 provider identity、team_id、league_id 不变。另有窄范围、可重复的 canonical refinement guard，只有当前值精确等于旧标签时才可迁移。
- 共享数据 PR [#18](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/18) merge SHA `4560981172ffaac20711c7fcb45f9be46b45ef5c`；后续全中文名称精炼 PR [#19](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/19) merge SHA `3db198e7e38514efbff692d837a2c4adc1f03e24`。唯一库仍是 `data/football_display_names/display_names.json`，未新增第二份名称库。
- 最新实算：正式范围并集 2,468 IDs，canonical 2,346，unresolved 122，覆盖率 95.06%；M1 1,528/1,553（98.39%）；M1 OU-R1 52/52；MR1 AH 1,826/1,921（95.05%）；MR1 AI 声明镜像 M1 1,528/1,553（98.39%，另 observed confidence≥50 样本 181/182）。共享库 12,276 IDs、4,362 canonical（35.53%）。剩余122条逐项名称和原因见共享库 `data/football_display_names/formal_scope_coverage.json#unresolved_records`：121 条缺可靠中文来源，1 条 `team_id=4931` 的 provider identity 是字面 `0`，须修复上游身份后才能命名。
- 本地显示验收：M1 AH/OU-R1 共用 formatter 使用最新共享文件；M1 tests 11/11 PASS。MR1 shared registry 与 AI formatter tests 4/4 PASS。隔离 fixture 中 M1 输出包含 `伊利里亚富舍克鲁亚`、`法莫斯·沃季科维基`；MR1 AI 实际格式器同样渲染两队中文。未发测试消息或新 Pick。
- 历史 Telegram 仅执行原有名称编辑工作流（不重发订单）：M1 AH/M1 OU-R1 repair run [38651673155](https://github.com/ljm198964-alt/quant-runner/actions/runs/38651673155) PASS，实际 edited=0、already_matching=41、缺原消息文本=99、unmapped=97、failed=0；MR1 AH run [38651677750](https://github.com/ljm198964-alt/quant-runner/actions/runs/38651677750) PASS，edited=0、already_processed=125、unresolved=0、failed=0。MR1 AI 未重试已确认 Telegram `400 message to edit not found` 的历史记录；已核对现存 MR1 AI sent ledger 不含本批两个 ID，故没有新的可编辑目标。历史成功编辑总数本批仍为0。
- 本轮仅共享展示映射、其证据/覆盖报告和本 handoff；未改变 M1、M1 OU-R1、MR1 AH、MR1 AI 的模型、策略、阈值、范围、盘口来源、下单、账本或结算。

## 2026-10-15 formal-scope 中文名称续补（batch 113，最新）
- 从共享库最新 master `278cf1c88be4c55b391e308f7e1b11b3d2257bc0` 接续，精确新增 TotalCorner `team_id=136147`：Flint Mountain FC → 弗林特山。来源为 Tips.GG 简体中文威尔士杯球队列表 `https://tips.gg/cn/tournament/football-faw-welsh-cup-2024-25/`，其中同一球队条目显示英文 Flint Mountain 和中文“弗林特山”；正式记录的 provider identity、ID 与威尔士联赛上下文均吻合。更新复用 `ops/curate_formal_scope_footystats_batch.py`，拒绝覆盖已有 canonical。
- 最新实算：正式范围并集 2,468 IDs，canonical 2,344，unresolved 124，覆盖率 94.98%；M1 1,528/1,553（98.39%）；M1 OU-R1 52/52；MR1 AH 1,824/1,921（94.95%）；MR1 AI 声明镜像 M1 1,528/1,553。共享库 12,276 IDs、4,360 canonical（35.52%）。完整余项及逐条原因见共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；team_id 4931 的 `0` 仍是上游身份无效，不属于可翻译队名。该口径以 merge 后 `formal_scope_coverage.json` 为准，修正了更早 handoff 中过期的 M1 数字。
- 来源复核：对剩余威尔士和埃及/塞浦路斯候选作定向中文足球资料检索；Llay Miners Welfare、Ynyshir Albions、Treowen Stars、Cardiff Draconians、Caerphilly Athletic、埃及低级别俱乐部及塞浦路斯乙级候选未找到能同时确认中文名与目标 TotalCorner 身份的中文来源，继续保留 unresolved，不编造译名。Tips.GG 中文赛事页可以确认 Flint Mountain；英/法/丹麦等页面或中文站点但仅显示英文队名不作为中文名称证据。
- 本地验证：M1 formatter/repair 单测 8/8 PASS；MR1 shared-registry 与 AI formatter 4/4 PASS，明确挂载本轮共享 JSON。
- 新映射 merge 后各运行一次现有历史名称修复流程，均未重发订单：M1/M1 OU-R1 run `38650371388` PASS，Telegram 实际 edit 0、already matching 41、缺原文 99、unmapped 97、failed 0；MR1 AH run `38650376783` PASS，edit 0、already processed 125、unresolved 0、failed 0；MR1 AI run `38650382575` PASS，但业务计数为候选9、实际 edit 0、unresolved 192、failed 9，9 条均由 Telegram 返回 `400 Bad Request: message to edit not found`。故本批历史消息真实编辑成功数仍为0；workflow PASS 不等于编辑成功。
- 共享数据 PR #17 已合并，merge SHA `f9b33f3c3cfb4187979facee37db8849b1cb6d55`；quant-runner handoff 变更已推送到 main（本条后续提交）。无正式扫描/新 TG 发送。只增加展示映射/审计；模型、策略、阈值、赛事范围、赔率、账本、结算与通知规则未改。

## 2026-10-15 formal-scope 中文名称续补（batch 112，最新）
- 在 batch 111 基础上继续查剩余项，新增 TotalCorner `team_id=88074`：Karcagi SE→卡尔察吉队。证据为 Tips.GG 简体中文历史对阵页将 Karcagi 标为“卡尔察吉队”，并保留英文队名；TotalCorner ID 88074 球队页独立确认原名 Karcagi SE、联赛 Hungary NB II。来源分别为 `https://tips.gg/cn/archive/karcagi-se-football-vs-monori-se-football/` 与 `https://www.totalcorner.com/team/view/88074`。未按不确定的 Tips.GG 内部球队排名 ID 做连接，只以 TotalCorner ID 和精确英文名核验。
- 实际统计：正式并集 2,468；canonical 2,343；unresolved 125；覆盖率 94.94%。M1 1,551/1,553（99.87%，不变）；M1 OU-R1 52/52；MR1 AH 1,823/1,921（94.90%）；MR1 AI 声明镜像 M1 1,551/1,553（99.87%）。共享库 12,276 IDs、4,359 canonical。全部125条及原因在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 验证：M1 display/history repair 测试 11/11 PASS；MR1 shared registry 2/2、MR1 AI Telegram formatter 2/2 PASS；脚本编译、JSON 校验及 `git diff --check` PASS。无生产扫描或 Telegram 发送/编辑；历史实际 TG 编辑数保持0，本批只影响合并后读取共享库的后续格式化。
- 共享名称更新 PR #16 已合并至 `totalcorner-research-bridge/master`，merge SHA `278cf1c88be4c55b391e308f7e1b11b3d2257bc0`。MR1 既有 workflow 每次运行会 checkout 该仓库 master；本轮未触发 Actions，因此未声称云端/频道已即时复核。
- 仅修改共享 display data/curation audit 和范围报告；没有改策略、模型、阈值、scope、账本、结算或发送规则。

## 2026-10-15 formal-scope 中文名称续补（batch 111，最新）
- 从共享 registry 最新 `master`（起始 SHA `ff1aeba465d40af963fa58eebb17e42642fa633a`）继续；仅新增 6 个有简体中文比赛页明确对照英文队名、且可与 TotalCorner `team_id` / Kosovo Division 2 联赛上下文精确核对的名称：45225 KF Rahoveci→KF拉霍维奇；170478 KF Podujeva→KF波度瓦；167867 KF Dardania→达尔达尼亚；154157 KF Rilindja 1995→KF里林杰1995；49845 KF Arberia→阿伯利亚；170997 TOP Football→TOP足球。联赛 `39226 Kosovo Division 2`→科索沃乙级联赛。来源链接、英文身份、原 ID 和来源说明保存在唯一共享 `display_names.json` 与 curation reports；没有使用模糊 ID 匹配或改写既有 canonical。
- 执行后实算：正式并集 2,468；canonical 2,342；unresolved 126；覆盖率 94.89%。M1 1,551/1,553（99.87%，未变）；M1 OU-R1 52/52；MR1 AH 1,822/1,921（94.85%）；MR1 AI 声明镜像 M1 1,551/1,553（99.87%）。共享库 12,276 IDs、4,358 canonical。完整 126 条清单和原因位于共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。历史 scope 的 `systems` 是观察标签、并非精确的各模型 scope 成员清单；本批六个 ID 仅计入 MR1 AH，M1/MR1 AI 镜像沿用其正式快照，不以标签重复加总。
- 验证：M1 Telegram formatter 与历史修复单测 11/11 PASS；MR1 shared-registry 测试 2/2、MR1 AI Telegram formatter 2/2 PASS；本地按六个 ID 渲染得到中文赛事/球队名。M1 repair 的只读 dry-run 报 eligible 41、缺历史发送原文 99、无映射 97；**未执行真实编辑**。近期 quant-runner 历史 repair 回执显示 MR1 AI 9 次编辑因 Telegram `400 message to edit not found` 失败。未运行生产扫描、未发测试或重发订单。
- 四条格式器继续使用同一共享 registry：M1 AH/M1 OU-R1 在 M1 Python display helper；MR1 AH/MR1 AI 从 `external/football-display-registry` checkout 读取共享仓库 master。共享 PR #15 已合并，master SHA `1690a3acf310499ed4d4ead386c4f67f3042739b`；MR1 后续既有 checkout 将自动读取此 master。最近 M1 live scan Actions 仍失败且账户存在支出限制，本轮未 dispatch 工作流。实际历史 TG 更新数仍为 0，不能将本地渲染 PASS 说成已在线更新。
- 本轮仅展示名称数据/审计、curation scripts 和本 handoff；未改任何模型、策略、阈值、赛事范围、盘口来源、锁单、ledger、settlement 或通知规则。

## 2026-10-15 formal team-name curation and Telegram edit recheck (latest)
- Continued from the current shared `master` without repeating bulk identity recovery. Formal union snapshot after the change: 2,468 team IDs, 2,335 canonical Chinese names, 133 unresolved (94.61%). Per-model: M1 1,550/1,553 (99.81%; 3 unresolved); M1 OU-R1 52/52; MR1 AH 1,816/1,921 (94.53%; 105 unresolved); MR1 AI declared M1 mirror 1,550/1,553 (99.81%; observed confidence≥50 cohort 181/182, 99.45%). Complete unresolved identities and reason fields remain in shared `data/football_display_names/formal_scope_coverage.json`.
- Added exactly one verified Chinese display name: TotalCorner `team_id=13106`, `FK FAP` → `FAP普里霍`. Source: FootballAnt zh-CN team profile `https://www.footballant.com/zh-CN/football-data/team/67568`; identity cross-check includes provider team name and league ID 337 (`Serbia Prva Liga`). Mapping is scoped only to this ID. All remaining unverified identities were left unresolved; no guessed translations.
- Shared registry PR #13 merged as `c3319afae736601355c2a1c37e663a7714f82fe4` (source branch commit `f99196f0`). M1 display + history-repair tests passed 10/10; MR1 `node test.js` with the shared registry passed; JSON validation and `git diff --check` passed.
- Re-ran existing name-only repair workflows after the shared merge; none sends new Telegram messages or changes wager terms. M1/M1 OU-R1 run [38645567631](https://github.com/ljm198964-alt/quant-runner/actions/runs/38645567631) completed PASS: eligible 41, edited 0, already matching 41, original text missing 99, unmapped 97, failed 0. MR1 AH run [38645567493](https://github.com/ljm198964-alt/quant-runner/actions/runs/38645567493) completed PASS: 125 already processed, edited 0, unresolved 0, failed 0; status-only receipt persisted as `d402cd46a8`. MR1 AI first run [38645568619](https://github.com/ljm198964-alt/quant-runner/actions/runs/38645568619) edited 0 but receipt push lost a concurrent-ref race; serial rerun [38645832441](https://github.com/ljm198964-alt/quant-runner/actions/runs/38645832441) completed PASS and persisted `ee1df11f38`, with business result candidates 9, edited 0, unresolved 192, failed 9 (`400 message to edit not found`). No historical TG message was edited successfully in this pass; none was resent.
- No M1/M1 OU-R1/MR1 AH/MR1 AI strategy, scope, thresholds, provider, ledger, settlement or send rules changed. One shared display mapping only.

## 2026-10-15 unresolved 来源交叉核验补充
- 对共享 formal unresolved 中有 Wikidata entity bridge 的 43 个英文球队身份，使用 Reep 公共 `teams.csv` 精确规范化匹配；批量取回对应 43 个 Wikidata 实体，逐项检查 `zh`/`zh-cn`/`zh-hans`/`zh-hant` labels 及 `zhwiki` sitelink。结果：精确身份 bridge 43，中文标签 0，中文维基条目 0，因此本轮不能从该来源新增 canonical。候选身份 bridge 只能辅助后续找中文体育来源，不能被当成中文名称证据。
- 对 7M live search `liveq.aspx` 针对 Karcagi SE、FK FAP、FC Yerevan、KF Hajvalia、Pembroke Athleta 查询均返回空结果；这只是赛事实时搜索索引未覆盖的证据，不代表球队不存在。FootballAnt 的 Qena SC profile 页面仍显示英文名，简体中文 profile 请求返回 502，未据此建映射。
- 公开体彩队名映射 CSV 全表 24,888 条（11,197 条含中文队名）再次对剩余正式名称作 exact normalized join，0 命中。此前覆盖清单中 133 条仍为 `NO_VERIFIED_CANONICAL_ZH`；team_id 4931 已在共享 master `be1ac9e` 正确标记 `PROVIDER_IDENTITY_INVALID`。formal 2,334/2,468（94.57%）不变，未猜译、未修改策略。

## 2026-10-15 未匹配项数据质量分类更正
- 共享库已合并 PR #10，master commit `be1ac9e29e0db197bd97fc13684060c597ea7c14`。没有新增球队中文名称，正式覆盖率保持 2,334/2,468（94.57%）。
- 将 team_id `4931` 的 unresolved 原因从普通中文译名待确认改为 `PROVIDER_IDENTITY_INVALID`：存储的 provider_name 是字面值 `0`，需先修正上游球队身份；未猜名。formal coverage 与 curated batch report 均同步，134 项合计为 133 个 `NO_VERIFIED_CANONICAL_ZH`、1 个 `PROVIDER_IDENTITY_INVALID`。
- 用公开 体彩英文—中文队名映射表（24,888 行）再对全部 formal unresolved 做精确规范化匹配，命中 0；此前本轮 `lottery-football` 历史比分数据中英字段也命中 0。此类搜索结果不是“所有资料已穷尽”的证明；仍按证据边界保留 unresolved。
- 上轮三条 name-only Telegram 工作流已对最新名称映射运行：M1 run `38641413548` PASS（编辑0；41已匹配、99缺原文、97无映射）；MR1 AH `38641420542` PASS（125已处理、编辑0）；MR1 AI `38641427355` 工作流 PASS 但9条编辑均因 Telegram 找不到原 message ID 失败，192 unresolved。新 PR 只修正 coverage 原因，不改变 `display_names.json` 的 canonical 名称，因此不重复触发 Telegram 编辑。

## 2026-10-15 中文名称余项与正式 Telegram 复核（本轮）
- 从共享库最新 master `0284d3727ecb2cd140e0ecef83b9bbd0fd43b6e3` 接续。正式范围实际快照仍为 2,468 IDs、2,334 canonical、134 unresolved（94.57%）；M1 1,549/1,553（99.74%，4 未匹配），M1 OU-R1 52/52（100%），MR1 AH 1,815/1,921（94.48%，106 未匹配），MR1 AI 声明镜像 M1 1,549/1,553（99.74%，4 未匹配）；全共享库 12,276 team IDs、4,350 canonical。完整 134 项含 ID、provider name、league/system 上下文及原因，以唯一共享文件 `data/football_display_names/formal_scope_coverage.json#unresolved_records` 为准。
- 本轮没有重做历史身份恢复。将 unresolved 英文名与公开 `lottery-football` 历史赛果数据的英文/中文球队列作精确连接，0 个正式 ID 命中；对余项作定向中文来源搜索，没有获得可同时确认中文名称与具体球队身份的新增来源。Wikidata API 对请求返回 HTTP 429，故不据此声称已穷尽该来源。新增 canonical 数量为 0；没有用机器音译或模糊同名填库。`team_id 4931` 的 provider identity 字符串为 `0`，应优先修复上游身份标签，不应猜译。
- 四条正式通知链继续共用 `display_names.json`：M1 AH 与 M1 OU-R1 使用 M1 Python formatter；MR1 AH、MR1 AI formatter 通过 `external/football-display-registry` 读取该文件。M1 两项测试 9/9 PASS，MR1 shared-registry 与 V6 name-only repair 两项测试均 PASS；测试不代表尚未命中的 134 个名称已中文化。没有改模型/策略或 Telegram 格式。
- 本轮在 `quant-runner` 实际运行现有历史 name-only repair（不新发订单）：M1/M1 OU-R1 run [38641413548](https://github.com/ljm198964-alt/quant-runner/actions/runs/38641413548) PASS，报告 eligible 41、edited 0、already matching 41、缺发送原文 99、无映射 97、failed 0；MR1 AH run [38641420542](https://github.com/ljm198964-alt/quant-runner/actions/runs/38641420542) PASS，125 条均已处理/跳过，edited 0、unresolved 0、failed 0；MR1 AI run [38641427355](https://github.com/ljm198964-alt/quant-runner/actions/runs/38641427355) workflow PASS，但业务修复报告 total 201、candidate 9、edited 0、unresolved 192、failed 9；9 次编辑均收到 Telegram `400 Bad Request: message to edit not found`。历史消息实际编辑仍为 0；没有重发 TG，也没有改账本。
- 共享映射无需新提交：最新 BSK 映射已在 PR #9 merge `0284d372`。本次仅更新 Runner handoff，已推送提交 `ee62867` 到 `quant-runner/main`。未改 M1 AH、M1 OU-R1、MR1 AH、MR1 AI 模型/策略、赛事范围、阈值、盘口源、账本或结算。

更新日期：2026-10-15（北京时间）
性质：项目事实与工作进度快照。**不是新增策略规则或验收 Gate。** 每次引用成绩必须核对账本的 generated_at，不得把本文件历史快照冒充实时值。

## 用户已经明确的要求
- 正式实战 = 实际向 Telegram 发送的正式策略订单；测试消息、影子测试、研究回测均不得算实战。
- 盘口来源严格使用 Crown；不允许以其他公司盘口替代。
- M1 AH、M1 OU 旧线、M1 OU R1、MR1 AH、MR1 AI、对手分别统计，MR1 AH 与 MR1 AI **绝非同一模型**。
- 用户目标：M1 OU R1 **完全恢复**自动扫描、真实 TG 派单、正式账本回写和后续结算；不接受仅代码修复或 TG 测试成功就宣布恢复。
- 新工作优先公开仓库；用户此前要求停止使用私有运行链路并最终移除不再需要的私有仓库。当前运行链路仍依赖私有仓库，属于尚未解决的工程遗留问题，不得误报已经迁移。
- 不得擅自新增数量门槛、Gate、策略参数、测试/发布阻塞条件。未确认的建议不得当作已冻结规则。

## 2026-10-15 正式范围中文库续补（十一）
- 从共享库最新 master `4d67fd5531d7d55384b60226951329abd327043a` 接续，没有覆盖已有 canonical。当前待合并批次为 3 个有成熟中文资料对应的正式 team ID：Leevon PPK（144651）→ 沙尔杜斯利维诺（7M 简体中文球队页，拉脱维亚足协身份交叉核对）；Aragvi Dusheti（46813）→ 阿拉吉夫杜塞提（7M 简体中文球队页）；FC Besa Peja（150935）→ 贝萨佩贾（FootballAnt 简体/英文同一 profile ID 对照）。同一映射写入唯一共享文件 `data/football_display_names/display_names.json`，脚本/批次来源审计随变更提交。
- 更新后文件实算：formal union 2,468，canonical 2,327，未匹配 141（94.29%）；M1 1,542/1,553（99.29%）；M1 OU-R1 52/52（100%）；MR1 AH 1,808/1,921（94.12%）；MR1 AI 声明镜像 1,542/1,553（99.29%）；MR1 AI observed confidence≥50 为 181/182（99.45%）。共享库 12,276 team IDs，4,343 canonical；完整 141 条及各项原因见共享 `formal_scope_coverage.json` 的 `unresolved_records`。
- 搜索 7M、Sofascore、FootballAnt 等资料后，对剩余低级别俱乐部仅在中文名可与同一球队身份对应时入库；搜索结果仅有英文、仅有其他语种或存在同名身份冲突的仍保留 unresolved，不用临时音译补数。当前 141 项多属埃及低级别、科索沃/东欧/威尔士/波罗的海地区俱乐部；`CS Stefanesti`、`El Hammam`、`Vllaznia/Vllazina` 等存在身份歧义的不得互相借名。
- 验证：共享 curator 幂等重跑 `added=0`；`git diff --check` 通过；M1 Telegram display + history-repair 测试 8/8；MR1 完整 `npm test` 通过。使用新增真实 team ID 做 M1 formatter 隔离渲染及 MR1 AI formatter 实际渲染，显示方向、主客队中文正确；`Georgia First League` 的 league_id 702 本身仍无可靠中文资料，未硬译，故该示例赛事名仍回退英文。
- 共享变更已由 PR #6 合并，master merge commit `7599cb21cabf28fb72d912f977f31044c96413f2`。合并后运行现有历史名称修复工作流：M1 run `38634559249` 成功，eligible 41、edited 0、already matching 41、跳过缺原始文本 99、跳过未映射 97、failed 0；MR1 AH run `38634568096` 成功，already processed 125、edited 0、unresolved 0、failed 0；MR1 AI run `38634575356` 成功结束，但 candidates 9、edited 0、failed 9（Telegram `400 Bad Request: message to edit not found`），unresolved 192。三条工作流都不重发消息；没有历史消息被编辑成功，本轮实际编辑数为 0。AI 失败项所指 Telegram 消息已无法通过当前 bot/chat 的 message ID 定位，不能宣称修复。
- Runner 交接更新提交 `bffb047` 已推送至 `quant-runner/main`。本轮未修改 M1、M1 OU-R1、MR1 AH、MR1 AI 的模型、策略、盘口、范围、阈值、账本、结算或正式发送条件；未运行生产预测/派单。

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

## 2026-10-12 正式范围中文名称续补（七十四）
- 共享名称库新增 TotalCorner team_id 4221（provider `San Jose`）→圣何塞地震。正式范围记录归属 MLS（league_id 85）；Sofascore 简中球队档案将 San Jose Earthquakes 称为“圣何塞地震”，7M 中文档案以“圣荷西地震”对应同一球队。采用简体主流名称并把繁体名/完整英文名保留为 alias；未改变 provider identity、ID 或球队实体。
- 当前正式范围 union 2,468：canonical 1,985、unresolved 483（80.43%）；M1 1,542/1,576（97.84%）；M1 OU-R1 52/52；MR1 AH 1,517/1,921（78.97%）；MR1 AI declared mirror 1,542/1,576（97.84%）。共享 registry 总计 12,276 个 team ID、4,001 个 canonical 中文名；完整 unresolved 清单与逐项原因见共享 `formal_scope_coverage.json`。
- 本轮 M1 display/runtime pytest 20/20、MR1 shared-registry 与 AI formatter/parser 定向测试 8/8 通过。映射来源：[Sofascore 简中 San Jose Earthquakes 档案](https://www.sofascore.com/zh/football/team/san-jose-earthquakes/21825)；[7M 圣荷西地震档案](https://team.7m.com.cn/133/index.shtml)。
- 此项映射已提交共享库后，需复跑既有 M1、MR1 AH、MR1 AI 历史消息名称修复工作流并记录真实回执。不得重发历史 Pick；不修改 M1/MR1 策略、模型、正式账本或结算。

## 2026-10-12 正式范围中文名称续补与 Telegram 实际复核（七十五）
- 在唯一共享 registry 中再新增 2 个有中文赛事实录配对的正式 ID：Caerau Ely（919）→凯劳埃利、AFA Olaine（2220）→AFA奥莱内；共享提交 `94ad6d822b6b4c2d861388bd385f0f95afd9e9a3`。此前 San Jose 映射提交 `8a9be4f2a83f643e06d23685e494b7eb6a59b531`，之后再提交此批，均保留原英文 provider identity、ID、aliases 和来源。
- 最新正式范围 union 2,468：canonical 1,987、unresolved 481（80.51%）；M1 1,544/1,576（97.97%）；M1 OU-R1 52/52（100%）；MR1 AH 1,519/1,921（79.07%）；MR1 AI declared mirror 1,544/1,576（97.97%）。全共享库 12,276 team IDs、4,003 canonical 中文名。逐项未匹配和原因保存在共享 `data/football_display_names/formal_scope_coverage.json`，没有猜译。
- 对最终共享库版本完成本地验证：M1 display/runtime pytest 20/20；MR1 registry、browser-forward、AI formatter/parser 定向 Node 测试 8/8。
- 最新版历史 Telegram 只编辑校正工作流均 success：M1 run `38213593018`（报告 eligible 37、edited 0、already matching 37、缺历史原文 99、无映射 70、failed 0；覆盖 M1 AH 和 M1 OU-R1）；MR1 AH run `38213597764`（edited 0、skipped 125、unresolved 0、failed 0）；MR1 AI run `38213602140`（201 条中 9 个可评估候选、edited 0、192 unresolved、9 failed，Telegram 对 9 条均返回 `400 message to edit not found`）。因此本轮历史消息实际编辑数为 0；不存在可安全编辑的目标文本，不以重发代替，失败项和缺数据项如实保留。
- 三个工作流均仅针对原消息做名称校正并保存各自回执；没有发送新 Pick、触发策略扫描或改比赛/盘口/方向/水位，也未修改模型、策略、正式账本、settlement 或 MR1 AI 发送规则。后续继续只对剩余 481 个 formal-scope unresolved ID 寻找来源可核验的 canonical 中文名。

## 2026-10-12 正式范围中文名称续补与 Telegram 实际复核（七十六）
- 再补入唯一共享库 2 个正式 ID：Lija Athletic（3348）→丽加竞技、Slavija Sarajevo（4131）→萨拉热窝斯拉维亚队；均由 Tips.GG 中文赛事实录直接以英文队名和中文名配对，保留精确 provider identity/ID、aliases、reference。共享最新提交 `e05f9e3b4a6cdcce5634cabc134f3156a940d5a6`。
- 当前 formal union 2,468：canonical 1,989、unresolved 479（80.59%）；M1 1,544/1,576（97.97%）；M1 OU-R1 52/52（100%）；MR1 AH 1,519/1,921（79.07%）；MR1 AI declared mirror 1,544/1,576（97.97%）。共享全库 12,276 team IDs，4,005 canonical 中文名。尚未确认条目和原因完整列于共享 `formal_scope_coverage.json`。
- 本地定向测试通过：M1 pytest 20/20；MR1 canonical registry、browser-forward 和 Telegram formatter/parser Node 测试 8/8。
- 本版共享 registry 的三个既有历史消息名称修复 workflow 均成功：M1 `38213931932`（eligible 37 / edited 0 / already matching 37 / missing original text 99 / unmapped 70 / failed 0）；MR1 AH `38213936620`（edited 0 / already processed 125 / unresolved 0 / failed 0）；MR1 AI `38213940539`（201 条中 9 candidates、edited 0、192 unresolved、9 failed，Telegram 原消息均返回 400 `message to edit not found`）。即本轮实际编辑仍为 0，不重发历史单。
- 未更改比赛信息、盘口、方向、水位、模型、策略、正式 ledger、结算或 Telegram 发送规则；继续逐批按可核验来源处理余下 479 项。

## 2026-10-12 正式范围中文名称续补与 Telegram 实际复核（七十七）
- 共享 registry 在上述版本后又新增 4 个准确 ID 映射：AZAL PFC Baku（4172）→巴库奥林匹克；FK Indjija（9250）→因吉亚；Okzhetpes Kokshetau（9804）→奥肯咸特普斯；OLS（3960）→奥卢OLS足球俱乐部。来源为对应中文俱乐部资料页：[Newton AZAL 中文档案](https://www.newton.com.tw/wiki/巴庫奧林匹克足球俱樂部/19738010)、[百度百科因吉亚俱乐部页](https://bkso.baidu.com/item/因吉亚足球俱乐部/9613553)、[7M 奥肯咸特普斯页](https://team.7m.com.cn/5020/index_gb.shtml)、[Tips.GG OLS Oulu 中文页](https://tips.gg/cn/team/ols-oulu-football/)。共享最新提交 `9140391293fe401d5ba0e141555ee61b7ccd4aec`。原始 provider 名称、ID、aliases 均保留；未把相似队伍合并。
- 当前正式范围 union 2,468：canonical 1,993、unresolved 475（80.75%）；M1 1,546/1,576（98.10%）；M1 OU-R1 52/52（100%）；MR1 AH 1,520/1,921（79.13%）；MR1 AI declared mirror 1,546/1,576（98.10%）。共享全库 12,276 team IDs、4,009 canonical 中文名。剩余逐队 ID、英文名、system、league IDs 和 reason 均在共享 `data/football_display_names/formal_scope_coverage.json`，当前 475 条 reason 均为 `NO_VERIFIED_CANONICAL_ZH`，未编造译名。
- 本版定向测试：M1 pytest 20/20；MR1 shared registry/browser-forward/formatter/parser Node tests 8/8。
- 对此版本运行既有历史 TG 名称编辑流程并全部成功：M1 `38214736179`（eligible 37、edited 0、already matching 37、缺原文 99、unmapped 70、failed 0）；MR1 AH `38214740925`（edited 0、processed 125、unresolved 0、failed 0）；MR1 AI `38214745642`（201 条中 9 candidates、edited 0、192 unresolved、9 failed，Telegram 均报 400 `message to edit not found`）。因此没有历史消息实际改字成功，也没有重发。运行只检查/编辑既有消息，不派发信号或策略扫描。
- 继续复用同一 registry 的 M1 AH、M1 OU-R1、MR1 AH、MR1 AI 展示层；未修改模型、策略、盘口条件、交易字段、账本、settlement 或 Telegram 发送规则。余下 475 项仍需按来源逐项补齐。

## 2026-10-12 正式范围中文名称续补（七十八）
- 共享 registry 已推送到 `totalcorner-research-bridge/master`，提交 `0eae45e2b55678ea7636fd18facca1d625fbdd82`。本轮为 20 个未映射正式 team ID 添加有中文公开来源的名称：Kremin（4426）克雷明、HB Torshavn（13484）托尔斯港、Spartak Pleven（14806）普列文斯巴达、Al-Jabalain（39314）查巴莱、IF Vestri（30761）韦斯特里、Shaanxi Athletic（40143）陕西长安竞技、SalPa（11689）莎埃帕、Ballymena（41377）巴利米纳联、Rudar Velenje（42157）韦莱涅鲁达、FC Minai（49142）米奈足球俱乐部、Smiltene（14544）斯米尔特内、Vllaznia（42913）维拉斯尼亚、Pogon Grodzisk Mazowiecki（10464）波贡马佐维克、Puchov（32395）MSK贝塞夫、Trepca 89（39890）查比卡89、Septemvri Sofia（41502）索菲亚塞普泰姆夫里、Al Jubail（43725）朱拜勒、Samgurali（42019）萨古拉利、Sileks（32900）施历斯、Bylis Ballsh（43721）拜利斯。来源及 provider identity/aliases 逐条保存在唯一 `display_names.json`。
- 最新实算 formal union 2,468：canonical 2,013、unresolved 455（81.56%）；M1 1,570/1,576（99.62%）；M1 OU-R1 52/52（100%）；MR1 AH 1,538/1,921（80.06%）；MR1 AI declared mirror 1,570/1,576（99.62%）。全共享库 12,276 个 team ID，4,029 个 canonical 中文名；remaining unresolved 全量在 `formal_scope_coverage.json`，未以无来源翻译填充。
- M1 runtime/display 18 tests 通过；MR1 shared display/browser-forward/formal notifier/AI formatter 7 tests 通过。没有更改任何策略、模型、赛事范围、订单、结算、TG 发送规则。
- 新版名称库的既有历史消息名称编辑工作流实际结果：M1 run `38216991349` success（eligible 37、edited 0、already matching 37、缺原文 99、未映射 70、failed 0）；MR1 AH `38216995917` success（edited 0、processed/skipped 125、unresolved 0、failed 0）；MR1 AI 第一次 `38217000632` 的名称编辑步骤执行完成，但与 MR1 AH 并发推送回执时发生 branch ref race，随后串行重跑 `38217285572` success 并已持久化。AI 最终仍是 total 201、9 candidates、edited 0、unresolved 192、failed 9；9 条均为 Telegram 400 `message to edit not found`。历史 TG 实际改字 0；没有重发消息。
- 后续从剩余 455 项继续逐项查可核验中文来源；未确认名称保持英文 provider identity 和 `NO_VERIFIED_CANONICAL_ZH` 状态。
- 来源审计补正：复核发现 Samgurali（42019）的首次引用是 7M 赛程页而非该队中文名称页；后改为中文维基球队条目（该条目/中文联赛资料使用“萨古拉利”），只更正 source reference/kind/evidence_note 和 verified_at，不变更 canonical/identity。更正提交 `dd2b599`，formal-scope 统计不变。已知来源分布在更正后：中文维基 8、7M 6、雷速 2，另中国足协、球探天下、Wikidata、球迷屋各 1。

## 2026-10-12 正式范围中文名称续补（七十九）
- 共享唯一 registry 提交 `22ff011` 已推送至 `totalcorner-research-bridge/master`。新增两条有身份交叉证据的 formal team ID：MOIK Baku（4762，league_id 227）→MOIK巴古，来源 Titan007 中英球队页；PFK Turan Tovuz（4797，league_id 299）→图兰，来源 Tips.GG 中文球队/对阵页。原 provider 名、team ID、联赛归属保留；图兰 B 队没有合并进一线队。来源引用及审计说明写入 `display_names.json`。
- 最新实算正式范围 union 2,468：canonical 2,015、unresolved 453（81.65%）；M1 1,572/1,576（99.75%）；M1 OU-R1 52/52（100%）；MR1 AH 1,540/1,921（80.17%）；MR1 AI declared mirror 1,572/1,576（99.75%）。共享库 12,276 team IDs、4,031 个 canonical 中文名。完整未匹配逐条清单及原因仍以共享 `formal_scope_coverage.json` 为准。
- M1 Telegram display/repair 本地测试 8/8 通过。当前工作树既存 `.gitignore`、`package-lock.json`、`__pycache__`、`results/competitor_zou/` 变更未纳入共享库提交。
- 只读 MR1 共享库烟测 run `38218108249` 已派发但 GitHub 在 5 秒内以 failure 结束，job steps 为空且 `--log-failed` 无日志；因此云端读取验证未执行。相同测试本机将 `FOOTBALL_DISPLAY_REGISTRY_DIR` 指向共享库运行，2/2 通过。历史 TG repair workflow 本轮未触发：仓库 API 当前工作流清单未列出此前使用的 repair workflow；不宣称有生产运行或历史消息编辑。最近有记录的历史编辑结果仍为 0；未来消息是否已镜像最新共享提交需另行验证实际 runtime 部署。
- 未改模型/策略、赛事范围、盘口、订单账本、结算或 Telegram 发送规则；缺少可靠来源的名称继续保留 unresolved。

## 2026-10-12 正式范围中文名称续补（八十）
- 继续从最新 452 个 unresolved 中找到 7M 可核验球队档案，新增 Olympic El Qanal（team_id 7113，league_id 417）→阿尔卡纳；7M 中文队页标题直接标注“阿尔卡纳(Olympic Al Qanah)”。共享库提交 `179a8c7` 已推送 master；英文 provider identity、ID、赛事归属和别名均保留，未触碰已有不同 ID 映射。
- 当前实算 formal union 2,468：canonical 2,016、unresolved 452（81.69%）；M1 1,573/1,576（99.81%）；M1 OU-R1 52/52；MR1 AH 1,541/1,921（80.22%）；MR1 AI declared mirror 1,573/1,576（99.81%）。共享库 12,276 IDs、4,032 canonical names。
- M1 display/repair unittest 8/8 通过。7M 来源：[阿尔卡纳（Olympic Al Qanah）球队档案](https://team.7m.com.cn/7510/index_gb.shtml)。MR1 云端只读 registry smoke 上轮 run `38218108249` 在 0 个 job steps 后失败；本轮未重复派发。历史 Telegram repair workflows 仍不在当前 workflow 清单，未编辑或重发任何消息。
- 未修改生产模型、策略、账本、结算、Telegram 内容/规则；未有可靠来源的球队保留 unresolved。

## 2026-10-12 正式范围中文名称续补（八十一）
- 新增两条 Khazar Lankaran/Lenkoran 拼写记录，分别保留 TotalCorner team_id 4307（M1，league_id 299，provider `Khazar Lenkoran`）与 5990（M1，league_id 299，provider `Khazar Lankaran`），canonical 均为“哈扎尔连科兰”；没有跨 ID 合并，只按各自原 identity 记录。中文历史赛程由澳客及新浪赛事页将俱乐部名用于阿塞拜疆赛事实录。共享提交 `96712ab` 已推送 master。
- 最新实算 formal union 2,468：canonical 2,018、unresolved 450（81.77%）；M1 1,575/1,576（99.94%）；M1 OU-R1 52/52；MR1 AH 1,541/1,921（80.22%）；MR1 AI declared mirror 1,575/1,576（99.94%）。共享 registry 12,276 IDs、4,034 canonical names。
- M1 display/repair unittest 8/8 通过。来源：[澳客阿塞超赛程与哈扎尔连科兰中文记录](https://www.okooo.com/soccer/league/709/schedule/11033/)、[新浪球队对阵历史中的哈扎尔连科兰](https://match.sports.sina.com.cn/football/team_vs.php?id=1887825)。未修改任何生产模型、策略、ledger、settlement 或 Telegram 发送规则。

## 2026-10-12 正式范围中文名称续补（八十二）
- 复用经验证的既有 Misr Lel Makasa 中文名称，为正式 ID 17050（provider `Misr El Maqasha`，league_id 417，M1/MR1）新增 canonical“艾玛卡沙”；英文写法关系由 Wikidata 与埃及联赛历史记录交叉确认，中文 canonical 来自已有 FootyStats 简中俱乐部页/共享库 team_id 3466。独立保留 ID 17050，不覆盖或合并原记录。共享提交 `c0d1e24` 已推送 master。
- 当前实算 formal union 2,468：canonical 2,019、unresolved 449（81.81%）；M1 1,576/1,576（100%）；M1 OU-R1 52/52；MR1 AH 1,542/1,921（80.27%）；MR1 AI declared mirror 1,576/1,576（100%）。共享库 12,276 IDs、4,035 canonical names。
- M1 display/repair unittest 8/8 通过。来源：[现有 FootyStats 中文球队页](https://footystats.org/cn/clubs/misr-lel-makasa-1120)、[Wikidata Misr Lel Makkasa 实体](https://www.wikidata.org/wiki/Q3049707)、[埃及联赛历史表中两种拼写](https://en.wikipedia.org/wiki/2010%E2%80%9311_Egyptian_Premier_League)。没有修改任何策略、账本、结算或通知规则。

## 2026-10-12 用户明确要求 MR1 AH / MR1 AI 停止正式 Telegram 派单，改为影子跟踪
- 用户最新决定：所有带【MR1】和【MR1 AI】签名的**新正式策略通知**暂停发送 Telegram；两条模型继续运行研究/影子记录和模拟成绩。M1 AH、M1 OU R1 不受影响。
- MR1 AH：公开 Runner `mr1-free-runtime.yml` 移除 `Deliver MR1 V6 AH formal signals` 步骤，提交 `03b6b327c7f15434af0ae5a9c627c4c768544f66`。采集、V6 forward、既有正式订单结算及持久化保留。新的 AH 研究评估仍由 forward 记录；不能把未发 TG 的信号算成正式成绩。
- MR1 AI：`mr1-shadow/src/v7-ai-picks-telegram.js` 改为新合格信号写 `data/mr1-ai-shadow/signals/<id>.json` 而不调用 TG 发送，提交 `96d4e23b045e9076ee412de6143eca7e223cf778`；`persist-mr1-ai-state.js` 纳入独立影子目录，提交 `ac0723fd7e0947181a38a30df0ddd1153a11d798`。不写正式 `telegram-ah-sent.jsonl`，已有正式 TG 订单继续独立结算。
- **验证状态**：代码已提交；尚未取得新生产运行成功回执；MR1 AI 影子订单后续实际赛果结算尚未完成实现与核实。不得把仅保存影子候选冒充影子已结算成绩。
- 后续检查其他潜在 MR1 / MR1 AI TG 发送入口及并行调度；验证真实运行不再发送新 TG，影子记录能持续生成和结算。不要擅自恢复正式 TG。

## 2026-10-12 正式范围中文名称续补（八十三）
- 共享 registry 新增 3 个经中文来源与 provider identity 核对的正式队名：Banha（team_id 6273）→班哈、Ingulets Petrovo（31952）→因古列茨、Nesebar（30104）→PFC尼塞巴尔。来源分别为 Tips.GG 中文队名/比赛页；各原 team_id、provider_name 和 league_ids 保留，未合并球队。共享库提交 `6f42e5cbf3381fd63afdf37af3b09d82495b5154` 已推送 `totalcorner-research-bridge/master`。
- formal union 仍为 2,468 IDs；canonical 2,023、unresolved 445（81.97%）。共享库 12,276 IDs、4,039 canonical。M1 基础正式范围统计经现行 `m1_runtime_policy.scope_status` 重建为 1,556 IDs，其中 1,432 canonical、124 unresolved（92.03%）；当前扫描摘要的 176 个 ID 未带 ID 明细，单独维持 175/176，未擅自合并。脚本现不再按泛化 `systems` 标签累加 M1，避免产生超过 100% 的错误值。MR1 AH 沿用既有正式范围快照口径，未伪称完成重算。
- M1 display/repair unittest 8/8 通过；`git diff --check` 通过。只改 shared display registry、coverage/batch report 和中文映射整理脚本；无模型、策略、账本、结算或 Telegram 发送逻辑变更。本轮尚未运行云端历史 TG 编辑 workflow，故不报告历史消息实际修改结果。

## 2026-10-12 正式范围中文名称续补（八十四）
- 新增 7M 可核验记录 Tartu JK Welco（team_id 29760）→塔尔图维尔克；7M 球队页将繁体“塔圖維爾克”与英文原名并列，canonical 使用简体展示，英文和繁体保留为 alias。共享提交 `50d523982582c8409846b71b7e26bbb3a7c6b346` 已推送 master。
- 当前 union 2,468：canonical 2,024、unresolved 444（82.01%）；共享库 12,276 IDs、4,040 canonical。M1 可审计基础范围 1,556 中 1,432 已映射（92.03%）；另有当前 M1 scan 聚合 175/176，因缺 team ID 清单暂不并入。M1 OU-R1 仍 52/52。MR1 AH 既有正式范围总集 1,921，按本轮新增且经赛事范围交叉验证的 4 个 ID 更新为 1,547 canonical、374 unresolved（80.53%）；总集本身仍沿用原正式范围快照口径。
- M1 display/repair unittest 8/8 通过；本轮仍未运行云端历史 Telegram 编辑流程，未编辑或重发历史消息。未改任何模型、策略、订单、结算或通知逻辑。
- 覆盖统计修正另推共享提交 `790cf57cbcc81dba9fad60a7247d83a1e6d07cba`；M1 统计已从历史累计误值改为 runtime policy 下可审计的身份/正式账本基础范围，当前扫描 176 个 ID 仍独立展示，避免把缺失 ID 明细的扫描摘要并入造成虚假精确度。

## 2026-10-12 正式范围中文名称续补（八十五）
- 再新增两条经 Tips.GG 中文埃及足球赛事实录核对的队名：Dekernes（team_id 10774）→德克恩斯；Al Nasr Taaden（team_id 8692，来源页面采用拼写 Nasr Taadeen）→拿斯尔塔丁。仅增加来源别名，不更改 provider identity/ID/联赛。共享提交 `f7bd59a1e0736be4879be02fb214909e7be211c6` 已推送 master。
- formal union 2,468：canonical 2,026、unresolved 442（82.09%）；共享全库 12,276 IDs、4,042 canonical。M1 可审计基础范围 1,556 中 1,432 mapped（92.03%），独立当前 scan 175/176；MR1 AH 1,549/1,921（80.64%）；M1 OU-R1 52/52。
- M1 display/repair unittest 8/8 通过。MR1 AI Telegram formatter 与 AI-pick parser tests 5/5 通过，且指定共享库路径隔离渲染新补名称成功。未运行正式发送或历史消息编辑；未更改模型、策略、账本、结算和通知规则。

## 2026-10-12 正式范围中文名称续补（八十六）
- Tips.GG 北爱尔兰足球中文赛事实录明确显示 Knockbreda＝诺克布雷达；为正式 team_id 5168 写入该 canonical 及来源证据，保留原始 provider name。共享提交 `b1d7a92aaf01e113690741dad8e03f5ce377cf63` 已推送 master。
- union 2,468：canonical 2,027、unresolved 441（82.13%）；M1 可审计基础范围 1,432/1,556（92.03%），独立当期 scan 175/176；MR1 AH 1,550/1,921（80.69%）；M1 OU-R1 52/52。共享全库 12,276 IDs、4,043 canonical。
- M1 display/repair tests 8/8 通过；没有启动/编辑/重发 Telegram 历史消息。本次只改展示名称记录和 coverage/curation 数据，不改模型与交易运行链。

## 2026-10-12 正式范围中文名称续补（八十七）
- 7M 中文球队档案以“FC列日 (RFC Liege)”并列标注俱乐部名。已为 TotalCorner team_id 13878 添加 canonical“FC列日”、来源与别名，未更改原始名称或 ID。共享提交 `8a8a5f394ec0c212dc1af127842d8da328d45c12` 已推送 master。
- formal union 2,468：canonical 2,028、unresolved 440（82.17%）；共享库 12,276 IDs、4,044 canonical；M1 可审计基础范围 1,432/1,556（92.03%），当期 scan 175/176；MR1 AH 1,551/1,921（80.74%）；M1 OU-R1 52/52。
- M1 display/repair tests 8/8 通过。该提交只更新名称数据/整理脚本与统计，无策略或模型变化；历史消息编辑仍未实际执行。

## 2026-10-12 正式范围中文名称续补（八十八）
- 7M 中文球队页将 Veres Rivne 对应为“维勒斯”；为现有 TotalCorner ID 33592（provider `Veres`）补入 canonical 及来源，保留原始身份。共享提交 `4d52f68d7124c8a82e2953fa67051736e0ce57b4` 已推送 master。
- 当前 formal union 2,468：canonical 2,029、unresolved 439（82.21%）；共享库 12,276 IDs、4,045 canonical。M1 可审计范围 1,431/1,553（92.14%），current scan 单独为 175/176；MR1 AH 快照 1,551/1,921（80.74%）；OU-R1 52/52。
- M1 display/repair tests 8/8 通过。没有发送或编辑 TG 消息；模型/策略、正式账本和结算均未改。

## 2026-10-12 正式范围中文名称续补（八十九）
- 为 TotalCorner MLS team_id 33406（provider `New England`）新增 canonical“新英格兰革命”；以中文维基俱乐部条目核验常用名称，league_id 85 消除与新英格兰革命B队的歧义，B队未合并。共享提交 `da9c43de72751ae0597f43eef416d261ba0326bb` 已推送 master。
- 同步把 M1 基础覆盖重算纳入队名层 hard-exclusion（如 University/reserve/youth），避免只按联赛计入被政策排除的球队。当前 M1 可审计基础范围 1,432/1,553（92.21%）；独立 scan 175/176。正式 union 2,468：2,030 canonical、438 unresolved（82.25%）；MR1 AH 1,552/1,921（80.79%）；M1 OU-R1 52/52；共享库 12,276 IDs、4,046 canonical。
- M1 display/repair tests 8/8 通过。未发送或编辑 TG 消息，未改模型/策略/账本/结算。

## 2026-10-12 正式范围中文名称续补（九十）
- 按用户最新任务继续使用唯一 `display_names.json`；没有历史身份全量重扫。本轮增加 20 个来源核验 team ID：Shkendija 79 Tetovo、Kampaniakos Chalastras、Dundela、Senglea Athletic、Vittoriosa Stars、Zejtun Corinthians、St Andrews（马耳他）、Swieqi Utd、Port Fouad、Tamiya Youth Center、Al Marekh、Egypt Insurance、Talayie Alaistul、M S Koum Hamada、Telephonaat Bani Suweif、Makadi FC、Harras Al Hodoud、Markaz Shabab Koom Hamada、Maleyat Kafr El Zayat、Gomhoryet Shebin。保留 provider identity、team_id 和别名；青年队身份未与成年队合并。部分同队异写仅复用已有 canonical，team ID 未合并。
- 共享库已推送提交 `805253dd9f54ed70341947f01e7bc1ccabb6cd3d`。最新正式 union 2,468：canonical 2,050、unresolved 418（83.06%）。M1 1,436/1,553（92.47%）；M1 OU-R1 52/52（100%）；MR1 AH 1,569/1,921（81.68%）；MR1 AI 声明镜像 M1 为 1,436/1,553（92.47%），已存 prospective pool 1,718/1,857（92.57%）。最新 M1 scan pool 175/176（99.43%）；MR1 AH prospective fixture pool 1,529/1,934 slots（79.06%，含 IDless alias 解析）。完整 418 项及逐项 `NO_VERIFIED_CANONICAL_ZH` 原因保存在共享 `data/football_display_names/formal_scope_coverage.json`，不得以猜译补齐。
- M1 formatter 与历史修复 dry-run 使用唯一 registry；MR1 AH 和 MR1 AI runtime 均从同一共享 registry 加载。M1 display/repair unittest 8/8 通过；MR1 registry、AI formatter/parser 与交付定向 Node tests 7/7 通过。覆盖统计从提交数据重算，无模型策略、范围、盘口、订单、结算或通知规则修改。
- 另单独运行 MR1 AH 的旧消息修复单测 1/1 通过；`test-v6-ah-formal.js` 的 synthetic integration case 仍失败在其 fixture：它给已知 `league_id=1` 配 `Test League` override，却断言 override 必须覆盖 provider ID；当前 resolver 对已知 ID 以 canonical registry 为准，不采用该 override。此为测试夹具/预期冲突，本轮未改 MR1 显示或策略代码。真实共享 registry 直读 fixture（有 canonical league/team IDs）输出中文。
- 最新历史 Telegram dry-run：37 条可作名称替换候选、99 条缺 ledger 原文、70 条仍无映射；dry-run 本身未编辑。按用户授权触发既有 `m1-tg-history-name-repair.yml`，run `38223169902` success；artifact 实证 `eligible=37, edited=0, already_matching=37, skipped_missing_original_text=99, skipped_unmapped=70, failed=0`。因此本轮历史 M1 TG 实际编辑 0 条，37 条已是当前中文，不重发。
- 同一批新 registry 发布后，MR1 AH 修复 run `38223585697` success：edited 0、skipped/already processed 125、unresolved 0、failed 0；回执提交 `3c2d586da12c245f2a5379eea582cd4756620b23`。MR1 AI 修复 run `38223686575` success：历史总计 201，9 条候选、edited 0、192 unresolved、9 failed（Telegram 400 `message to edit not found`）；回执提交 `463d2224186e04f0a5042a835eead8d902e5c6b1`。没有重发历史 Pick。
- 本机没有 M1/MR1 Telegram 环境变量；不得读取或复用另一系统凭据。代码路径通过隔离测试，但在该次云端历史修复 workflow 完成之前，不能宣称历史 TG 中文修复成功。
- GitHub Actions 的 M1/MR1 AH/MR1 AI 历史名称修复 workflow 均完成，无需新增 workflow；没有触发正式 scan、发送测试消息或生产 Pick。运行链接：M1 https://github.com/ljm198964-alt/quant-runner/actions/runs/38223169902 ，MR1 AH https://github.com/ljm198964-alt/quant-runner/actions/runs/38223585697 ，MR1 AI https://github.com/ljm198964-alt/quant-runner/actions/runs/38223686575 。

## 2026-10-12 正式范围中文名称续补（九十一）
- 在 `805253d` 后继续检查唯一共享库及 418 项 unresolved。基于同库已验证别名、比赛联赛归属和中文来源，新增 6 个正式 ID：Bur Fouad（92834）→福阿德港SC；FK Sujeska（35609）→苏捷斯卡；PAS Gianena（43047）→吉安尼纳；FC Zorya（52914）→佐尔娅；FK Fushe Kosova（95879）→科索沃波列；Instituto Córdoba（175622）→科尔多瓦学院。均保留独立 team_id/provider_name，不合并实体；相关 exact crosswalk 与证据说明写入 shared registry 和现有批量 curator。未采纳同名但联赛/身份不一致的 fuzzy 建议。
- 共享库提交 `c82a146` 和 `a0d2a79` 已推送 master。最新 formal union 2,468：canonical 2,056、unresolved 412（83.31%）；M1 1,441/1,553（92.79%）；M1 OU-R1 52/52（100%）；MR1 AH 1,572/1,921（81.83%）；MR1 AI declared mirror 1,441/1,553（92.79%）。全共享库 12,276 IDs、4,072 canonical 中文名。最新完整 unresolved 清单和逐项 `NO_VERIFIED_CANONICAL_ZH` 原因以 `data/football_display_names/formal_scope_coverage.json` 为准。
- M1 Telegram display/repair tests 8/8 pass；`git diff --check` pass。此次没有重跑历史 TG 编辑、不发送消息、不触碰正式 ledger/策略/模型/结算。非策略用户文件 `.gitignore`、`package-lock.json`、`__pycache__/`、`results/competitor_zou/` 未纳入提交。
- 调查发现 WDQS 对此客户端触发 429（每分钟限额），没有用其不完整结果回填；一个精确 same-league canonical-alias 反查得到 Bur Fouad 映射，另 4 条可交叉核验的 spelling/duplicate ID 映射来自保留证据。剩余 412 个仍需继续查证；不做机械音译或猜名。

## 2026-10-12 正式范围中文名称续补（九十二）
- 在共享库提交 `a0d2a79` 后，本轮从中文公开球队页/官方记录继续确认 6 个 ID：Liaoning Ironman（143671）→辽宁铁人；Dingnan Ganilan FC（161724）→定南赣联；SJK Akatemia（79459）→SJK学院；Kispest Honved（185126）→布达佩斯洪韦德；NK Posusje（54098）→波苏谢；Szeged-Csanad Grosics（69648）→塞格德农学院。保留 provider name、team_id、别名和来源；SJK Academy 身份单独保留。搜索发现 FK Zhenys 女队中文名，不与男子 FK Zhenys 混用；FC Elimai Semey 本轮无足够中文来源，仍未匹配。
- 共享库提交 `482ecb2` 与 `6bfee8c` 已推送 master。当前 formal union 2,468：canonical 2,062、unresolved 406（83.55%）；M1 1,443/1,553（92.92%）；M1 OU-R1 52/52；MR1 AH 1,578/1,921（82.14%）；MR1 AI declared mirror M1 1,443/1,553（92.92%）。完整剩余清单及未确认原因以共享 `formal_scope_coverage.json` 为准。
- M1 display/repair tests 8/8 pass，`git diff --check` pass。仅改唯一共享 display registry、curation/audit data 和 curator；无 TG 发送/编辑、无策略、模型、正式 ledger 或结算改动。未加入到本地本任务仓库的其他工作树变更保持原样。

## 2026-10-12 正式范围中文名称续补（九十三）
- 在共享库 `5e07067` 基础上新增 4 个经过公开简体中文足球资料交叉核实的正式 team ID：FK Pobeda Junior（5858）→FC波别达；NK Dubrava Zagreb（5299）→杜布拉瓦萨格勒布；Amed SK（41990）→阿美德；Celta Fortuna（150119）→塞尔塔B队。中文资料分别来自出奇体育、中文 Livescore、Sofascore 简中及中文 Livescore/雷速赛事资料；保留各 provider 原名、team_id、aliases，不把相似队伍或青年队合并。Celta Fortuna 以官方 RC Celta 资料核验其预备队身份。来源参考：<https://data.chuqi.com/football/team-detail/237081/>、<https://www.livescore.com/zh/zuqiu/team/name/7524/tables/25537/>、<https://www.livescore.com/zh/zuqiu/team/amed-sportif/3707/overview/>、<https://www.sofascore.com/zh/football/team/celta-vigo-b/24336>、<https://rccelta.es/club/actualidad/el-filial-celeste-se-denominara-desde-la-proxima-temporada-celta-fortuna-como-homenaje-a-los-origenes-del-club/>。共享提交 `b9795b7` 已推送 `totalcorner-research-bridge/master`。
- 当前实算 formal union 2,468：canonical 2,068、unresolved 400（83.79%）；M1 1,445/1,553（93.05%）；M1 OU-R1 52/52（100%）；MR1 AH 1,583/1,921（82.40%）；MR1 AI declared mirror 1,445/1,553（93.05%）。共享库 12,276 IDs、4,084 canonical names；完整剩余清单和逐项 `NO_VERIFIED_CANONICAL_ZH` 原因见共享库 `data/football_display_names/formal_scope_coverage.json`。不为覆盖率虚构名称。
- M1 Telegram display/repair tests 8/8 通过，`git diff --check` 通过。仅更新唯一共享显示库、coverage/curation 报告和 curator；没有修改模型、策略、盘口、正式 ledger、结算或 TG 规则，也没有发送或编辑历史 TG。

## 2026-10-12 正式范围中文名称续补（九十四）
- 在 `b9795b7` 后又核实并加入 3 个正式球队：76 Igdir Belediyespor（85676）→厄德尔（捷报中文队页）；Esenler Erokspor（76129）→埃森勒尔埃罗克体育（Sofascore 简中）；Krumovgrad（108427）→克鲁莫夫格勒（Tips.GG 中文赛事实录，并以俱乐部官方历史核对旧名关系）。保留原 ID/英文名及身份，未将别队、预备队或同名球队合并。共享提交 `183dc32` 已推送 `totalcorner-research-bridge/master`。
- 最新实际 coverage：formal union 2,468，canonical 2,071，unresolved 397（83.91%）；M1 1,445/1,553（93.05%）；M1 OU-R1 52/52（100%）；MR1 AH 1,586/1,921（82.55%）；MR1 AI declared mirror 1,445/1,553（93.05%）。唯一共享库 12,276 IDs、4,087 canonical。完整 unresolved 名单及每条原因在 `data/football_display_names/formal_scope_coverage.json`。
- M1 Telegram display/repair tests 8/8 通过，`git diff --check` 通过。仅更改唯一共享名称数据/报告/curator；无 TG 发送或历史消息编辑，未修改任何模型、策略、账本、结算或 Telegram 规则。

## 2026-10-12 正式范围中文名称续补（九十五）
- 在共享库 `183dc32` 后新增 3 个有明确简中球队页配对的 formal IDs：Al-Ula（151747）→阿尔乌拉（17500）；Nordic United FC（119002）→北欧联合（7M）；Baglan Dragons（124892）→巴格兰龙（Tips.GG）。ID/英文 provider identity/aliases 原样保留。共享提交 `d790b64` 已推送 `totalcorner-research-bridge/master`。
- 最新实算 formal union 2,468：canonical 2,074、unresolved 394（84.04%）；M1 1,445/1,553（93.05%）；M1 OU-R1 52/52（100%）；MR1 AH 1,589/1,921（82.72%）；MR1 AI declared mirror 1,445/1,553（93.05%）。共享 registry 12,276 IDs、4,090 canonical names。未匹配完整名单及各条保留原因位于共享 `data/football_display_names/formal_scope_coverage.json`。
- M1 Telegram display/repair tests 8/8 pass；`git diff --check` pass。仅变更唯一共享显示库及其 curation/coverage 产物；未修改模型、策略、盘口、账本、结算、Telegram 规则，未发送或编辑历史 Telegram。

## 2026-10-12 正式范围中文名称续补（九十六）
- 新增 4 个以中文足球赛事实录明确配对英文球队身份的 formal IDs：Imisli（135067）→伊米什利；FC Livyi Bereh（86544）→利沃贝雷赫；Epitsentr Kamianets-Podilskyi（133667）→埃皮岑特尔；FK Trayal Krusevac（47593）→特拉亚尔·克鲁塞瓦茨。来源为 Vitibet、Mezha 简中乌克兰足球报道和 Betimate 中文比赛前瞻，均保留原始 team ID/provider name。共享提交 `9ce3d2c` 已推送 master。
- 最新实算 formal union 2,468：canonical 2,078、unresolved 390（84.20%）；M1 1,445/1,553（93.05%）；M1 OU-R1 52/52（100%）；MR1 AH 1,593/1,921（82.82%）；MR1 AI declared mirror 1,445/1,553（93.05%）。共享库 12,276 IDs、4,094 canonical；剩余完整名单与原因在 `formal_scope_coverage.json`。
- M1 Telegram display/repair tests 8/8 通过，`git diff --check` 通过。改动仅限唯一显示名称数据和 curation/audit 输出；未改模型、策略、正式账本、结算及 Telegram 规则，也未发送或编辑消息。

## 2026-10-12 正式范围中文名称续补（九十七）
- 新增 Corum FK（team_id 75036）→乔鲁姆；Futmetrix 简中球队资料页直接将 Corum FK 标为“乔鲁姆”，原始 team ID/name 和联赛身份保留。共享提交 `fcb0cd1` 已推送 master。
- 最新实算 formal union 2,468：canonical 2,079、unresolved 389（84.24%）；M1 1,445/1,553（93.05%）；M1 OU-R1 52/52；MR1 AH 1,594/1,921（82.87%）；MR1 AI declared mirror M1 1,445/1,553（93.05%）。共享 registry 12,276 IDs、4,095 canonical names。其余清单按 `formal_scope_coverage.json` 为准。
- M1 display/repair tests 8/8 pass，`git diff --check` pass。只改共享 display registry/curation/coverage，不改任何模型、策略、账本、结算或 Telegram 生产行为。

## 2026-10-12 正式范围中文名称续补（九十八）
- 新增 3 条经简体中文足球资料交叉核对的 formal team ID：JDFS Alberts（10525）→阿尔伯茨JDFS（Tips.GG 中文俱乐部页）；FK Kaspyi Aktau（13793）→卡斯比阿克套（7M 简中页，NowScore 对英文身份交叉核验；与其独立 B 队 ID 分开）；Nevezis（10852）→内韦日斯（中文足球俱乐部条目）。共享库提交 `8429ccdddcdbb130eaf463cc1acc6fb0455fedf6` 已推送 `totalcorner-research-bridge/master`。
- 最新 coverage 文件实算 formal union 2,468：canonical 2,082、unresolved 386（84.36%）；M1 1,451/1,553（93.43%）；M1 OU-R1 52/52（100%）；MR1 AH 1,595/1,921（83.03%）；MR1 AI 声明镜像 M1 范围 1,451/1,553（93.43%）。唯一共享 registry 12,276 IDs、4,098 canonical。逐 ID 未匹配清单及 `NO_VERIFIED_CANONICAL_ZH` 原因保存在共享库 `data/football_display_names/formal_scope_coverage.json`，不以临时音译凑数。
- M1 Telegram display/repair unittest 8/8 通过，`git diff --check` 通过。仅更新唯一共享名称 registry、scope coverage、batch audit 和 curation script。未运行云端正式 TG 链、未编辑或重发历史消息；没有修改 M1/MR1/MR1 AI 模型、策略、订单、结算或 TG 规则。

## 2026-10-12 正式范围中文名称续补（九十九）
- 再加入两个经简体中文足球来源确认的 formal IDs：FK Otrant Ulcinj（33964）→奥特兰特（FootyStats 简中页面；俱乐部官网核验 Otrant Olympic 与 Ulcinj 身份），Aegir（12947）→埃吉尔（Sofascore 简中队页）。此外，续补提交内保留前序已加入的 JDFS Alberts（10525）、FK Kaspyi Aktau（13793）和 Nevezis（10852）；统一共享提交 `20019a09fc4fd09ca8b9cc222d245d00abab9718` 已推送 `totalcorner-research-bridge/master`。
- 最新实算 formal union 2,468：canonical 2,084、unresolved 384（84.44%）；M1 1,453/1,553（93.56%）；M1 OU-R1 52/52（100%）；MR1 AH 1,597/1,921（83.13%）；MR1 AI declared mirror M1 1,453/1,553（93.56%）。唯一共享库 12,276 IDs、4,100 canonical。逐条未匹配 ID 与原因仍以共享 `data/football_display_names/formal_scope_coverage.json` 为准。
- M1 Telegram display/repair 测试 8/8 通过，`git diff --check` 通过。已对当前 M1 formal ledger 做不发送 dry-run：37 条具备 names-only edit 条件，99 条缺少原始文本，70 条未命中中文映射；dry-run 未调用 Telegram API。M1 OU-R1、MR1 AH、MR1 AI 历史消息尚未逐链执行编辑，不能计作修复。没有新增 workflow；也未改模型、策略、正式订单、结算或 Telegram 规则。

## 2026-10-12 正式范围中文名称续补（一百）
- 为正式 ID 补入冰岛球队：Grotta Seltjarnarnes（8623）→格罗塔、Njardvik（8935）→尼哈德维克，均由 7M 简中球队档案按英文身份与当地信息核对；原 provider identity、ID 保留。共享提交 `8ebde007a10027881876469bb0cc5da11d0a7f7b` 已推送 master。
- 最新实算 formal union 2,468：canonical 2,086、unresolved 382（84.52%）；M1 1,452/1,553（93.50%）；M1 OU-R1 52/52；MR1 AH 1,600/1,921（83.29%）；MR1 AI declared mirror M1 1,452/1,553（93.50%）。共享库 12,276 IDs、4,102 canonical。尚未匹配的完整球队 ID/name/reason 见唯一共享库 `data/football_display_names/formal_scope_coverage.json`。
- M1 display/repair 单测 8/8 通过；无生产 TG 发送或历史消息编辑。历史 TG repair dry-run 的 M1 计数见上一节，其他三链还未完成可验证的编辑盘点；没有更改策略、模型、订单或结算。

## 2026-10-12 正式范围中文名称续补（一百零一）
- 新增 Hegelmann Litauen（team_id 31954）→赫格尔曼立陶宛（Tips.GG 简中俱乐部页，俱乐部资料核对其旧名/现名）；Tikves Kavadarci（39947）→蒂克韦什（7M 简中球队页）。保留原 team ID/provider identity 和 aliases。共享提交 `c781cb3bbb310eb5156e33a9f3c19f6184997a97` 已推送 master。
- 最新 formal union 2,468：canonical 2,088、unresolved 380（84.60%）；M1 1,454/1,553（93.63%）；M1 OU-R1 52/52（100%）；MR1 AH 1,602/1,921（83.39%）；MR1 AI declared mirror 1,454/1,553（93.63%）。唯一共享 registry 12,276 IDs、4,104 canonical；未匹配逐 ID 清单见 `data/football_display_names/formal_scope_coverage.json`。
- M1 display/repair tests 8/8 pass；未进行正式 Telegram 编辑或发送。仅修改共享映射和 coverage/curation 产物，不触及策略/模型/账本/结算。

## 2026-10-12 正式范围中文名称续补（一百零二）
- 继续在唯一共享库内为 9 个正式 team ID 补入来源核验名称：Szentlőrinc SE（15638）→辛特罗尼克（Sofascore 简中）；ND Beltinci（12680）→贝尔廷齐（雷速）；Muglaspor（34336）→慕拉斯堡（雷速）；Atlanta Utd（164719）→亚特兰大联、Minnesota Utd（164723）→明尼苏达联（Sofascore 简中）；Beni Suef SC（51640）→贝尼苏夫、Dingnan Jiangxi United（162798）→定南赣联（分别复用共享库中同英文身份已验证别名，team ID 不合并）；Kazincbarcikai BSC（44038）→卡辛巴斯凯、Ankara Keciorengucu（151261）→基斯奥伦高古（7M 简中）。各自保留原 TotalCorner ID/provider name、别名与来源。共享库提交 `c7c90af26482c8c3ccfab986a209396dfde4ecf8` 已推送 `totalcorner-research-bridge/master`。
- 最新正式并集实算 2,468 IDs：canonical 2,097、未匹配 371（84.97%）；M1 1,457/1,553（93.82%）；M1 OU-R1 52/52（100%）；MR1 AH 1,611/1,921（83.86%）；MR1 AI declared mirror M1 1,457/1,553（93.82%）；MR1 AI observed confidence≥50 为 181/182（99.45%）；共享库 12,276 IDs、4,113 canonical。剩余 371 条逐项 ID/name/league/system/reason 保存在 `data/football_display_names/formal_scope_coverage.json`，均为 `NO_VERIFIED_CANONICAL_ZH`，不以猜译补齐。
- 本机与 MR1 Node 隔离渲染均确认新增 7 个队名可通过同一共享 `display_names.json` 输出中文；M1 display/repair unittest 8/8、MR1 registry/AI formatter 定向测试 4/4 通过。M1 AH/OU-R1 共用 M1 formatter；MR1 AH、MR1 AI 的 runtime workflow 均 checkout 同一共享 master。
- 使用现有名称修复流程对历史消息实际验收（没有重发）：M1 run `38228550080` success，37 条候选全部 Telegram 回 `already_matching`，实际编辑 0；按市场分为 AH 16、OU 21，其中 OU-R1 11 条均已匹配。另有 M1 OU-R1 82 条 SENT 缺保存原文、3 条 UNKNOWN 无 provider message ID，不能安全编辑；M1 另外 70 条旧记录未命中当前映射。MR1 AH run `38228804250` success：125 skipped/already processed、edited 0、unresolved 0、failed 0，receipt commit `445737ea27e4754baa24d7182003a79032b6a8bd`。MR1 AI run `38228929018` success：201 条中 9 条候选均失败于 Telegram HTTP 400 `message to edit not found`，192 unresolved，edited 0，receipt commit `cb32df75744c63d43af236e7557af5c176de3f29`。因此不得把 M1/MR1 AI 历史消息称作已成功编辑。
- 只变更共享展示映射/curation/coverage 和历史名称修复的既有回执；没有发送新 Pick、修改价格/盘口/方向/时间、结算或交易账本，也没有改策略、模型或通知规则。未解决球队完整清单仍以共享 coverage JSON 为准，后续继续来源核验；已验证中文名不得被覆盖。

## 2026-10-12 正式范围中文名称续补（一百零三）
- 对 unresolved 清单与已验证 aliases 再做精确身份交叉后，为 TotalCorner team_id 174374（provider `Kazincbarcika SC`，league_id 241）补入“卡辛巴斯凯”；该 ID 与既有 team_id 44038（Kazincbarcikai BSC）各自保留，不合并。名称来自同一 7M 简中俱乐部档案与匈乙身份上下文，写入来源注释。共享提交 `9e35997bfb396ad942f9d27c17ab024efe5d6c50` 已推送 master（之前本轮提交 `c7c90af26482c8c3ccfab986a209396dfde4ecf8` 已包含前 9 项）。
- 最新实算 formal union 2,468：canonical 2,098、unresolved 370（85.01%）；M1 1,457/1,553（93.82%）；M1 OU-R1 52/52；MR1 AH 1,612/1,921（83.91%）；MR1 AI mirror 1,457/1,553（93.82%）；共享库 12,276 IDs、4,114 canonical。完整 unresolved ID/name/league/system/reason 以 `data/football_display_names/formal_scope_coverage.json` 为准，370 项均为 `NO_VERIFIED_CANONICAL_ZH`。
- 在最新 registry 提交后再次执行既有 Telegram names-only repair：M1 run `38229542407` success，37 eligible、0 edited、37 already_matching、99 缺原文、70 unmapped、0 failed；MR1 AH run `38229784323` success，125 skipped、0 edited、0 unresolved、0 failed，receipt commit `f8e9b8d17f59e96363178dd3bf84ea8e53180473`；MR1 AI run `38229917464` success，9 candidates 仍全部 HTTP 400 `message to edit not found`、192 unresolved、0 edited，receipt commit `a1b476b3f266bb52586bec82f230bdc2f85242a7`。未重新发送任何旧策略。
- M1 display/formal-runtime tests 20/20 pass；本机 MR1 shared-registry/AI formatter tests 4/4 pass；新添 Kazincbarcika 名称已由两边 formatter 隔离渲染为中文。未修改策略/模型、赛程范围、正式账本、结算、投注条款、TG 新消息发送规则。历史 TG 实际成功编辑仍为 0；MR1 AI 的旧 Telegram message IDs 对应内容已不再可编辑，不能称为修复成功。

## 2026-10-12 正式范围中文名称续补与 Telegram 复核（一百零四）
- 共享库 `totalcorner-research-bridge/master` 新提交 `41ef7dd7` 已推送。本轮新增 8 个经中文公开足球资料/精确球队身份核验的 formal ID：Athens Kallithea（147679）→雅典卡利地亚；Caersws（8128）→凯尔斯维斯；Mold Alexandra（30803）→莫尔德亚历山大；Denbigh Town（9658）→丹比队；Penrhyncoch（40046）→彭林科奇；Cwmbran Celtic（30758）→康布兰凯尔特；Al Kawkab（39919）→阿尔科瓦克；FC Gonio（161441）→贡尼奥。每条保留 provider name、team_id、competition IDs、aliases 与来源，没有按相似音译合并球队。中文资料分别可核对于 [NowScore Athens Kallithea/雅典卡利地亚](https://info.nowscore.com/cn/team/Summary.aspx?teamid=569)、[Tips.GG Caersws](https://tips.gg/cn/team/caersws-football/)、[Mold Alexandra](https://tips.gg/cn/team/mold-alexandra-football/)、[Denbigh Town](https://tips.gg/cn/team/denbigh-town-football/)、[Penrhyncoch](https://tips.gg/cn/team/penrhyncoch-football/)、[Cwmbran Celtic](https://tips.gg/cn/team/cwmbran-celtic-football/)、[Al Kawkab](https://tips.gg/cn/archive/al-kawkab-football-vs-mudhar-football/) 与 [FC Gonio](https://tips.gg/cn/tournament/football-georgian-cup-2024/)。
- 更新后从 `formal_scope_coverage.json` 实算：正式并集 2,468，canonical 2,106、未匹配 362、覆盖 85.33%；M1 1,458/1,553（93.88%）；M1 OU-R1 52/52（100%）；MR1 AH 1,620/1,921（84.33%）；MR1 AI 声明镜像 M1 为 1,458/1,553（93.88%）；MR1 AI observed confidence≥50 历史 cohort 181/182（99.45%，成员范围沿用原快照）。共享库 12,276 team IDs、4,122 canonical；未匹配 ID、联赛、系统和 `NO_VERIFIED_CANONICAL_ZH` 原因见共享 `data/football_display_names/formal_scope_coverage.json`。
- M1 pytest 20/20；MR1 使用唯一共享 registry 的 formatter/parser 定向 Node tests 4/4。历史名称修复实际运行：M1 runner run `38230790424` success，37 eligible 中 AH 16、OU 21 均 `ALREADY_MATCHING`，实际编辑 0，缺原始发送文本 99、未命中名称 70、失败 0；MR1 AH run `38231035875` success，125 skipped/already processed、edited 0、unresolved 0、failed 0，receipt commit `408bb3907fbac0435b584a3233c1da6474018a3e`；MR1 AI run `38231163138` success，201 total、9 candidates、edited 0、192 unresolved、9 failed，失败均为 Telegram HTTP 400 `message to edit not found`，receipt commit `e26d64a9b0a96375a570eedd3c71202975c99178`。本轮没有成功改写历史消息，也没有重发历史 Pick。
- MR1 项目本地只读 formatter 测试前先 fast-forward 到当时远端 master `0fb03810e7`，本地仓库未产生提交。runner handoff 更新为本节；共享中文库仍未覆盖的 362 项继续留空待核实。没有修改任何模型、策略、范围、盘口、正式交易 ledger 或 settlement 规则。

## 2026-10-12 19:32 北京时间 M1 调度缺失与紧急恢复
- M1 正式工作流 `m1-free-runtime.yml` schedule 为 UTC 04:05/10:05/16:05/22:05；最新定时运行 `38191159491` 在 UTC 2026-10-12 01:15 开始并成功，但 UTC 04:05 和 10:05 对应运行缺失。现有 `m1-schedule-watchdog.yml` 同样没有对应补偿运行，工作流仍 active。不要将一次成功冒充持续调度恢复。
- 旧失败运行 `38171198684` 失败于 `Persist scan and locks`；详细错误尚未取得，不能推断是策略问题。
- 已经通过 GitHub API 真实触发 M1 正式工作流 `38243313565`（UTC 2026-10-12 11:32:32），已从 queued 进入 in_progress，secrets 检查成功，checkout 进行中。链接 https://github.com/ljm198964-alt/quant-runner/actions/runs/38243313565 。
- **待完成**：检查此运行的真实扫描、正式锁单、TG 发送回执、账本回写；调查 GitHub schedule/watchdog 漏触发原因，并解决持续调度可靠性。用户目标是完全恢复，不是仅触发一次。未改变 M1 策略或盘口来源。

## 2026-10-13 M1 定时漏触发补偿修复
- 用户明确要求直接修复 M1 自动扫描漏触发，不得只讨论方案。本次在**现有** `.github/workflows/m1-schedule-watchdog.yml` 增加 `workflow_run` 事件，由连续运行的 `MR1 Free Runtime` 完成事件唤醒同一份 M1 漏扫描检查；保留原有 04:05/10:05/16:05/22:05 UTC M1 四个扫描时段与原有 04:35/10:35/16:35/22:35 UTC Watchdog 时段。代码提交 [`ffe077a`](https://github.com/ljm198964-alt/quant-runner/commit/ffe077aff1655d17f47c8118336d483b8b4c438a)。
- 为避免额外不必要的 Runner 消耗，MR1 完成事件仅在 M1 原定扫描小时及下一小时运行检查，沿用原有每时段20分钟后检查和去重行为；这仅是运维补偿，不改变策略/盘口/正式发单频次与身份，不让 MR1 发 M1 TG。
- `push` 触发验证工作流 [`38336594903`](https://github.com/ljm198964-alt/quant-runner/actions/runs/38336594903) 已成功（2026-10-13 02:22 UTC）；日志输出 `M1_ALREADY_ATTEMPTED_NO_DUPLICATE`，确认检测到该时段已有 M1 成功运行 `38319250438`（2026-10-12 22:54 UTC），未重复派单。
- **仍需核对**：新增的 `workflow_run` 由 MR1 完成事件真正触发的记录；下一个原计划扫描时段发生漏触发时能否正确补发 M1；实际 M1 TG 回执/账本状态。GitHub Actions 若整体不可用，此 GitHub 内部补偿同样可能不可用，不得称为完全独立调度。原有私有代码与正式账本依赖仍在。

## 2026-10-13 M1 漏触发补偿最终接线（覆盖此前仅 workflow_run 的临时方案）
- 为保证 **真正触发**，已在一直运行的公开 `.github/workflows/mr1-public-ticker.yml` 中增加轻量 M1 漏扫描检查的主动派发：仅在原 M1 UTC 04/10/16/22 扫描时段25分钟后及其下一小时，针对同一时段发起一次 `m1-schedule-watchdog.yml` 的 `workflow_dispatch`；唤醒失败会尝试下一次原有 MR1 5分钟 tick。M1 Watchdog 自己先核查同一时段有无 M1 已尝试运行，再决定是否派发 M1 正式工作流；不直接发送 TG、不修改策略或 4 次/天扫描计划。
- 公开 Ticker 代码提交 [`a328093`](https://github.com/ljm198964-alt/quant-runner/commit/a328093636dd63de402c5ebe378c2804230ed698)。此前 `workflow_run` 事件方案存在由 `GITHUB_TOKEN` 调用的 MR1 workflow_dispatch 链式触发不确定性，因此已从 M1 Watchdog 移除该事件监听，改用 Ticker 主动 dispatch，提交 [`7a83ec1`](https://github.com/ljm198964-alt/quant-runner/commit/7a83ec1c086289ec6cd2b8a43ed23df57b643fbd)。
- 部署实际验证：公开 Ticker 新版本运行 [`38337120541`](https://github.com/ljm198964-alt/quant-runner/actions/runs/38337120541) 已进入 `in_progress`，并成功发起 MR1 正式研究采集运行 `38337129409`。M1 Watchdog 最新 [`38337154316`](https://github.com/ljm198964-alt/quant-runner/actions/runs/38337154316) 成功，输出 `M1_ALREADY_ATTEMPTED_NO_DUPLICATE`，正确发现 2026-10-12 22:05 UTC 对应 M1 运行 `38319250438` 已成功，未重复派单。**尚未观察到真实 M1 时段漏触发后由新 Ticker 补派的案例，不得宣称这一行为已被实测。**
- 曾经失败的 `M1` 运行 `38171198684` 根因是扫描提交时 `data/football_display_names/auto_curation.json` 与中文库同步更新产生 rebase conflict；现行 `m1_commit_state.sh` 的 scan stage 已不再包含该旧文件。该历史冲突的直接触发点已移除，但不能据此保证未来不存在其他 Git 冲突。
- **局限**：此修复利用已经正常运行的公开 MR1 Ticker，避免依赖 M1/Wachdog 两条可能漏触发的定时器；但仍属于 GitHub Actions 内部补偿，如果 GitHub 托管 Runner 整体不可用，仍需要独立执行环境。请不要将其称为已脱离 GitHub Actions。

## 2026-10-13 11:02 北京时间：其他模型核查与 MR1 AI TG 停发遗漏补丁
- MR1 AH：正式绩效来自 `ljm198964-alt/mr1-shadow/data/mr1-v6-cross-market/formal/performance.json`，生成 UTC 2026-10-13 03:02:26，历史 TG 正式已发送 125、已结算 118、待结算 7，47全赢/7半赢/9走水/6半输/49全输，净 -5.755U、ROI -4.88%。公开 `MR1 Free Runtime` 运行 [38339549770](https://github.com/ljm198964-alt/quant-runner/actions/runs/38339549770) success，其中历史已发单结算及持久化步骤成功；正式新 TG 发送步骤继续暂停。
- MR1 AI：`data/mr1-ai-browser-forward/formal-performance/summary.json` 生成 UTC 2026-10-13 01:41:10，历史已发18、结算17、待结算1，净 -5.75U、ROI -33.82%；公开 `MR1 AI Browser Settlement` 运行 [38332789670](https://github.com/ljm198964-alt/quant-runner/actions/runs/38332789670) success。最新浏览器采集 UTC 2026-10-12 20:06（北京10月13日04:06），监控 UTC 2026-10-13 01:41 标 `STALE`，因此**MR1 AI 新前瞻采集不能称为正常**；尚无可核对的 MR1 AI 新影子正式结算成绩。
- 发现 MR1 AI 历史停发操作只封住了 `src/v7-ai-picks-telegram.js`，但 `src/mr1-ai-browser-forward-notify.js` 仍可调用实际 Telegram 发送，公开 `mr1-ai-local-browser-forward.yml`、`mr1-ai-ah-recovery-notify.yml` 仍提供 Telegram token。为贯彻用户之前已确认的“MR1 AH/AI 停发新 TG、转影子”的规则，本轮已修复：私人 MR1 源码 `src/mr1-ai-browser-forward-notify.js` 对默认生产发送器改为通过 Crown 合格验证后写入独立 `data/mr1-ai-shadow/signals/<signal_id>.json`，含 `signal_status:SHADOW_ONLY` 与 `telegram_write:false`，原正式历史发送回执不变，提交 [1fefa78](https://github.com/ljm198964-alt/mr1-shadow/commit/1fefa78c439522af96c6d283fceb4e164d61c1d2)。注入测试发送器路径仅用于已有回归测试；实际 production 默认调用不会调用 sendTelegram。
- 公开 Runner 对应三个工作流均已移除 MR1 Telegram secrets 并保留采集、Crown 报价校验、持久化、已有正式结算：`mr1-ai-local-browser-forward.yml` [a336437](https://github.com/ljm198964-alt/quant-runner/commit/a3364372f215ed94a04c794dcbfdce61cdf757ce)、`mr1-ai-ah-recovery-notify.yml` [54dbe96](https://github.com/ljm198964-alt/quant-runner/commit/54dbe9687bf66950648907890d7b7c6ff42cc918)、`mr1-ai-runtime.yml` [2c1b544](https://github.com/ljm198964-alt/quant-runner/commit/2c1b54433959c701f6d243cd9d0a62ce4d7d6e53)。**源码与工作流已修改并提交，暂未经过新浏览器采集运行的端到端验收**；不能声称已形成独立影子结算账本。旧 `formal-policy.json` 的 `mode:LIVE_PRODUCTION` 是历史声明，不能覆盖现在执行代码的 shadow-only 状态。
- M1 OU 旧线＋R1：正式 M1 账本至 UTC 2026-10-12 23:10:56，OU 合并已发101、结算93、未结8，净 -1.135U、ROI -1.22%；**必须保持旧线与 R1 身份独立，当前账本尚未独立拆分，不可把101单都称为 R1**。
- 对手邹：`results/opponent_settlement_latest.json` 仍是 UTC 2026-10-10 06:28 的旧报告（旧227订单、已结算179、未解决48，净 +0.185U、ROI+0.10%；AH 98 +2.325U，OU 81 -2.140U），另新增242封 AH/OU 邮件，合计去重469。公开对手结算最近失败 [38160391037](https://github.com/ljm198964-alt/quant-runner/actions/runs/38160391037)，实际失败于 `opponent_cache_reconcile_v2.py` 中 `TWO_TEAM_KICKOFF_LEAGUE_VALIDATION_FAILED`，持久化未执行。**不得绕过球队/开球/联赛校验来虚构结算**；剩余242尚未进入已结算报告。

## 2026-10-13 11:39 北京时间：MR1 AH / MR1 AI 停发后的真实影子实战
- 按用户既有指令，新 MR1 AH 与 MR1 AI **停止正式 TG 派单但继续虚拟下单、按原 Crown 盘口锁价、赛后独立结算**；历史已 TG 发送的 MR1 AH 125单和 MR1 AI 18单仍保留在各自正式账本，禁止与影子合并。
- **MR1 AH 冻结正式策略的影子账本已生产实证运行**：`src/v6-ah-formal-notify.js` 新增 `shadowOnly` 模式（复用原正式模型的正EV、源为已核验 Crown、原受认可联赛范围、赛前时间及相同信号去重）并以 CLI 默认 shadow-only；独立写 `data/mr1-v6-cross-market/shadow/signals/<signal_id>.json`，不触碰正式 Telegram 出站与 `formal/sent.jsonl`。提交 `f5495088ca17df9df8491573267527899faf1aab`、进一步正式出站隔离修正 `aa81eeb2de43063c5ea55b9255d2086a8c87eca0`。`src/v6-ah-shadow-settlement.js` 专用 verified FT 结算提交 `28a64a658d35d4a494c67a17550b793a01e1eea2`；定向隔离测试 `test-v6-ah-shadow.js` 提交 `fb0ac3f02645fedfb780ad33a0007af4415da77f`。公开 `mr1-free-runtime.yml` 接线 `90415d100e5d378a36698f951ea6e0f845b09c30`，运行 [38342256402](https://github.com/ljm198964-alt/quant-runner/actions/runs/38342256402) SUCCESS（阴影测试、锁单、结算、历史正式结算、持久化均成功）。
- MR1 AH 生产影子绩效 `data/mr1-v6-cross-market/shadow/performance.json` UTC 2026-10-13T03:37:48：**新影子已锁5、已结0、待结5、错误0、ROI=null、正式TG发送0**。其独立 shadow notify 状态约 28 eligible、20 已正式派过跳过、3 已影子存在、5 新记录。不能把 5 单视作已结算，也不能用旧正式成绩充当影子。
- **MR1 AI 独立影子结算代码已进入生产**：先前 `src/v7-ai-picks-telegram.js` 与 `src/mr1-ai-browser-forward-notify.js` 已改默认生产 shadow-only。新 `src/mr1-ai-shadow-settlement.js` 提交 `11089b129f4355b698156ea4bab5118731cbfdee`，独立读取 Crown 赛前 shadow signals，借用 API 验证后的历史 FT **仅提取赛果、重新按信号锁定的 Crown line/price 核盈亏**，绝不复制研究账本曾使用的 Bet365 盈亏，也不写正式历史 Telegram 账本。定向测试 `test-mr1-ai-shadow-settlement.js` 提交 `aa094d3cdf6bd7ca0c563ef372492cb1e9bc877b`；公开 `mr1-ai-browser-settlement.yml` 接线提交 `981f01958e768a240a075c781c1362457388e821`，运行 [38342289154](https://github.com/ljm198964-alt/quant-runner/actions/runs/38342289154) SUCCESS，影子测试、影子结算、持久化成功。
- MR1 AI **当前 shadow 仍无真实订单**：`data/mr1-ai-shadow/performance.json` UTC 2026-10-13T03:38:45：recorded 0, settled 0, pending 0, errors 0, ROI null。`data/mr1-ai-browser-forward/collector-watch-status.json` 同时生成 UTC 03:38:48，`STALE`、heartbeat 最后 UTC 2026-10-12T20:06:07（北京时间10月13日04:06），超时 452.7 分钟。浏览器采集依赖用户正常Chrome会话，本轮**不能声明已恢复 MR1 AI 持续新影子选单**。应继续优先修复稳定新数据源并真实验收新影子入账；切忌将旧的 `browser-forward/settlement/summary.json` 1011 单研究账本、历史正式 TG 18 单混算为这次真实 Crown-only 阴影成绩。

## 2026-10-13 11:42 北京时间：MR1 AI 影子采集恢复诊断
- 为不打断现有 Crown API / TG 正式链路，`mr1-ai-runtime.yml` 添加仅当 workflow push 时执行的 **只读云端网页诊断**（只访问 TotalCorner AI Picks 今日/明日两张网页、无 Crown API 请求、无 TG、无任何订单），提交 [`92534bc`](https://github.com/ljm198964-alt/quant-runner/commit/92534bc1b5518d702213bb70376ac5ca6d26a6f2)。现有 `workflow_dispatch` 运行策略和派单暂停逻辑不变。
- 公开 GitHub Actions 运行 [38342924818](https://github.com/ljm198964-alt/quant-runner/actions/runs/38342924818) `success`，其中源码诊断 UTC 2026-10-13 03:42:22 输出：`parsed_ah_picks:0`、今日页面 `HTTP_403`、明日页面 `UPCOMING_VIP_RESTRICTED`、两页 `request_authentication:NO_WEBSITE_SESSION`，`telegram_write:false,crown_requests:0`。`TOTALCORNER_WEB_COOKIE` 在**公开 Runner** 未配置，GitHub 云端源不能直接替代用户正常 Chrome 已登录会员采集。
- 结论：**MR1 AI 影子锁单、价格冻结、独立赛后结算的生产软件链路已通过测试，当前0新影子订单的实际原因是上游会员浏览器采集超时；云端无有效会员会话且网页拒绝/锁定**。不得用 HTTP 403/网页无权限的结果当作“没有 AI 推荐”，也不得在缺会员源时从其他庄家/研究快照伪造 Crown 影子单。后续恢复真实本地 Chrome 采集后使用已部署的公开 `MR1 AI Local Browser Forward` 工作流把新符合条件信号写入 `data/mr1-ai-shadow/signals`；旧正式 TG 18单独立结算。

## 2026-10-13 12:23 北京时间 MR1 AI Chrome 采集稳定性修补（不代表本机已恢复）
- 本轮从现行私有 MR1 源码审查到浏览器会员采集依赖用户本机已登录 Chrome、`chrome-extension/mr1-ai/background.js` 的 MV3 每小时 alarm、`content.js` 到 `127.0.0.1:17864` 的本机桥接、launchd KeepAlive。最后正式采集心跳仍为 UTC 2026-10-12T20:06:07（北京10月13日04:06）；没有证据能区分 Mac 睡眠/Chrome 停止、扩展停止、bridge 断线、或 GitHub push 失败，不能直接断言单一根因。
- 已修补扩展源：`chrome-extension/mr1-ai/background.js` 在 service worker 恢复时检查/重建原每小时 alarm，并在桥接临时不可达时保留自动标签页供重试，提交 [`f9e9a04`](https://github.com/ljm198964-alt/mr1-shadow/commit/f9e9a04ef6f9ffa9e397c2de3eaac7d2d5f59d50)；`content.js` 通过原已显示的会员页面对本机桥接临时断线重试，提交 [`10b74f7`](https://github.com/ljm198964-alt/mr1-shadow/commit/10b74f7302c208a0deb21c37edb256ae9400fe9f)。不上传 cookie/登录信息、不改会员来源、不新增 Crown 请求或 Telegram 派单。
- 新增扩展回归断言到 `test-mr1-ai-chrome-extension.js` [`f4e016d`](https://github.com/ljm198964-alt/mr1-shadow/commit/f4e016d48cadcf5a66d41c858aa8e1522b271e65)；公开 MR1 runner `mr1-free-runtime.yml` 纳入该源代码静态回归 [`599de9a`](https://github.com/ljm198964-alt/quant-runner/commit/599de9a9959e2b4e3c7bccf4ebe074ced2429643)，运行 [`38345933472`](https://github.com/ljm198964-alt/quant-runner/actions/runs/38345933472) 实际完成成功：源代码回归套件 3/3 pass、影子隔离套件 1/1 pass；并继续 MR1 AH 影子扫描/锁单/结算。
- 回归中曾出现旧 `test-v6-ah-formal.js` 失败：其测试夹具用不存在的联赛 canonical ID 强行期待别名覆盖，且期待正式盘口发送时重新报价到1.93，与**现行权威ID中文名及冻结最初 Crown 水位1.90**不符。已只修正模拟夹具及期待值，未修改模型/真实价格/策略，提交 [`86e282c`](https://github.com/ljm198964-alt/mr1-shadow/commit/86e282c6e69efccddef7b807cc2059e0661152b7)，经上述公开 runner 完整3/3 复测通过。
- 公开 Runner 的官网来源探测仍证实无用户会员 Web session，今日页面403、明日受VIP限制。官方 TotalCorner API 公告仅赛事、赛果、赔率等，未发现可直接替代原会员 AI Picks 的同源API；现有 Gmail 也未收到可直接替代的 AI Picks 推荐通知。因此本机 Chrome 会话仍是正式前瞻数据源。
- **重要阻塞**：代码已提交且公开CI验收，但用户本机Chrome及桥接服务没有在本次工具环境中被远程重新启动，不能宣布本机Chrome已更新或 MR1 AI 新影子订单已产生。影子订单依旧0、结算0，下一步需在已有授权Mac上确认 Chrome 运行、launchd bridge、扩展加载与远端新心跳；不接触用户私密浏览器cookie。原有 Desktop Commander 工具报告当月调用额度耗尽（明确不重试），不能伪称已操作用户Mac。
- 同时 M1 本日 UTC 04:05（北京时间12:05）计划定时触发截至北京时间12:23仍缺失；已有独立 `MR1 Public Ticker` 的备用Watchdog预定 UTC 04:25以后检测缺失。**应继续真实验收：Ticker唤醒Watchdog→M1 dispatch→scan→Telegram receipts→ledger persist，不得仅凭Watchdog源代码声明已恢复。**

## 2026-10-13 12:28 北京时间 M1 正式漏扫备援实测
- UTC 2026-10-13 04:05（北京时间12:05）主 `M1 Free Runtime` GitHub schedule 未生成对应运行，截至12:24仍无本时段正式运行。现有公开 `MR1 Public Ticker` 按原已确认 5min 心跳实际唤醒 M1 Watchdog。
- **真正自动补发已发生**：公开 [Watchdog run 38346335574](https://github.com/ljm198964-alt/quant-runner/actions/runs/38346335574) 在 UTC 04:25:05 创建且 SUCCESS，日志 UTC 04:25:13.590 明确输出 `{"status":"M1_MISSING_SCAN_DISPATCHED","slot_utc":"2026-10-13T04:05:00+00:00","age_minutes":20.18,"destination":"m1-free-runtime.yml","strategy_rules_changed":false,"tg_direct_send":false}`。新 [M1正式运行38346345917](https://github.com/ljm198964-alt/quant-runner/actions/runs/38346345917) 在 UTC 04:25:13 创建、04:25:17 job启动。**这是生产链路真实漏发后由备援自动发起，不是手动或模拟。**
- 截至UTC 04:28：M1 已通过secret检查、checkout、policy selftest、seed历史索引和Crown研究测试，处于 `Run M1 scan with retry` 扫描中。**正式TG送达、scan commit、通知回写/结算更新均还未验证，不能把自动启动误报成整条链路成功**。
- 后续必须检查 [run 38346345917](https://github.com/ljm198964-alt/quant-runner/actions/runs/38346345917) 的最终Job步骤、`results/latest.json` 的扫描完成状态、`results/m1_formal_report.json` 的TG确认数和更新时间、ledger状态；如果失败，定位并修复。主schedule漏触发本身仍存在，当前已验证的是watchdog补发。

## 2026-10-13 12:30 北京时间 M1 备援真实发送及账本回写完整验收（覆盖上节进行中状态）
- **全链路成功**：M1 当日 UTC04:05 scheduled run 漏触发，`MR1 Public Ticker` 自动唤醒 Watchdog [38346335574](https://github.com/ljm198964-alt/quant-runner/actions/runs/38346335574) UTC04:25:05 SUCCESS，并输出 `M1_MISSING_SCAN_DISPATCHED`，继而触发原正式生产 [M1 Free Runtime 38346345917](https://github.com/ljm198964-alt/quant-runner/actions/runs/38346345917) UTC04:25:13 SUCCESS。M1 job 所有关键步骤实际 `success`：`Run M1 scan with retry`、完整度审计、`Lock formal signals`、`Persist scan and locks`、`Claim pending notifications`、`Persist notification claims`、`Deliver or reconcile notifications`、`Persist delivery receipts`。
- 生产 `ljm198964-alt/totalcorner-research-bridge/results/latest.json` 更新于 UTC04:28:40.725（北京12:28:40），`run_id=M1_20261013T042541Z`、`scan_status=COMPLETE`、fixtures_scanned=9、candidate_count=5、new_signal_count=3、error_count=0；本次新增订单全部来自 Crown 合规证据。
- 逐单正式 Telegram 收据 `results/m1_formal_ledger.json` 最新 Git blob `fed1b5bf8068169ceade22da11b0494c6f57164b`，`notifications[*].telegram.status=SENT` 新增3条，provider_message_id **624**（M1 AH，Estonia Meistriliiga，UTC04:27:55）、**625**（M1 OU R1，Estonia Meistriliiga，UTC04:28:00，策略身份 `M1-OU-R1|M1_SELECTION_20260924_EARLY_ROBUST`）、**626**（M1 AH，Czechia First League，UTC04:28:38）。三个 `picks[*].market_evidence.source_bookmaker=crown`，且各自独立 TG正式回执已写账。
- `results/m1_formal_report.json` UTC04:28:49.564：`source=M1 confirmed Telegram-sent receipts only`、confirmed **211**（原208+3），其中 M1 AH **109** 已发/101已结/8未结、+3.005U ROI+2.98%，M1 OU **旧线+R1混账** **102** 已发/93已结/9未结、-1.135U ROI-1.22%；M1总 **211已发/194已结/17未结、+1.870U ROI+0.96%**。另3个 UNKNOWN历史通知不得冒充正式 TG成功或盲目补发。OU旧线/R1完整成绩仍需按身份拆分；不要将合并102单视为R1。
- **限制和下一步**：主GitHub schedule 的漏触发问题没有自行消失，但免费公开 Runner 的Watchdog兜底**已由真实漏扫及真实新增TG订单证明端到端有效**；仍需继续观察下一时段有无长时间延误、重复订单或其他失败。新版Ticker备用运行属于公开仓库，但其M1代码、账本仍依赖私有`totalcorner-research-bridge`，不能声称完全迁移或删除私有仓库。
- 并行MR1：扩展source/bridge容错补丁 `f9e9a04`/`10b74f7`、校验 `f4e016d`，旧测试夹具修复 `86e282c`，公开 [MR1 run 38345933472](https://github.com/ljm198964-alt/quant-runner/actions/runs/38345933472) 中源码回归3/3、独立AH影子隔离1/1通过；实机会员Chrome采集仍需确认恢复。为防止项目状态误报，私有MR1 `src/github-shadow-runtime.js` 的 `chain_status.MR1.formal_delivery` 和说明已改成`TG_PAUSED_AH_SHADOW_ONLY`，提交 [`cd4e24b`](https://github.com/ljm198964-alt/mr1-shadow/commit/cd4e24bbc51ae7ea838ff275ba105d6005e8d104)。UTC04:25那轮MR1 `run-status.json` 仍使用较早代码写出旧标签，下次新代码实际运行后须再验收。

## 2026-10-14 正式中文库补齐与历史 Telegram 名称复核
- 先快进读取了本文件此前最新 handoff commit `ab19816` 及当日其后的远端 main 更新；共享库不重建、不覆盖既有映射。最新 `totalcorner-research-bridge/master` 为 `450340dd`（含 `4e954d36` 与 `450340dd`；较早先行提交 `815828e2` 已在其历史中）。本轮补入 6 个有可核验简中来源的正式球队 ID：Dergview FC（10178）→德格维尤队、Porthmadog（31546）→波特马多克、Brickfield Rangers（33038）→布里克菲尔德流浪者、CPD Bangor 1876（133139）→邦戈1876、CPD Y Rhyl（165363）→里尔队、CPD Llanuwchllyn（186100）→兰尼瓦克林；另补 league_id 10415 Northern Ireland Premier Intermediate League → 北爱尔兰中级联赛。team_id/provider identity/league IDs/aliases 独立保留，没有按相似名称合并。对已保存名称与 curation rerun 的幂等性作修复，重复运行不再无意义改写生成时间。名称参考：Tips.GG Porthmadog、Bangor/Rhyl、Llanuwchllyn 中文页面/记录，OddsGPT Brickfield 简中球队页，FootyStats 北爱尔兰中级联赛中文页；来源链接详见本次任务交接。另一个 league_id 44797 的 Northern Ireland Conference Premier 暂无核实中文来源，继续列为未匹配。
- 从共享库最新 `formal_scope_coverage.json` 实算（generated_at `2026-10-14T11:20:24Z`）：正式并集 2,468，canonical 2,112，unresolved 356，覆盖 85.58%；M1 1,458/1,553（93.88%）；M1 OU-R1 52/52（100%）；MR1 AH 1,626/1,921（84.64%）；MR1 AI 声明镜像 M1 范围 1,458/1,553（93.88%），历史 confidence≥50 cohort 181/182（99.45%，沿用已存 cohort membership）。共享库 12,276 team IDs、4,128 canonical。356 项均保留英文 provider identity 并标 `NO_VERIFIED_CANONICAL_ZH`；完整逐项清单、team ID、联赛、系统和原因见唯一共享库 `data/football_display_names/formal_scope_coverage.json`。未虚构名称。
- formatter/回归：M1 formatter 对新增比赛的隔离输出为 `【M1】2026-10-03 17:30 威尔士冠军联赛北区 波特马多克 vs 邦戈1876 全场让球 波特马多克 +0.25@0.95`；MR1 AI 使用共享 registry 的 formatter 输出相同中文赛事/队名并保留 `【MR1 AI】` 身份。M1 display/runtime/repair tests 20/20 pass，MR1 registry/AI formatter Node tests 4/4 pass；`git diff --check` pass。上述为 formatter 本地渲染验证，不是新生产单。
- 依用户授权对既有 TG 消息执行 names-only edit 工作流，没有重发订单：M1 run [38556246442](https://github.com/ljm198964-alt/quant-runner/actions/runs/38556246442) success，eligible 37、edited 0、already matching 37、缺原始文本 99、unmapped 98、failed 0；MR1 AH run [38556512685](https://github.com/ljm198964-alt/quant-runner/actions/runs/38556512685) success，already processed 125、edited 0、unresolved 0、failed 0；MR1 AI run [38556666514](https://github.com/ljm198964-alt/quant-runner/actions/runs/38556666514) success，201 条中 192 unresolved，9 条虽可匹配 fixture/message ID 但 Telegram 均回 HTTP 400 `message to edit not found`，edited 0。三条链历史消息实际编辑成功合计 0；失败或不可编辑的旧消息未重发，生产账本/结算未改。
- 唯一共享库来源已由 M1 与 MR1 formatter 读取；M1 AH 和 OU-R1 复用 M1 formatter。未修改任何 M1、MR1 AH、MR1 AI 模型、策略、参数、范围、订单、结算或 Telegram 派单规则。本节记录名称展示层工作，不代表 356 个 unresolved 已完成中文化。

## 2026-10-14 正式范围续补：核实 3 队名、2 联赛名
- 用户交接中“剩余 740”属于更早快照；本轮开始时远端 `master` (`450340dd`) 的最新正式范围快照实际为 356 unresolved。基于最新清单继续来源核验，新增 3 个球队 canonical 与 2 个联赛 canonical，没有做全历史身份重扫：team_id 3927 CS Afumati → CS阿富马蒂（IFFHS 中文比赛页）；10835 FK Tauras → 塔拉斯（Sofascore 简中，托拉斯保留 alias）；119746 FC Elimai Semey → 叶利迈塞米（7M 中文队页并核对俱乐部身份）。league_id 298 Estonia Meistriliiga → 爱沙尼亚甲级联赛；345 Kazakhstan Premier League → 哈萨克斯坦超级联赛。来源链接及身份说明保存在共享 registry 的记录中。脚本重复执行幂等，无覆盖既有 canonical。
- 共享库提交 `d011fb513cd5239b924bf590554cdba0f51698bc` 已推送 `totalcorner-research-bridge/master`。本轮后 formal union 2,468：canonical 2,115、unresolved 353（85.70%）；M1 1,459/1,553（93.95%）；M1 OU-R1 52/52（100%）；MR1 AH 1,629/1,921（84.80%）；MR1 AI 声明镜像 M1 1,459/1,553（93.95%）。未匹配球队逐条 ID/name/league/system/reason 仍以共享库 `data/football_display_names/formal_scope_coverage.json` 为准；未确认名称不做猜译。
- 对 M1 最近实际保存的扫描 `M1_20261014T102912Z`（32 fixtures、64 team slots）执行隔离 display preflight：64/64 球队、10/10 联赛均已解析，`ALL_DISPLAY_NAMES_RESOLVED`，`strategy_gate=false`，`registry_mutated=false`。M1 回归测试 20/20、MR1 共用 registry/AI formatter 测试 4/4、`git diff --check` 全通过。Curator 再运行 `added:0`，确认幂等。
- 本轮没有 Telegram 发送或历史编辑；未改变 M1/MR1/MR1 AI 策略、模型、正式 ledger、结算或派单规则。此提交只确认了 3 个 formal team ID 和 2 个联赛名，尚余 353 个 formal team IDs 未获得可靠 canonical，任务继续进行。

## 2026-10-14 正式范围继续补齐（第二批）
- 以共享 master `d011fb51` 的 353 条当前 unresolved 为输入继续来源核验；新增 6 个正式 team ID 的中文名称：PFK Simurq（4308）→FK西穆克（中文俱乐部资料）；KS Flamurtari Vlore（14521）→法拿莫达利（中文足球俱乐部条目）；Turan Turkistan（84070）→图兰突厥斯坦（7M）；Metalurh Zaporizhya（42610）与 MFC Metalurh Zaporizhya（47790）均采用来源支持的扎波罗热冶金，两个 TotalCorner ID 分别保留且不合并；KF Teuta（42641）→图塔杜雷斯（雷速球队页）。来源链接、provider 名、team_id、联赛上下文与别名都记在共享 registry；中文源不能确认的其余队名不猜译。
- 新共享提交 `08d5220b86d413c5f627bf43ef2ab3082c3bb5d1` 已推送到 `totalcorner-research-bridge/master`。最新实算正式范围：2,468 IDs，2,121 canonical、347 unresolved，85.94%；M1 1,460/1,553（94.01%），M1 OU-R1 52/52，MR1 AH 1,634/1,921（85.06%），MR1 AI 声明镜像 M1 1,460/1,553（94.01%）。唯一共享 registry 全量 12,276 IDs/4,137 canonical；正式清单详见 `data/football_display_names/formal_scope_coverage.json`。
- 本轮 curator 重跑结果 `added:0`，确认幂等；`git diff --check` 通过。M1 telegram display 定向测试 6/6 pass；MR1 registry + AI formatter tests 4/4 pass，使用环境变量指向同一共享 registry。M1 display + formal-runtime 联合集成测试共 14 项，9 pass、5 fail；失败集中在现有正式运行通知夹具预期缺少 `999990001|AH` 条目及 `email_unknown` 计数，不涉及本轮触碰的名称 curation 文件；没有因这些错误修改正式 runtime/策略，需后续单独核查夹具兼容性。没有触发实际 Telegram 发送或历史编辑。
- 仅增量更新共享展示数据、来源记录、coverage 和既有 curator；策略/模型/参数/赛事范围/账本/结算/Telegram 派单规则保持不变。用户的历史“718”基数不是当前数；本节推进后仍有 347 个正式 team IDs 未获可靠 canonical，继续按真实清单处理。

## 2026-10-14 正式范围继续补齐（第三批）
- 从当时 formal unresolved 中补入 7 个有明确中文足球资料对应的 ID：Pogradeci（43827）→堡加迪斯（中文维基条目）；Sportist Svoge（72314）→斯夫格、Vihren Sandanski（42571）→韦伦桑丹斯基、FC Sevlievo（42783）→FC塞弗列沃（雷速中文联赛/球队上下文）；Muscelul Campulung（110588）→坎普龙（雷速）；Skanstes SK（86496）→斯坎斯特、Ogre United（144725）→奥格雷联（7M）。保留原 team ID/provider name、别名和来源引用，没有合并不同 TotalCorner ID。
- 共享库提交 `e165c02f624bdcc8b55724963aa04e698107179b` 已推送 `totalcorner-research-bridge/master`。最新实算 formal union 2,468：canonical 2,128、unresolved 340、覆盖率 86.22%；M1 1,461/1,553（94.08%）；M1 OU-R1 52/52（100%）；MR1 AH 1,641/1,921（85.42%）；MR1 AI declared mirror M1 1,461/1,553（94.08%）；历史 MR1 AI confidence≥50 cohort 181/182（99.45%）。剩余完整清单见唯一共享库 `data/football_display_names/formal_scope_coverage.json`；curator 重跑 `added: 0`，`git diff --check` 通过。
- 本地 formatter 验证：M1 display tests 6/6 通过；MR1 shared-registry + MR1 AI formatter Node tests 4/4 通过（环境显式指向最新共享 registry）。这是隔离测试，不代表新生产扫描或 Telegram 收据。M1 AH 与 OU-R1 共用 M1 formatter；MR1 AH/MR1 AI formatter 使用共享 registry，策略和账本仍独立。
- 本轮未触发历史 Telegram 修复 workflow，也未编辑或重发旧消息。M1 name-only 工具需要 `M1_TELEGRAM_BOT_TOKEN`、`M1_TELEGRAM_CHAT_ID`；本机运行环境两者缺失。MR1 AH/AI 需由既有专用 workflow 写入各自 edit receipts。当前 Actions 账户限制仍是实际执行阻碍，因此本轮历史 Telegram 编辑成功数为 0，不能宣称历史消息已修复；继续按已知原因保留无法编辑/缺原文的旧消息，不重发。
- 针对剩余球队做了定向中文来源查询，但 Csakvari TK、Balmazujvaros、埃及地区队及部分巴尔干/北爱尔兰低级别球队本轮仍无足以确认 canonical 的中文来源；这些记录保留 provider 英文身份并标 `NO_VERIFIED_CANONICAL_ZH`，不以猜译填充。未改 M1/MR1/MR1 AI 策略、模型、参数、赛事范围、正式订单或结算。

## 2026-10-14 共享库增量后的历史 Telegram 实际复核
- 在用户授权的 names-only / no-resend 范围内，用 quant-runner 既有工作流读取最新共享 master 并处理旧消息；没有创建 Pick、发送新消息或更动交易内容。
- M1 含 AH 与 OU-R1 的 run [38559663544](https://github.com/ljm198964-alt/quant-runner/actions/runs/38559663544) SUCCESS：41 eligible，4 EDITED、37 ALREADY_MATCHING，0 failed；另 99 条缺已保存原文、94 条因现有映射不足跳过。报告中 4 次编辑均为名称字段改动。该 workflow 将报告作为 artifact 保存，不改正式 ledger/结算。
- MR1 AH run [38559668601](https://github.com/ljm198964-alt/quant-runner/actions/runs/38559668601) SUCCESS：0 edited、125 already processed/skipped、0 unresolved、0 failed；edit receipt 写入 MR1 master commit `665970baab`（随后 MR1 AI receipt 更新远端 master）。
- MR1 AI run [38559674257](https://github.com/ljm198964-alt/quant-runner/actions/runs/38559674257) SUCCESS：201 条历史记录中，192 unresolved；9 条有 message ID 的候选全部被 Telegram 拒绝，HTTP 400 `message to edit not found`；实际编辑 0。失败回执 commit `dc2914c64043c318df534aa84a8e9806e1bca716` 已推送 MR1 master。不得重发这些历史消息或把 workflow SUCCESS 写成消息编辑成功。
- 本次历史消息实际编辑合计 4 条，全部来自 M1（含 AH/OU-R1）；MR1 AH 0、MR1 AI 0。未来新消息仍由各自 formatter 读取同一个 canonical registry；本机定向测试 M1 6/6、MR1 4/4 PASS。生产策略、模型、参数、范围、正式 Pick、ledger 与 settlement 均未修改。

## 2026-10-14 再补一条并验证幂等
- 对剩余 formal names 再查现成公开中文资料，补 team_id 15224 `ASK Bravo Publikum` → 布拉沃佩利根，中文球队资料来源 https://www.qtx.com/dbsoccer/team_138792.html；映射保留 TotalCorner ID、原名和 aliases。共享提交 `d541916cf9776d6a0077d453ebc776e4f15f2510` 已推送 master。formal union 更新为 2,468 IDs、2,129 canonical、339 unresolved（86.26%）；共享 registry 12,276 IDs、4,145 canonical。curator 再跑 `added:0`，`git diff --check` pass。
- 新映射后再次运行 M1 历史 names-only 工作流 [38560323027](https://github.com/ljm198964-alt/quant-runner/actions/runs/38560323027)：SUCCESS，41 eligible、0 新编辑、41 already matching、99 缺原文、94 unresolved/unmapped、0 failed。说明旧消息当前均已是当下 registry formatter 的名称输出；没有重发。

## 2026-10-14 再续补 Loznica 并完成三链复核
- 新增 team_id 12966 `Loznica` → 洛兹尼察，来源为 [Sofascore 简中球队页](https://www.sofascore.com/zh/football/team/fk-loznica/203041)，并以 TotalCorner league_id 337 的塞尔维亚一级联赛身份交叉核对。保留 provider 原名与 ID。共享提交 `6bfc94ca6db90ba8a0d697a42f46ebb0fec6f6e5` 已推送 master。最新 formal union 2,468：canonical 2,130、unresolved 338（86.30%）；M1 1,462/1,553（94.14%）；M1 OU-R1 52/52（100%）；MR1 AH 1,642/1,921（85.48%）；MR1 AI mirror M1 1,462/1,553；observed confidence≥50 cohort 181/182（99.45%）。curator 幂等结果 `added:0`。
- M1 历史修复 [38560880090](https://github.com/ljm198964-alt/quant-runner/actions/runs/38560880090) SUCCESS：41 eligible、0 edited、41 already matching、99 missing source text、94 unmapped、0 failed。MR1 AH 历史修复 [38560886576](https://github.com/ljm198964-alt/quant-runner/actions/runs/38560886576) SUCCESS：0 edited、125 already processed、0 unresolved、0 failed。MR1 AI 历史修复 [38560893085](https://github.com/ljm198964-alt/quant-runner/actions/runs/38560893085) 在 Telegram 检查后写回 receipts 时失败：本轮仍是 9 个旧 message IDs 均 `message to edit not found`、192 unresolved、0 edited；随后其他 MR1 runtime 同时更新了 master，发生 Git ref lock/CAS 冲突，导致回执 push 被拒。Telegram 本身未编辑任何消息；前次同类失败回执已保存在 MR1 master `dc2914c64043c318df534aa84a8e9806e1bca716`。
- 最新共享 registry 定向回归：M1 formatter 6/6 PASS；MR1 shared registry + AI formatter 4/4 PASS；`git diff --check` PASS。没有策略、模型、订单、账本或结算更改，也未重发历史订单。

## 2026-10-14 后续正式名称增量
- 继续复核现有中文足球页面后，新增两支 formal team：ASK Bravo Publikum（15224）→布拉沃佩利根（球天下 https://www.qtx.com/dbsoccer/team_138792.html）；Loznica（12966）→洛兹尼察（Sofascore 简中 https://www.sofascore.com/zh/football/team/fk-loznica/203041）。随后新增 Hanacka Slavia Kromeriz（2545）→克罗梅日什哈拿茨卡斯拉维亚（LiveScore 简中 https://www.livescore.com/zh/zuqiu/team/sk-hanacka-slavia-kromeriz/82979/overview/；Tips.GG/雷速短译保留为 alias）。保留 TotalCorner ID 和原名，不做实体合并。
- 最新共享 master `bfb3e816b5542df280331b962e855a26aa8778e8` 已推送。formal union 2,468：canonical 2,131、unresolved 337（86.35%）；M1 1,462/1,553（94.14%）；M1 OU-R1 52/52；MR1 AH 1,643/1,921（85.53%）；MR1 AI mirror M1 1,462/1,553，confidence≥50 cohort 181/182（99.45%）。Curator 重跑 `added:0`，`git diff --check` 通过。
- M1 Telegram display tests 6/6、MR1 shared registry/AI formatter tests 4/4 通过。检索 M1 与 MR1 AH/AI 历史正式 ledger 未发现 Kromeriz 相关订单，因此没有触发不必要的历史编辑；既往实际历史编辑数不变。尚余 337 个正式 ID 未有足够可靠中文 canonical，列表与原因仍以唯一共享 registry 的 coverage 文件为准。

## 2026-10-14 正式名称增量：保加利亚与希腊队
- 基于最新 unresolved 清单，补入 3 个可核验的正式球队映射：`43177 Minyor Pernik` → 明约佩尼克（中文维基俱乐部条目；佩尔尼克矿工足球俱乐部/明约匹尼克作 alias）；`43234 Dobrudzha 1919 Dobrich` → 多布里奇（LiveScore 简中球队页及中文联赛资料）；`43266 AE Kifisias` → 基菲萨（楚棋中文球队页，7M 同队常见译名保留 alias）。三个 TotalCorner team_id、原英文 identity、league IDs 与来源说明均写入唯一共享 `display_names.json`，无 ID 合并或原字段改写。
- 共享库 master 已推送提交 `9a949b0bd7a205bd9ffcbaa165fa59fc6e60259a`。本次最终文件实算：formal union 2,468，canonical 2,134、unresolved 334，覆盖率 86.47%；M1 1,463/1,553（94.20%）；M1 OU-R1 52/52（100%）；MR1 AH 1,645/1,921（85.63%）；MR1 AI declared mirror 1,463/1,553（94.20%）；全共享 registry 12,276 IDs、4,150 canonical（33.81%）。剩余逐条清单/原因以共享 master 的 `formal_scope_coverage.json` 为准。
- M1 Telegram display tests 6/6 通过；MR1 shared registry + MR1 AI formatter tests 4/4 通过（显式指向同一共享库）；`git diff --check` 通过。M1 AH 与 OU-R1 沿用同一 formatter，MR1 AH/AI 读取同一 canonical registry，后台账本与去重仍各自独立。M1 正式账本中未发现这三队的 Telegram 正式订单；`Dobrudzha` 仅出现在扫描/市场研究记录，不能据此编辑 Telegram。没有因此触发或发送消息；历史消息此前实绩仍为 M1 4 条编辑、MR1 AH/AI 0 条编辑（旧消息 Telegram 返回 message-not-found，详见前节）。本批没有新增可安全编辑的历史消息。
- 只更新展示名称 curation、共享映射与审计；没有改任何策略、模型、盘口、正式订单/账本/结算或派单规则，也没有触发生产扫描/Telegram。继续逐条处理剩余 334 个正式 unresolved，不虚构中文名。

## 2026-10-14 正式范围继续补齐：Vlasenica
- 在当前正式 unresolved 清单中确认 `12512 FK Vlasenica` 有雷速中文球队页直接标注“FK弗拉塞尼察”，并与 TotalCorner 的 Bosnia and Herzegovina 1st League (`league_id=911`) 身份对应；将该 canonical 及 Vlasenica/Fudbalski klub aliases 写入唯一共享 registry。
- 共享 master 提交 `7aa62690d1e89a8e89ed42ac696f91842c8d8bf1` 已推送。正式并集现为 2,468：2,135 canonical、333 unresolved（86.51%）；M1 1,464/1,553（94.27%）；M1 OU-R1 52/52；MR1 AH 1,647/1,921（85.74%）；MR1 AI mirror 1,464/1,553（94.27%）；共享 registry 12,276 IDs、4,151 canonical（33.81%）。
- M1 formatter tests 6/6、MR1 shared registry/AI formatter tests 4/4 通过；定向展示使用单一 shared registry。此次只增补名称/来源/coverage，无模型或策略变更，未发或编辑 Telegram。该映射对应 MR1 formal scope；没有据此推断存在已发送历史订单。其余 333 条继续逐项核实，不猜译。

## 2026-10-14 正式名称增量：Viimsi 与 IMT
- 新增两条直接简中来源：`18546 IMT Novi Belgrade` → IMT新贝尔格莱德（17500 简中赛程页，QTX 简中比赛记录交叉核对；Beograd/Belgrade 为同一城市拼写）；`30301 Viimsi JK` → 维姆西（Sofascore 简中一线队页面）。特别核验 7M 搜索结果所示的是 `Viimsi JK Women's` 且有不同 provider ID，因此没有将女队映射到男队 ID 30301。
- 共享库 master 已推送 `c4baac493b1218e6ff99313e18c0067c9d5e78ea`。formal union 2,468 IDs：2,137 canonical、331 unresolved（86.59%）；M1 1,464/1,553（94.27%）；M1 OU-R1 52/52；MR1 AH 1,649/1,921（85.84%）；MR1 AI mirror 1,464/1,553（94.27%）；shared registry 12,276 IDs、4,153 canonical（33.83%）。完整未匹配项继续查共享库 coverage 文件。
- M1 Telegram formatter tests 6/6、MR1 shared registry/AI formatter tests 4/4 pass，`git diff --check` pass。M1 formal ledger、MR1 AH sent/AI sent-prospective ledgers 未找到这两队对应订单；未发送或编辑 Telegram。仅更新展示 registry/来源审计与 curator，不改模型/策略/账本/结算。继续处理剩余 331 个 ID。

## 2026-10-14 正式范围名称增量：Jedinstvo UB 与 Academica Clinceni
- 新增 `33419 Jedinstvo UB` → 乌布耶丁斯特沃（中文球队资料页明确对应 FK JEDINSTVO UB；league IDs 303/337 保留）；`33772 FC Academica Clinceni` → 克林辛尼学院（中文欧洲俱乐部名录 crosswalk）。后者限定为历史 Academica Clinceni identity，不因关联实体后续重组为 LPS HD/Inter Ilfov 而改写历史 ID/名称。
- 共享 registry `display_names.json` 已推送 `adac353f3dbe84df151c2a23c1ebd1ce3630f589`。最新 formal union 2,468：2,139 canonical、329 unresolved（86.67%）；M1 1,467/1,553（94.46%）；M1 OU-R1 52/52；MR1 AH 1,650/1,921（85.89%）；MR1 AI mirror 1,467/1,553（94.46%）；shared registry 12,276 IDs、4,155 canonical（33.85%）。
- M1 formatter 6/6、MR1 shared registry/AI formatter 4/4 PASS，diff check PASS。M1 formal ledger 与 MR1 AH/AI send/prospective evidence 中未检出这两队的订单，本批无安全可改历史 TG；未发送/编辑 Telegram。仅映射、来源和审计变化，生产模型、策略、账本与结算保持原样；尚有 329 个 formal IDs 待核验。

## 2026-10-14 正式范围继续增量：希腊、科索沃、马其顿与埃及
- 在远端最新共享 registry `adac353f3dbe84df151c2a23c1ebd1ce3630f589` 基础上继续处理，无覆盖旧映射。本次新增 5 个精确正式 ID：`39946 KF Ferizaj`→费里扎伊（Tips.GG 简中比赛档案）；`42581 Egaleo`→埃加莱奥、`42792 Makedonikos`→马其顿尼科斯（Tips.GG 简中球队/比赛页）；`4609 FK Kozuv Gevgelija`→科祖夫（Tips.GG 简中比赛档案）；`10612 Sed Elmahla`→赛德艾尔玛拉（雷速球队页明确给出英文/简中名称）。来源及交叉身份说明已随唯一 `display_names.json` 保存；不合并相似球队。
- 最新本地正式范围实算（coverage `generated_at=2026-10-14T12:27:37Z`）：正式 union 2,468，canonical 2,144、unresolved 324，覆盖 86.87%；M1 1,469/1,553（94.59%）；M1 OU-R1 52/52；MR1 AH 1,654/1,921（86.10%）；MR1 AI declared mirror 1,469/1,553（94.59%）；共享库 12,276 IDs、4,160 canonical。余下 324 的 team_id、provider 英文名、league IDs、系统归属和 `NO_VERIFIED_CANONICAL_ZH` 原因完整保留在唯一共享库 `data/football_display_names/formal_scope_coverage.json` 的 `unresolved_records`。
- 验证：M1 display formatter 6/6 PASS；MR1 shared registry/MR1 AI formatter 4/4 PASS，确认 MR1 使用挂载的同一共享库；`git diff --check` PASS。针对本次 5 个英文 identity 的定向查找未在 M1 正式账本及 MR1 AI 发送/前瞻 ledger 中发现对应策略消息，因此没有可确认的旧 TG message ID 可编辑；未调用 Telegram、未发送/编辑消息。历史消息更广范围编辑仍未完成。
- 当前变更待提交/推送至共享库仓库；本机 `quant-runner` 交接工作区仍在 `6752840081932906b79c56670b1b0dfe34f42901`，本轮 GitHub HTTPS fetch 曾返回 `SSL_ERROR_SYSCALL`，因此交接更新和两仓库 push 尚未完成。待网络恢复后先核对远端头，再提交共享库数据与本交接记录；不要误报云端部署或历史 Telegram 编辑成功。
- 本次仅涉及名称展示映射、curation/coverage 审计和 handoff；没有修改模型、策略、盘口、正式范围、订单/结算账本或 Telegram 派单规则。

## 2026-10-14 正式范围继续核名：Vitosha 与 FK Čelik
- 在共享 master `c69a09079042fb32e9d534048a06330309265550` 基础上继续处理 unresolved。新增 `40493 FK Celik` → `尼克希奇钢铁`，依据简体中文尼克希奇钢铁俱乐部条目（https://zh.wikipedia.org/wiki/尼克希奇钢铁足球俱乐部），TotalCorner `league_id=47`、原 team ID 与 FK Čelik Nikšić identity 保持绑定；`40821 FK Vitosha` → `比斯特里察维托沙`，依据 Sofascore 简中队页（https://www.sofascore.com/zh/football/team/fc-vitosha-bistritsa/113703），并保留“维托沙”别名。两项均不覆盖既有 canonical，也不合并不同球队。
- 共享库最新实算：formal union 2,468 IDs，2,155 canonical、313 unresolved，覆盖率 87.32%；M1 1,474/1,553（94.91%）；M1 OU-R1 52/52（100%）；MR1 AH 1,660/1,921（86.41%）；MR1 AI declared mirror 1,474/1,553（94.91%），retained confidence≥50 cohort 181/182（99.45%）。全 registry 12,276 IDs、4,171 canonical；313 个剩余正式未匹配项及 `NO_VERIFIED_CANONICAL_ZH` 原因见共享库 `data/football_display_names/formal_scope_coverage.json`。
- M1 display tests 6/6 PASS；MR1 shared-registry / AI formatter tests 4/4 PASS，测试使用本轮共享 registry；`git diff --check` PASS。未触发生产扫描、未发送或编辑 Telegram。本轮历史 TG 编辑 0；旧消息修复状态仍按上节记录，不把 formatter 测试当成线上消息编辑证据。
- 共享库变更与本交接更新随后分别提交推送；仅名称、来源、coverage/curation 报告及 handoff 变化。未修改 M1、MR1 AH、MR1 AI 的策略、模型、阈值、范围、正式 ledger、结算或发单规则。
- 历史消息工作流随后实际复核完成：M1 run [38566139404](https://github.com/ljm198964-alt/quant-runner/actions/runs/38566139404) SUCCESS，41 条 eligible 均 `ALREADY_MATCHING`，0 编辑、0 失败；另 99 条缺原文、94 条无映射/安全替换。MR1 AH run [38566145896](https://github.com/ljm198964-alt/quant-runner/actions/runs/38566145896) SUCCESS，0 编辑、125 条已处理/跳过、0 unresolved/failed。MR1 AI run [38566151168](https://github.com/ljm198964-alt/quant-runner/actions/runs/38566151168) SUCCESS，但 9 个已有 message ID 的 Telegram edit 均实际失败 `400 message to edit not found`；192 条无可安全确定的编辑资料，实际编辑 0。工作流 SUCCESS 仅表示程序/回执步骤结束，不表示 Telegram edits 成功；没有重发消息。

## 2026-10-14 后续复核：埃及、冰岛与塞浦路斯队名
- 再次以最新共享 registry 为基线，本轮确认并新增 `8690 Volsungur`→沃尔松古尔·胡萨维克（SportScore 简中比赛页与 Titan007 简中球队页交叉对应）；`10776 Belqas`→贝尔卡斯城（Football Kit Archive 简中 Egyptian Second Division B 队页标注 Belqas City SC / Delta United FC，另有中文赛果记录使用“贝尔卡斯”）；`15887 Digenis Morphou`→迪加尼斯莫尔富（中文 Digenis Akritas Morphou 俱乐部条目，规范化为简体）。保留 provider IDs 和英文身份，不将女队或相似俱乐部合并。
- 共享提交 `ac2f8829` 已将 formal coverage 推至 2,157/2,468（87.40%）；后续 `45660b48a5ab72233209b7b250183556ee5912e6` 加入 Digenis 后，当前为 2,158/2,468（87.44%），310 unresolved。全库 12,276 IDs / 4,174 canonical；M1 1,474/1,553，MR1 AH 1,663/1,921，M1 OU-R1 52/52；MR1 AI follows its declared M1 mirror at 1,474/1,553. 最新明细以共享 master `data/football_display_names/formal_scope_coverage.json` 为准。
- 最新增量的 M1 formatter tests 6/6 与 MR1 shared-registry/AI tests 4/4 均通过；历史 Telegram 的三条 workflow 结果沿用上一节，新增名称之后没有再次运行历史编辑工作流，也没有触发任何发送/编辑。名称库工作继续，remaining formal team IDs 不可用无来源音译补齐。
- 随后核验 `44911 NK Igman Konjic`：简体中文俱乐部条目把其展示 clubname 标为“列文科尼茨”，2025/26 中文波黑顶级联赛球队表也将“列文科尼茨”与 FK Igman Konjic 对应；TotalCorner `league_id=33` 与同一科尼茨俱乐部赛事身份一致。该 alias/显示名新增至 shared registry（提交 `119d21ad6791f94412aa5fdf8e9385c6e5a82e2b`）；当前 formal union 2,159/2,468（87.48%），309 unresolved；shared registry 12,276 IDs / 4,175 canonical，M1 1,474/1,553，M1 OU-R1 52/52，MR1 AH 1,664/1,921，MR1 AI mirror 1,474/1,553。对应 formatter tests 再次通过（M1 6/6，MR1 4/4）。此更新没有触发历史 Telegram 编辑。

## 2026-10-14 正式范围中文名称续补：北爱尔兰、匈牙利、威尔士、埃及与乌克兰
- 在最新共享库 `totalcorner-research-bridge/master` (`c69a0907f5…`) 基础上，只写入公开中文来源可核验且与 TotalCorner team_id/联赛一致的映射：`23695 Portstewart`→波特斯图尔特、`11406 Coagh Utd`→科阿联队、`39562 Dollingstown`→多林斯敦、`31174 AL Fayoum`→法尤姆FC、`8137 SW Bregenz`→布雷根茨、`7338 Renova Dzepciste`→雷诺瓦、`15380 Pontypridd Town`→庞蒂普里德、`69357 FC Nagykanizsa`→纳吉卡尼扎（只限男队 ID，不映射女队）、`43026 FK Lviv`→利沃夫。原 ID、英文名、别名、league IDs 和每条来源证据均在唯一 `display_names.json` 中；没有合并身份。
- 正式范围从 2,468 IDs / 2,144 canonical / 324 unresolved 更新为 2,468 / 2,153 / 315（87.24%）。M1 为 1,472/1,553（94.78%）；M1 OU-R1 52/52（100%）；MR1 AH 1,660/1,921（86.41%）；MR1 AI declared mirror of M1 1,472/1,553（94.78%）。整个共享 registry 12,276 IDs、4,169 canonical。315 条未匹配记录全部有 `NO_VERIFIED_CANONICAL_ZH` 原因，完整 team_id/name/league/system 清单见共享 `data/football_display_names/formal_scope_coverage.json`。
- 验证：M1 Telegram formatter tests 6/6 PASS；MR1 shared registry + MR1 AI formatter tests 4/4 PASS（测试显式读取唯一共享库）；`git diff --check` PASS。M1 AH/OU-R1 继续使用 M1 formatter；MR1 AH/AI 使用共享 registry；后台 ledger/dedupe 隔离保持不变。
- 历史 Telegram：本轮没有执行 API 编辑或重新发送。此前 dry-run 的 M1 history repair 41 eligible、99 缺原消息文本、94 无映射/无安全替换、实际改写 0；本机未配置可用 M1/MR1 Telegram 发送凭据，且没有找到安全的现成编辑 workflow。不能声称任何历史 TG 已修复。新名称写入 registry 并推送不等于生产进程已拉取或历史消息已编辑。
- 共享库提交 `c69a0907f5…` 已推送 master。此 handoff 更新不改变模型、策略、范围、账本、结算、盘口或 Telegram 派单逻辑。后续继续逐条核验剩余 315 项，不用临时音译填充。

## 2026-10-14 正式名称续补及历史 Telegram 编辑验收（当前）
- 基于共享库当时最新 master `119d21ad6791f94412aa5fdf8e9385c6e5a82e2b`，补入两个可核验 canonical：`10310 Csakvari TK`→查克瓦里（Tips.GG 简中球队页），`7590 Meshakhte Tkibuli`→梅沙赫特（OddsGPT 简中比赛/积分资料）；并补联赛 `41 Hungary Cup`→匈牙利杯、`241 Hungary NB II`→匈牙利足球乙级联赛。来源链接及 identity 证据随映射保存在唯一共享库。对仍未找到可靠简中标准名的名称不猜译，例如错误机翻的 Sirens（“警报”）不采纳。
- 共享库已推送提交 `c9e4bc204555f297d0f0f882278014c6a67ac16c`。最终文件实算：formal union 2,468，canonical 2,161，unresolved 307（87.56%）；M1 1,475/1,553（94.98%）；M1 OU-R1 52/52（100%）；MR1 AH 1,666/1,921（86.73%）；MR1 AI declared mirror of M1 1,475/1,553（94.98%）；历史 confidence≥50 cohort 181/182（99.45%）。共享库 12,276 team IDs / 4,177 canonical，league IDs 771 / 334 canonical。全量剩余307项的 ID、英文身份、联赛、系统和未匹配原因在共享 `data/football_display_names/formal_scope_coverage.json` 的 `unresolved_records`。
- 隔离 formatter 验证：M1 输出包含“匈牙利足球乙级联赛 查克瓦里”及“格鲁吉亚甲级联赛 梅沙赫特”；MR1 shared display helper 对相同 IDs 输出相同中文。M1 display/repair/formal-runtime pytest 20/20 PASS；MR1 shared registry/AI formatter Node tests 4/4 PASS；JSON 和 diff check PASS。
- 三条既有历史名称编辑 workflow 已在新 registry 推送后实际运行：M1 [38568037059](https://github.com/ljm198964-alt/quant-runner/actions/runs/38568037059) SUCCESS，`eligible=41, edited=0, already_matching=41, failed=0, missing_original_text=99, unresolved=94`；因此本轮 M1 没有需要编辑的新消息，41条均已经匹配。MR1 AH [38568036201](https://github.com/ljm198964-alt/quant-runner/actions/runs/38568036201) SUCCESS，`edited=0, skipped/already_processed=125, unresolved=0, failed=0`。MR1 AI [38568035660](https://github.com/ljm198964-alt/quant-runner/actions/runs/38568035660) SUCCESS，但 edit report 为 `total=201,candidates=9,edited=0,failed=9,unresolved=192`；9个 Telegram edit 均返回 `400 message to edit not found`，其余192条没有安全可编辑的匹配资料。MR1 AI 回执提交 `20982a4fb3`；未重发任何历史订单。Workflow success 只表示修复脚本及回执持久化步骤完成，不代表 Telegram edit 成功。
- 只改共享展示名库、审计和本 handoff；没有改 M1、M1 OU-R1、MR1 AH/AI 的模型、策略、范围、正式 ledger、settlement、Telegram 出单规则或历史交易内容。历史 message edit 实际成功数本轮为0（M1 0、MR1 AH 0、MR1 AI 0）；Telegram 实际失败9（均为 MR1 AI 400 message not found），M1另有99缺原文、94未映射，MR1 AI另有192 unresolved。正式范围剩余307项继续按证据逐条处理。

## 2026-10-14 追加：威尔士球队中文名
- 新增 `30294 Penrhiwceiber Rangers`→彭里赫齐伯流浪者，来源为 Tips.GG 简中威尔士杯球队表（页面直接展示“彭里赫齐伯流浪者”）；映射保留 TotalCorner team ID 与 provider 原名。共享库提交 `08d76d7814334c0388e80255d9707e085149898b` 已推送 master。
- 当前正式范围实算：2,468 IDs，2,162 canonical / 306 unresolved（87.60%）；M1 1,475/1,553（94.98%）；M1 OU-R1 52/52；MR1 AH 1,666/1,921（86.73%）；MR1 AI declared M1 mirror 1,475/1,553（94.98%）；共享库 12,276 IDs / 4,178 canonical，联赛 334/771。剩余306条完整身份、系统归属和未匹配原因见共享 `formal_scope_coverage.json`。
- M1定向测试20/20通过；MR1共享映射/AI formatter测试4/4通过；隔离渲染正确显示新增名称。检查 M1 正式账本与 MR1 AH/AI 已发送记录，team IDs 10310、7590、30294 均无历史 TG 订单，因此上方在共享提交 `c9e4bc20` 后完成的历史编辑 workflow 结果仍适用于本批，没有因名称更新重复编辑/发送。此处只更新名称库及交接，无模型、策略、账本或交易规则变化。

## 2026-10-14 正式范围继续补齐（追加）
- 从当前共享 master `2e1288c20a58a072e3483f4a6d6a250c98739a4d` 的正式 unresolved 清单出发，再补 3 个可核实 ID：Rudar Kakanj（9157）→卡坎吉鲁达尔（Tips.GG 简中比赛页）；NK Jarun（30623）→雅鲁恩队（Tips.GG 简中球队对阵页）；FC Hebar Pazardzhik（42568）→赫巴（中国足球数据球队资料页）。来源 URL、provider 原名、team ID、别名均在共享 `display_names.json` 留档；无公开中文惯用名证据的球队仍保留 unresolved。
- 最新共享 master 为 `2e1288c20a58a072e3483f4a6d6a250c98739a4d`。按提交时最新 `formal_scope_coverage.json`：2,468 formal IDs，2,165 canonical、303 unresolved，覆盖 87.72%；M1 1,476/1,553（95.04%），M1 OU-R1 52/52（100%），MR1 AH 1,670/1,921（86.93%），MR1 AI declared mirror M1 1,476/1,553（95.04%）。完整未匹配名称、ID、联赛及系统范围以该文件 `unresolved_records` 为准。
- 定向检查本地 M1 正式 ledger 与可访问的 MR1 AI prospective records，没有发现 team IDs 9157、30623、42568 对应的已发送订单，因此新增名称没有待编辑的历史 TG 文本。最近一次名称修复实际回执仍是前节记录：M1 编辑4条；MR1 AH编辑0条；MR1 AI编辑0条（9条旧消息由 Telegram 返回400 `message to edit not found`，192条 unresolved）。当前未为这3个 ID 再触发 workflow，未重发或修改任何旧消息。
- M1 formatter/formal-runtime 定向回归此前20/20通过；MR1 registry/AI formatter此前4/4通过。共享工作区保持 clean；本追加只更新交接文档，不涉及生产代码、模型、策略、范围、账本、结算或派单条件。任务仍未完成：303 formal IDs 尚无可靠 canonical 中文名，需继续核证。

## 2026-10-14 正式范围继续补齐（第四批）
- 在保留既有 canonical 的前提下，新增正式 team_id 11023 `Queens University` → 贝尔法斯特女王大学。简中名称依据[贝尔法斯特女王大学中文资料](https://zh.wikipedia.org/wiki/贝尔法斯特女王大学)，球队身份由[Queen's University Belfast AFC 官方历史](https://www.qubafc.com/history)及 Northern Ireland Championship league_id 765 交叉确认。共享 registry 最新 master 提交 `1ac2efcaa24d86d12bd675b4a6e918998af93c74`；本轮新增1队，现正式范围 2,468 IDs、2,166 canonical、302 unresolved（87.76%）。M1 1,476/1,553（95.04%）、M1 OU-R1 52/52、MR1 AH 1,671/1,921（86.99%）、MR1 AI mirror M1 1,476/1,553（95.04%）。
- 查询本机 M1 正式 ledger 和现存 MR1 AH/AI 正式记录时，未发现新增 ID 9157、30623、42568、11023 对应的已发送 Pick，故无需为它们回补或编辑历史 TG 文本。既有历史修复回执不变：M1 4条编辑成功；MR1 AH 0条；MR1 AI 0条，9条旧消息由 Telegram 拒绝（400 `message to edit not found`）、192条 unresolved。无重发。
- 本轮直接使用最新共享目录隔离验证：M1 `test_m1_telegram_display.py` 6/6通过；MR1 shared registry 与 AI formatter Node tests 4/4通过。M1 合并执行 display+formal-runtime tests 为9通过、5失败，失败仍为既有 fixture 的 candidate key/notification count 预期不匹配（与名称 formatter 无关）；没有改 runtime 来绕过。共享 JSON 解析和 `git diff --check`通过。未触发云端生产 runtime或 Telegram。
- 最新 `formal_scope_coverage.json` 为本轮统计的唯一依据，302个未匹配明细全部留在其 `unresolved_records`。名称代码和正式策略数据未动；本轮仍属于局部补充，未完成全覆盖。

## 2026-10-14 正式范围继续补齐（第五批）
- 新增 team_id 43931 `FC Podillya Khmelnytskyi` → 波迪利亚赫梅利尼茨基。Tips.GG 简中球队档案和对阵页直接使用该译名，分别见 https://tips.gg/cn/team/podillya-khmelnytskyi-football/ 和 https://tips.gg/cn/archive/bratslav-vinnytsia-football-vs-podillya-khmelnytskyi-football/；正式 provider name、team ID 与乌克兰赛事上下文保持原样。最新共享 master 提交 `638c95f34ba2081f00321cda06aab6d67e5b4b99`，formal union 2,468、canonical 2,167、unresolved 301（87.80%）；M1 1,476/1,553（95.04%）、OU-R1 52/52、MR1 AH 1,672/1,921（87.04%）。
- M1 ledger 对本轮已核实的 9157、30623、42568、11023、43931 均无对应已发送 Pick；没有历史消息需重发或编辑。MR1 AH/AI 的正式回执工作流历史结果仍见 2026-10-14 既有记录，本轮未重复触发或修改 Telegram。
- 使用此最新共享 registry 的隔离 formatter 检查：M1 Telegram display 6/6通过，MR1 shared-registry + AI formatter 4/4通过。M1 formal-runtime 集成夹具的5个已知失败仍单独记录，未修改运行逻辑。完整剩余301项及原因见共享 `formal_scope_coverage.json`；尚未达到全覆盖。

## 2026-10-14 正式范围继续补齐（第六批）
- 新增 team_id 8761 `FK Backa Palanka` → 巴奇卡帕兰卡。Sofascore 简中队页使用该名称，中文球队资料将 FK Bačka Bačka Palanka 与该俱乐部对应；按名称沿革，不与 FK Bačka 1901 或其他同名球队合并。共享 master 最新提交 `b51cdd1bc7c17255e4302ca06db4ba7bf8fafd52`。formal union 2,468：2,168 canonical、300 unresolved（87.84%）；M1 1,476/1,553（95.04%），OU-R1 52/52，MR1 AH 1,673/1,921（87.09%），MR1 AI mirror M1 1,476/1,553（95.04%）。
- M1 Telegram display tests 6/6通过；MR1 shared-registry + AI formatter tests 4/4通过。M1 正式 ledger 未发现 team_id 8761 对应的既有 Pick；未触发历史消息编辑、重发或生产 workflow。
- 剩余300条的完整 ID/名称/联赛/系统归属及原因仍以共享库 `data/football_display_names/formal_scope_coverage.json` 为准。未修改模型策略、范围、订单、结算或派单规则。

## 2026-10-14 正式范围继续补齐（第七批）
- 根据 Tips.GG 简中阿尔巴尼亚杯页面，本轮新增 `KS Kastrioti Kruje`（48501）→卡斯特里奥蒂克鲁耶、`KS Besa Kevaje`（43150）→贝萨卡瓦耶、`KS Korabi Peshkopi`（43752）→科拉比佩什科皮。页面以中文显示对应球队/比赛，保留 TotalCorner team_id 和英文原名；Besa 的 Kavaje/Kevaje 是拼写 alias，不扩成实体合并。来源页：https://tips.gg/cn/tournament/football-albanian-cup-2024-25/。
- 共享 registry 最新 master 提交 `bafc42ce06a0dcd38257e0588f1e4ae6df74a277`。最新实算：formal 2,468，canonical 2,171、unresolved 297（87.97%）；M1 1,477/1,553（95.11%）；M1 OU-R1 52/52；MR1 AH 1,675/1,921（87.19%）；MR1 AI mirror M1 1,477/1,553（95.11%）。297项逐项详情以唯一共享 `formal_scope_coverage.json` 为准。
- formatter 回归使用最新共享库：M1 Telegram display tests 6/6通过；MR1 registry/AI formatter tests 4/4通过。无生产扫描、Telegram 发送/编辑；策略、模型、范围、ledger、settlement 均未修改。完成度仍非全量。

## 2026-10-14 正式范围继续补齐（第八批）
- 为正式范围 `FK Zhenys`（team_id `99519`，league_id `345`）核实中文名“珍尼斯”。Tips.GG 简中哈萨克斯坦球队对阵页直接以“珍尼斯”标注 Zhenis：https://tips.gg/cn/archive/fc-kairat-almaty-football-vs-zhenis-football/；保留 TotalCorner provider identity、team ID 与既有联赛，不合并其他球队。唯一共享 registry master 提交 `3636fd8aa972e441e7a9eefe07ee3708d8d4a979` 已推送。
- 从提交后的 `formal_scope_coverage.json` 实算：正式范围 2,468 IDs，canonical 2,173、unresolved 295，覆盖率 88.05%；共享库 12,276 team IDs、4,189 canonical。完整未匹配清单和原因仍以该文件 `unresolved_records` 为准。
- 使用该最新共享映射隔离验证：M1 Telegram formatter 6/6 PASS；MR1 shared-registry/AI formatter 4/4 PASS。没有触发生产扫描、历史 Telegram 编辑或发送；未修改策略、模型、赛事范围、订单账本或结算。正式范围全量补齐和历史 TG 逐条修复仍未完成。

## 2026-10-14 正式范围继续补齐（第九批）
- 继续仅处理现存 formal unresolved，新增两条有简中足球资料直接显示的身份：`FK Minija`（12812）→米尼亚队（Tips.GG 简中球队档案 https://tips.gg/cn/team/fk-minija-football/）；`NK Croatia Zmijavci`（9903）→克罗地亚兹米亚夫齐队（Tips.GG 简中对阵页 https://tips.gg/cn/archive/hnk-vukovar-91-football-vs-nk-croatia-zmijavci-football/）。两条均保留 TotalCorner IDs、原 provider names 与 aliases，不与相似队伍合并。共享 master 后续提交 `61c6afd4a5067fce73e05980c36ccdb1ace3edfc` 已推送。
- 当前共享 registry 数据文件实算：formal union 2,468 IDs，canonical 2,175、unresolved 293，覆盖率 88.13%；共享 registry 12,276 IDs、4,191 canonical。Zhenis（99519）为前一共享提交 `3636fd8aa972e441e7a9eefe07ee3708d8d4a979` 新增；两项共享提交均已纳入。
- 对最终 registry 运行隔离展示测试：M1 Telegram formatter 6/6 PASS；MR1 共享 registry / AI formatter 4/4 PASS。没有真实 Telegram 发送/编辑或生产运行。完整未匹配明细以最新共享 `formal_scope_coverage.json` 为准；此轮只完成3条新增，任务继续未完成。

## 2026-10-14 正式范围继续补齐（第十批）
- 从当前 unresolved 名单新增4个可核验 provider ID：`NK Bilje`（44026）→比尔耶、`FK Babrungas`（47453）→巴布龙加斯（Tips.GG 简中球队/对阵页面）；`Tsarskoye Selo`（32425）和 `Tsarsko Selo 2015`（42101）→特萨斯科塞洛（球天下中文资料 https://www.qtx.com/dbsoccer/team_26228.html）。两个 Tsarsko Selo 的 TotalCorner IDs 分开保留，未作 ID 合并。共享 master 提交 `fbcc389a3b6b8581126bcbfc80bf5f04d1128cde` 已推送。
- 最新正式范围实算 2,468 IDs，canonical 2,179、unresolved 289，覆盖 88.29%；共享库 12,276 IDs、4,195 canonical。完整未匹配球队、联赛和原因以共享 `formal_scope_coverage.json` 当前版本为准。
- 使用共享库当前版本运行 formatter 回归：M1 6/6、MR1 shared registry/AI 4/4 PASS。仅有名称数据/审计变化；未触发 Telegram 编辑、发送或生产扫描，也未更改模型、策略、正式订单或结算。此目标仍未完成。

## 2026-10-14 正式范围继续补齐（第十一批）
- 依据 Tips.GG 简中希腊杯赛档案对 Ilioupoli 的直接显示“伊利乌波利”，为正式 team_id `43653` 增加 canonical 映射（https://tips.gg/cn/archive/aek-athens-football-vs-ilioupoli-football/）；保留 TotalCorner ID、原 provider 名和希腊赛事 ID，不作实体合并。共享 master 提交 `e9a822f427c14722b995db08b453fa0ebbd8f4ba` 已推送。
- 最新 formal union 2,468 IDs，canonical 2,180、unresolved 288，覆盖 88.33%；共享 registry 12,276 IDs、4,196 canonical。请以最新共享 `formal_scope_coverage.json` 的完整未匹配记录为准。
- 最终共享库定向回归：M1 display formatter 6/6 PASS；MR1 shared display registry + AI formatter 4/4 PASS。只增加展示名称证据；未触发真实 Telegram、订单、模型或生产运行。仍有288个正式范围未匹配，任务未完成。

## 2026-10-14 正式范围继续补齐（第十二批）
- 新增 formal `Orijent`（team_id `48734`）→奥利简特。雷速中文球队数据页将英文全名 HNK Orijent 1919 对应为“奥利简特”，并列出粤语别名“奥利真特”：https://www.leisu.com/data/zuqiu/team-13272/data。保留 TotalCorner ID 与原名，不与 HNK Rijeka 混同。共享 master 提交 `b96b0e785443298b38fe4d8cb4f9ec7c87aa0f71` 已推送。
- 最新 formal union 2,468 IDs，canonical 2,181、unresolved 287（88.37%）；共享 registry 12,276 IDs、4,197 canonical。全部未匹配队伍以最新共享 coverage 文件为准。
- 最新共享映射隔离回归：M1 formatter 6/6、MR1 shared registry/AI formatter 4/4 PASS。没有生产 Telegram 修改或推送；只改 display data/evidence，正式规则与 ledger 未动。287条仍未完成。

## 2026-10-14 正式范围继续补齐（第十三批）
- 为正式 `Al-Arabi Al-Saudi`（team_id `49740`，Saudi league_id `246`）补 canonical `阿尔阿拉比（沙特）`。FootyStats 简中 Saudi First Division 球队档案使用“阿尔阿拉比”，并与其对阵 Al Bukayriyah 的球队身份对应：https://footystats.org/cn/clubs/al-arabi-club-5120。括注保留为区分其他国家同名 Al-Arabi，TotalCorner ID 和 provider identity 未变。共享 master 提交 `a0074264bb9e13102df99ad1bff6cd8efbfbc488` 已推送。
- 最新正式范围 2,468 IDs：2,182 canonical、286 unresolved（88.41%）；共享 registry 12,276 IDs、4,198 canonical。完整 unresolved 清单以最新共享 coverage 文件为准。
- M1 Telegram display formatter 6/6、MR1 shared registry/AI formatter 4/4 PASS。无真实 Telegram 编辑/发送、无策略/模型/账本/结算变更；剩余286个 formal IDs 继续逐项核实。

## 2026-10-14 正式范围继续补齐（第十四批）
- 新增三项来源核实映射：`Lokomotiv Kyiv`（45342）→基辅火车头（球天下简中球队资料 https://football.chuqi.com/football/team-match/244840/）；`Serik Belediyespor`（48935）→塞里克（球天下 https://data.qtx.com/qiudui/0Q7Lrbg6YB.html）；`FK Vora`（48956）→沃拉（中文阿尔巴尼亚联赛参赛队表）。逐条保留 TotalCorner team ID / provider name 和原赛事范围，无实体合并。共享 master 提交 `7e0f40f73a0f97abec5d6d11fe3fddefa1020fa8` 已推送。
- 最新 formal union 2,468 IDs：2,185 canonical、283 unresolved（88.53%）；共享库 12,276 IDs、4,201 canonical。完整 remaining list 以最新共享 `formal_scope_coverage.json` 为准。
- 最新共享库回归：M1 formatter 6/6，MR1 shared registry/AI formatter 4/4 PASS。无生产 Telegram 编辑/发送或策略/账本改动。尚有283项未匹配。

## 2026-10-14 正式范围继续补齐（第十五批）
- 新增两支格鲁吉亚队的直接简中名称：`FC Gori`（46970）→FC哥里（7M 简中球队页 https://team.7m.com.cn/115920/index_gb.shtml）；`FC Spaeri`（50839）→斯佩里队（Tips.GG 简中球队档案 https://tips.gg/cn/team/spaeri-fc-football/）。保留 team_id、TotalCorner provider name 与 league IDs。共享 master 提交 `0dd59b09b0ecfc41fba4ca816931871822e44b32` 已推送。
- 最新 formal union 2,468 IDs：2,187 canonical、281 unresolved（88.61%）；共享库 12,276 IDs、4,203 canonical。完整 remaining list 以最新共享 `formal_scope_coverage.json` 为准。
- M1 formatter 6/6、MR1 shared registry/AI formatter 4/4 PASS。只有 display curation 更新；没有真实 Telegram 编辑/发送、生产运行或策略/账本改动。尚有281项待核实。

## 2026-10-14 正式范围继续补齐（第十六批）
- 新增两支直接简中来源对应：`Al-Bukayriyah FC`（50581）→布凯里耶（球天下球队页 https://data.qtx.com/qiudui/29W8VM2jvb.html）；`BFA Vilnius`（52319）→BFA 维尔纽斯（Tips.GG 简中球队页 https://tips.gg/cn/team/bfa-vilnius-football/）。保留 TotalCorner ID、provider name 与联赛身份。共享 master 提交 `d4b71367fa682120b1d62ae68f85d74496347be5` 已推送。
- 最新 formal union 2,468 IDs：2,189 canonical、279 unresolved（88.70%）；共享 registry 12,276 IDs、4,205 canonical。剩余项以共享库最新 `formal_scope_coverage.json` 为准。
- 最新共享映射验证：M1 formatter 6/6，MR1 shared registry/AI formatter 4/4 PASS。没有真实 Telegram 修改或生产运行；正式策略、账本、结算未改。279 项仍待核实。

## 2026-10-14 正式范围继续补齐（第十七批）
- 复核共享 master 后，正式并集仍为2,468个ID，上一批279项未匹配。本轮依雷速体育中文球队档案新增5条：Kima Aswan（77134）→克玛阿斯罔（https://www.leisu.com/data/zuqiu/team-30909）；El Obour SC（80942）→埃尔奥布尔（https://www.leisu.com/data/zuqiu/team-60233/data）；FK Liria（32246）→FC利里亚（雷速页以FC Liria列名，https://www.leisu.com/data/zuqiu/team-85397/data）；FK Ibar Rozaje（40486）→伊巴罗扎伊（https://www.leisu.com/data/zuqiu/team-20222/data）；Malisheva（54405）→马利舍瓦（https://www.leisu.com/data/zuqiu/team-53247/best）。原始 provider ID/name、aliases、联赛身份均保留，没有合并 team IDs。
- 共享中文库提交 `0ff2c9441b5ada2f3e46d12c1c475ce1161117ae` 已推送至 `totalcorner-research-bridge/master`。从生成后的 `formal_scope_coverage.json` 实算：formal union 2,468，canonical 2,194，unresolved 274，覆盖88.90%；M1 1,483/1,553（95.49%）；M1 OU-R1 52/52（100%）；MR1 AH 1,696/1,921（88.29%）；MR1 AI declared mirror M1 1,483/1,553（95.49%），observed confidence≥50 cohort 181/182（99.45%）。剩余274项的完整 ID/name/league/system/reason 以共享库 `data/football_display_names/formal_scope_coverage.json` 为准。
- 使用共享 master registry 定向验证：M1 telegram display tests 6/6 PASS；MR1 shared registry/AI formatter tests 4/4 PASS；curation generator 与 `git diff --check` 通过。未做生产 Telegram 发送或历史编辑，未改任何模型、策略、订单账本、结算或派单规则。历史 Telegram 修复数本轮为0；正式范围名称补齐仍未完成。

## 2026-10-14 正式范围继续补齐（第十八批）
- 本轮从球天下公开简中球队档案核实两项：Desna（team_id `80828`）→丹斯那切尼赫夫（https://www.qtx.com/dbsoccer/team_3536.html）；FK Zlatibor（team_id `42548`）→兹拉蒂博尔卡捷提娜，来源页球队名为 Zlatibor Cajetina（https://www.qtx.com/dbsoccer/team_139225.html）。保留 TotalCorner ID/provider name 与 aliases，不合并实体。
- 共享中文库提交 `1bf1c97dc52e820bfb0ccb0f088222616f4847d0` 已推送至 `totalcorner-research-bridge/master`。最新 coverage 实算正式并集 2,468，canonical 2,196，unresolved 272（88.98%）；M1 1,485/1,553（95.62%）；M1 OU-R1 52/52（100%）；MR1 AH 1,696/1,921（88.29%）；MR1 AI 声明镜像 M1 1,485/1,553（95.62%）；AI confidence≥50历史观测 cohort 181/182（99.45%）。完整剩余272条见共享库 `data/football_display_names/formal_scope_coverage.json`。
- 最新共享库 formatter 回归：M1 6/6 PASS、MR1 registry/AI formatter 4/4 PASS；生成器与 `git diff --check` 通过。本轮未运行生产 TG、未编辑历史消息，也未修改模型、策略、订单/结算或发布规则；全量名称补齐继续进行。

## 2026-10-14 正式范围继续补齐（第十九批）
- 本轮在共享库最新 master `1bf1c97dc52e820bfb0ccb0f088222616f4847d0` 基础上新增4条有可核验简中显示来源的映射：SV Stripfing/Weiden（team_id `14342`）→斯特里普芬（Tips.GG 中文对阵页 https://tips.gg/cn/archive/rapid-vienna-youth-football-vs-sv-stripfing-weiden-football/）；OFK Malzenice（`14677`）→马尔泽尼采（https://tips.gg/cn/team/ofk-malzenice-football/）；Belasica Strumica（`14658`）→贝拉西察（https://tips.gg/cn/archive/academy-pandev-football-vs-belasica-strumica-football/）；Ballymacash Rangers（`107202`）→巴利马卡什（https://tips.gg/cn/archive/ards-rangers-football-vs-ballymacash-rangers-football/）。映射均保留 provider identity、team ID、aliases 和来源，不做 ID 猜测/实体合并。
- 唯一共享 registry 已推送提交 `63648b442651d820ba9c7f78bbf3670b5eab24dd`。最新 `formal_scope_coverage.json` 实算：正式并集2,468 IDs，2,200 canonical、268 unresolved，覆盖89.14%；M1 1,486/1,553（95.69%）；M1 OU-R1 52/52（100%）；MR1 AH 1,700/1,921（88.50%）；MR1 AI 声明镜像 M1 1,486/1,553（95.69%），AI confidence≥50观测 cohort 181/182（99.45%）。完整剩余清单与数据源原因以共享库 `data/football_display_names/formal_scope_coverage.json` 为准。
- 基于最新共享库隔离测试：M1 formatter 6/6 PASS；MR1 shared registry/AI formatter 4/4 PASS。未做真实 Telegram 发送或历史消息编辑，没有生产触发；因此本轮历史 TG 编辑数为0（非失败数），不能声称已修复已发送消息。没有修改任何模型、策略、正式赛事范围、订单账本、结算或派单逻辑。中文补齐仍在进行，268项尚未获得可靠 canonical 名称。

## 2026-10-14 正式范围继续补齐（第二十批）
- 最新共享 master `63648b442651d820ba9c7f78bbf3670b5eab24dd` 的 formal unresolved 清单中，team_id `4689` 的 provider name 为 `Jadran LP`，正式范围含 M1/MR1。Tips.GG 简中页面将同名克罗地亚球队显示为“雅德兰”，并标示国家为克罗地亚：https://tips.gg/cn/archive/jadran-lp-football-vs-nk-lucko-football/；克罗地亚足协页面确认 NK Jadran-LP Ploče 的正式身份：https://semafor.hns.family/en/clubs/1976/nk-jadran-lp/?cid=78204094。本批补入 canonical “雅德兰”，保留 `NK Jadran-LP` 等别名及来源证据，不合并其他球队 ID。
- 共享库提交 `fe5b97e4f26ad6ffd693bee2bec44d6d111ff4a5` 已推送。最新 formal union 2,468 IDs：2,201 canonical、267 unresolved，覆盖89.18%；M1 1,486/1,553（95.69%）；M1 OU-R1 52/52；MR1 AH 1,701/1,921（88.55%）；MR1 AI declared mirror M1 1,486/1,553（95.69%）。完整 unresolved 名单在唯一共享 `formal_scope_coverage.json`。
- 使用当前共享库：M1 Telegram display 测试6/6通过，MR1 `test-football-display-names.js` 1/1通过。扩大执行的 M1 runtime 测试另有5个既有 fixture/candidate-key 失败；MR1 AI 广泛 send-chain 测试因当前本地工作区 fixtures/ledger 不齐而6项失败，不能视为名称层回归或生产发送验证。未进行真实 Telegram 编辑/发送；本轮没有历史修复回执。没有模型、策略、ledger、结算或派单改动。余下267项继续按来源核验，未将不可靠直译填入共享库。

## 2026-10-14 正式范围继续补齐（第二十一批）
- 从7M中文球队资料核实两条正式范围映射：`FC Tallinn`（team_id `67634`）→“塔林FC”（7M页面标示爱沙尼亚并列出球队赛程：https://team.7m.com.cn/452435/index_gb.shtml）；`Unia Skierniewice`（`33235`）→“尤尼亚斯凯尔涅维采”（7M页面标示波兰并列出球队赛程：https://team.7m.com.cn/453386/index_gb.shtml）。ID、provider 原名、aliases 和来源均保留，没有改正式 identity。
- 共享 registry 提交 `0e27ab163016248de713a1fbd1fbc75b6e2b9d55` 已推送。formal union 实算 2,468 IDs、2,203 canonical、265 unresolved（89.26%）；M1 1,488/1,553（95.81%），M1 OU-R1 52/52，MR1 AH 1,702/1,921（88.60%），MR1 AI declared mirror M1 1,488/1,553（95.81%）。全量 unresolved 记录在共享 `data/football_display_names/formal_scope_coverage.json`。
- 共享库名称层验证：M1 formatter 6/6 PASS，MR1 `test-football-display-names.js` 1/1 PASS。没有真实 Telegram 编辑或发送，本轮历史消息修复数为0；不宣称已修改已发送订单。未改模型、策略、范围、ledger、结算或派单逻辑。265项仍在继续核证。

## 2026-10-14 正式范围继续补齐（第二十二批）
- 继续查证后新增 `FK Tekstilac Odzaci`（team_id `133202`）→“特克斯蒂拉茨”。FootyStats 简中球队档案直接标注 FK Tekstilac Odzaci 与该中文队名：https://footystats.org/cn/clubs/fk-tekstilac-odzaci-704721；塞尔维亚官方球队站确认 Tekstilac Odžaci 的球队身份：https://fktekstilac1919.com/。保留 provider identity、ID 与拼写别名，不作合并。
- 最新唯一共享 registry 提交 `960d1597d6e97d6460831a0ac44aca3c0649e243` 已推送；当前 formal union 2,468 IDs、2,204 canonical、264 unresolved（89.30%）。M1 1,489/1,553（95.88%），OU-R1 52/52，MR1 AH 1,703/1,921（88.65%），MR1 AI declared mirror M1 1,489/1,553（95.88%）。之前第21批两项与本批项均由共享 `formal_scope_coverage.json` 更新，264条剩余明细以该文件为准。
- M1 formatter 6/6 PASS；MR1共享 display-name test 1/1 PASS。未编辑/发送任何 Telegram 历史消息，本轮生产 TG 修复仍未执行；未修改模型、策略、赛事范围、账本、结算或出单规则。264条继续逐项来源核验。

## 2026-10-14 正式范围继续补齐（第二十三批）
- FootyStats 简中球队档案明确以“扎基里斯B队”展示 `VMFD Žalgiris Vilnius II`，并列出立陶宛1 Lyga赛程/球队资料：https://footystats.org/cn/clubs/vmfd-zalgiris-vilnius-ii-1240。本次仅为精确 provider name `Vmfd Zalgiris II`（team_id `10705`）录入 canonical “扎基里斯B队”，保留 provider ID/name、拼写 aliases 和 source；没有把另一个 provider team ID `71679` 自动合并。
- 共享中文库提交 `d6dd1a4e4ebeca6a284b1bb12d10c379f6877e8a` 已推送。当前 formal union 2,468 IDs，2,205 canonical，263 unresolved（89.34%）；M1 1,490/1,553（95.94%），M1 OU-R1 52/52，MR1 AH 1,704/1,921（88.70%），MR1 AI declared mirror M1 1,490/1,553（95.94%）。完整未匹配列表以共享 `formal_scope_coverage.json` 为准。
- 名称层隔离回归：M1 Telegram formatter 6/6 PASS，MR1共享 registry test 1/1 PASS。没有真实 Telegram编辑/发送或生产触发；模型、策略、范围、账本、结算和派单条件未改。263条继续查证。

## 2026-10-14 正式范围中文名追加：Hertha Wels
- 从最新共享 master `d6dd1a4e4ebeca6a284b1bb12d10c379f6877e8a` 继续处理 formal unresolved；仅新增已核实 `team_id 165677`（provider `Hertha Wels`）→ `WSC赫塔威尔斯`。球探中文球队页明确列出“WSC赫塔威尔斯”与英文 `WSC Hertha Wels`（https://info.titan007.com/cn/team/Summary.aspx?TeamID=39076），FootyStats 同时确认俱乐部英文正式名 WSC Hertha Wels、地点 Wels、Austria Regionalliga（https://footystats.org/clubs/wsc-hertha-wels-3335）。原 TotalCorner ID/provider name 和联赛 ID 保留；不与其他 Hertha 球队合并。
- 最新共享文件实算：formal union 2,468 IDs，canonical 2,206，unresolved 262，覆盖 89.38%；M1 1,487/1,553（95.75%）；M1 OU-R1 52/52（100%）；MR1 AH 1,706/1,921（88.81%）；MR1 AI declared mirror 1,487/1,553（95.75%）。完整逐队未匹配表以共享 `data/football_display_names/formal_scope_coverage.json` 为准。
- 当前 M1 formatter tests 6/6 PASS，MR1 shared-registry display test 1/1 PASS。仅新增共享展示映射及审计统计，无生产 TG 发送/编辑；此前 TG repair 的真实状态仍见上方历史记录，不把测试当作线上修复。模型、策略、盘口、赛事范围、账本、结算与派单逻辑均未改。候选 `FK TransINVEST`、`FC Altai Semey`、`BSK Banja Luka`、`OFK Vršac`、`Sirens` 等本轮未找到足以绑定到精确 TotalCorner identity 的简体中文权威/成熟足球资料，继续保持 unresolved，不按音译猜填。
- 共享映射更新后实际执行既有 MR1 Formal Telegram Historical Name Repair：run [38575869834](https://github.com/ljm198964-alt/quant-runner/actions/runs/38575869834) SUCCESS，批次回执 `edited=0, eligible=0, skipped=125, unresolved=0, failed=0`。没有 MR1 AH 现存已发送消息需要因本批 Hertha 映射再次改写。M1 最近历史修复 run `38568037059` 为 41 条 `ALREADY_MATCHING`、0 编辑、0 失败；M1 OU-R1 与 AH 共用同一展示 formatter。MR1 AI 最近的 9 个 edit 仍是 Telegram 400 `message to edit not found`，没有重发；本轮未因不相关的 M1 镜像范围重复执行该 workflow。

## 2026-10-14 正式范围新增：Changnyeong 女足
- 继续从当前 unresolved 清单核实 `team_id 46706`、provider `Changnyeong (W)`：球探简中档案标题使用“昌宁女足”，英文名为 `Changnyeong (W)`（https://info.nowscore.com/cn/team/Summary.aspx?TeamID=37682）；Sofascore 简中球队页另称“昌宁郡女子足球俱乐部”（https://www.sofascore.com/zh/football/team/changnyeong-wfc/284610）。选取符合简体盘口语境的 canonical `昌宁女足`，保留女队英文别名和 team ID，不与任何男子队合并。
- 本批复算 formal union：2,468 IDs，2,207 canonical、261 unresolved，覆盖率 89.42%；M1 1,487/1,553（95.75%）；M1 OU-R1 52/52（100%）；MR1 AH 1,707/1,921（88.86%）；MR1 AI declared mirror 1,487/1,553（95.75%）。M1 formatter 6/6、MR1 registry display test 1/1 通过。只更新展示名库与审计文件；本批没有触发 Telegram 发送或编辑、没有改策略或账本。
- 随后再次运行 MR1 历史名称编辑工作流核验新映射：run [38576577641](https://github.com/ljm198964-alt/quant-runner/actions/runs/38576577641) SUCCESS，回执 `edited=0, eligible=0, skipped=125, unresolved=0, failed=0`。Telegram 未产生修改；这项回查只证明现有正式消息集没有待改文本，不代表尚未发送的新消息。

## 2026-10-14 正式范围新增：FC Chernigiv
- `team_id 46376` / provider `FC Chernigiv` 新增 canonical `切尔尼戈夫`。Tips.GG 简中球队档案以“切尔尼戈夫队”显示该乌克兰俱乐部（https://tips.gg/cn/team/fc-chernigiv-football/）；registry 保留队名来源别名及原 TotalCorner ID，不把它与其他 Chernihiv 队混并。
- 当前 formal union 2,468 IDs：2,208 canonical、260 unresolved（89.47%）；M1 1,487/1,553（95.75%），M1 OU-R1 52/52，MR1 AH 1,708/1,921（88.91%），MR1 AI declared mirror 1,487/1,553（95.75%）。M1 display tests 6/6、MR1 shared display test 1/1 通过。仅更新名称数据/审计；本条之后尚未重新运行历史 Telegram 编辑器，也没有生产发送。
- 映射推送后执行最新 MR1 历史名称编辑核验：run [38577009608](https://github.com/ljm198964-alt/quant-runner/actions/runs/38577009608) SUCCESS，结果 `edited=0, eligible=0, skipped=125, unresolved=0, failed=0`；125 条均已处理，没有因 FC Chernigiv 产生可编辑历史消息。本次仍未重发 Telegram。

## 2026-10-14 正式范围继续补齐（第二十四批）
- 基于最新共享 master `19be08f5a1062e54a988b5bb033d069cfe025b20` 核实两支正式队伍并加入唯一 registry：M1 `Incheon University`（team_id `50784`, league_id `75`）→“仁川大学”，来源为球探/Titan007 中文球队页（https://zq.titan007.com/cn/team/Summary/5749.html）；MR1 `B71 Sandur`（team_id `52647`, league_id `10635`）→“B71桑杜尔”，来源为奥客简中法罗群岛赛事列表（https://www.zh-sport-aoke.com/），中文别名“B71桑多伊”保留。均保留 TotalCorner ID、provider identity、赛事关联和来源说明；不与同地区、大学或其他 B71 球队合并。
- 共享库提交 `ff1df24680fcb542c03a31839d95cd3f79ac1272` 已推送 master。生成文件实算：正式并集2,468队，canonical 2,210，unresolved 258，覆盖89.55%；M1 1,487/1,553（95.75%）；M1 OU-R1 52/52（100%）；MR1 AH 1,709/1,921（88.96%）；MR1 AI declared mirror 1,487/1,553（95.75%）。本轮真实新增2条。
- 名称层测试：M1 telegram formatter 6/6 PASS；MR1 shared registry test 1/1 PASS；批量 curator 和 `git diff --check` 通过。未改模型、策略、盘口源、赛事范围、账本、结算或派单逻辑。
- 新 registry 后执行现有历史 names-only 工作流（仅修改已有消息文本，不重发）：M1 run [38577697804](https://github.com/ljm198964-alt/quant-runner/actions/runs/38577697804) SUCCESS，`eligible=41, edited=0, already_matching=41, skipped_missing_original_text=99, skipped_unmapped=94, failed=0`；因此本批没有历史 M1/OU-R1 消息发生编辑。MR1 AH run [38577707560](https://github.com/ljm198964-alt/quant-runner/actions/runs/38577707560) SUCCESS，`edited=0, eligible=0, skipped=125, unresolved=0, failed=0`。MR1 AI run [38577715706](https://github.com/ljm198964-alt/quant-runner/actions/runs/38577715706) SUCCESS，201条历史记录中9条可尝试、0编辑、9次 Telegram API `400: message to edit not found`；另192条显示名 unresolved。没有重发历史消息。正式范围仍有258个 ID 未获可靠中文名，不能称为全量完成。

## 2026-10-14 正式范围继续补齐（第二十五批）
- 对 MR1/M1 正式范围 `FC Gareji`（team_id `53098`，league_ids `702/10480`）找到精确中文对照：中文格鲁吉亚足球超级联赛球队表将 `FC Gareji 1960` 列为“加雷治”（https://zh.wikipedia.org/wiki/格鲁吉亚足球超级联赛）。以“加雷治”为 canonical，将 FC Gareji 1960 作为英文别名，保留现有 TotalCorner team ID、provider 名和联赛身份，不合并其他 FC Gareji/Gareji ID。
- 共享库提交 `a8d11859faaf692984c0a3fd1e5248ceceb18ab6` 已推送 master。最新正式范围实算2,468 IDs，2,211 canonical、257 unresolved，覆盖89.59%；M1 1,487/1,553（95.75%），M1 OU-R1 52/52，MR1 AH 1,709/1,921（88.96%），MR1 AI declared mirror 1,487/1,553（95.75%）。本批新增1条。
- curator 与 `git diff --check` 通过，M1 formatter 6/6、MR1 registry test 1/1 PASS。仅名称展示层变更。新映射后再次执行三条既有 names-only workflows：M1 run [38578502520](https://github.com/ljm198964-alt/quant-runner/actions/runs/38578502520) SUCCESS，`eligible=41, edited=0, already_matching=41, skipped_missing_original_text=99, skipped_unmapped=94, failed=0`；MR1 AH run [38578509884](https://github.com/ljm198964-alt/quant-runner/actions/runs/38578509884) SUCCESS，`edited=0, eligible=0, skipped=125, unresolved=0, failed=0`；MR1 AI run [38578519490](https://github.com/ljm198964-alt/quant-runner/actions/runs/38578519490) SUCCESS，仍是201条记录、9条可编辑候选但0编辑，9条 Telegram API `400: message to edit not found`，192条显示名 unresolved。本节之后没有任何新订单或重发消息。

## 2026-10-14 正式范围继续补齐（第二十六批）
- 从中文百科/俱乐部档案核实两条同一奥地利俱乐部展示身份：M1 team_id `47946` / provider `Admira` 与 team_id `50777` / provider `FC Flyeralarm Admira`，均规范显示“阿德米拉”；Newton 中文球队条目列出 FC Flyeralarm Admira、FC Trenkwalder Admira Wacker Mödling，并给出简称 Admira（https://www.newton.com.tw/wiki/阿德米拉）。两个 TotalCorner IDs、provider name、league_id 29 均单独保留，没有合并ID；不映射到其他 Admira 球队。
- 共享 master 提交 `d03b1b3869ec1ecd50ea09275fb3ec7481048689` 已推送。formal union 2,468 IDs：2,213 canonical、255 unresolved（89.67%）；M1 1,489/1,553（95.88%），M1 OU-R1 52/52；MR1 AH 1,709/1,921（88.96%）；MR1 AI mirror 1,489/1,553（95.88%）。新增2条。
- 测试：M1 formatter 6/6，MR1 shared registry 1/1；generator 和 `git diff --check` 通过。M1 names-only historical workflow [38579272297](https://github.com/ljm198964-alt/quant-runner/actions/runs/38579272297) SUCCESS；报告为 `eligible=41, edited=0, already_matching=41, skipped_missing_original_text=99, skipped_unmapped=94, failed=0`。因此本轮没有历史 TG 消息实际编辑；仅中文展示映射有变更。

## 2026-10-14 正式范围继续补齐（第二十七批）
- 新增两条精确来源映射：MR1/M1 formal `FC Suduroy`（team_id `45817`）→“苏德罗”，球探/Titan007 中文球队档案直接对应英文队名（https://info.titan007.com/cn/team/Summary/13660.html）；MR1/M1 `FC West Armenia`（team_id `53659`）→“西亚美尼亚”，中文亚美尼亚球队列表直接列出英文与繁体“西亞美尼亞”，canonical 规范为简体（https://zh.wikipedia.org/wiki/亚美尼亚足球俱乐部列表）。ID、provider names、league associations 均保留，不合并身份。
- 共享 master 提交 `a4bf18dcef3e0d2bb97a23133541e8f1b525661c` 推送完成。正式范围2,468 IDs：2,215 canonical、253 unresolved（89.75%）；M1 1,491/1,553（96.01%），M1 OU-R1 52/52，MR1 AH 1,709/1,921（88.96%），MR1 AI declared mirror 1,491/1,553（96.01%）。
- formatter/registry tests：M1 6/6、MR1 1/1 PASS；curator 与 `git diff --check` 通过。没有策略/模型/ledger 变化。新映射对应的 MR1 AH repair run [38580144444](https://github.com/ljm198964-alt/quant-runner/actions/runs/38580144444) SUCCESS，`edited=0, eligible=0, skipped=125, unresolved=0, failed=0`；MR1 AI run [38580152755](https://github.com/ljm198964-alt/quant-runner/actions/runs/38580152755) SUCCESS，9条编辑候选0编辑，9条 Telegram `400 message to edit not found`、192 unresolved。M1 names-only run [38580135728](https://github.com/ljm198964-alt/quant-runner/actions/runs/38580135728) SUCCESS，`eligible=41, edited=0, already_matching=41, skipped_missing_original_text=99, skipped_unmapped=94, failed=0`。无消息重发。

## 2026-10-14 正式范围继续补齐（第二十八批）
- 为 M1 正式队伍 `FC Altai Semey`（team_id `72494`，Kazakhstan league_id `345`）补入 ScoreBat 简中赛程页的明确用名“阿尔泰塞梅伊”；页面标题路径为 Altay Semey 对阵 Yelimay Semey（https://www.scorebat.com/zh-cn/altay-semey-vs-yelimay-semey-live-stream/）。保留 TotalCorner ID、provider 拼写与联赛 identity，未与其他 Altai 球队合并。
- 共享 master commit `26c42162b2fc167cd813b2592a953c5bcee68df4` 已推送。正式范围 2,468 IDs：2,216 canonical、252 unresolved（89.79%）；M1 1,492/1,553（96.07%），M1 OU-R1 52/52；MR1 AH 1,709/1,921（88.96%）；MR1 AI declared mirror M1 1,492/1,553（96.07%）。
- M1 formatter 6/6、MR1 shared registry 1/1 PASS；curator 与 `git diff --check` 通过。只改显示名称。M1 names-only historical edit workflow [38580903328](https://github.com/ljm198964-alt/quant-runner/actions/runs/38580903328) 最终 SUCCESS；回执 `eligible=41, already_matching=41, edited=0, skipped_missing_original_text=99, skipped_unmapped=94, failed=0`，没有重发消息。

## 2026-10-14 正式范围继续补齐（第二十九批）
- Tips.GG 简中 ASK Voitsberg 球队档案明确显示“沃伊茨贝格”，并标为奥地利球队（https://tips.gg/cn/team/ask-voitsberg-football/）。为 TotalCorner `team_id 6553` / provider `ASK Voitsberg` 写入 canonical“沃伊茨贝格”，保留 `Voitsberg` alias、奥地利 league IDs 与来源说明；不合并其他队伍。
- 共享库提交 `8702885b` 已推送 master。正式范围共2,468个 team IDs，2,217 canonical、251 unresolved，覆盖89.83%；M1 1,491/1,553（96.01%），M1 OU-R1 52/52，MR1 AH 1,714/1,921（89.22%），MR1 AI declared mirror M1 1,491/1,553（96.01%）。剩余逐队记录与原因见唯一共享 `data/football_display_names/formal_scope_coverage.json`。
- M1 formatter 6/6、MR1 shared display test 1/1 PASS，curator 和 `git diff --check` PASS。M1 历史 names-only repair run [38580903328](https://github.com/ljm198964-alt/quant-runner/actions/runs/38580903328) SUCCESS；报告：41 eligible，其中41 already matching、0 edited、0 failed；99 条缺原始文本，94 条未映射。未重发历史订单。
- 新映射提交后，按既有 workflow 完成 MR1 AH [38581522342](https://github.com/ljm198964-alt/quant-runner/actions/runs/38581522342) 与 MR1 AI [38581530871](https://github.com/ljm198964-alt/quant-runner/actions/runs/38581530871) names-only 历史编辑。MR1 AH 回执 `edited=0, eligible=0, skipped=125, unresolved=0, failed=0`；MR1 AI 回执 `total=201, candidates=9, edited=0, already_matching=0, failed=9, unresolved=192`，9次 Telegram API 均返回 `400: message to edit not found`，因此不能将其记为已修复；MR1 AI 编辑回执已由既有工作流推送到 MR1 shadow，commit `9cff9e6575`。没有重发历史消息。此次只处理中文展示；未改任何策略、模型、正式交易数据、结算或派单规则。

## 2026-10-14 正式范围继续补齐（第三十批）
- 雷速中文球队档案明确将 `Tiszakecske` 对应为“提斯扎高克”（https://www.leisu.com/data/zuqiu/team-37903/transfer），将 `Prykarpattya Ivano Frankivsk` 对应为“普里卡帕亚”（https://www.leisu.com/data/zuqiu/team-21138/lineup）。为 TotalCorner `team_id 45054` 与 `46291` 分别加入标准名和源证据，保留各自 ID/provider identity、别名及联赛关联，不跨 ID 合并。
- 共享库提交 `9baf93b5` 已推送 master。正式范围2,468 IDs：2,219 canonical、249 unresolved（89.91%）；M1 1,493/1,553（96.14%），M1 OU-R1 52/52，MR1 AH 1,716/1,921（89.33%），MR1 AI declared mirror M1 1,493/1,553（96.14%）。完整未匹配项与原因仍在共享 `formal_scope_coverage.json`。
- M1 display 6/6 与 MR1 shared registry 1/1 tests、curator 和 `git diff --check` 均通过。基于最新库的 M1 [38582090624](https://github.com/ljm198964-alt/quant-runner/actions/runs/38582090624) SUCCESS，`eligible=41, edited=0, already_matching=41, skipped_missing_original_text=99, skipped_unmapped=94, failed=0`；MR1 AH [38582100828](https://github.com/ljm198964-alt/quant-runner/actions/runs/38582100828) SUCCESS，`edited=0, eligible=0, skipped=125, unresolved=0, failed=0`。MR1 AI 首轮 [38582109611](https://github.com/ljm198964-alt/quant-runner/actions/runs/38582109611) 的回执提交与 MR1 AH 并发 push 发生竞态；随后串行重跑 [38582416283](https://github.com/ljm198964-alt/quant-runner/actions/runs/38582416283) SUCCESS 并持久化回执，结果仍为 `total=201, candidates=9, edited=0, failed=9, unresolved=192`；9条 Telegram API 均返回 `400: message to edit not found`。回执 commit `4a4be39dc2` 已推送到 MR1 shadow。没有发送或重发消息。

## 2026-10-14 正式范围继续补齐（第三十一批）
- 中文足球俱乐部列表将北马其顿 FK Borec 对应为“博雷斯”（https://zh.wikipedia.org/wiki/欧洲顶级足球俱乐部列表）。为 TotalCorner `team_id 43110` / provider `FK Borec` 加入 canonical“博雷斯”、原拼写 aliases 和可追溯来源；其 North Macedonia league identity 保留，不与其他 Borec 队合并。
- 共享库提交 `4bf322c8` 已推送 master。按该提交保存的 coverage 文件实算：正式范围 2,468 IDs，2,220 canonical、248 unresolved；M1 1,492/1,553，OU-R1 52/52，MR1 AH 1,716/1,921，MR1 AI mirror 1,492/1,553。
- M1 formatter 6/6 和 MR1 registry display test 1/1 PASS，数据 curator 与 `git diff --check` PASS。仅共享 display data/source report 变更；未改任何策略、模型、交易 ledger、settlement 或 Telegram dispatch criteria。正式剩余列表继续以共享 `formal_scope_coverage.json` 为准。

## 2026-10-14 正式范围继续补齐（第三十二批）
- 雷速中文球队档案明确显示 `Sutjeska Foca` 的标准中文名为“苏捷斯卡”，且描述其为波黑地区联赛球队（https://www.leisu.com/data/zuqiu/team-18688/best）。为 TotalCorner team_id `11405` 添加 canonical、英文拼写别名及来源证据，保留 Foča 联赛身份并明确不与 Sutjeska Nikšić 等同名队混并。
- 共享库提交 `40107b98` 已推送 master。按该提交保存的 coverage 文件实算：正式范围2,468 IDs，2,221 canonical、247 unresolved；M1 1,492/1,553，M1 OU-R1 52/52，MR1 AH 1,717/1,921，MR1 AI declared mirror 1,492/1,553。
- M1 formatter 6/6、MR1 registry test 1/1 PASS；curator 与 `git diff --check` PASS。仅共享中文展示数据与审计统计更新，不改策略、模型、账本、结算、信号条件或正式范围；未发送 Telegram。

## 2026-10-14 正式范围继续补齐（第三十三批）
- Sofascore 简中 Serbian team profile 将 Leskovac 的 GFK Dubočica 显示为“杜博奇察”（https://www.sofascore.com/zh/football/team/gfk-dubocica-leskovac/301263）。结合 TotalCorner 原名 `FK Dubocica`、team_id `49647` 和 Serbian league_id `337`，新增该 ID 专属 canonical；保留 `GFK Dubočica` 等英文别名，不与别的 Dubočica ID 合并。
- 共享库提交 `caeeba6c` 已推送 master。按该提交保存的 coverage 文件实算：正式范围2,468 IDs，2,222 canonical、246 unresolved；M1 1,492/1,553，M1 OU-R1 52/52，MR1 AH 1,718/1,921，MR1 AI declared mirror 1,492/1,553。
- curator、`git diff --check`、M1 formatter 6/6 与 MR1 registry test 1/1 均通过。仅共享中文展示名及审计文件有改动；生产策略、模型、交易账本、结算和 TG 派单规则不变。未发送 Telegram；剩余项逐条记录于共享 `formal_scope_coverage.json`。

## 2026-10-14 正式范围继续补齐（第三十四批）
- 7M 简体中文球队页将 `MFK Stara Lubovna` 列为“路博夫纳”（https://team.7m.com.cn/4928/index_gb.shtml）。为 TotalCorner `team_id 53586` / `league_id 355` 添加独立 canonical 和来源证据，保留 provider identity 与原拼写 aliases。
- 共享库提交 `896a702d` 已推送 master。coverage 文件实算：正式范围2,468 IDs，2,223 canonical、245 unresolved（90.07%）；M1 1,492/1,553（96.07%），OU-R1 52/52，MR1 AH 1,719/1,921（89.48%），MR1 AI mirror 1,492/1,553（96.07%）。
- M1 formatter 6/6、MR1 shared registry display test 1/1、curator 与 `git diff --check` 均通过。仅展示映射/审计文件变更；生产策略、模型、账本、结算及 Telegram 派单逻辑未改。

## 2026-10-14 正式范围继续补齐（第三十五批）
- 球天下体育中文赛果/球队索引将 `Zabbar Saint Patrick` 显示为“扎巴尔圣帕特里克”（https://live.qtx.com/fenxi/pjroKQ1868.html）；以其马耳他联赛身份和公开俱乐部资料核对 TotalCorner `team_id 19664` / `Saint Patrick FC Zabbar`，新增该 ID 专属 canonical 与 aliases，不与爱尔兰 Saint Patrick's Athletic 混同。
- 共享库提交 `82060357c1d0d152b6474c5b151e52a137518391` 已推送 master。coverage 文件实算：正式范围2,468 IDs，2,224 canonical、244 unresolved（90.11%）；M1 1,493/1,553（96.14%），OU-R1 52/52，MR1 AH 1,720/1,921（89.54%），MR1 AI mirror 1,493/1,553（96.14%）。
- M1 formatter 6/6、MR1 shared registry display test 1/1、curator 与 `git diff --check` 均通过。仅共享中文展示数据/审计产物有变更；生产策略、模型、账本、结算及 Telegram 派单逻辑未改，未发送或编辑 Telegram。

## 2026-10-14 正式范围继续补齐（第三十六批）
- SportScore 简体中文球队/比赛页面将 Nestos Chrisoupolis 显示为“内斯托斯·奇里苏波利斯”（https://sportscore.com/zh/football/team/aps-zakynthos/dj2ryohk45xq1zp/）；据希腊球队身份及该页面赛果关联核对 TotalCorner `team_id 15812`，写入 ID 专属 canonical 和拼写 aliases。
- 共享库提交 `e25c5a2388450893b5af229800dfbbade5d915af` 已推送 master。coverage 文件实算：正式范围2,468 IDs，2,225 canonical、243 unresolved（90.15%）；M1 1,493/1,553（96.14%），OU-R1 52/52，MR1 AH 1,721/1,921（89.59%），MR1 AI mirror 1,493/1,553（96.14%）。
- M1 formatter 6/6、MR1 shared registry display test 1/1、curator 与 `git diff --check` 均通过。只更新共享展示数据/审计产物；未改策略、模型、账本、结算、Telegram 派单规则，未发送或编辑 Telegram。

## 2026-10-14 正式范围继续补齐（第三十七批）
- 核对 TotalCorner `team_id 54358` / `Digenis Ypsonas`：OddsGPT 的精确比赛页将该队显示为“迪杰尼斯伊普索纳斯”（https://www.oddsgpt.com/yuce/football/1603561/digenis-ypsonas-vs-aris/zh），并与 500.com 的“迪杰尼斯”以及 Tips.gg 的“伊普索纳斯”中文队名相互印证。新增该 ID 专属 canonical 与来源别名。
- 雷速中文球队档案明确将 `Iraklis Yerolakkou` 显示为“伊拉克利斯耶罗拉”（https://www.leisu.com/data/zuqiu/team-54376/data）；为 TotalCorner `team_id 15888` 增加对应 canonical 和原名别名。
- 共享库提交 `14d174ae96f4c1d170e414e83fdfa91465cadba8` 已推送 master。本次新增2条。最新实算 formal union 2,468 IDs：2,227 canonical、241 unresolved（90.24%）；M1 1,494/1,553（96.20%）；M1 OU-R1 52/52（100%）；MR1 AH 1,722/1,921（89.64%）；MR1 AI declared mirror 1,494/1,553（96.20%）。完整剩余清单和原因以共享 `formal_scope_coverage.json` 为准。
- M1 Telegram formatter tests 6/6 PASS，MR1 shared registry test 1/1 PASS，curator 与 `git diff --check` PASS。只更新共享名称数据及审计文件；无历史 Telegram 编辑/重发，也未改生产模型、策略、账本、结算或派单逻辑。

## 2026-10-14 正式范围继续补齐（第三十八批）
- 7M 球队页将 `Buducnost Banovici` 与“巴諾維奇”直接并列（https://team.7m.com.cn/4424/index.shtml）。为 TotalCorner `team_id 12109` 保存简体 canonical“巴诺维奇”，繁体译名作为 alias；没有合并其他同名/近名 ID。
- 共享库提交 `64f9b53d6ab7e87f87e661ada45043d8327cede2` 已推送 master，本批新增1条。当前 formal union 2,468 IDs：2,228 canonical、240 unresolved（90.28%）；M1 1,494/1,553（96.20%）；M1 OU-R1 52/52；MR1 AH 1,723/1,921（89.69%）；MR1 AI declared mirror 1,494/1,553（96.20%）。
- M1 formatter 6/6、MR1 shared registry test 1/1、curator 与 `git diff --check` 均通过。变更仅为中文展示 registry/coverage/audit；未触及模型、策略、账本、结算、Telegram 正式发送，也未编辑历史消息。其余未匹配球队保持逐队核验，不以猜译填充。

## 2026-10-14 正式范围继续补齐（第三十九批）
- 中文维基“诺亚足球会”条目说明该俱乐部最初名为“阿尔察赫足球会（FC Artsakh）”（https://zh.wikipedia.org/wiki/诺亚足球会）。为 TotalCorner `team_id 43401` / provider `Artsakh`、Armenia league_id `55` 记录该历史名称“阿尔察赫”及来源别名，ID 独立保留，不与其他 Artsakh 命名球队合并。
- 共享库提交 `78ff52837971826f0ff1d47fb08cdeaece2850d2` 已推送 master。本批新增1条。formal union 2,468 IDs：2,229 canonical、239 unresolved（90.32%）；M1 1,495/1,553；M1 OU-R1 52/52；MR1 AH 1,723/1,921；MR1 AI declared mirror 1,495/1,553。M1 formatter 6/6、MR1 shared registry test 1/1 PASS，curator 与 `git diff --check` PASS。
- 仅更新共享名称库及审计产物；无 Telegram 发送/编辑，无模型、策略、账本、结算或派单规则变更。

## 2026-10-14 正式范围继续补齐（第四十批）
- Wikimedia Commons 中文分类页将 TB Tvøroyri 列为“TB特沃罗伊里”，并给出“特沃罗伊里足球俱乐部”中文条目（https://commons.wikimedia.org/wiki/Category:TB_Tv%C3%B8royri?uselang=zh）。为 TotalCorner `team_id 52432` / provider `TB Tvoroyri`（法罗群岛 league IDs `1439/10635`）新增 canonical“TB特沃罗伊里”和中文/原文别名，保持该 reserve/club identity 的现有 ID。
- 共享库提交 `60191cb33e1f888fe6278bc440ed65d77da08cf1` 已推送 master。本批新增1条。formal union 2,468 IDs：2,230 canonical、238 unresolved（90.36%）；M1 1,495/1,553（96.27%）；M1 OU-R1 52/52；MR1 AH 1,724/1,921（89.74%）；MR1 AI declared mirror 1,495/1,553（96.27%）。
- M1 formatter 6/6 与 MR1 shared registry test 1/1 PASS，curator 和 `git diff --check` PASS。仅共享展示名/审计数据变化，无 Telegram 发送/编辑，也未修改生产模型、策略、账本、结算和派单条件。

## 2026-10-14 正式范围继续补齐（第四十一批）
- 中文足球赛事页面将 `FC Viktoriya Sumy` 显示为“维多利亚苏梅”，球队页同时标出英文名 VictoriaSumy（https://zuqiuba-iqiyi.com/qiudui/BcPWy/）；并由中文赛事列表中的“维多利亚苏梅足球俱乐部”赛程用例核对该队身份。为 TotalCorner `team_id 135826` 加入 canonical 与别名，不与其他 Viktoriya/Victoria 球队合并。
- 共享库提交 `767f1f19294b88a69ac969713fd2ec73c07a5a76` 已推送 master。本批新增1条。正式范围2,468 IDs：2,231 canonical、237 unresolved（90.40%）；M1 1,495/1,553（96.27%）；OU-R1 52/52；MR1 AH 1,725/1,921（89.80%）；MR1 AI declared mirror 1,495/1,553（96.27%）。
- M1 formatter 6/6、MR1 shared registry display test 1/1 PASS，curator 和 `git diff --check` PASS。只更新展示名库和审计文件；无 TG 操作，无模型、策略、账本、结算或派单规则变更。

## 2026-10-14 正式范围继续补齐（第四十二批）
- 中国足球赛事数据页将黑山乙 `FK Podgorica` 显示为“FK波德戈里察”（https://data.chuqi.com/football/comp-integral/11070/）；7M/雷速赛程中也以此名称标示该队，并与另一个 `Internacional Podgorica` 区分。为 TotalCorner `team_id 53919` 新增此 ID 专属 canonical。
- Tips.GG 简中球队页将 `Halkanoras Idaliou` 标为“伊达利欧哈卡诺拉斯队”（https://tips.gg/cn/team/halkanoras-idaliou-football/）。为 TotalCorner `team_id 18247` 记录去“队”后缀的 canonical“伊达利欧哈卡诺拉斯”及 Chalkanoras/Halkanoras 别名。
- 共享库提交 `e1b6c75eb64439a6270c342ea5593436065a156e` 已推送 master，本批新增2条。正式范围2,468 IDs：2,233 canonical、235 unresolved（90.48%）；M1 1,496/1,553（96.33%）；OU-R1 52/52；MR1 AH 1,727/1,921（89.90%）；MR1 AI declared mirror 1,496/1,553（96.33%）。
- M1 formatter tests 6/6 与 MR1 shared-registry test 1/1 PASS，curator 和 `git diff --check` PASS。只更新公共中文名称数据/审计；无 Telegram 发送/编辑，策略、模型、账本、结算及信号规则未改。

## 2026-10-14 正式范围继续补齐（第四十三批）
- 中文维基条目“哈尔科夫足球俱乐部”对应当前英文 `FC Kharkiv` 身份；Wikimedia Commons 使用页也明确将英文 FC Kharkiv 对应至该中文条目（https://zh.wikipedia.org/wiki/哈爾科夫足球俱樂部）。为 TotalCorner `team_id 184801` 新增 canonical“哈尔科夫足球俱乐部”，并保留 `Metalist 1925 Kharkiv` 作为名称沿革别名；不与 Kharkiv 其他俱乐部 ID 合并。
- 共享库提交 `fd0e16d04ec52b59953fb5b5a9ef00edba876571` 已推送 master。本批新增1条。formal union 2,468 IDs：2,234 canonical、234 unresolved（90.52%）；M1 1,497/1,553（96.39%）；OU-R1 52/52；MR1 AH 1,728/1,921（89.95%）；MR1 AI declared mirror 1,497/1,553（96.39%）。
- M1 Telegram formatter 6/6 与 MR1 shared display test 1/1 PASS，curator / `git diff --check` PASS。仅名称映射与 coverage/audit 更新，无 Telegram 发送/编辑，生产策略、模型、账本、结算不变。

## 2026-10-14 正式范围继续补齐（第四十四批）
- 中文维基百科球队条目“斯塔爾卡緬斯科耶足球會”明确对应英文 Stal Kamianske（https://zh.wikipedia.org/wiki/斯塔爾卡緬斯科耶足球會）；为 TotalCorner `team_id 33616` 新增该身份的简体中文 canonical“斯塔尔卡缅斯科耶足球会”，保留英文及繁体标题别名，不与其他 Stal 球队合并。
- 共享库提交 `93ccc20765b5e955a74e6a5f691951b824d2096d` 已推送 master。本批新增1条。正式范围2,468 IDs：2,235 canonical、233 unresolved（90.56%）；M1 1,498/1,553；M1 OU-R1 52/52；MR1 AH 1,729/1,921；MR1 AI declared mirror 1,498/1,553。
- M1 Telegram formatter 6/6 与 MR1 shared display test 1/1 PASS，curator 和 `git diff --check` PASS。仅共享展示名称与审计数据更新；无 Telegram 发送/编辑，也未修改模型、策略、账本、结算或派单规则。

## 2026-10-14 正式范围继续补齐（第四十五批）
- 中文维基百科“索哈杰”条目提供埃及 Sohag 的稳定简体中文地名（https://zh.wikipedia.org/wiki/索哈傑）；与已存 provider identity `Suhag` 对应的埃及足球队用于 canonical“索哈杰”。仅处理 TotalCorner `team_id 12078`，未将另一条拼写近似的 `Sohag`（team_id 31006）合并或擅自赋名。
- 共享库提交 `e01cecbf5fdd5b488ec2836d1da6529373ef24bd` 已推送 master。本批新增1条。正式范围2,468 IDs：2,236 canonical、232 unresolved（90.60%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,729/1,921（90.01%）；MR1 AI declared mirror 1,498/1,553（96.46%）。
- M1 formatter 6/6、MR1 shared display test 1/1 PASS，curator 和共享库 `git diff --check` PASS。仅更新公共展示名称与审计数据；无 Telegram 发送/编辑、无模型/策略/正式账本/结算/派单规则修改。

## 2026-10-14 正式范围继续补齐（第四十六批）
- Sofascore 简体中文 CSM Slatina 球队页将球队展示为“斯拉蒂纳CSM”（https://www.sofascore.com/zh/football/team/csm-slatina/298063）。为 TotalCorner `team_id 48550` 加入对应 canonical 和全称别名，保持其罗马尼亚俱乐部身份。
- 共享库提交 `905d2b66d91bc29093294deba8e8458c5bd8f110` 已推送 master。本批新增1条。正式范围2,468 IDs：2,237 canonical、231 unresolved（90.64%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,730/1,921（90.06%）；MR1 AI declared mirror 1,498/1,553（96.46%）。
- M1 formatter 6/6、MR1 shared display test 1/1 PASS，curator 与 `git diff --check` PASS。仅展示名称及审计产物更新，无 Telegram 操作，生产模型、策略、账本、结算和派单规则未动。

## 2026-10-14 正式范围继续补齐（第四十七批）
- Tips.GG 简体中文历史比赛页将 `KF 2 Korriku` 显示为“KF 2科里库”（https://tips.gg/cn/archive/kf-2-korriku-football-vs-kf-ramiz-sadiku-football/）；为 TotalCorner `team_id 52049` 新增该 canonical 与 Prishtinë 拼写别名，Kosovo 队身份和 team ID 独立保留。
- 共享库提交 `1a27e48e666cfe0a07cab7208c2f888fa5f350a4` 已推送 master。本批新增1条。正式范围2,468 IDs：2,238 canonical、230 unresolved（90.68%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,731/1,921（90.11%）；MR1 AI declared mirror 1,498/1,553（96.46%）。

## 2026-10-14 正式范围继续补齐（第四十八批）
- Tips.GG 中文乌克兰杯球队表将 Khust City 标为“胡斯特城”（https://tips.gg/cn/tournament/football-ukrainian-cup-2024-25/），与 TotalCorner `team_id 114055` / `FC Khust` 身份匹配；Tips.GG 中文历史页将 FC Suhareka 显示为“苏哈雷卡”（https://tips.gg/cn/archive/fc-suhareka-football-vs-kf-tefik-canga-football/），并由俱乐部官方资料确认 FC Suhareka 身份（https://www.fcsuhareka.com/）。新增这2个独立 ID 的 canonical，不与近名球队合并。
- 共享库提交 `9ce5197635cc85202287b48aa9e9392c08546977` 已推送 master，本批新增2条。正式范围2,468 IDs：2,240 canonical、228 unresolved（90.76%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,731/1,921（90.11%）；MR1 AI declared mirror 1,498/1,553（96.46%）。M1 Telegram formatter 6/6、MR1 shared registry test 1/1 PASS；curator 与 `git diff --check` PASS。仅修改共享展示名称数据及策展记录，未触及生产策略/模型/账本或发送、编辑任何 Telegram 消息。

## 2026-10-14 正式范围继续补齐（第四十九批）
- Tips.GG 简体中文历史赛程和球队页将 `Al Qous` 显示为“库斯”（https://tips.gg/cn/archive/al-liwaa-football-vs-al-qous-club-football/）；为 TotalCorner `team_id 118984` 新增 canonical“库斯”及 Al-Qous 全称别名，保留沙特球队独立身份。
- 共享库提交 `a03008526f822a20471e8336105df3b07ef67dce` 已推送 master，本批新增1条。formal union 2,468 IDs：2,241 canonical、227 unresolved（90.80%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,731/1,921（90.11%）；MR1 AI declared mirror 1,498/1,553（96.46%）。M1 formatter 6/6 PASS；共享库 consumer test 1/1 PASS（上一批复验）；curator 与 `git diff --check` PASS。仅修改展示名称数据，无生产策略或 TG 历史消息修改。

## 2026-10-14 正式范围继续补齐（第五十批）
- Tips.GG 中文保加利亚乙级联赛球队表将 Belasitsa Petrich 显示为“贝拉西察佩特里奇”（https://tips.gg/cn/tournament/football-bulgaria-second-professional-league-2023-24/）；为 TotalCorner `team_id 14865` / provider `Belasitza Petrich` 新增 canonical 与规范拼写别名，球队 ID 保持独立。
- 共享库提交 `efb499642d1c45c543bfa531c09f55c9709da342` 已推送 master，本批新增1条。formal union 2,468 IDs：2,242 canonical、226 unresolved（90.84%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,731/1,921（90.11%）；MR1 AI declared mirror 1,498/1,553（96.46%）。M1 formatter 6/6 PASS；curator 与 `git diff --check` PASS。仅展示库更新，生产策略及 TG 历史消息未改。
- M1 formatter 6/6、MR1 shared display test 1/1 PASS，curator 和 `git diff --check` PASS。只更新共享显示名称及审计文件；无 Telegram 发送/编辑或生产策略、模型、账本、结算变更。

## 2026-10-14 正式范围继续补齐（第五十一批）
- 雷速中文球队页直接显示 `FC Bacau` 为“FC贝卡”（https://m.leisu.com/data/zuqiu/team-76388）；该页的英文身份与 provider 名完全一致，联赛范围为罗马尼亚；为 TotalCorner `team_id 134085` 增加 canonical“FC贝卡”及 FC Bacău 拼写别名，未与其他罗马尼亚球队合并。
- 共享库提交 `8a4f03b7ad78130f94f7419fe1d03c80e4c80568` 已推送 master（先纳入远端新提交 `31b830f7` 后快进发布）。本批新增1条。formal union 2,468 IDs：2,243 canonical、225 unresolved（90.88%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,731/1,921（90.11%）；MR1 AI declared mirror 1,498/1,553（96.46%）。M1 formatter 6/6 PASS；curator 与 `git diff --check` PASS；MR1 shared registry consumer test 最近复验1/1 PASS。生产策略、账本及既有 Telegram 消息未修改。

## 2026-10-14 正式范围继续补齐（第五十二批）
- Tips.GG 简体中文球队页将当前的 `Gloria Bistrita` 显示为“比斯特里察荣耀队”，页面赛事/赛程明确为罗马尼亚乙级联赛 2026/27，并列出与 FC Bacau 等本季对手的同一赛程（https://tips.gg/cn/team/fc-gloria-bistrita-football/）；与官方当前 CS Gloria Bistrița 身份资料交叉确认（https://gloria2018.ro/）。为 TotalCorner `team_id 113178` / `CS Gloria 2018 Bistrita-Nasaud` 增加 canonical 和名称别名，保持与历史已解散的 Gloria Bistrița 俱乐部身份区分。
- 共享库提交 `930e1e7725b5ad2d0e59deb39318196f999ed08a` 已推送 master，本批新增1条。formal union 2,468 IDs：2,244 canonical、224 unresolved（90.92%）；M1 1,498/1,553（96.46%）；M1 OU-R1 52/52；MR1 AH 1,731/1,921（90.11%）；MR1 AI declared mirror 1,498/1,553（96.46%）。M1 formatter 6/6、MR1 shared registry consumer test 1/1 PASS；curator 与 `git diff --check` PASS。仅展示名映射更新，未修改模型、策略、账本或历史 Telegram。

## 2026-10-14 正式范围继续补齐（第五十三批）
- 中文足球比赛记录将希腊 Diagoras 标为“迪亚戈拉斯”（https://www.okooo.com/soccer/match/1156257/form/）；FootyStats 中文赛事页亦以“迪亚戈拉斯”指称 Diagoras GS Rodos（https://footystats.org/cn/greece/ao-chania-kissamikos-fc-vs-diagoras-gs-rodos-h2h-stats）。TotalCorner `team_id 43745` 的希腊联赛上下文与该队相符，登记为独立 canonical，不合并其他同名 Diagoras。
- 共享库提交 `c806bae5b5e5de40be0b148792f075198bb3acdd` 已推送 master。本批新增1条。formal union 2,468 IDs：2,245 canonical、223 unresolved（90.96%）；M1 1,499/1,553（96.52%）；M1 OU-R1 52/52；MR1 AH 1,738/1,921（90.47%）；MR1 AI declared mirror 1,499/1,553（96.52%）。M1 Telegram formatter 6/6 PASS；curator 与共享库 `git diff --check` PASS。MR1 最新 master 源码已确认按 team ID 读取同一 registry；本机消费者 checkout 存有未提交文件，未覆盖或改动。未发送或编辑历史 Telegram；未验证实际生产消息内容或历史 TG 编辑权限。策略、模型、账本、结算、派单规则未改。

## 2026-10-14 正式范围继续补齐（第五十四批）
- 球探体育中文球队档案明确列出 `FK Neptunas Klaipeda`（页面显示 FK海王星克萊佩達，英文名一致：https://zq.titan007.com/big/team/Summary/48661.html）；将 TotalCorner `team_id 67240` canonical 定为简体“海王星克莱佩达”，并保留“克莱佩达海王星”等中文别名，未与其他立陶宛球队合并。
- 共享库提交 `ae532bf2b271b4df8076e4a72f9cf328ffd9232f` 已推送 master，本批新增1条。formal union 2,468 IDs：2,246 canonical、222 unresolved（91.00%）；M1 1,499/1,553（96.52%）；M1 OU-R1 52/52；MR1 AH 1,739/1,921；MR1 AI declared mirror 1,499/1,553。M1 formatter 6/6、curator 与 `git diff --check` PASS。未进行 Telegram 发送/编辑，也未更改模型、策略、账本、结算或派单规则。

## 2026-10-14 正式范围继续补齐（第五十五批）
- 中文维基百科安道尔球队列表逐行列出 Penya Encarnada d'Andorra 与中文名“佩尼亚恩卡纳达”（https://zh.wikipedia.org/wiki/佩尼亞恩卡納達安道爾）；TotalCorner `team_id 50972` 对应安道尔赛事范围，加入 canonical 和繁体/英文别名，保持球队身份独立。
- 共享库提交 `f12f67914aee3b7cc83453195e9d80da6f3d4561` 已推送 master。本批新增1条。formal union 2,468 IDs：2,247 canonical、221 unresolved（91.05%）；M1 1,499/1,553（96.52%）；M1 OU-R1 52/52；MR1 AH 1,740/1,921；MR1 AI declared mirror 1,499/1,553。M1 formatter 6/6、curator 与 `git diff --check` PASS。其余本轮检索对象无可靠中文球队名出处，保留 unresolved；不涉及任何 Telegram 发送/编辑及生产策略、模型、账本、结算修改。

## 2026-10-14 正式范围继续补齐（第五十六批）
- 7M 中文球队档案分别明确标注 FK TransINVEST 为“特兰斯因维斯特”（https://team.7m.com.cn/650201/index.shtml）、FK TransINVEST B 为“特兰斯因维斯特B队”（https://team.7m.com.cn/726884/index_gb.shtml）；按 TotalCorner 独立 team IDs `101061` 和 `145681` 写入，B队不与一线队合并。
- 共享库提交 `3f9061170850154f451249c9cfb72898f29b7bab` 已推送 master，本批新增2条。formal union 2,468 IDs：2,249 canonical、219 unresolved（91.13%）；M1 1,499/1,553（96.52%）；M1 OU-R1 52/52；MR1 AH 1,742/1,921；MR1 AI declared mirror 1,499/1,553。M1 formatter 6/6、curator 与 `git diff --check` PASS。只更新共享展示库和审计数据；无 Telegram 发送/编辑或模型、策略、账本、结算、派单规则变更。

## 2026-10-14 正式范围继续补齐（第五十七批）
- FootyStats 中文档案将 VMFD Žalgiris Vilnius II 标为“扎基里斯B队”，并明确 Lithuania 1 Lyga 及俱乐部官网身份（https://footystats.org/cn/clubs/vmfd-zalgiris-vilnius-ii-1240）；TotalCorner `team_id 71679` 的 provider name FK Zalgiris Vilnius II 与其别名及 league_id 542 匹配。为该独立 provider ID 复用已核验 canonical，不与一线队或另一 team ID 合并。
- 共享库提交 `5b0cde28ee6bda35a7eeb4fbcdd2139d42f5dc2b` 已推送 master，本批新增1条。formal union 2,468 IDs：2,250 canonical、218 unresolved（91.17%）；M1 1,500/1,553（96.59%）；M1 OU-R1 52/52；MR1 AH 1,743/1,921；MR1 AI declared mirror 1,500/1,553。M1 formatter 6/6、curator 与 `git diff --check` PASS。只更新共享展示名称及审计文件；未触及模型、策略、正式账本、结算或 Telegram。

## 2026-10-14 正式范围继续补齐（第五十八批）
- 中文维基百科《欧洲顶级足球俱乐部列表》明确以 KF Gjilani 对应中文名“格尼拉内”（https://zh.wikipedia.org/wiki/歐洲頂級足球俱樂部列表）；官方俱乐部实体名 Klubi Futbollistik Gjilani 与 TotalCorner `team_id 71368` provider short name Gjilani 对应，联赛 ID 8293 一致。为该独立 ID 登记 canonical 与全名/异体别名。
- 共享库提交 `e4f77c67c826301b23a2e8721379444230839283` 已推送 master，本批新增1条。formal union 2,468 IDs：2,251 canonical、217 unresolved（91.21%）；M1 1,500/1,553（96.59%）；M1 OU-R1 52/52；MR1 AH 1,744/1,921；MR1 AI declared mirror 1,500/1,553。M1 formatter 6/6、curator 与 `git diff --check` PASS。未修改生产策略、模型、账本、结算或任何 Telegram 消息。

## 2026-10-14 正式范围继续补齐（第五十九批）
- Tips.GG 中文历史球队记录提供 FC Nagykanizsa 的 canonical “纳吉卡尼扎”（https://tips.gg/cn/archive/fc-ajka-football-vs-ufc-nagykanizsa-football/）；TotalCorner `team_id 133452` provider 原名明确含 `(W)`，本次新增“纳吉卡尼扎女足”，保留独立女子球队身份，不与男子队混同。
- 共享库提交 `23980713224d871da030998ccad8bfa92fe75b4a` 已推送 master，本批新增1条。formal union 2,468 IDs：2,252 canonical、216 unresolved（91.25%）；M1 1,500/1,553（96.59%）；M1 OU-R1 52/52；MR1 AH 1,745/1,921；MR1 AI declared mirror 1,500/1,553。M1 formatter 6/6、curator 与 `git diff --check` PASS。只更新共享中文展示数据与审计信息，无 TG 操作及策略/模型/账本/结算改动。

## 2026-10-14 正式范围继续补齐（第六十批）
- Sofascore 简体中文 Flint Town United 队页显示“富林特联”（https://www.sofascore.com/zh/football/team/flint-town-united/37090）；TotalCorner 的 Flint Town Utd 赛历和 team_id 40413 的 Wales Premier League league_id 177 相互印证。映射为“富林特联”；明确不与 Flint Mountain 合并。
- SportScore 中文 MEAP Nisou 球队页显示“MEAP尼苏”（https://sportscore.com/zh/football/team/meap-nisou/vjxm8gh4w9nr6od/）；为 TotalCorner `team_id 26815` 保存该 canonical，原始 ID/name 保持。
- 共享库提交 `f0f0fdf1` 已推送 master，本批新增2条。formal union 2,468 IDs：2,254 canonical、214 unresolved（91.33%）；M1 1,500/1,553；M1 OU-R1 52/52；MR1 AH 与 MR1 AI mirror 按最新共享 `formal_scope_coverage.json` 生成。M1 formatter 测试6/6、curator、`git diff --check` PASS。未发送或编辑任何 Telegram 消息；未更改生产模型/策略、账本或结算。

## 2026-10-14 正式范围继续补齐（第六十一批）
- QTX 中文比赛报道将来自科索沃贾科维察的 KF Vëllaznimi 显示为“维尔拉兹尼米”（https://live.qtx.com/fenxi/J6YdX3BljM.html）。为 TotalCorner provider IDs `41854`、`45431`、`92798` 分别补 canonical/alias，但保留三个 provider ID 独立、不合并近名 Vllaznia 球队。
- 共享 registry 已推送 `6acf8105f557a1284cf959cd76675dd67b494bec`。curator 实际结果：正式范围 2,468 IDs，2,259 canonical / 209 unresolved（91.53%）；M1 1,506/1,553（96.97%）；M1 OU-R1 52/52（100%）；MR1 AH 1,749/1,921（91.05%）；MR1 AI declared mirror 1,506/1,553（96.97%）。整个 registry 12,276 team IDs / 4,275 canonical（34.82%），联赛 334/771；209 条未匹配清单及逐条原因见共享 `formal_scope_coverage.json`。
- M1 display tests 6/6 PASS，curator 和 `git diff --check` PASS。新 registry 发布后重跑既有历史“仅编辑消息” workflows：M1 run `38593680540` success，报告 eligible=41、edited=0、already_matching=41、missing original text=99、unmapped=97、failed=0；MR1 Formal run `38593688095` success（收据 eligible=0、edited=0、skipped=125、unresolved=0、failed=0）；MR1 AI run `38593695129` success（报告 total=201、edited=0、failed=9、unresolved=192；9 条均为 Telegram 400 `message to edit not found`，其余名称仍缺可靠映射）。三个流程本轮实际历史编辑均为0，不能描述为历史 TG 已修复。
- M1 OU-R1 名称覆盖为 52/52，但当前 M1 仓库没有独立 formal Telegram ledger / 历史名称编辑器，无法核验或编辑其历史消息。未新增工作流。生产模型、策略、范围、订单账本、结算及派单规则未改。

## 2026-10-15 正式范围继续补齐（第六十三批）
- Sofascore 简体中文 Porto Suez 球队页显示“苏伊士波尔图”，并标识埃及球队（https://www.sofascore.com/zh/football/team/porto-suez/298274）；为 TotalCorner `team_id 48944` 增加该 canonical。移除容易与独立 `team_id 80563 Porto EL Sokhna SC` 混淆的 Porto El-Sokhna 别名，不跨 ID 合并。
- 中文维基俱乐部条目提供 Hegelmann 的稳定名称“赫格尔曼”（https://zh.wikipedia.org/wiki/赫格尔曼足球俱乐部）；为 TotalCorner `team_id 82640 Hegelmann Litauen II` 记为“赫格尔曼B队”，保留 II 预备队身份且不与一线队 `31954` 合并。
- 最新共享库提交 `e01fc0dea6a74ee22d6d47a16bda7d2c847fc9c0` 已推送 master。本批之后正式范围最新口径为 2,468 IDs：2,262 canonical、206 unresolved（91.65%）；M1 1,506/1,553（96.97%）、M1 OU-R1 52/52（100%）、MR1 AH 1,752/1,921（91.20%）、MR1 AI 声明范围镜像 M1 为 1,506/1,553（96.97%），MR1 AI confidence≥50 observed cohort 181/182（99.45%）。准确明细以该共享库 `formal_scope_coverage.json` 为准。
- 上一批 TG 历史 name-only 检查：M1 run `38595095719` success，eligible=41、edited=0、already_matching=41、缺失原文=99、未映射=97、failed=0；MR1 Formal `38595103478` success，125 already processed、edited=0、unresolved=0；MR1 AI `38595110762` success，total=201、edited=0、failed=9、unresolved=192，9 条均 Telegram API 400 `message to edit not found`。
- 针对 `e01fc0de` 最新映射的同一组现有历史修复工作流已再次运行：M1 `38595595398`、MR1 Formal `38595603040`、MR1 AI `38595610655`。MR1 Formal 已 success；M1 与 MR1 AI 在本次交接更新时仍运行中，结束状态/实际编辑数须补记后再宣称完成。未触发新消息发送。
- 三个上述运行现已全部 success：M1 `38595595398` 再次 eligible=41、edited=0、already_matching=41、缺原文99、unmapped97、failed0；MR1 Formal `38595603040` eligible0、edited0、already processed125、unresolved0、failed0；MR1 AI `38595610655` total201、edited0、failed9、unresolved192，失败均为 Telegram `400 message to edit not found`。所以本批没有一条历史 TG 成功改字，也没有任何重发。
- 本地 `test_m1_telegram_display_repair.py` 2/2 PASS；M1 formatter 6/6 与 MR1 shared display test 1/1 的既有验证仍通过。MR1 运行仓库代码通过 `src/football-display-names.js` 读取唯一外部 `display_names.json`；MR1 AI unresolved 只写诊断计数，不阻塞通知。所有覆盖率及 206 条逐队名称/原因见共享 `formal_scope_coverage.json`。
- 当前 unresolved 206 条保留于共享库 `formal_scope_coverage.json`，按无唯一、可核验中文来源而未赋名；没有用猜测音译补覆盖率。M1 formatter、MR1 display 接入及历史名称修复不改变任何模型、策略、正式账本、结算或订单条件。

## 2026-10-15 正式范围继续补齐（第六十四批）
- 懂球帝简体中文球队页将 Llanelli Town 明确显示为“拉内利”，同页列明英文名 Llanelli Town（https://www.allfootballapp.com/zh-CN/team/16236）。为正式范围 `team_id 147575` 添加 canonical“拉内利”及 Llanelli Town AFC 别名，ID 保持独立。
- 共享库提交 `0a71864c13c50d426d74bbb159c94db6d1ad1e20` 已推送 master。正式范围 2,468 IDs：2,263 canonical、205 unresolved（91.69%）；M1 1,507/1,553（97.04%）、OU-R1 52/52（100%）、MR1 AH 1,753/1,921（91.25%）、MR1 AI 声明范围镜像 M1 为 1,507/1,553（97.04%）。
- 本批之后既有 name-only Telegram 修复工作流均 success：M1 `38596342571` eligible41、edited0、already_matching41、缺原文99、unmapped97、failed0；MR1 Formal `38596348767` edited0、already_processed125、unresolved0、failed0；MR1 AI `38596356968` total201、edited0、unresolved192、failed9，9 条均 Telegram 400 `message to edit not found`。本批实际 TG 历史改字仍为0，没有重发。
- `test_m1_telegram_display_repair.py` 2/2 PASS；M1 formatter 6/6、MR1 shared-registry display test 1/1 既有验证通过。只有展示名数据更新，未更改任何生产模型、策略、账本、结算或信号条件。

## 2026-10-15 正式范围继续补齐（第六十五批）
- 核验已推送的 Llanelli `team_id 147575` 映射被唯一共享库记录，当前 registry SHA 为 `0a71864c13c50d426d74bbb159c94db6d1ad1e20`；coverage 已重算为正式范围 2,468 IDs：2,263 canonical、205 unresolved（91.69%）；M1 1,507/1,553（97.04%）、OU-R1 52/52（100%）、MR1 AH 1,753/1,921（91.25%）、MR1 AI declared mirror 1,507/1,553（97.04%）。
- 依该 registry 的历史 Telegram 校验：M1 `38596342571` success（eligible41、edited0、already_matching41、缺原文99、unmapped97、failed0）；MR1 Formal `38596348767` success（edited0、already_processed125、unresolved0、failed0）；MR1 AI `38596356968` success（total201、edited0、unresolved192、failed9，9条均 `400 message to edit not found`）。未重发消息。
- 本轮 `test_m1_telegram_display_repair.py` 2/2 PASS，`git diff --check` PASS。实际历史编辑为0；没有修改生产模型/策略/账本/结算/信号条件。剩余完整名单与逐条原因见共享 `formal_scope_coverage.json`。

## 2026-10-15 正式范围继续补齐（第六十六批）
- Football Kit Archive 简体中文 Lori FC 页面以“洛里主场球衣”称呼 Lori FC（https://www.footballkitarchive.com/zh/lori-fc-2020-21-zhu-chang-qiu-yi-15489/）。核对 TotalCorner `team_id 43638` 属于 Armenian league_id 55，且 registry 中无同名 canonical 冲突，为其新增 canonical“洛里”。
- 共享库提交 `79c3bc6e80e634b2cb244256f9cdb65b303de6bf` 已推送 master。正式范围 2,468 IDs：2,264 canonical、204 unresolved（91.73%）；M1 1,508/1,553（97.10%）、M1 OU-R1 52/52、MR1 AH 1,753/1,921（91.25%）、MR1 AI declared mirror of M1 1,508/1,553（97.10%）。`test_m1_telegram_display_repair.py` 2/2 PASS，curator 和 `git diff --check` PASS。
- 新共享库后的历史 TG workflows：M1 `38597295291` success（eligible41、edited0、already_matching41、missing original text99、unmapped97、failed0）；MR1 Formal `38597304876` success（edited0、already processed125、unresolved0）；MR1 AI 编辑步骤运行成功但整体 run `38597313033` failure，候选9条均仍为 Telegram `400 message to edit not found`、unresolved192、edited0。最后的“Persist actual edit receipts” push 遇 MR1 runtime 并发更新导致 GitHub 拒绝 non-fast-forward/ref lock（远端 master 当时已前进至 `7c15870e…`，期望旧 ref `13b14d25…`）；因此本轮没有可确认的 MR1 AI repair receipt 持久化。没有新发策略消息。
- 生产策略、模型、阈值、订单账本、结算均未修改；历史 TG 实际编辑数仍为0。204条未匹配逐条清单及原因以共享 `formal_scope_coverage.json` 为准。

## 2026-10-15 正式范围继续补齐（第六十七批）
- 7M 简体/繁体中文足球数据页对 TotalCorner `team_id 86494 CSC 1599 Selimbar` 给出名称“瑟利姆壩”，同页列出英文队名和罗马尼亚赛程；为该 ID 新增简体 canonical“瑟利姆坝”，保留繁体别名，不与其他 Selimbar 身份合并。
- 共享库提交 `d4082d56ba2e50c61b641295513527673ab03864` 已推送 master。正式范围 2,468 IDs：2,265 canonical、203 unresolved（91.77%）；M1 1,508/1,553（97.10%）、OU-R1 52/52、MR1 AH 1,754/1,921（91.31%）、MR1 AI declared mirror M1 1,508/1,553（97.10%）。M1 display repair tests 2/2 PASS，curator / `git diff --check` PASS。
- 最新 registry 后的 name-only Telegram workflows：M1 `38598104393` success（eligible41、edited0、already_matching41、缺原文99、unmapped97、failed0）；MR1 Formal `38598117419` success（edited0、already processed125、unresolved0）；MR1 AI `38598124608` success，但仍 total201、edited0、unresolved192、failed9，9条均 Telegram `400 message to edit not found`。没有重发历史策略消息。
- 只更改共享展示名和 coverage/audit，未更改任何模型、策略、阈值、正式账本、结算或发送规则。203 条待核实明细见共享 `formal_scope_coverage.json`。

## 2026-10-15 正式范围补齐跟进（第六十八批，来源复核）
- 从最新共享 master `d4082d56ba2e50c61b641295513527673ab03864` 重新核对，正式范围仍为 2,468 个去重 team ID，canonical 2,265，未匹配 203（91.77%）；M1 1,508/1,553（97.10%），M1 OU-R1 52/52，MR1 AH 1,754/1,921（91.31%），MR1 AI declared mirror of M1 1,508/1,553（97.10%）。此前交接里的“718/740”不是当前 master 数字。
- 继续对照当前 unresolved 清单中罗马尼亚、塞尔维亚、波黑、马耳他、乌克兰、匈牙利等队伍及既有 REEP/Wikidata 中文证据。官方/可核验资料确认了 AFC Metalul Buzău、SC Popești-Leordeni、NK Jedinstvo Bihać、FK Kabel、Ahrobiznes Volochysk、Pembroke Athleta 等英文身份，但本轮检索到的来源未提供可确认的主流简体中文队名；没有新增 canonical，保留 unresolved，避免将自行音译写成权威名。
- 当前唯一共享库未有数据变更；没有为制造提交而改写 coverage。历史 name-only workflows 最近一次回执仍是 batch 67：M1 0 条成功编辑（41 条已匹配、99 条缺原文、97 条未映射）；MR1 Formal 0 条编辑（125 已处理）；MR1 AI 0 条编辑、9 条 Telegram `message to edit not found`、192 条名称未解析。历史消息未重发。
- 本轮未修改模型、策略、订单账本、结算或 Telegram 发送条件。后续继续只对找到可靠中文来源的具体 ID 入库；未匹配及逐条原因以共享仓库 `data/football_display_names/formal_scope_coverage.json` 为准。

## 2026-10-15 正式范围继续补齐（第六十二批）
- Tips.GG 简体中文 Goytre United 球队页明确显示“戈伊特雷联队”（https://tips.gg/cn/team/goytre-utd-football/）；与 TotalCorner `team_id 54106` / provider `Goytre Utd`、Welsh league_id 11959 一致，新增 canonical 与官方拼写别名。
- 共享 master 提交 `b209e795039a32eb2dc7c0a9f86a06d63f4a4dd6`；正式范围 2,468 IDs，2,260 canonical / 208 unresolved（91.57%）；M1 1,506/1,553（96.97%）、M1 OU-R1 52/52（100%）、MR1 AH 1,750/1,921（91.10%）、MR1 AI declared mirror 1,506/1,553（96.97%）；confidence≥50 observed cohort 181/182（99.45%）。M1 formatter 6/6 PASS，curator 和 `git diff --check` PASS。
- 新 registry 后再次运行既有历史 name-only Telegram workflows，运行号：M1 `38594324496`、MR1 Formal `38594334081`、MR1 AI `38594342938`，全部 success。M1 报告 eligible=41、edited=0、already_matching=41、missing original text=99、unmapped=97、failed=0；MR1 Formal eligible=0、edited=0、skipped=125、unresolved=0、failed=0；MR1 AI total=201、edited=0、failed=9（Telegram 400 message to edit not found）、unresolved=192。此次没有历史消息改字成功，也没有重发历史策略。

## 2026-10-15 正式范围继续补齐（第六十九批）
- 从当前共享 master `4b26ab62157c326ac40a73294be4ed599afb77f3` 核对：正式范围 2,468 个 team ID，2,265 已匹配、203 未匹配（91.77%）；M1 1,508/1,553（97.10%），M1 OU-R1 52/52，MR1 AH 1,754/1,921（91.31%），MR1 AI declared mirror 1,508/1,553（97.10%）。
- 7M 简体中文比赛记录 `https://analyse.7m.com.cn/4882320/index_gb.shtml` 将英文 `SC Lokeren-Temse` 标为“洛克伦特姆塞”；按精确英文队名及比利时赛事上下文，为 TotalCorner `team_id 73791` 新增该 canonical 与来源别名。共享库提交 `72ae84ea` 已推送 `totalcorner-research-bridge/master`。更新后正式范围 2,266/2,468（91.82%），未匹配 202；M1 1,508/1,553，OU-R1 52/52，MR1 AH 1,755/1,921，MR1 AI mirror 1,508/1,553。全库 12,276 IDs，4,282 canonical 中文名。
- M1 Telegram formatter / repair 单测 8/8 PASS；隔离 formatter 对 73791 展示为中文“洛克伦特姆塞”，未发送 TG。MR1 Formal 与 MR1 AI 的正式名称修复 workflow 均读取同一共享库。
- 实际历史修复：MR1 Formal workflow `38600053362` success，eligible 0 / edited 0 / 125 skipped / unresolved 0；MR1 AI workflow `38600062256` success，201 总项、9 个可定位候选、edited 0、unresolved 192、failed 9；9 条均为 Telegram 400 `message to edit not found`，没有重发。M1 历史名称修复 workflow `38600406058` success：eligible 41、edited 0、already matching 41、缺原消息文本 99、未映射 97、failed 0。没有重发任何历史单。
- 当前正式范围未匹配清单及逐项原因以共享 `data/football_display_names/formal_scope_coverage.json` 的 `unresolved_records` 为准。本批只增补1个有来源名称；未改模型、策略、阈值、赛事范围、正式账本、结算或 Telegram 发送规则。

## 2026-10-15 正式范围继续补齐（第七十批）
- 沿用同一共享库；没有重做历史身份恢复。本批新增4个有来源的 canonical：`team_id 33958 Santa Lucia FC → 圣卢西亚队`（OddsGPT 马耳他挑战联赛比赛页，特意与危地马拉俱乐部及圣卢西亚国家队区分）；`135321 AF Elbasani → 艾巴辛尼`（百度中文阿尔巴尼亚超级联赛球队表，500彩票网交叉使用；不与历史 KF Elbasani 合并）；`33403 Banbridge Town → 班布里奇镇`（FootyStats 中文北爱尔兰联赛赛程）；`43365 Rilski Sportist → 里尔斯基斯普迪斯特`（FootyStats 中文保加利亚联赛赛程）。来源分别为：<https://www.oddsgpt.com/yuce/football/1629689/st-andrews-4610-vs-santa-lucia/zh>、<https://bkso.baidu.com/item/阿尔巴尼亚足球超级联赛/3902473?fromModule=lemma_inlink>、<https://footystats.org/cn/northern-ireland/premier-intermediate-league/half-time-table>、<https://footystats.org/cn/bulgaria/second-league/fixtures>。保留各自 TotalCorner team ID 与 provider name，没有靠发音猜名。
- 唯一共享库已推送：`totalcorner-research-bridge/master` commit `b2ea59a9f19433d3a21b157731ac7fdcccb86878`。最新正式范围 2,468 ID：2,270 canonical、198 unresolved（91.98%）；M1 1,509/1,553（97.17%）；M1 OU R1 52/52（100%）；MR1 AH 1,758/1,921（91.51%）；MR1 AI 声明镜像 M1 为1,509/1,553（97.17%）。完整未匹配名单和逐项原因在共享 `data/football_display_names/formal_scope_coverage.json` 的 `unresolved_records`。
- M1 formatter 与历史修复单测 8/8 PASS，`git diff --check` PASS。M1 AH/OU-R1 后续 formatter 仍按同一 registry 解析；MR1/MR1 AI 正式历史修复 workflow 均显式 checkout 此共享库。MR1 AI 的九个既有候选仍因 Telegram 返回 `400 message to edit not found` 而不能编辑；192 条仍缺唯一 canonical。
- 本轮真实 name-only workflow：M1 `38601917849` success，eligible41、edited0、already_matching41、缺原文99、未映射97、failed0；MR1 Formal `38601926220` success，eligible0、edited0、already processed125、unresolved0；MR1 AI `38601934936` success，201总项、9候选、edited0、failed9（均为 Telegram `message to edit not found`）、unresolved192。没有重发历史消息，也没有更改 provider_message_id、盘口、投注方向或账本。
- M1 OU-R1 专属历史消息未见单独历史修复 ledger/workflow；本批确认其 52/52 名称覆盖与共享读取范围，但不据此声称 OU-R1 历史 Telegram 已被实际回查或编辑。所有生产模型、策略、订单和结算保持不变。
- MR1 私有仓库的只读共享库 smoke workflow `38602761639` 已尝试，但 job 在 runner 启动前即被 GitHub 账户付款/支出限制拦截（GitHub 原始注释：recent account payments failed or spending limit needs increase）；不是名称测试失败。MR1 Formal/AI 既有 quant-runner workflow 本轮均完成并读取共享 registry；仍不能把云端 smoke 标成 PASS。

## 2026-10-15 正式范围继续补齐（第七十一批）
- 继续只使用可核验来源，未做大规模历史身份恢复。新增 `team_id 31535 NK Jesenice → 耶塞尼采`；Sofascore 简体中文球员/球队上下文将该队称为“耶塞尼采”，比赛与联赛仍绑定斯洛文尼亚 NK Jesenice 身份：<https://www.sofascore.com/zh/football/player/anej-kujovic/1476302>。
- 本次累计新补5个 ID：Santa Lucia FC（33958）、AF Elbasani（135321）、Banbridge Town（33403）、Rilski Sportist（43365）、NK Jesenice（31535）。唯一共享库最新提交 `5a43941ecad925a7ff99f543048f44f370af1120` 已推送 `totalcorner-research-bridge/master`。正式范围 2,468 ID：2,271 canonical、197 unresolved（92.02%）；M1 1,509/1,553（97.17%），M1 OU R1 52/52（100%），MR1 AH 1,758/1,921（91.51%），MR1 AI declared mirror 1,509/1,553（97.17%）。准确逐项待补名单和既有原因见共享 `formal_scope_coverage.json` 的 `unresolved_records`。
- M1 formatter / name-repair 本地单测 8/8 PASS，curator 运行及 `git diff --check` PASS。共享 resolver 仍以 team_id 优先。没有改模型、策略、市场、结算、账本、订单或 Telegram 发送条件。
- 采用最终共享库后的历史 TG 核查：M1 `38603045617` success，eligible41、edited0、already_matching41、缺原文99、未映射97、failed0；MR1 AI `38603061892` success，total201、候选9、edited0、failed9（均是 Telegram `400 message to edit not found`）、unresolved192；MR1 Formal `38603053523` 的 edit step 成功（eligible0、edited0、skipped125、unresolved0），但 workflow 最终因写回状态时 MR1 runtime 并发推进 master、GitHub 拒绝旧 expected ref（non-fast-forward/ref lock）而失败。没有任何历史消息重发或投注字段修改；也没有历史消息实际编辑成功。
- MR1 私有仓库只读 registry smoke `38602761639` 被 GitHub 账户付款/支出限制在 runner 启动前拦截；云端独立 smoke 未 PASS。M1 OU-R1 当前名称覆盖仍为52/52，但没有发现它自己的历史 TG repair ledger/workflow，故不声称其历史消息已逐条编辑验收。

## 2026-10-15 正式范围继续补齐（第七十二批）
- 从剩余正式范围待补项中，以 FootyStats 简体中文斯洛文尼亚 2. SNL 对阵记录核实 `Ankaran Hrvatini → 安卡兰`，并按 TotalCorner 原身份/联赛上下文写入 `team_id 7256`；英文别名 `Ankaran` 入库，不与地点或其他球队合并。来源：<https://footystats.org/cn/clubs/nk-bela-krajina-crnomelj-2002>。
- 唯一共享库提交 `839eecd6`（完整 SHA 见 totalcorner-research-bridge/master）已推送。正式范围仍为2,468 IDs：2,272 canonical、196 unresolved（92.06%）；M1 1,510/1,553（97.23%），M1 OU-R1 52/52（100%），MR1 AH 1,759/1,921（91.57%），MR1 AI declared mirror 1,510/1,553（97.23%）。全库12,276 IDs、4,288 canonical；完整未匹配队伍及原因继续以共享 `data/football_display_names/formal_scope_coverage.json` 的 `unresolved_records` 为准。
- curator 二次运行幂等（added=0）；M1 Telegram formatter / name-repair 本地单测8/8 PASS，`git diff --check` PASS。M1 formatter 已确认读取唯一共享 registry。此批没有在 MR1 / MR1 AI 生产运行环境执行 formatter，也未执行历史 Telegram 编辑工作流；不得据此声称四条生产链已实时验收或旧消息已编辑。未改模型、策略、赛事范围、账本、结算或 TG 派单规则。
- 随后用最新共享 master 实际运行既有历史 name-only workflow：M1 run `38604165962` success，eligible 41、edited 0、already-matching 41、原文缺失 99、未映射 97、failed 0；MR1 Formal run `38604174616` success，edited 0、125 already processed、unresolved 0；MR1 AI run `38604185143` success，201 总项、9 个可编辑候选、edited 0、192 unresolved、9 failed，均为 Telegram `400 message to edit not found`。没有历史 TG 消息被实际编辑或重发。M1 OU-R1 仍无专属历史编辑 workflow。该轮日志只证明现有程序可运行及历史编辑结果，不代表四链新消息均已实测。
- Runner handoff commit `e35e75debfaae7f691e2c397747a12a003b8415d` 已推送 main。其 push 触发了仓库既有 MR1 Free Runtime（run `38604186271`）；记录时仍运行中，需后续只读检查结果，不要手动重复 dispatch。

## 2026-10-15 正式范围继续补齐（第七十三批）
- 中文维基百科《塞凡足球会》条目明确把 Sevan FC（曾名 Junior Sevan FC）称为“塞凡足球会”，并记载其参加亚美尼亚职业联赛：<https://zh.wikipedia.org/wiki/塞凡足球會>。与 TotalCorner `team_id 53319`、provider `Sevan FC` 及 Armenian league_id 55 对照后，新增 canonical“塞凡”，别名保留 Sevan；不和其他 Sevan 命名实体合并。
- 共享库提交 `684b46a086caf3797b9511940373d9ff3ffa180d` 已推送 master。正式范围2,468队：2,273 canonical、195 unresolved（92.10%）；M1 1,511/1,553（97.30%），M1 OU-R1 52/52，MR1 AH 1,759/1,921（91.57%），MR1 AI declared mirror 1,511/1,553（97.30%）。全库12,276 IDs、4,289 canonical。未匹配逐项清单仍以 `formal_scope_coverage.json#unresolved_records` 为准。
- 新 registry 上再次执行历史 name-only workflows：M1 `38604890837` success（eligible41、edited0、already_matching41、missing original text99、unmapped97、failed0）；MR1 Formal `38604898662` success（edited0、125 already processed、unresolved0）；MR1 AI `38604906335` success（201项、9候选、edited0、192 unresolved、9 failed，均 Telegram 400 `message to edit not found`）。故实际历史消息编辑数仍为0；没有重发。由 handoff push 触发的 MR1 Free Runtime `38604911139` 已完成 success。M1 formatter/name-repair 测试8/8 PASS；本轮仅修改共享展示映射与交接记录，未改模型、策略、赛事范围、账本、结算或通知规则。

## 2026-10-15 正式范围继续补齐（第七十四批）
- 两项经中文足球资料与 TotalCorner ID/赛事上下文交叉核实的新增：`team_id 97868 Al Jandal → 阿尔詹达尔`（Tips.GG 沙特比赛档案直接使用该译名，https://tips.gg/cn/archive/al-adalah-football-vs-al-jndal-football/）；`team_id 89494 Iraklis 1908 FC → 伊拿克里斯`（360百科球队资料明确列名“伊拿克里斯足球会”及英文身份，https://baike.so.com/doc/1708334-1806137.html）。保留原始 provider_name、Team ID 和别名，不合并其他同名球队。
- 共享库提交 `bff3f3502771bfbe6bb7c94da6f2489d1c495bd6` 已推送 master。正式范围2,468队：2,275 canonical、193 unresolved（92.18%）；M1 1,512/1,553（97.36%），M1 OU-R1 52/52，MR1 AH 1,761/1,921（91.67%），MR1 AI declared mirror 1,512/1,553（97.36%）；全库12,276 IDs、4,291 canonical。完整 unresolved 及原因见共享 `formal_scope_coverage.json#unresolved_records`。
- curator 本轮新增2条、再次执行幂等；M1 formatter/name-repair 测试8/8 PASS，`git diff --check` PASS。名称数据和来源已入唯一共享库；本批尚未以该新 registry 运行历史 TG 编辑工作流，也没有可作为新消息的生产实测样本。未修改策略、模型、市场、账本、结算或 TG 派单逻辑。

## 2026-10-15 正式范围继续补齐（第七十五批）
- Sofascore 简体中文 KF Drenica 球队页将该队显示为“德雷尼察地区斯尔比察”，并列出 Skënderaj 城市信息（https://www.sofascore.com/zh/football/team/kf-drenica/229754）。与 TotalCorner `team_id 40318`、provider `KF Drenica Skenderaj` 交叉核对后，新增该 canonical；只写入此稳定 ID，不套用于其他 Drenica 名称。
- 共享库提交 `6c5ad6956c7bf7476b911e472ddf464a5fb69ccc` 已推送 master。本批新增1条；正式范围2,468队：2,276 canonical、192 unresolved（92.22%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52，MR1 AH 1,762/1,921（91.72%），MR1 AI declared mirror 1,513/1,553（97.42%）；全库12,276 IDs、4,292 canonical。未匹配队伍及原因以共享 `formal_scope_coverage.json#unresolved_records` 为准。
- curator 本轮新增1条；M1 formatter/name-repair 测试8/8 PASS，`git diff --check` PASS。只更新共享展示映射与审计/交接信息，未修改策略、模型、赛事范围、账本、结算或 Telegram 派单逻辑；本轮没有发送或编辑 Telegram 消息。

## 2026-10-15 正式范围继续补齐（第七十六批）
- 球探网球队资料将匈牙利足球俱乐部 BVSC Zuglo 明确显示为“布达佩斯瓦苏塔斯”（https://football.chuqi.com/football/team-match/230816/）。与 TotalCorner `team_id 70974`、provider `BVSC Zuglo` 及匈牙利联赛 league_id 241 核对后新增 canonical，并保留 Budapesti VSC、BVSC-Zugló 等别名。
- 共享库提交 `65a62803b39687d6e13992fbf4153e26b22c8597` 已推送 master。本批新增1条；正式范围2,468队：2,277 canonical、191 unresolved（92.26%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52，MR1 AH 1,763/1,921（91.78%），MR1 AI declared mirror 1,513/1,553（97.42%）；全库12,276 IDs、4,293 canonical。逐项 unresolved 以共享 `formal_scope_coverage.json#unresolved_records` 为准。
- curator 新增1条；M1 formatter/name-repair 测试8/8 PASS，`git diff --check` PASS。仅更新共享展示映射与交接记录，未修改生产策略、模型、赛事范围、账本、结算、Telegram 派单规则，未发送或编辑 TG 消息。

## 2026-10-15 正式范围继续补齐（第七十七批）
- 雷速简体中文 FK Garliava 球队资料明确显示“加尔利阿瓦”，同时列出英文 identity FK Garliava（https://www.leisu.com/data/zuqiu/team-40518/transfer）。与 TotalCorner `team_id 84086` 和立陶宛 league_id 542 对照后新增 canonical；保持 team ID 不变，不对相似拼写做泛化。
- 共享库提交 `dce28cac0c1749a09fae0c20f68641411adf7b71` 已推送 master。本批新增1条；正式范围2,468队：2,278 canonical、190 unresolved（92.30%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52，MR1 AH 1,764/1,921（91.83%），MR1 AI declared mirror 1,513/1,553（97.42%）；全库12,276 IDs、4,294 canonical。完整 unresolved 以共享 `formal_scope_coverage.json#unresolved_records` 为准。
- curator 新增1条；M1 formatter/name-repair 测试8/8 PASS，`git diff --check` PASS。只改共享展示映射及交接记录，没有发送/编辑 TG，也没有修改模型、策略、赛事范围、账本或结算。

## 2026-10-15 正式范围继续补齐（第七十八批）
- 为 TotalCorner `team_id 89762`、provider `Kema Aswan` 新增 canonical“克玛阿斯罔”。雷速简体中文球队页将 Kima Aswan 显示为“克玛阿斯罔”（https://www.leisu.com/data/zuqiu/team-30909），FootballAnt 中文比赛页也使用该译名（https://www.footballant.com/zh-CN/matches/2548461/live）；埃及乙级联赛历史对阵资料在不同赛季对同一阿斯旺俱乐部使用 Kema/Kima 两种拼写。独立保留 89762 和既有 77134，不合并或改写任一 ID。
- 共享库提交 `8638a5f14ef6b7f0c91001dfe330608740d58cd3` 已推送 `totalcorner-research-bridge` master。本批新增1个正式范围映射；最新权威统计：正式范围2,468 IDs，2,279 canonical、189 unresolved（92.34%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52（100%），MR1 AH 1,765/1,921（91.88%），MR1 AI 声明范围镜像 M1 为1,513/1,553（97.42%）；全共享库12,276 IDs、4,295 canonical。逐项 unresolved 清单及原因以共享库 `formal_scope_coverage.json#unresolved_records` 为准。
- M1 formatter/name-repair 测试8/8 PASS，curator 运行后再运行新增数为0（幂等），`git diff --check` PASS。仅更新共享展示映射、curation 证据及统计；未改模型、策略、赛事范围、账本、结算或 Telegram 规则。本批没有触发或编辑任何 Telegram 历史消息。

## 2026-10-15 正式范围继续补齐（第七十九批）
- 博体中文球队资料将 Odishi 1919 显示为“奥迪希1919”（https://data.boti.net/league/index-1.aspx?path=%2Fteam%2Fsummary.aspx%3Fteamid%3D22312&type=a）；格鲁吉亚足协 Erovnuli Liga 官网列出全名 Odishi 1919 Zugdidi（https://www.erovnuliliga.ge/en/club/odishi-1919）。为 TotalCorner `team_id 31172` 添加该 canonical，保留 provider 全名、别名及 team ID，不合并其他 Odishi/Zugdidi 身份。
- 共享库提交 `9ae4a62230b829f4165ee7aef2d53844506bea0d` 已推送 master。本批新增1项；正式范围2,468 IDs：2,280 canonical、188 unresolved（92.38%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52，MR1 AH 1,766/1,921（91.93%），MR1 AI 声明范围镜像 M1 为1,513/1,553（97.42%）；全库12,276 IDs、4,296 canonical。权威逐项清单见共享库 `formal_scope_coverage.json#unresolved_records`。
- M1 formatter/name-repair 测试8/8 PASS，curator `git diff --check` PASS。本轮仅更新共享展示映射和审计统计，无生产链/策略/账本/结算/Telegram 修改；未发送或编辑 Telegram 消息。

## 2026-10-15 正式范围继续补齐（第八十批）
- Tips.GG 中文历史赛程页将威尔士 Newport City 明确显示为“新港城”（https://tips.gg/cn/archive/carmarthen-football-vs-newport-city-football/），并列出 Newport City 身份；其 Cymru South/Welsh football 语境与 TotalCorner `team_id 147659` 的联赛范围吻合。新增该 ID 的 canonical“新港城”，保留原 provider identity；不与 Newport County 混同。
- 共享库提交 `b1d762dee1cbb76b61ca70c45017e8d15b05d5c2` 已推送 master；Runner 交接提交 `dd7d3a9`（本次交接追加）已推送 main。本批新增1条；正式范围2,468队：2,281 canonical、187 unresolved（92.42%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52，MR1 AH 1,767/1,921（91.98%），MR1 AI declared mirror 1,513/1,553（97.42%）；全库12,276 IDs、4,297 canonical。权威 unresolved 明细见共享库 `formal_scope_coverage.json#unresolved_records`。
- M1 formatter/name-repair 测试8/8 PASS，`git diff --check` PASS。仅更新共享展示映射、curation evidence 与统计，没有修改模型、策略、赛事范围、账本、结算或 Telegram 规则；未发送/编辑 Telegram 历史消息。

## 2026-10-15 Telegram 显示接入与历史修复核查
- 当前 M1 formatter 直接读取唯一共享库 `data/football_display_names/display_names.json`；MR1 AH、MR1 AI 的正式通知/AI formatter 通过 `src/football-display-names.js` 读取 `external/football-display-registry/data/football_display_names/`，按 team_id 优先解析，确认四条显示读取路径接入同一共享库。M1 显示回归测试8/8 PASS；本轮没有修改消息格式或发送规则。
- M1 历史消息修复器只读 dry-run：41条具备已发送原文及映射，可编辑；99条缺少原消息文本，97条当前无可替换的已确认映射。由于本机未配置 M1/MR1 Telegram 凭据，且 GitHub Secrets 不可读回，本轮没有调用 editMessageText；实际历史编辑成功0、失败0（未执行）。不得把候选可编辑数说成已修复数。

## 2026-10-15 正式范围继续补齐（第八十六批）
- 将 TotalCorner `team_id 31006` `Sohag` 与同为埃及乙级联赛 `league_id 417` 的共享库 `team_id 12078` `Suhag` 做精确别名复用：现有 canonical“索哈杰”来源为中文维基球队条目，别名中明确包含 `Sohag`。该 exact alias 在共享 registry 中唯一，保留两个 provider team_id，不合并身份。
- 共享 master commit `50271ade` 已推送；叠加第八十五批，正式范围2,468 IDs：2,288 canonical、180 unresolved（92.71%）；M1 1,515/1,553（97.55%），M1 OU-R1 52/52（100%），MR1 AH 1,774/1,921（92.35%），MR1 AI 声明镜像 M1 为1,515/1,553（97.55%）。全共享库12,276 IDs、4,304 canonical。未匹配清单以共享 `formal_scope_coverage.json#unresolved_records` 为准。
- M1 formatter/name-repair tests 8/8 PASS，`git diff --check` PASS。只有展示别名复用与证据/覆盖报告变化；未修改模型、策略、赛事范围、盘口、账本、结算或 Telegram 派单逻辑，也未发送/编辑历史消息。

## 2026-10-15 正式范围赛事名与历史 Telegram 复核（第八十七批）
- 在唯一共享库补齐 `league_id 242` Latvia 1. Liga →“拉脱维亚甲级联赛”（7M、17500 中文赛事页）和 `league_id 10635` Faroe Islands Div 1 →“法罗群岛足球甲级联赛”（Wikidata 简体中文标签及中文赛事资料）。验证 M1 formatter 隔离输出中的赛事、双方球队和 AH 方向均为中文。共享库提交 `ff3c2c62` 已推送 master。当前球队正式范围仍为2,288/2,468（92.71%），180 unresolved；M1 1,515/1,553（97.55%），M1 OU-R1 52/52，MR1 AH 1,774/1,921（92.35%），MR1 AI 声明范围镜像 M1 为1,515/1,553（97.55%）。全共享库12,276 team IDs、4,304 canonical team names；771 league IDs 中336 canonical、435 unresolved。
- 新共享 registry 后运行历史修复：M1 TG workflow `38611061935` SUCCESS，41 eligible、0 edited、41 already matching、99 缺失原文、97 未映射、0 failed；MR1 Formal `38611070222` SUCCESS，0 eligible、0 edited、125 skipped/already processed、0 unresolved；MR1 AI `38611077975` SUCCESS，201 总项、9 候选、0 edited、192 unresolved、9 failed，失败均为 Telegram `400 message to edit not found`。没有重发任何消息。M1 formatter/name-repair tests 8/8 PASS，`git diff --check` PASS。
- 本轮只改共享展示名、赛事名、相关统计/证据和本交接；不改模型、策略、赛事范围、盘口、正式账本、结算或通知规则。Telegram 历史实际编辑数为0，MR1 AI 旧消息失败原因明确；后续新消息由已接入共享库的通知 formatter 读取 canonical 映射。

## 2026-10-15 四链中文 formatter 隔离验收
- 使用共享 master 最新 registry 对 M1 formatter 和 MR1 `displayFootballFixture`、MR1 AH formatter、MR1 AI `formatAiAhTelegram` 做隔离渲染；示例为 HB Torshavn II vs HB Torshavn 与 Rigas FS II vs Sohag，赛事名、双方队名、方向均输出中文，盘口/水位值原样保留。未调用发送函数、未生成/修改正式订单。
- MR1 测试代码按 `FOOTBALL_DISPLAY_REGISTRY_DIR` 读取同一 `display_names.json`；M1 测试 8/8 PASS。正式共享 master 最新为 `ff3c2c62`；quant-runner handoff 最新为 `4255480`。无新增策略/模型规则；历史 TG workflow 实际编辑为0，MR1 AI 的旧 message ID 不可编辑原因见第87批。

## 2026-10-15 正式范围剩余名称来源复核
- 从最新共享 master `ff3c2c6253ee432a77eebf6765f51a94454d73e1` 重算：正式范围 2,468 个 ID，2,288 有 canonical 中文、180 unresolved（92.71%）；M1 1,515/1,553（97.55%）、M1 OU-R1 52/52、MR1 AH 1,774/1,921（92.35%）、MR1 AI 声明镜像 M1 1,515/1,553。逐项未匹配清单及 reason 留在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 对 180 条执行精确 canonical alias 复用检查，无额外唯一 alias 命中。评估公开 lottery-football `team_name_mappings.csv` 后确认其记录是英文 standard/alias，且该仓库未声明 license；未复制或引用为中文来源。针对埃及、科索沃、阿尔巴尼亚、乌克兰及匈牙利小联赛候选检索到的多数仅为外文身份材料；个别近似同名条目存在国家/联赛冲突（例如 Kosovo `Vllaznia` 与 Albania `Vllaznia Shkodër`），故未强行映射。当前没有可负责任新增的 canonical 中文名；180 条继续标注 `NO_VERIFIED_CANONICAL_ZH`，不是技术解析遗漏。
- 本地验证 M1 formatter/name-repair tests 8/8 PASS；MR1 shared-registry smoke tests 2/2 PASS（`FOOTBALL_DISPLAY_REGISTRY_DIR` 指向同一共享 master），均未发送/编辑 Telegram。无策略、模型、scope、盘口、账本或结算变更。本轮只记录来源审查结论，不改共享 registry。

## 2026-10-15 正式范围继续补齐（第八十一批）
- NowScore 中文球队页将 TotalCorner provider `Nabrouh` 对应为“纳布洛”，并展示该队埃及第二级联赛比赛（https://info.nowscore.com/big/team/Summary/37053.html）；独立 Nabrouh/Nabarouh 身份资料及 TotalCorner 赛程交叉确认联赛身份。仅为 `team_id 45228` 新增 canonical，保留 provider identity 与现有别名，不与其他埃及球队合并。
- 共享库提交 `416fe3b9cb7eb7af959787d9748c681270a5d152` 已推送 master。本批新增1条；正式范围2,468队：2,282 canonical、186 unresolved（92.46%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52（100%），MR1 AH 1,768/1,921（92.04%），MR1 AI 声明范围镜像 M1 为1,513/1,553（97.42%）；全共享库12,276 IDs、4,298 canonical。未匹配明细及未能核实原因以该共享提交内 `formal_scope_coverage.json#unresolved_records` 为准。
- curator 本轮新增1条；M1 formatter/name-repair 测试8/8 PASS，`git diff --check` PASS。共享 registry 新名称可供四条已接入的显示读取链使用；本轮未触发生产扫描、未发送或编辑 Telegram 消息。历史编辑仍需本机已授权的正式 Telegram 执行环境，GitHub Secrets 不可读回；模型、策略、赛事范围、正式账本、结算与通知规则均未改。

## 2026-10-15 正式范围继续补齐（第八十二批）
- 7M 简体中文球队档案将 Arsenal Ceska Lipa 明确显示为“阿森纳利帕”（https://team.7m.com.cn/10803/index_gb.shtml）；俱乐部官网确认 FK Arsenal Česká Lípa 的身份。仅为 TotalCorner `team_id 40743` 新增 canonical，保留 provider spelling/身份，不与其他 Arsenal 球队合并。
- 共享库提交 `f9f4750ed1d2833132c3ffb6218d285ee9b52205` 已推送 master。本批在第八十一批基础上新增1条；正式范围2,468队：2,283 canonical、185 unresolved（92.50%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52（100%），MR1 AH 1,769/1,921（92.09%），MR1 AI 声明范围镜像 M1 为1,513/1,553（97.42%）；全共享库12,276 IDs、4,299 canonical。未匹配及未确认原因见共享 `formal_scope_coverage.json#unresolved_records`。
- curator 新增1条且定向复跑 8 个 M1 display/name-repair tests 全 PASS，`git diff --check` PASS。只改展示 registry/审计资料；无生产扫描、无 Telegram 发送或历史编辑，策略与账本不变。

## 2026-10-15 正式范围继续补齐（第八十三批）
- 7M 中文球队页将 Velez Nevesinje 显示为繁体“維勒茲內韋西涅”，并列出波黑联赛比赛（https://team.7m.com.cn/633746/index.shtml）；波黑足协资料确认 FK Velež 的 Nevesinje 身份。新增 TotalCorner `team_id 73240`，规范为简体“维勒兹内韦西涅”；与 Mostar 的 Velež 区分，不合并身份。
- 共享库提交 `d898bea0c98945a31631fb2d0d92f4c72b2344d2` 已推送 master。本批新增1项；正式范围2,468队：2,284 canonical、184 unresolved（92.54%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52（100%），MR1 AH 1,770/1,921（92.14%），MR1 AI 声明范围镜像 M1 为1,513/1,553（97.42%）；全共享库12,276 IDs、4,300 canonical。逐项 unresolved 与原因见共享 `formal_scope_coverage.json#unresolved_records`。
- curator 新增1条，M1 formatter/name-repair tests 8/8 PASS，`git diff --check` PASS。未触发生产扫描、未发送或编辑 Telegram；仅更新共享显示名称和审计/交接数据。

## 2026-10-15 正式范围继续补齐（第八十四批）
- 雷速简体中文球队资料直接将 `Raya Ghazl SC` 对应显示为“拉亚加兹尔”，并保留英文名/埃及赛事背景（https://www.leisu.com/data/zuqiu/team-78883/data）。与 TotalCorner unresolved `team_id 120757`、provider `Raya Ghazl SC`、Egypt Division 2 league_id 417 精确核对后新增 canonical；不映射到其他 Raya 身份。
- 共享库提交 `e39c9cecab12ceadad8eada2fd20183d10d73867` 已推送 master。本批新增1项；正式范围2,468队：2,285 canonical、183 unresolved（92.59%）；M1 1,513/1,553（97.42%），M1 OU-R1 52/52（100%），MR1 AH 1,771/1,921（92.19%），MR1 AI 声明范围镜像 M1 为1,513/1,553（97.42%）；全共享库12,276 IDs、4,301 canonical。完整 unresolved 与原因见共享 `formal_scope_coverage.json#unresolved_records`。
- curator 新增1条，M1 display/name-repair tests 8/8 PASS、`git diff --check` PASS。仅修改共享 display registry 和审计/交接，不触发正式扫描、不发送/编辑 Telegram、不改模型或策略。

## 2026-10-15 正式范围继续补齐（第八十五批）
- 对 TotalCorner `team_id 42239` `HB Torshavn II` 与 `team_id 102419` `Rigas FS II` 使用已有共享库中的母队中文名，并分别以公开母队中文资料及独立二队资料核验明确的 `II` 身份；新增展示名“托尔斯港二队”“里加足球学校二队”。两个 ID 保持独立，没有将二队并入一线队。来源分别为 7M HB Torshavn 中文队页 + National Football Teams HB II 资料，以及 Sofascore 简中 RFS 队页 + Sofascore FK RFS II 队页。
- 共享 master 本批增加2个 canonical。最新正式范围 2,468 IDs：2,287 canonical、181 unresolved（92.67%）；M1 1,514/1,553（97.49%），M1 OU-R1 52/52（100%），MR1 AH 1,773/1,921（92.30%），MR1 AI 声明镜像 M1 1,514/1,553（97.49%）。当前共享库 12,276 IDs、4,303 canonical。逐项未匹配名单仍以共享 `formal_scope_coverage.json#unresolved_records` 为准。
- 新 curator 幂等校验：首次增加2条，重复运行因目标 ID 已非 unresolved 而安全拒绝；M1 formatter/name-repair tests 8/8 PASS，`git diff --check` PASS。仅改共享名称库与审计/交接；未改模型、策略、赛事范围、账本、结算、TG 格式/发送逻辑。没有触发生产 TG 编辑或重发。

## 2026-10-15 正式范围 Wikidata 精确中文实体复核（第八十八批）
- 以 latest shared master `ff3c2c6253ee432a77eebf6765f51a94454d73e1` 的 180 条 `unresolved_records` 为输入，对 Wikidata 英文实体匹配与中文标签逐队核验。确认新增：`34379 KF Trepca Mitrovice → 特雷普察足球俱乐部` (Q1638392)、`43485 KF Besa Peje → 比沙佩积足球会` (Q1418838)、`45023 KS Luftetari Gjirokaster → 吉诺卡斯特足球俱乐部` (Q120064)、`48461 KF KEK-U → KEK足球会` (Q1519407)、`49705 KF Flamurtari Pristina → 法拿莫达利足球会` (Q1391848)。4 个 Wikidata `zh` 标签转为简体字形，1 个实体有简体标签；source QID、原英文名、ID、league IDs、provider aliases 均保存。curator 为 `ops/curate_formal_scope_wikidata_labels_20261015.py`，幂等重跑仅更正简繁来源说明，不重复计数。
- 过滤未收录有歧义项：`119602 KF Vllaznia` 对应搜索同时命中阿尔巴尼亚女队及科索沃男队；`42741 Flamurtari` 的候选身份为阿尔巴尼亚 Vlorë，与 stored Kosovo league context 冲突。两项继续 unresolved，不按队名猜。已提交共享 master `4f37343398f17bc38c65cc75fec39e4e83f5bb8c`。
- 现正式 union 2,468 IDs：2,293 canonical、175 unresolved（92.91%）；M1 1,519/1,553（97.81%），M1 OU-R1 52/52（100%），MR1 AH 1,778/1,921（92.56%），MR1 AI 声明镜像 M1 为1,519/1,553（97.81%）。本机 M1 display/name-repair 8/8、MR1 shared-registry smoke 2/2 PASS。隔离 formatter 对5个新 team ID 均渲染出中文方向。新 registry 下 M1 历史编辑 dry-run 为41 eligible、99 缺原文、97 尚未映射；不重发。上次生产 edit workflow 的 M1 41 条已是 ALREADY_MATCHING，MR1 Formal 0 eligible，MR1 AI 9 条仍因 Telegram `message to edit not found` 不可改；本轮未触发编辑或重发。未改任何模型/策略/正式账本/结算。

## 2026-10-15 正式范围赛事名补齐与四链历史 TG 复核（第八十九批）
- 补充 `league_id 877 Albania First Division → 阿尔巴尼亚甲组足球联赛`；中文赛事对照表明确将 `Kategoria e Parë` 对应该名称并标注为阿尔巴尼亚国内第二级联赛，显示名用简体规范字形。来源：https://zh.100ke.info/wiki/%E8%B6%B3%E7%90%83%E6%AF%94%E8%B5%9B 。比赛/联赛 ID 和模型输入不变；同时修正 curator 的幂等报告逻辑，避免无新增团队时清空上一批证据摘要。
- 共享 registry 已推 master：`7bf9ab6bb3757ff3509ec7ab36ea8de1e1d03e8e`。本批新增球队 canonical 0、赛事 canonical 1。正式范围仍为 2,468 队、2,293 有中文、175 未匹配（92.91%）；M1 1,519/1,553（97.81%），M1 OU-R1 52/52（100%），MR1 AH 1,778/1,921（92.56%），MR1 AI 声明镜像 M1 为1,519/1,553（97.81%）；MR1 AI observed confidence≥50 为181/182（99.45%）。完整未匹配 ID/英文名/联赛/系统及原因见共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`，175条目前均为 `NO_VERIFIED_CANONICAL_ZH`。全共享库12,276 team IDs、4,309 canonical；771 league IDs 中337 canonical、434 unresolved。
- 新联赛由 MR1 `displayFootballFixture` 隔离渲染为“阿尔巴尼亚甲组足球联赛”；对 team_id 45023 vs 43752 渲染为“吉诺卡斯特足球俱乐部 vs 科拉比佩什科皮”。M1 display/name-repair tests 8/8 PASS，MR1 `test-football-display-names.js` 1/1 PASS。M1、MR1 AH、MR1 AI 的现有 formatter 均读取共享 `display_names.json`；M1 OU-R1 使用 M1 同一 formatter，覆盖52/52。
- 基于最新共享 master 执行已有 name-only 历史修复 workflows（仅编辑原 message_id，不发送新消息）：M1 run `38614803918` PASS，eligible 41、edited 0、already_matching 41、缺保存原文本 99、未映射 97、failed 0；MR1 Formal run `38614811894` PASS，eligible 0、edited 0、already processed 125、unresolved 0、failed 0；MR1 AI run `38614819297` PASS，total 201、候选9、edited 0、unresolved 192、failed 9，9条均返回 Telegram 400 `message to edit not found`。故本批历史 Telegram 实际编辑数仍为0；没有重发或新发消息。M1 OU-R1 没有独立正式 TG ledger/历史编辑器，不能单独核验其旧消息文字。
- 生产策略、模型、赛事范围、正式订单、账本、结算、派单条件均未修改。云端 workflow 运行成功仅表示历史编辑器完成执行，不代表已有文字被编辑；下一步仍是逐项核验175条未匹配名称及原始消息可编辑性。

## 2026-10-15 正式范围继续补齐（第九十批）
- 7M 中文球队页明确将 Gangjin Swans Women's 对应为繁体“康津天鵝女足”，页面列有韩国 WK League 赛程（https://team.7m.com.cn/452151/index.shtml）。TotalCorner `team_id 181365` 的 provider name 明确为 `Gangjin Swans (W)`、`league_id 483`；新增简体 canonical“康津天鹅女足”，保留女子身份、ID 和英文别名，不与男子队/其他 Gangjin 身份合并。
- 共享库提交 `2fd9aa8de58ee1ec43446be97303ec143d2988fa` 已推送 `totalcorner-research-bridge/master`。正式 union 2,468 IDs：2,294 canonical、174 unresolved（92.95%）；M1 当前重算 1,517/1,553（97.68%），M1 OU-R1 52/52（100%），MR1 AH 1,779/1,921（92.61%），MR1 AI declared mirror 1,517/1,553（97.68%），observed confidence≥50 cohort 181/182（99.45%）。全库 12,276 team IDs、4,310 canonical；771 league IDs 中337 canonical、434 unresolved。与上轮快照相比 M1 scope 的已匹配数有2条重算差异；以上数字取本次当前 scope 输入重建的 `formal_scope_coverage.json`，不是把差异归功于本批映射。174条 unresolved 的完整 ID/英文名/联赛/系统/原因在同一文件 `unresolved_records`。
- M1 formatter/name-repair tests 8/8 PASS；MR1 共享 registry test 1/1 PASS；`git diff --check` PASS。隔离渲染确认该 canonical 可供共享 registry consumer 使用。本批没有找到该 team ID 对应的已发送正式 TG 消息，因此不需历史编辑；未发送测试/历史 Telegram。历史 TG 总体编辑状态仍沿用第八十九批运行证据（编辑成功0，MR1 AI 9条因原 Telegram message 不可定位失败）；本批未重跑历史编辑 workflow。
- 本批只改共享中文展示库、coverage/audit 与 curator 幂等行为；M1、M1 OU-R1、MR1 AH、MR1 AI 的模型、策略、范围、正式账本、结算和通知规则均未修改。GitHub Actions/生产 TG 本轮未触发。

## 2026-10-15 正式范围继续补齐（第九十一批）
- Tips.GG 简体中文匈牙利球队排名将 Balmazujvarosi 对应为“巴尔马祖伊瓦罗什”；其匈牙利杯球队记录出现精确 provider spelling `Balmazujvarosi FC`。为 `team_id 3477` 增加同名 canonical；`team_id 1536` 的 provider spelling `Balmazujvaros FC` 依据现有拼写 alias crosswalk 与同一 Hungary NB I league context 复用该 canonical。两个 TotalCorner ID 均独立保留，不合并 ID，也未推断预备队/一线队关系。另为 `league_id 40` 补充 `Hungary NB I → 匈牙利足球甲级联赛`，依据中文足球联赛条目确认其最高级别身份。
- 共享库 `ba409921` 已推送 `totalcorner-research-bridge/master`。当前 formal union 2,468 IDs：2,296 有 canonical、172 unresolved（93.03%）；M1 1,519/1,553（97.81%），M1 OU-R1 52/52（100%），MR1 AH 1,779/1,921（92.61%），MR1 AI declared mirror 1,519/1,553（97.81%），AI observed confidence≥50 cohort 181/182（99.45%）。全库12,276 team IDs、4,312 canonical；771 league IDs 中338 canonical、433 unresolved。完整 unresolved ID/英文名/联赛/系统/原因仍在共享 `formal_scope_coverage.json#unresolved_records`。
- M1 8/8 formatter/name-repair tests PASS；MR1 shared display formatter tests 3/3 PASS；M1 两个新 ID 的单行 TG 隔离渲染及 MR1 按 ID 隔离渲染均显示中文队名/方向/赛事。历史 ledger 中没有发现这两个新增 team ID 对应的已发送 M1 Pick。M1 历史 name-repair workflow `38617778290` PASS：41 eligible、0 edited、41 `ALREADY_MATCHING`、99 缺原文、97 未映射、0 failed；MR1 Formal `38617784570` PASS：0 eligible、0 edits、125 already processed、0 unresolved/failed；MR1 AI `38617791466` PASS：201 total、9 eligible、0 edited、192 unresolved、9 failed，均为 Telegram `400 message to edit not found`。这些既有 workflows 只尝试编辑原 message_id，不发送新消息。M1 dry-run同样为41 eligible、99缺原文、97未映射。
- 本轮只改唯一共享展示库、来源记录/覆盖报告和 curator；四条模型链及策略、scope、订单、settlement 均未修改。没有新的信号、订单或 Telegram 发送；历史 TG 实际编辑数0（可编辑消息原文已经与 formatter 一致，缺失原文/映射及 MR1 AI 不存在 message 均按报告保留）。运行链接：M1 https://github.com/ljm198964-alt/quant-runner/actions/runs/38617778290；MR1 Formal https://github.com/ljm198964-alt/quant-runner/actions/runs/38617784570；MR1 AI https://github.com/ljm198964-alt/quant-runner/actions/runs/38617791466。

## 2026-10-15 正式范围继续补齐（第九十二批）
- Tips.GG 简体中文 Slavia TU Kosice 球队档案以“斯拉維亞科希策”标注球队并确认斯洛伐克身份（https://tips.gg/cn/team/slavia-tu-kosice-football/）。新增 TotalCorner `team_id 41729 → 斯拉维亚科希策`，按简体字形规范展示，保留 provider 名、带变音符别名及 league IDs 133/355，不与其他 Slavia/Kosice 球队合并。
- 共享库 `38381601` 已推送 master。本批新增1队；formal union 2,468 IDs：2,297 canonical、171 unresolved（93.07%）。M1 1,519/1,553（97.81%），M1 OU-R1 52/52（100%），MR1 AH 1,780/1,921（92.66%），MR1 AI declared mirror 1,519/1,553（97.81%），AI observed confidence≥50 181/182（99.45%）。全库12,276 team IDs、4,313 canonical；771 league IDs 中338 canonical、433 unresolved。全部 unresolved ID/名称/联赛/系统/原因见同提交的 `formal_scope_coverage.json#unresolved_records`。
- M1 display/name-repair tests 8/8 PASS；MR1 shared display formatter tests 3/3 PASS。MR1 用实时加载的共享 registry 对 `team_id 41729` 与已有中文队名做 fixture 隔离渲染，结果为“斯拉维亚科希策 vs 巴尔马祖伊瓦罗什”；无生产单或 Telegram 发送/编辑。未改模型、策略、赛事范围、正式账本或结算。

## 2026-10-15 正式范围未匹配名称来源复核（第九十三批审查）
- 快进核对 `totalcorner-research-bridge/master` 为 `3838160121ad85f66db0ed00bb3d216d21461203`，工作树干净；`formal_scope_coverage.json` 当前仍列正式范围 2,468 IDs、2,297 canonical、171 unresolved（93.07%）：M1 1,519/1,553、OU-R1 52/52、MR1 AH 1,780/1,921、MR1 AI 声明镜像 M1 1,519/1,553。此轮未更改 registry，因此正式数值保持原样。
- 按 unresolved ID/原名/赛事上下文抽查了现成 FootyStats 中文资料、Tips.GG 中文球队页、7M/500 搜索及可找到的公开球队身份页。确认这些页面多数只能证明英文身份，不能提供可靠中文惯用队名；Tips.GG 对 Malta `Sirens` 的自动中文结果为“警报”，属于明显不适用译法，明确排除。其余样例包括 Pembroke Athleta FC、Mladost Carev Dvor、FK FAP、KF Hajvalia、埃及低级别队；未找到足以支持写入 canonical_zh 的主流中文名称证据。未根据发音临时造译名，也未合并疑似近名身份。
- 已检查本地旧身份档案、球队 alias crosswalk 和中文映射 wheel；未发现这些剩余记录的可复用可靠中文映射。由于没有合格的新映射，本轮没有提交空变更，也没有触发模型 runtime、Telegram 编辑/发送或 GitHub Actions。
- 后续继续从 171 条 unresolved 中按有明确中文来源者逐项写入唯一 `display_names.json`；单纯可恢复英文身份不算中文覆盖。不得把该抽查范围误报为 171 条全部逐项完成，也不得将当前 93.07% 报成全覆盖。
- 本轮继续做了源数据精确命中检查：从已审阅的 QiuXiaoCe `football-team-names-zh` 本地包与 171 个 provider name 逐字/归一匹配，命中 0；`footballant`、FootyStats、Sofascore、7M/500 搜索对若干埃及/科索沃/塞尔维亚队仍只返回英文身份。`Bani Ebaid` 可核对为 Beni Ebeid SC（不是中文名）；`FK FAP` 的官方缩写/身份明确，但没有可靠中文惯用名；均不写成推测译名。相关公开身份页面：<https://en.wikipedia.org/wiki/Beni_Ebeid_SC>、<https://fkfap1955.com/>。
- 当前 unresolved 按其正式联赛上下文集中于：Egypt Division 2 31 条、Kosovo Division 1 21 条、Kosovo Division 2 16 条、Ukraine Persha Liga 10 条、North Macedonia First League 8 条；未匹配记录跨系统去重总数仍是 171（联赛多归属计数不能相加替代总数）。后续应优先从这些本地联赛的中文完整赛程/赔率页逐轮做英文—队名配对，再处理散布的小联赛队伍。

## 2026-10-15 正式范围继续补齐（第九十四批）
- 为 TotalCorner `team_id 57747` (`KF Gostivari`) 新增“高斯迪华”，依据中文维基北马其顿甲级联赛历史球队表中“高斯迪華 | KF Gostivari”精确对应，并以英文俱乐部资料区分旧 `FK Gostivar` 身份；`team_id 87857` (`KF Besa Doberdoll`) 新增“贝萨多贝尔多尔足球俱乐部”，依据 Tips.GG 简体中文马其顿杯球队列表；`team_id 88073` (`FC Voska Sport`) 新增“沃斯卡体育”，依据雷速中文球队页，Tips.GG 中文列表交叉核验。三项均保留各自 provider 名、team_id、league_id 45，不合并相似球队。
- 共享库提交 `2d0aad1fc3c2bd0c1171800e3cb280cbf0ce30c9` 已推送 `totalcorner-research-bridge/master`。最新 formal union 2,468 IDs：2,300 canonical、168 unresolved（93.19%）；M1 1,522/1,553（98.00%），M1 OU R1 52/52（100%），MR1 AH 1,783/1,921（92.82%），MR1 AI 声明镜像 M1 1,522/1,553（98.00%）；observed AI confidence≥50 cohort 181/182（99.45%）。全共享库 12,276 team IDs、4,316 canonical；全部 unresolved ID、英文名、联赛、系统及原因见共享库 `formal_scope_coverage.json#unresolved_records`。
- M1 formatter/name-repair tests 8/8 PASS；MR1 shared registry/AI formatter tests 4/4 PASS；三条新 ID 的隔离 fixture 渲染赛事、主客队均为中文；`git diff --check` PASS。没有运行策略或正式单，也没有本轮发送/编辑 Telegram 历史消息；历史消息编辑结果仍应以先前 handoff 中 workflow 回执为准。
- 随后对最新共享库执行既有历史 name-only repair：M1 workflow `38620266687` 成功，41 eligible、0 edited、41 already matching、0 failed；MR1 Formal `38620267182` 成功，0 eligible、125 already processed、0 unresolved/failed；MR1 AI `38620306951` 成功，201 total、9 eligible、0 edited、192 unresolved、9 failed，9项均为 Telegram `400 message to edit not found`。没有重发消息；workflow 成功不等于有历史消息实际被改写。
- 本批只改共享显示名称、curation 来源和覆盖统计；没有修改 M1/M1 OU R1/MR1 AH/MR1 AI 模型、策略、赛事范围、账本、结算或 Telegram 规则。

## 2026-10-15 正式范围继续补齐（第九十五批）
- 为 TotalCorner `team_id 43108`、provider `Osogovo Kocani` 新增 canonical“奥索戈沃”。FootyStats 简体中文北马其顿对阵页明确将 FK Osogovo Kočani 称为“奥索戈沃”（https://footystats.org/cn/fyr-macedonia/fk-rabotnicki-skopje-vs-fk-osogovo-kocani-h2h-stats），Tips.GG 中文比赛页独立使用“奥索戈沃队”；保留 TotalCorner team_id 43108、league_id 45，不向其他 Osogovo 球队扩散映射。
- 共享库提交 `7ac0619521f32e67049ebdba9ecfc4de7c3c7485` 已推送 master。已重算 formal union 2,468 IDs：2,301 canonical、167 unresolved（93.23%）；M1 1,523/1,553（98.07%），M1 OU R1 52/52（100%），MR1 AH 1,784/1,921（92.87%），MR1 AI 声明镜像 M1 为1,523/1,553（98.07%），AI observed confidence≥50 cohort 181/182（99.45%）。全共享库12,276 team IDs、4,317 canonical；完整 unresolved ID/名称/联赛/系统/原因在 `formal_scope_coverage.json#unresolved_records`。
- M1 formatter/name-repair tests 8/8 PASS；MR1 shared-registry/AI formatter tests 4/4 PASS；以新 registry 隔离渲染 `Osogovo Kocani vs FC Voska Sport` 得到“奥索戈沃 vs 沃斯卡体育”，联赛为“北马其顿足球甲级联赛”；`git diff --check` PASS。没有生成订单、发送 Telegram 或执行历史消息编辑。
- 本批只改唯一共享 display registry、curation 来源和统计；没有修改任何模型、策略、赛事范围、正式账本、结算或 Telegram 规则。历史 TG 结果仍以第九十四批已记录的真实 workflow 回执为准。

## 2026-10-15 正式范围来源复核（第九十六批）
- 从最新共享 `master` 快进确认 HEAD/origin 均为 `7ac0619521f32e67049ebdba9ecfc4de7c3c7485`，共享库工作树干净。正式范围 2,468 个 team IDs，2,301 个有 canonical、167 个 unresolved（93.23%）；各模型范围口径及逐队 unresolved 名单以该提交 `data/football_display_names/formal_scope_coverage.json` 为准。本轮没有合格新增映射，因此未制造空数据提交，也未改共享 JSON。
- 对未匹配中的科索沃、埃及、马耳他及东欧队名继续查中文球队页和联赛资料，并做全库标准化 alias 交叉检查。确认 `Flamurtari` 与阿尔巴尼亚 `Flamurtari Vlorë` 不是同一队；`Besa` 存在多个国家/俱乐部同名身份；`FK Internacional` 在黑山联赛上下文中不能复用巴西国际 canonical。Tips.GG 将 Malta `Sirens` 自动翻成“警报”，该结果不采纳。英文身份或自动音译不足以建立 canonical，本轮全部继续保留 unresolved。
- 本次针对 M1 的 `test_m1_telegram_display.py` + `test_m1_telegram_display_repair.py` 8/8 PASS；MR1 共享名称与 AI formatter 测试 4/4 PASS。共享仓库 HEAD 与远端一致、工作树干净；无策略运行、无消息发送/编辑。既有历史 Telegram 修复回执不变：M1 0 条编辑（41 已匹配，99 缺原文，97 未映射）；MR1 Formal 0 条编辑；MR1 AI 9 条因 Telegram 原 message 不可定位失败、192 条 unresolved。
- 未改变 M1、M1 OU R1、MR1 AH、MR1 AI 的策略、scope、账本、结算、发送格式或规则；本批只记录来源审查与当前验证状态。

## 2026-10-15 正式范围继续补齐（第九十七批）
- 为 TotalCorner `team_id 8710`、provider `El Merrikh` 新增 canonical“马瑞克”。7M 中文球队页 `https://team.7m.com.cn/15682/index.shtml` 将埃及乙级 A/B 赛程中的该队显示为繁体“馬瑞克”，页面比赛记录与 El Merrikh 在埃及乙级联赛的身份一致。按简体写入，不与苏丹 Al-Merrikh 混并。
- 共享库提交 `e8401be96733e1c2cba1f99f1ff795000cfc993c` 已推送 master。formal union 2,468 IDs：2,302 canonical、166 unresolved（93.27%）；M1 1,523/1,553（98.07%），M1 OU R1 52/52，MR1 AH 1,784/1,921（92.87%），MR1 AI declared mirror 1,523/1,553（98.07%）。全部 unresolved 逐队明细仍以同提交 `formal_scope_coverage.json` 为准。
- M1 formatter/name-repair tests 8/8 PASS；MR1 shared registry/AI formatter tests 4/4 PASS；MR1 隔离读取共享新 registry 后将 team_id 8710 渲染为“马瑞克”，联赛“埃及第二级联赛”。M1 正式账本未发现 team_id 8710 的已发送 pick；未编辑/发送 Telegram。本轮没有触发生产 workflow。
- 只更新共享展示映射、覆盖报告、curation 与本交接；未更改任何模型/策略、赛事范围、账本、结算或 Telegram 规则。

## 2026-10-15 正式范围继续补齐（第九十八批）
- 继续读取最新共享库，不重跑历史身份恢复。为 TotalCorner team_id 138096 Alexandria Petroleum 新增“亚历山大石油”，来源为 Betimate 中文赛事页明确显示“亚历山大石油队”并标注埃及乙级B组；为 team_id 43017 Ahrobiznes Volochysk 新增“阿赫罗比兹内斯·沃洛奇克”（Tips.GG 中文球队档案）；为 team_id 48509 Ethnikos Neou Keramidiou 新增“埃斯尼科斯内乌克拉米迪乌队”（Tips.GG 中文球队档案）。未合并近似名/不同 team_id。同步补 league_id 63 Ukraine Persha Liga →“乌克兰足球甲级联赛”（FootyStats 中文赛事页）。
- 共享 master 最新提交 8043ba4b 已推送。正式 union 2,468 IDs：2,305 canonical、163 unresolved（93.40%）；M1 1,523/1,553（98.07%），M1 OU R1 52/52（100%），MR1 AH 1,787/1,921（93.02%），MR1 AI declared mirror 1,523/1,553（98.07%）；AI confidence≥50 observed cohort 181/182。全库 12,276 team IDs、4,321 canonical；覆盖及全部 unresolved 明细在共享 data/football_display_names/formal_scope_coverage.json。
- M1 Telegram formatter 单测 6/6 PASS；MR1 shared registry test 1/1、MR1 AI formatter tests 2/2 PASS。隔离加载刚推送的共享 JSON 后，三支新增球队及乌克兰甲级联赛均解析为中文，AH 主队方向同步中文。无策略运行或新 Pick。
- 最新 M1 ledger 中未发现这三个新增 team_id 的历史 Pick；因此本批名称没有可修复的 M1 已发送消息。历史 TG 编辑 workflow 仅在确认有待修复记录时使用；不得把 formatter 验证当成 Telegram 编辑回执。暂未编辑或重发 Telegram。
- 只更新共享中文展示名、来源/覆盖报告及本交接；模型、策略、阈值、scope、正式账本、settlement 和 TG 派单逻辑均未改。

## 2026-10-15 正式范围继续补齐（第九十九批）
- 沿用共享仓库最新 master，未重跑历史身份恢复。为 TotalCorner `team_id 89318` `CSC Dumbravita` 新增 canonical“杜姆布拉维察CSC队”，来源为 Tips.GG 简体中文比赛页；为 `team_id 35020` `SC Popesti Leordeni` 新增“SC 波佩什蒂-列奥尔代尼队”，来源为 Tips.GG 简体中文比赛页。记录保留原 provider name、别名、league IDs 及可核验来源，未与相似球队合并。来源：[CSC Dumbravita](https://tips.gg/cn/archive/acs-dumbravita-football-vs-scolar-resita-football/)、[SC Popesti-Leordeni](https://tips.gg/cn/matches/football/12-08-2026/sc-popesti-leordeni-vs-cs-dinamo-bucuresti/09-00/)。
- 共享库已推送 master，提交 `2a5aaeefb8b8c645892de30e575730fd9868bbcf`。从该提交的 `formal_scope_coverage.json` 实算：正式范围 2,468 IDs，2,307 canonical、161 unresolved（93.48%）；M1 1,523/1,553（98.07%），M1 OU R1 52/52（100%），MR1 AH 1,789/1,921（93.13%），MR1 AI declared mirror of M1 1,523/1,553（98.07%）；observed MR1 AI confidence≥50 cohort 181/182（99.45%）。共享库总计12,276 team IDs、4,323 canonical；联赛771个，其中339个已有中文名、432个 unresolved。完整未匹配 ID、原英文名、联赛上下文和原因保存在同提交 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；未虚构名称。
- 来源分布明细保存在 `formal_scope_coverage.json#source_distribution_canonical_team_rows`（按来源类别逐项统计），本批两条均为 `tips_gg_simplified_chinese_team_profile`。M1 formatter/name-repair 8/8 PASS；MR1 shared-registry 2/2、AI formatter 2/2 PASS。以当前共享 JSON 隔离渲染两支新球队，得到“杜姆布拉维察CSC队 vs SC 波佩什蒂-列奥尔代尼队”；这只验证展示读取，不触发模型或 Telegram。
- 历史修复 workflow 真实回执：M1 run [`38623200716`](https://github.com/ljm198964-alt/quant-runner/actions/runs/38623200716) PASS，eligible 41、edited 0、already_matching 41、缺原始消息文本99、未映射97、failed 0；MR1 Formal run `38623207575` PASS，edited 0、eligible 0、already processed 125；MR1 AI run [`38623214139`](https://github.com/ljm198964-alt/quant-runner/actions/runs/38623214139) PASS，但201条中9条候选编辑均被 Telegram 返回 `400 message to edit not found`，另192条 unresolved，实际 edited 0。三次 run 使用的是前一共享提交 `8043ba4b`，早于本批两个罗马尼亚名称；本批未重发任何历史单，也不把 workflow 成功误报为历史消息已修复。M1 OU R1 没有独立正式 TG 历史编辑链，无法提供单独旧消息编辑回执。
- 本节依据最新共享数据更新；后续如发现新来源再按 ID 逐项追加。仅改展示 registry/交接和来源证据，不改 M1、M1 OU R1、MR1 AH、MR1 AI 的策略、阈值、赛事范围、订单、账本、结算或 Telegram 规则。

## 2026-10-15 正式范围未匹配来源复核（第一百批）
- 从共享 master `2a5aaeefb8b8c645892de30e575730fd9868bbcf` 的最新 `unresolved_records` 复核，formal union 仍为 2,468 IDs、2,307 canonical、161 unresolved。按联赛上下文筛出 29 条关联 `league_id 417`（Egypt Division 2）的 unresolved，逐名检查 FootyStats 简体中文埃及乙级赛程/球队页与 7M 简体/繁体埃及乙级赛程页面。来源：[FootyStats 2026/27 中文赛程与积分](https://footystats.org/cn/egypt/second-division)、[FootyStats 中文赛程结果页](https://footystats.org/cn/egypt/second-division/fixtures)、[7M 埃及乙级A资料库](https://data.7m.com.cn/matches_data/998/big/index.shtml)。
- 该来源确实对部分俱乐部提供中文显示，但能从页面英文身份/队名上下文精确确认的中文名称对应已映射实体；涉及仍未匹配 ID 的页面条目继续显示英文，不能由资料中的阿拉伯文、城市名或近似俱乐部名推导中文队名。因此本次无安全新增，不改 `display_names.json` 或覆盖统计。`formal_scope_coverage.json#unresolved_records` 当前161项仍均标 `NO_VERIFIED_CANONICAL_ZH`。
- 同轮复核部分科索沃、罗马尼亚、乌克兰、格鲁吉亚、北马其顿未匹配队伍的精确中文网页检索，未得到可确认的主流中文球队名；不接受英文音译式临时猜名。此为来源审查结果，不是全量718历史名单完成的声明。后续可继续对各联赛寻找完整中文比分源/中英文赛程交叉表，再按 team ID逐项增补；保留当前161条正式范围口径。
- 未运行策略、生产扫描、TG发送/编辑或结算。仅此交接更新，不修改共享 registry、模型、策略、正式账本或通知。

## 2026-10-15 正式范围未匹配来源复核（第一百零一批）
- 继续以共享 `master` 最新 formal unresolved 清单为准（161条；正式范围2,468 IDs、2,307 canonical、93.48%），没有重跑历史身份恢复。围绕科索沃、马耳他、乌克兰、亚美尼亚、阿塞拜疆、法罗群岛、土耳其低级别队名，对7M/中文比分索引、365Scores中文页、Wikidata及俱乐部/足协官方资料做精确检索。
- 本轮未发现可安全新增的 canonical：`KF Vllaznia Pozheran` 的 Wikidata 实体无中文标签；中文资料中的 `Vllaznia` 指阿尔巴尼亚斯库台队，不能套到科索沃同名队。`Flamurtari` 的中文标签命中阿尔巴尼亚 Vlorë 队，不是储存赛事上下文中的 Kosovo/Pristina 队。`Besa` 亦有不同国家同名身份。`AFC Metalul Buzau`、`Agrobiznes Volochisk`、`FC Yerevan`、`FSC Mariupol`、`Marupes SC`、`Pembroke Athleta`、`Victoria Hotspurs` 等公开页面在本轮查到的来源中仍用英文；没有以地点音译替代主流中文队名。可复核页面包括 [365Scores 的 Metalul Buzau 中文地区赛程页](https://www.365scores.com/zh-tw/football/match/undefined-5513/liga-2-12581-53498-5513)、[Wikidata 的 KF Vllaznia Pozheran 实体](https://www.wikidata.org/wiki/Q30643286)、[Kosovo Cup 中文页](https://zh.wikipedia.org/wiki/%E7%A7%91%E7%B4%A2%E6%B2%83%E7%9B%83)及 [Victoria Hotspurs 官方站](https://www.victoriahotspursfc.com/)。搜索中出现的中文近名都经过国家/联赛上下文核对；身份不符者继续 unresolved。
- 因没有来源达标的新队名，本轮未修改共享 `display_names.json`/coverage 统计，也未制造空提交。当前精确计数仍以共享 master 的 `formal_scope_coverage.json` 为准：2,468 IDs、2,307 canonical、161 unresolved（93.48%）；M1 1,523/1,553（98.07%）、M1 OU R1 52/52、MR1 AH 1,789/1,921（93.13%）、MR1 AI 声明范围镜像 M1 为1,523/1,553。161条逐队 ID、英文名、league IDs、系统及 `NO_VERIFIED_CANONICAL_ZH` 原因均保留在 `unresolved_records`。
- 仅更新研究交接；没有触发生产策略、扫描、Telegram发送/编辑或结算，未修改任何模型、策略、范围、订单或账本。后续按联赛分组继续查找真实中文赛程表/团队档案交叉表；不因覆盖率目标接受错队映射、自动翻译或猜测音译。

## 2026-10-15 正式范围继续补齐与 MR1 只读接入验证（第一百零二批）
- 为 TotalCorner `team_id 100462` (`FK Tukums 2000/TSS II`, `league_id 242`) 新增 canonical “图库姆斯二队”。来源为 7M 简体中文球队档案 [Tukums-2000 II](https://team.7m.com.cn/650128/index_gb.shtml)，页面标题明确为“图库姆斯二队(Tukums-2000 II)”且赛果/赛程列有拉脱乙；英文 provider ID、二队身份和拉脱维亚联赛上下文完全吻合。保留 provider spelling 与 `Tukums-2000 II` 别名，不并入一线队。
- 共享 registry curator `ops/curate_formal_scope_7m_batch3.py` 增加一条可重复、ID 定向的 curation。共享仓库提交 `8d77259656b33fd1c66344c1e6e19dddfe5ddc15` 已推送 `totalcorner-research-bridge/master`。最新 formal union：2,468 IDs，2,308 canonical、160 unresolved（93.52%）；M1 1,524/1,553（98.13%），M1 OU R1 52/52（100%），MR1 AH 1,790/1,921（93.18%），MR1 AI declared mirror M1 1,524/1,553（98.13%）。共享库总计12,276 team IDs、4,324 canonical；完整160条未匹配及原因以该共享提交 `data/football_display_names/formal_scope_coverage.json#unresolved_records` 为准。
- M1 formatter/name-repair tests 8/8 PASS；MR1 shared display-registry tests 2/2 PASS；隔离加载最新共享 JSON 后 `displayFootballFixture` 将该 ID 渲染为“图库姆斯二队”，没有改动模型输入。最新本机 M1 正式订单/邮件账本未发现该 ID 的历史出单；MR1 对应正式 prospective entry/Telegram message 也未找到，因此本轮没有可按原 message ID 修复的旧 TG 文本，不重发任何历史单。MR1 只读共享库 smoke run `38625797996` 已派发但失败在 runner 启动之前：GitHub job API 返回 `runner_name` 为空、`steps=[]`，日志不可取；不能据此宣称云端 smoke PASS。生产运行会在正式 workflow checkout `master` 时读取此共享库。
- 仅新增一条显示名称及交接，不改 M1、M1 OU R1、MR1 AH、MR1 AI 的模型、策略、盘口、赛事范围、账本、结算、派单或 Telegram 格式；没有生成 Pick、发送或编辑 Telegram。历史 TG 修复回执仍以既有批次逐条记录为准。

## 2026-10-15 正式范围中文覆盖与历史 TG 审计（第一百零三批）
- 共享中文库从 `8d77259656b33fd1c66344c1e6e19dddfe5ddc15` 更新到 `b89955e08b09a4cdd94cd302073f82352e4ddf52`。新增 TotalCorner team ID `147566` (`FK Beitar Riga/Mariners`) →“比塔尔/里加水手”，来源 Tips.GG 中文比赛页明确同时列出中文队名、英文身份、拉脱维亚国家及与 Marupe 对阵；其拉脱维亚足协俱乐部页也核对了该英文身份。无同名球队合并。
- formal union 最新 2,468 IDs：2,309 canonical、159 unresolved，覆盖率 93.56%；M1 1,525/1,553（98.20%），M1 OU R1 52/52（100%），MR1 AH 1,791/1,921（93.23%），MR1 AI declared mirror of M1 1,525/1,553（98.20%）。全量未匹配清单及逐条 `NO_VERIFIED_CANONICAL_ZH` 原因保留在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；不音译猜名。
- 本机验证：M1 formatter/repair 8/8 PASS；MR1 shared display、V6 repair、AI Telegram formatter 4/4 PASS。隔离渲染四链 M1 AH、M1 OU R1、MR1 AH、MR1 AI 读取同一 registry，显示“比塔尔/里加水手”，并保持方向字段匹配队名。没有运行正式扫描或触发新信号。
- 历史 TG：本地 M1 ledger 有 237 条已发送 Telegram 记录，237/237 持久化原 `provider_message_id`，且所有 237 条根据原冻结 team/league ID 可生成中文替换候选；本轮实际编辑 0、未执行 237，阻碍是本机没有可用 M1 TG 凭据且不能从 GitHub Secret 读回明文，亦没有适合安全单独执行的现成 M1 edit job。MR1 AI 的既有历史 edit report 记录 `edited=0`、9 条失败（Telegram 返回 `message to edit not found`）、192 条 unresolved；MR1 V6 formal repair status 为 125 skipped、0 edited。没有重发或改账本。MR1 smoke run `38625797996` 在 runner 分配前失败，未宣称云端 PASS。
- 仅更新共享 display data、curation/statistics 和本 handoff；没有修改四个模型/策略、赛事范围、价格、订单、结算或 TG 内容规则。旧消息的 Telegram 文本编辑未完成，待存在安全凭据执行入口后再逐条使用原 message ID 编辑。

## 2026-10-15 正式范围继续补齐与 TG 中文链路审计（第一百零三批）
- 按最新共享库（本轮开始 HEAD `8d77259656b33fd1c66344c1e6e19dddfe5ddc15`）继续精确检查 formal unresolved 清单，没有重跑历史身份恢复。为 TotalCorner `team_id 147566`、provider `FK Beitar Riga/Mariners` 新增“比塔尔/里加水手”，别名保留 `FK Beitar / Riga Mariners`、`Beitar/Riga Mariners`。来源是 Tips.GG 简体中文比赛档案页面 [马鲁佩 vs 比塔尔/里加水手](https://tips.gg/cn/archive/beitar-riga-mariners-football-vs-marupe-football/)，并用拉脱维亚足协该俱乐部档案核对实体身份。 curator 加入 ID 定向、可重复的来源记录；未覆盖既有 canonical。
- 共享库更新后 formal union 2,468 IDs：2,309 canonical、159 unresolved（93.56%）；M1 1,525/1,553（98.20%），M1 OU R1 52/52（100%），MR1 AH 1,791/1,921（93.23%），MR1 AI declared mirror 1,525/1,553（98.20%）。完整未匹配 ID、英文名、赛事上下文及原因仍在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；159 条均保留 `NO_VERIFIED_CANONICAL_ZH`，没有用音译凑覆盖率。
- M1 formatter 与历史显示测试 8/8 PASS；MR1 shared-registry、formal display repair、AI Telegram formatter 测试 4/4 PASS。隔离渲染确认同一 registry 可让 M1 AH、M1 OU R1、MR1 AH、MR1 AI 的展示解析使用 canonical；新映射输出“比塔尔/里加水手”，对应拉脱维亚联赛名也为中文。M1 scan 与 MR1 runtime 均从共享 registry 路径读取；MR1 runtime checkout `master`。本轮没有正式扫描或发信。
- 历史 TG 只读账本审计：本地 M1 ledger 有 237 条 Telegram `SENT` 且 237 条均有原 provider message ID；中文替换候选可由同一 Pick 的冻结 team/league ID 生成。但本机未配置可用 M1 TG 环境凭据，且不能从 GitHub Secret 读取明文；因此本轮实际编辑 0、237 条均未执行（阻碍：缺少受控执行凭据及适用的安全编辑执行入口），没有重发、没有改账本。MR1 V7 已有针对 AI Telegram 的历史编辑脚本，但本机也无 MR1 TG token；MR1 formal 的实际编辑尚不能宣称完成。GitHub Actions 只读 smoke 的既有 run `38625797996` 在 runner 分配前失败（`runner_name` 为空、`steps=[]`）；本轮未重新触发。历史 TG 实际修复数仍为 0，不能把 formatter 测试算成线上编辑成功。
- 除共享展示库、其来源/覆盖报告和本交接外，没有改模型、策略、范围、价格、选单规则、正式订单、结算、Telegram 格式或消息状态。另：公开搜索来源显示 7M/其他中文比分索引中大量剩余低级别队伍仍只给英文/身份不足；不根据地名或自动翻译猜中文名。

## 2026-10-15 正式范围中文名称续补（第一百零四批）
- 从共享库提交 `b89955e08b09a4cdd94cd302073f82352e4ddf52` 继续，未重跑历史身份恢复。新增 7 个 ID 定向中文名称并提交至共享库 `a78f341f`：42821 AFC梅塔卢尔布泽乌、168037 马尔丁1969、147657 弗拉特里亚队、153877 AP布雷拉斯特鲁米察、151027 巴库体育、151005 贾布雷伊尔、42741 弗拉穆塔里。每条保留原英文身份、别名及来源 URL；未覆盖既有 canonical。来源为 Tips.GG 简体中文球队页/比赛页，按球队身份及国家/赛事上下文交叉核对。
- 最新 formal union：2,468 IDs，2,316 canonical、152 unresolved（93.84%）；M1 1,531/1,553（98.58%），M1 OU R1 52/52（100%），MR1 AH 1,797/1,921（93.55%），MR1 AI declared mirror of M1 1,531/1,553（98.58%）。完整未匹配 ID、身份、联赛上下文和 `NO_VERIFIED_CANONICAL_ZH` 原因在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；不为覆盖率猜名。
- 验证：M1 formatter/repair `8/8 PASS`；MR1 shared display + AI Telegram formatter `4/4 PASS`；V6 historical edit repair test 单独运行 `1/1 PASS`。隔离 resolver 读取最新共享文件，MR1 将 team ID 147657/相同路径解析到 canonical；M1 formatter 对新增正式 ID 生成中文球队方向。测试不等于线上 Telegram 文本编辑。
- 历史 Telegram 本轮未编辑、未重发；没有触发生产扫描、通知或账本写入。此前记录的阻碍仍是缺少安全可用的生产 TG 编辑凭据/受控 edit job，且 Telegram 已删除或不可编辑的消息需按真实 API 回执判定。未修改模型、策略、赛事范围、盘口、Pick、结算或发送规则。

## 2026-10-15 正式范围名称续补（第一百零五批）
- 从共享库 `a78f341f3922a85f85e4b97ea86108976e93fba0` 继续，仅检索现存 unresolved 清单。新增 TotalCorner team ID `168001` `Safa Baku` →“萨法巴库队”，来源为 Tips.GG 简体中文球队页，页面给出中文名、英文队名和阿塞拜疆身份；映射已提交到共享库 `3643c58f805e718753bad6d1403ed63883e3c73b`。没有按相似英文名称合并其他 team ID。
- 正式范围更新为 2,468 IDs、2,317 canonical、151 unresolved（93.88%）；M1 1,532/1,553，M1 OU R1 52/52，MR1 AH 1,798/1,921，MR1 AI 镜像 M1 1,532/1,553。权威分项及完整未匹配清单见该共享提交的 `formal_scope_coverage.json`。
- 本轮 M1 formatter/repair 测试 8/8 通过；未触发正式扫描、TG 发送或历史编辑。其他抽查未找到可靠中文名的名称保留 unresolved；策略、赛事范围、盘口、账本、结算和发送逻辑未修改。

## 2026-10-15 unresolved 身份防误并复核
- 对当前 unresolved 批量抽查了 FK FAP、Qena/Asyut 低级别队、Shkëndija Haraçinë、Kosovo Prishtinë 等候选；没有把缺少可靠中文惯用名的球队强行映射。本轮 formal 数仍为 2,468 总 ID、2,317 canonical、151 unresolved（93.88%）。
- 更新共享覆盖报告 `formal_scope_coverage.json` 并推送 `1c209ca4b1140b40c7f42f39364f35bd0d1fbb66`：对 ID 42262 `Vllaznia` 记录其 Kosovo Superliga 上下文不能套用阿尔巴尼亚维拉兹尼亚中文名；对 ID 43486 `Vllazina` 记录不可仅凭近似拼写与前者合并；对 ID 45722 `KF Kosova Prishtine` 记录其 Kosovo Division 2 身份不同于 FC Prishtina，不复用普莱斯堤纳映射。证据 URL 直接保存在各 unresolved 记录的 `reason_detail`。
- 本轮没有新增 canonical 行，没有运行模型/生产流程，也未发送或编辑 Telegram。名称库测试仍以最近批次 M1 8/8、MR1 display/AI formatter 4/4、V6 repair 1/1 为准；未因纯证据注释更改测试代码。

## 2026-10-15 正式范围名称续补：OFK Vrsac
- 新增共享 team ID `107746`：`OFK Vrsac` → `OFK弗尔沙茨`，别名保留 `OFK Vršac`。中文比赛数据页 [JQ007 OFK弗尔沙茨 vs Dubocica](https://www.jq007.com/h2h/fk-dubocica-vs-ofk-vrsac) 给出该中文显示名；俱乐部官网 `ofkvrsac.com` 核对 OFK Vršac 的塞尔维亚身份，正式 league ID 337 也对应塞尔维亚甲级联赛。映射通过可重复 ID 定向 curator 写入，未改动其他同名/近名球队。
- 共享库提交 `8e3d6a03e6513de70b04aa8895bf8cd134051c35`。正式 union 2,468 IDs：2,318 canonical、150 unresolved（93.92%）；M1 1,533/1,553（98.71%），M1 OU R1 52/52（100%），MR1 AH 1,799/1,921（93.65%），MR1 AI declared mirror of M1 1,533/1,553（98.71%）。完整清单以该提交 `formal_scope_coverage.json#unresolved_records` 为准。
- 验证：M1 formatter/repair 8/8 PASS；挂载本次共享库目录的 MR1 display/AI formatter 4/4 PASS；V6 display repair 1/1 PASS。只做隔离 resolver/formatter 测试，无正式扫描、TG 发送或历史消息编辑；生产策略、订单与结算均未修改。

## 2026-10-15 正式范围名称续补：Riga Mariners
- 从最新 `master`（父提交 `8e3d6a03e6513de70b04aa8895bf8cd134051c35`）继续，未重跑历史身份恢复。为 TotalCorner `team_id 164677` (`Riga Mariners`) 添加 canonical `里加水手`，以中文足球赛事列表的“里加水手队”标签为名称证据，并用拉脱维亚足协俱乐部页及官方俱乐部站交叉核验英文身份。该名称只写入 ID 164677；未与相似旧 ID 合并。
- 共享库提交 `8fb30cda977683bbdb3a2f19e54cdc5c3e39bfd7` 已推送 `totalcorner-research-bridge/master`。formal union 2,468 IDs：2,319 canonical、149 unresolved（93.96%）；M1 1,534/1,553（98.78%），M1 OU R1 52/52（100%），MR1 AH 1,800/1,921（93.70%），MR1 AI declared mirror of M1 1,534/1,553（98.78%）。完整剩余清单和逐条原因见同一提交的 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 验证：M1 Telegram display/repair 8/8 PASS；MR1 shared registry/AI formatter 4/4 PASS（实际挂载最新共享 JSON）；MR1 V6 display-repair 1/1 PASS。没有运行正式模型或订单，也没有发送或编辑历史 Telegram。
- 本次只新增 1 个已核实名称；149 个仍缺可靠 canonical 的球队继续保留未匹配状态。历史 TG 的批量改字未在本次执行，不能宣称已实际修复；需依据各自正式账本、可用的安全编辑执行环境和 Telegram API 回执单独核验。未修改策略、盘口、赛事范围、账本或结算。

## 2026-10-15 正式范围名称续补：KF Oriku
- 从刚更新的共享 `master` 继续，仅处理正式 unresolved。为 TotalCorner `team_id 50971` (`KF Oriku`) 新增 canonical `KF奥里库`，依据雷速中文球队页对该队的中文名及英文身份标注；按 team ID 单独写入，不推断/合并其他 Oriku 或近名俱乐部。
- 共享库提交 `5367ebd557806076830112c11bc85162658dc9b7` 已推送 `totalcorner-research-bridge/master`。formal union 2,468 IDs：2,320 canonical、148 unresolved（94.00%）；M1 1,535/1,553（98.84%），M1 OU R1 52/52（100%），MR1 AH 1,801/1,921（93.75%），MR1 AI declared mirror of M1 1,535/1,553（98.84%）。以该提交的 `formal_scope_coverage.json#unresolved_records` 为剩余清单。
- M1 display/repair 测试 8/8 PASS；MR1 resolver/AI Telegram formatter 4/4 PASS；MR1 V6 display-repair 测试 1/1 PASS（隔离环境串行执行）。本批未发送/编辑 Telegram，也未触发正式策略运行或结算。
- 新映射仅增加正式范围覆盖；其他尚无可靠中文名称的条目继续保留 unresolved。本轮不涉及策略、Crown、赛事范围、正式账本和结算逻辑。

## 2026-10-15 展示链路抽样与剩余项复核
- 共享库当前 master `5367ebd557806076830112c11bc85162658dc9b7`；正式 union 2,468 IDs、2,320 canonical、148 unresolved（94.00%）。本轮另复查 Sirens、Pembroke Athleta、FC Hoyvik、FS La Massana、GFK Ohrid Lichnidos、Shturmi、Spartakos Kitiou 及埃及低级别球队。所查页面多只保留英文；一个雷速结果实际是 `Shturmi II`，与正式 unresolved `Shturmi` 不同，故排除，未误配。
- 隔离实渲染确认新增 ID 可读：M1 formatter 对 Riga Mariners 输出中文联赛/球队；MR1 shared resolver 同样按 team ID 输出 `里加水手`、`KF奥里库`。抽样的未映射 Marupes SC 仍显示 provider 英文名，说明 148 个缺口仍会造成部分未来消息英文 fallback；没有以虚构译名遮盖。
- 本轮历史 Telegram 实际编辑数为 0；没有具备本任务可用的既有一次性编辑 workflow，因此未新增 workflow、未触发真实策略扫描，也未发送/编辑消息。格式器测试只能证明本地渲染，不是 TG API 回执或已编辑历史消息的证据。后续如启用已有受控编辑执行链，应按每条账本中的原 provider message ID 核验成功/不可编辑回执。
- 其余 148 个逐条记录、英文身份、赛事上下文和未匹配原因可从共享 `formal_scope_coverage.json#unresolved_records` 读取；不得把目前 94.00% 说成全量完成。策略、派单、账本与结算未修改。

## 2026-10-15 正式范围中文名称续补：乌克兰甲级球队
- 从共享 master `b30668ac9091dbb95a79e71d0d5c7d5ea3ca9679` 继续。经7M简体球队档案及独立中文赛事页面核对，新增 `team_id 150733 FC Probiy Horodenka → 普罗比霍洛登卡`；经 Vitisport 中文赛程中英队名与 TotalCorner 乌克兰甲级历史身份交叉核对，新增 `team_id 43272 Agrobiznes Volochisk → 沃洛奇斯克农业企业`。来源、交叉核验说明、英文别名均写入唯一共享 `display_names.json`。没有根据 ID 猜名，也未覆盖既有映射。
- 共享 registry PR #5 已合入 master，提交 `4d67fd55`（merge commit；curation commit `3c2b44bcf36567df35c7c84fbdc91ea407265c97`）。本次正式范围从2,468队、2,320 canonical/148 unresolved（94.00%）更新至2,468队、2,324 canonical/144 unresolved（94.17%）。分项：M1 1,539/1,553（99.10%）；M1 OU-R1 52/52（100%）；MR1 AH 1,805/1,921（93.96%）；MR1 AI 声明镜像 M1 1,539/1,553（99.10%）；MR1 AI observed confidence≥50 cohort 181/182（99.45%）。全部未匹配 ID/英文名/联赛/系统及原因详见共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 本机验证：M1 formatter/name-repair 8/8；MR1 shared registry + AI Telegram formatter 4/4；MR1 V6 historical display repair test 1/1。隔离渲染 `league_id 63` 及两个 team ID 为“乌克兰足球甲级联赛 沃洛奇斯克农业企业 vs 普罗比霍洛登卡”，反向主客也正确。以上均为展示层测试，不触及模型字段。
- 已各运行一次现存 name-only historical edit workflow（仅编辑旧 message ID，不重发）：M1 run `38632933246` PASS，41 eligible、edited 0、already matching 41、缺原消息文本99、未映射97、failed 0；MR1 Formal `38632933636` PASS，125 already processed、0 edit、0 fail；MR1 AI `38632932673` PASS，201 total、9 edit candidates、edited 0、9 failed（Telegram 400 `message to edit not found`）、192 unresolved。没有任何历史订单重发，也没有测试/新 Telegram 消息；本轮实际编辑数为0。
- 只更新共享中文展示数据、curator/coverage 与此 handoff；M1、M1 OU-R1、MR1 AH、MR1 AI 的模型、策略、范围、盘口、订单、账本、结算与发送条件均未修改。

## 2026-10-15 最新 master 核对及历史 TG 修复回执
- 从共享仓库最新 `master` `5b0ac813c6b209f05fa9df89a05f7544c38cb69d` 快进核对，没有覆盖远端的 M1 运行数据。当前正式范围仍是 2,468 IDs、2,320 canonical、148 unresolved（94.00%）；M1 1,535/1,553（98.84%）、M1 OU R1 52/52、MR1 AH 1,801/1,921（93.75%）、MR1 AI declared mirror 1,535/1,553（98.84%），观察到的 MR1 AI confidence≥50 cohort 181/182（99.45%）。共享库统计为12,276个team ID、4,336个 canonical。未找到足以核验中文队名的新来源，本轮不新增或猜译；逐条剩余名单仍以共享库 `formal_scope_coverage.json#unresolved_records` 为准。
- 复核英文身份/中文资料的具体例子：`Dinaz Vyshgorod`、`Hirnyk-Sport Horishni Plavni`、`Marupes SC`、`FC Yerevan`、`KF Podujeva` 的本轮搜索结果不能证明主流简体中文队名；`Marupes` 的韩文站本地化结果、俄/乌语及机器翻译均不作为中文 canonical。没有把地点音译或相似队名塞入 ID 映射。
- 从 quant-runner Actions 读取到 M1 历史修复旧回执：run `38132221201` 为158条已发送记录、13条可改且13条编辑成功、0失败，99条无原消息回执、46条无映射。最新 run `38623200716` PASS：41条待校验记录均已与目标中文文字一致（`already_matching=41`），0新编辑、0失败；99条无原始文本、97条无可用映射。此处“已匹配”不计作本轮编辑。
- MR1 AH 正式消息的历史修复旧回执：run `38132942734` 实际编辑2条、0失败；最新 run `38623207575` PASS，125条已处理、0待编辑、0失败，远端 repair status 有98个已完成 fingerprint。MR1 AI 最新 run `38623214139` PASS 仅指 workflow 执行成功：201条中192条未解析、9条尝试编辑均因 Telegram `400 message to edit not found` 失败，实际编辑0条。不得把 workflow PASS 表述为全部历史消息已修复。
- 四条链的未来消息 formatter/registry 接入沿用同一共享 JSON；M1 formatter、MR1 resolver及AI formatter测试保持前述 PASS。M1 OU R1共用M1正式消息修复链，不另造映射或账本。由于本轮无新增 canonical，未重复派发历史 TG 编辑工作流，也未运行模型/扫描/结算；策略、盘口、范围、派单规则、账本均未变。

## 2026-10-15 正式范围中文库续补：埃及球队与实际 Telegram 复核
- 基于共享库最新 `master` 新增五个有 FootballAnt 简体中文球队档案及同站英文身份档案交叉验证的 TotalCorner ID：`76195 Sporting Alexandria → 亚历山大竞技`、`90142 Al Madina Al Monawara SC → 麦地那莫纳瓦拉`、`49591 Shoban Moslemen Qena → 索巴尼莫勒梅`、`5988 El Hammam → 哈马姆`、`44010 Bani Ebaid → 巴尼`。对应 FootballAnt 双语球队页分别为 profile IDs `51384`、`59265`、`18740`、`36170`、`9405`；映射、原 provider 名、别名和来源说明均写入唯一共享库。没有合并同名/近名 ID。
- 共享 PR [#7](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/7) 已合并，master merge commit `a05ac74b17c350a5037b642886928bd890bbe523`。最新正式 union 2,468 IDs，2,332 有 canonical、136 未匹配（94.49%）；M1 1,547/1,553（99.61%，6 未匹配），M1 OU R1 52/52（100%），MR1 AH 1,813/1,921（94.38%，108 未匹配），MR1 AI declared mirror 1,547/1,553（99.61%）；旧 observed confidence≥50 子集 181/182（99.45%，口径沿用原快照）。完整未匹配 team ID、原名、league IDs、系统和 `NO_VERIFIED_CANONICAL_ZH` 说明见共享库同提交 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 实际 formatter 验证：MR1 AI 用正式调用所需 `display.home/away` 结构渲染为“【MR1 AI】…埃及第二级联赛 亚历山大竞技 vs 麦地那莫纳瓦拉…亚历山大竞技 -0.25@0.95”；展示仍读取 shared registry。MR1 AI 调用方会拆解 shared resolver 的 `match` 填充主客队字段，无需改 formatter/调用代码。MR1 `npm test`、M1 formatter/name-repair 8/8 PASS；策略和消息格式未改。
- 合并后真实运行既有 name-only 历史修复：M1/M1 OU 共用 run [38636108570](https://github.com/ljm198964-alt/quant-runner/actions/runs/38636108570) PASS：eligible 41、edited 0、already matching 41、missing original text 99、unmapped 97、failed 0。MR1 AH formal run [38636424190](https://github.com/ljm198964-alt/quant-runner/actions/runs/38636424190) PASS：already processed 125、eligible/edit 0、unresolved 0、failed 0。MR1 AI run [38636611573](https://github.com/ljm198964-alt/quant-runner/actions/runs/38636611573) PASS（表示 workflow 完成，不代表编辑成功）：total 201、candidates 9、edited 0、unresolved 192、failed 9；9 条 Telegram API 均返回 `400 message to edit not found`。没有重发消息、没有新测试通知；实改总数仍为0，MR1 AI 的失败明细已持久化至 `mr1-shadow` commit `7279135109`。未来消息使用最新共享映射；6 条 M1/108 条 MR1 AH 未匹配仍可能显示原 provider 英文名，不以猜译补齐。
- 本轮只变更共享中文展示数据/报告及本交接；没有修改 M1、M1 OU R1、MR1 AH、MR1 AI 策略、模型、Crown、scope、阈值、正式订单/结算或 Telegram 格式/发送规则。

## 2026-10-15 正式范围中文库续补：FK Internacional
- 从 `88370dce`（PR #8 merge）接续唯一共享 registry，新增 TotalCorner `team_id 133668`、`FK Internacional` → `波德戈里察国际`。来源为 7M 中文球队档案 `https://team.7m.com.cn/652136/index_gb.shtml`，其队名/黑山身份与黑山足协 FK Internacional（Podgorica）记录及 formal `Montenegro Druga Liga` 上下文交叉核验。新增源证据及可重复 curator 记录一并提交；未覆盖既有 canonical。
- 最新正式范围：2,468 个 team ID，2,333 mapped、135 unresolved（94.53%）；M1 1,548/1,553（99.68%），M1 OU R1 52/52，MR1 AH 1,814/1,921（94.43%），MR1 AI declared mirror 1,548/1,553（99.68%）。逐条剩余身份及 `NO_VERIFIED_CANONICAL_ZH` 原因在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- PR #8 `5ff59b5f641b985327270d4cc7ffececfebcd5c6` 已合并，master merge commit `88370dce`。M1 display/history repair 测试 8/8 PASS。本轮在本地 totalcorner checkout 的结果/账本文本搜索未找到该 ID 的正式 Telegram 旧消息证据，因此未调用历史编辑工作流；MR1 仓库未逐条复查，且没有 Telegram 编辑或发送。检索其余样本未得到可核验常用中文名称的，继续保留 unresolved。
- 本轮只更新共享名称库、curation/audit 与交接记录；未修改任何模型、策略、赛事范围、账本、结算或 Telegram 规则。

## 2026-10-15 正式范围余项复核与历史 TG 名称回执
- 以共享 `master` `88370dce0df268e0896006581b7b3337cf14e6a7` 的实际文件为准：正式并集 2,468 team IDs，canonical 中文 2,333，unresolved 135（94.53%）；M1 1,548/1,553（99.68%，余 5），M1 OU R1 52/52，MR1 AH 1,814/1,921（94.43%，余 107），MR1 AI declared mirror 1,548/1,553（99.68%）。完整 135 项（ID、英文 provider name、联赛、系统和逐项原因）仍在共享库 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。本轮不重复做全历史身份恢复。
- 对当前剩余清单做定向中文足球资料核验（包括 CS Ștefănești、Pembroke Athleta、KF Hajvalia、Qena/埃及低级别俱乐部、FC Hoyvík、BSK Banja Luka、Stupčanica、FSC/Feniks Mariupol、Mostaqbal Watan 等）。找到的页面多仅有英文/其他语种名称，或不能证明与具体 TotalCorner ID 为同一队；未发现可安全新增的主流简体 canonical，新增数为 0。尤其不把阿尔巴尼亚 Vllaznia 中文名挪给 Kosovo league ID，也不合并 Vllaznia/Vllazina；不把旧 FC Mariupol 的名称直接迁移给 FSC/Feniks 身份。未知名称维持 unresolved，不编造译名。M1/MR1/MR1 AI 格式器继续共用 `display_names.json`，无 reader/策略代码变更；M1 display + history-repair 单测 8/8 PASS。
- 为最新共享映射实际运行现有 name-only 编辑工作流（均只对账本既存 Telegram message ID 执行 edit，不发送新单）：
  - M1 / M1 OU-R1 共用 run [38638714213](https://github.com/ljm198964-alt/quant-runner/actions/runs/38638714213) PASS：41 eligible，edited 0，already matching 41，缺原始发送文本 99，仍无映射 97，failed 0。真实 API 回执说明这 41 条此前已是本次期望中文，不是本轮新增编辑。
  - MR1 AH formal run [38638720307](https://github.com/ljm198964-alt/quant-runner/actions/runs/38638720307) PASS：125 条均 already processed，eligible/edit 0，unresolved 0，failed 0；本轮没有实际编辑。
  - MR1 AI run [38638725770](https://github.com/ljm198964-alt/quant-runner/actions/runs/38638725770) workflow PASS，但 Telegram edit 结果为 total 201、candidate 9、edited 0、unresolved 192、failed 9；9 条均返回 `400 Bad Request: message to edit not found`，不能再通过当前 bot/chat message ID 修改。失败记录由现有工作流保存；未重发历史策略。
- 本轮历史消息实际编辑 0 条。新增 mapping 为 0，因此没有所谓新译名即时覆盖到这些历史单；41 条 M1 已匹配仅代表其当前 TG 文本已满足 formatter 目标。M1 的 97 条 unresolved、MR1 AI 的 192 条 unresolved 以及旧消息缺原文等是剩余显示限制。运行器账户当前允许上述 3 个修复 workflow 执行；这不等于之前受付款限制的生产定时扫描已恢复。
- 本轮仅补充本 handoff 和进行展示/名称证据核验；没有修改共享 registry 数据、模型、策略、比赛范围、Crown、账本、结算或正式通知规则，也没有触发预测/扫描或发送测试 Telegram。

## 2026-10-15 正式范围中文库续补：BSK Banja Luka
- 从共享库 `88370dce` 接续，新增 TotalCorner `team_id 102308`、`BSK Banja Luka` → `巴尼亚卢卡BSK`。7M 简体中文球队页明确列出“巴尼亚卢卡 (BSK Banja Luka)”：https://team.7m.com.cn/11694/index.shtml；中文俱乐部列表另将 FK BSK Banja Luka 标为“班查魯卡BSK”。由于同城 `Borac Banja Luka` 已独立对应 team_id 417，本条保留 BSK 标识以防串队。映射原始英文身份、别名、来源说明写入唯一共享 `data/football_display_names/display_names.json`；curator 和 M1 formatter regression test 同步更新。
- PR #9 已合并，共享 master merge commit `0284d372`（PR: https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/9）。正式 union 2,468 IDs，canonical 2,334、unresolved 134（94.57%）；M1 1,549/1,553（99.74%，4 unresolved）；M1 OU-R1 52/52；MR1 AH 1,815/1,921（94.48%，106 unresolved）；MR1 AI declared mirror 1,549/1,553（99.74%）；全共享库 12,276 team IDs、4,350 canonical。逐条剩余 ID、英文身份、league IDs、系统和原因见共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。本轮只新增1条，未跑全历史身份恢复；其余未找到可靠中文资料的仍保留 unresolved。
- M1 formatter、历史 repair、formal runtime 测试 21/21 PASS；MR1 最新 master 的 shared-registry 与 AI formatter 测试 4/4 PASS。team IDs 102308/417 隔离样本验证 M1 AH/M1 OU-R1 共用 formatter 及 MR1 AH/MR1 AI resolver 输出“巴尼亚卢卡BSK vs 巴尼亚”，方向也为“巴尼亚卢卡BSK”；模型数据未改。另，MR1 旧 V6 display-repair fixture test 与当前实现行为不一致：旧断言预期缺中文时 `edited=0`，而现有实现会替换历史未知占位符、实际 `edited=1`；本轮未改 MR1 修复代码。M1 ledger 没有 team_id 102308 的已发送 Pick；MR1 master 当前正式路径检索也未找到该 ID 的正式单，因此此新增映射对应的历史 Telegram 实际编辑数为0，没有发送或重发消息。
- 仅共享 display registry/curator/test 和此交接变化；未来运行读取同一共享库。未改任何 M1、M1 OU-R1、MR1 AH、MR1 AI 模型、策略、赛事范围、盘口、阈值、账本、结算、Telegram 格式或发送规则，也未运行生产扫描。

## 2026-10-15 正式范围赛事中文显示补充
- 按共享库最新 master 接续；正式球队范围仍是 2,468 IDs / 2,334 canonical / 134 unresolved（94.57%），M1 1,549/1,553（99.74%）、M1 OU R1 52/52、MR1 AH 1,815/1,921（94.48%）、MR1 AI declared mirror 1,549/1,553。未做历史身份大恢复，本轮未新增球队中文名；完整 134 条及逐项原因见 `totalcorner-research-bridge/data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 同一共享 registry 新增9个可核验正式赛事中文显示：Greece Cup→希腊杯、Czech Cup→捷克杯、Romania Cup→罗马尼亚杯、Cyprus Division 2→塞浦路斯乙级联赛、Georgia First League→格鲁吉亚足球甲级联赛、Saudi Arabia Division 2→沙特乙级联赛、Albania Championship→阿尔巴尼亚锦标赛、Andorra Second Division→安道尔乙级联赛、North Macedonia Second League→北马其顿乙级联赛。来源及可重复 curator 记录在 `data/football_display_names/competition_curation_20261015.json`；总联赛映射由771/339提升为771/348，未映射432降为423。对 Czechia First League Play-Offs、Lithuania II Lyga、Malta Challenge League、Kosovo Division 2、Northern Ireland Conference Premier 未找到足够准确的中文源，保留未映射。
- 共享库 PR #11 merge `68ec38fc582be5b69502341e7e95f7f62151541b`；PR #12 增加 curator 无变更时不产生时间戳差异，merge `1c3275c2ff857579084bf3c2cebdc8e84a9bd156`。M1 display/history repair 测试10/10 PASS；MR1 `node test.js` PASS，并对9个联赛 ID 的共用 resolver 做隔离渲染验证。未改模型、比赛/账本/策略字段或 Telegram 消息格式。
- 三条既有历史 name-only workflow 本轮均使用 ledger 既有 message ID，未重发：M1 run [38644448095](https://github.com/ljm198964-alt/quant-runner/actions/runs/38644448095) PASS，eligible 41、edited 0、already matching 41、缺发送原文99、未映射97、failed 0。MR1 AI run [38644447559](https://github.com/ljm198964-alt/quant-runner/actions/runs/38644447559) 完成但实际编辑0；9条 Telegram `message to edit not found`，192条 unresolved。MR1 AH 首次 run [38644447745](https://github.com/ljm198964-alt/quant-runner/actions/runs/38644447745) 未编辑任何消息，保存回执 push 与 MR1 AI 并发提交发生 master ref 锁冲突；已安排串行重跑 run `38644859754`，须核对最终状态后再补记。当前三条 workflow 实际编辑成功数均为0。
- MR1 AH 串行重跑 [38644859754](https://github.com/ljm198964-alt/quant-runner/actions/runs/38644859754) PASS：125 already processed、eligible/edit 0、unresolved 0、failed 0，回执保存成功。尚余正式范围134个未匹配球队显示名；逐条清单在共享 `formal_scope_coverage.json#unresolved_records`，继续保留未核实名，不虚构名称。三条本轮历史修复 workflow 的实际编辑成功数均为0；M1 41条为 already matching，MR1 AH 125条为 already processed，MR1 AI 9条旧消息不可由 Telegram 定位、192条没有可用中文映射。未来新消息通过共用 registry 使用已确认中文名。

## 2026-10-15 正式范围未匹配续查（第106批）
- 先核对最新共享仓库 `origin/master=c3319afae736601355c2a1c37e663a7714f82fe4`；此前 handoff 的 740 未匹配是过时快照。当前权威 `data/football_display_names/formal_scope_coverage.json` 为 2,468 个正式范围球队 ID，2,335 canonical、133 unresolved（94.61%）：M1 1,550/1,553（99.81%），M1 OU-R1 52/52（100%），MR1 AH 1,816/1,921（94.53%），MR1 AI declared mirror 1,550/1,553（99.81%），AI confidence≥50 cohort 181/182。逐项完整名单（team_id、英文身份、联赛上下文、系统、原因）仍由共享库 `formal_scope_coverage.json#unresolved_records` 提供，未另建库。
- 对最新133项运行共享 registry 全量 provider-name/alias 精确归一化连接，并要求联赛上下文相交；命中为0，没有误并。重新筛查公开数据集：公开中文队名包 `ddzyx/football-team-names-zh` 以共享 unresolved 英文名/别名精确连接命中0；此前核对的 `qqyg000/lottery-football` 映射也没有精确命中。`openfootball/clubs` 是公开英文俱乐部名/别名库而非中文名库，不能补 canonical。抽查 Tips.GG、7M、中文足球站搜索结果（如 Qena SC、FC Hoyvík、KF Hajvalia、埃及低级别队）只得到英文或不同实体/身份资料，未据此猜写简体标准名。
- 发现 SC Sports 的球队接口文档声明具有中/英/繁体球队名字段，但请求要求 token，站点说明访问权限可能需购买；本轮未调用需鉴权接口、未注册/购买服务、未写任何密钥。若用户要对这132个真实队名缺口做进一步数据库级补齐，需取得现有合法 API 权限/令牌；`team_id 4931` 的存储身份是字面值 `0`，原因仍为 `PROVIDER_IDENTITY_INVALID`，不能先定中文名。
- 本轮安全新增 canonical 数为0。四系统共享显示设计并未变更：MR1 resolver 指向 `external/football-display-registry/data/football_display_names/display_names.json`；M1 formatter 从共享 registry 数据路径解析；M1/MR1/MR1 AI/M1 OU-R1 仍依赖 team/league ID canonical，未知项按既有 fallback。只读隔离检查没有触发模型、策略或生产链。历史 Telegram 本轮实际编辑0；既有最近回执仍是 M1 0 edits、MR1 AH 0 edits、MR1 AI 0 edits（9条 Telegram 返回 message-to-edit-not-found、192条未解析），不得宣称历史消息已中文化。没有可用的本轮安全 edit 执行凭据/通道，故未触发 workflow。
- 最新共享库提交未变化：`c3319afa`；名称新增0，因此没有共享库提交。quant-runner handoff 在本条记录后更新并提交。模型/阈值、赛事范围、盘口源、订单、结算、发送规则均未修改；Actions 运行限制不是本轮数据工作的阻碍，实际数据阻碍是无免费公开中文映射命中以及剩余来源需要授权。

## 2026-10-15 正式范围中文名继续取证（第107批）
- 再次从远端 `master` 的当前 133 个 unresolved 开始；共享中文库无变更。查询 7M、雷速、Sofascore 中文站和开放足球映射来源，Sofascore 中文比赛/球队页对 Pembroke Athleta 等仍展示英文实体名；7M 对多项未匹配英文名的定向精确搜索无结果。公开搜索对 Qena SC、KF Hajvalia、FC Hoyvík 等命中的是英文身份或不同实体资料，不能将这些作为中文 canonical 证据。
- 只读验证 Sofascore 公共搜索接口 `https://www.sofascore.com/api/v1/search/all?q=Qena%20SC` 在当前环境返回 HTTP 403 Forbidden；没有尝试伪装客户端、绕过限制或改用受限端点。该路径目前不能用来对133项批量补名。SC Sports、球小策与部分机构数据仍需 token/权限；没有擅自注册、购买或读取不相关凭据。
- 本批新增中文 canonical 仍为0；没有变更 `display_names.json`，正式范围仍为2,468 / 2,335 canonical / 133 unresolved（94.61%）。M1 display 单测6/6 PASS；MR1 shared display 1/1、MR1 AI browser-forward 3/3 PASS，均为本地隔离验证，不是线上 Telegram 编辑证明。TG 本批没有发信或编辑；历史编辑成功仍未增加。完整未匹配项继续以共享库 `formal_scope_coverage.json#unresolved_records` 为准。
- 本批仅更新本交接；无模型、策略、scope、账本、settlement、正式通知或共享 registry 变更。继续推进需要可合法使用且覆盖低级别国际俱乐部的简体中文源（或相应已授权 API）；不得用音译/机器翻译把 133 项凑成全覆盖。

## 2026-10-15 正式范围中文名补录：Pembroke Athleta（第108批）
- 对最新正式 unresolved 133 项中的 TotalCorner `team_id 3343`（`Pembroke Athleta FC`）找到可直接核验的 Sofascore 简体中文球队页：`https://www.sofascore.com/zh/football/team/pembroke-athleta-fc/60766`。页面以英文俱乐部名展示实体，中文叙述称“彭布罗克”，并显示马耳他身份；formal 记录的原始 provider identity 与页面精确一致，league ID 46 上下文兼容。唯一共享库新增 canonical `彭布罗克`，原英文名/ID 不变，source kind 为 `sofascore_simplified_chinese_team_profile`。没有将其他 Pembroke 相近球队合并。
- PR [#14](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/14) 已合并；merge commit `ff1aeba465d40af963fa58eebb17e42642fa633a`，源分支 commit `dacdf43eacca38247140459a03c5a4362ef30402`。最新 formal scope：2,468 IDs、2,336 canonical、132 unresolved（94.65%）；M1 1,551/1,553（99.87%），M1 OU-R1 52/52（100%），MR1 AH 1,816/1,921（94.53%），MR1 AI declared mirror 1,551/1,553（99.87%）。逐条剩余项仍以共享库 `formal_scope_coverage.json#unresolved_records` 为准。
- 新增可重复 curation 路径并补 M1 formatter regression。验证：共享 repo M1 Telegram display/repair `11/11 PASS`；MR1 使用刚合并的共享 registry 挂载测试 `2/2 PASS`，其中 `3343` 真实 resolver render 为“彭布罗克”；M1 formatter 隔离渲染输出中文球队/方向，未改 price/line/selection 原始字段。M1 formal ledger 按冻结 team ID 检查没有 team ID 3343 的历史 Pick，因此无需针对该名编辑旧消息；本轮没有实际发送或编辑任何 TG，也没有触发生产策略。
- 仅共享 display data/curator/test 和本 handoff 变化；模型、阈值、scope、Crown、交易账本、settlement、Telegram 内容/发送规则和 scheduler 均未修改。名称新增1；历史 Telegram 编辑数0（该 team ID 无对应历史单）。

## 2026-10-15 unresolved 公开中文页面续查（第109批）
- 共享库最新仍为 `ff1aeba465d40af963fa58eebb17e42642fa633a`：正式 2,468 IDs、2,336 canonical、132 unresolved（94.65%）。本轮没有 registry 更改。
- 将 Reep 开放实体表按正式未匹配 provider 英文名作精确归一化连接，找到42条与 Reep 实体一致的 formal identity，其中包含 Wikidata QID；批量查验这些 QID 的中文 labels、aliases 和 zhwiki sitelink，中文证据为0。Reep 的英文 ID crosswalk 有助实体身份复核，但本身不提供这些队伍的 canonical 中文名。
- 再核查 Sofascore 简中/多语页面与搜索索引，包括 Sirens FC、Qena SC、Dikernis SC、Karcagi SE、ASIL Lysis、KF Rahoveci、FC Yerevan。可核验页面展示仍以英文俱乐部名为主；未发现可用简体中文 canonical。对 ASIL Lysis 的希腊/阿拉伯等语种转写不自行转换为中文，不用机器翻译补名。Pembroke Athleta 是上一批已根据其中文页成功新增的唯一名称。
- 因无新增可靠中文证据，本批新增0；未改模型、scope、ledger、Telegram 或 settlement。现有 M1/MR1 resolver/formatter 检验仍分别为 M1 11/11、MR1 mounted shared registry 2/2、MR1 AI forward 3/3 PASS（均为本地）；没有 TG 发送或编辑。完整132项依然由共享 `formal_scope_coverage.json#unresolved_records` 跟踪。

## 2026-10-15 正式范围中文名核验（第110批）
- 以合并后的共享 master `ff1aeba465d40af963fa58eebb17e42642fa633a` 为基线重新核对；正式范围仍为 2,468 个 ID、2,336 canonical、132 unresolved（94.65%）。分项：M1 1,551/1,553（99.87%），M1 OU-R1 52/52（100%），MR1 AH 1,816/1,921（94.53%），MR1 AI declared mirror 1,551/1,553（99.87%）。未匹配完整明细由 `data/football_display_names/formal_scope_coverage.json#unresolved_records` 提供。
- 本轮对 7M、500彩票网、雷速、Tips.GG、Sofascore 中文页及埃及中文比分记录做了针对性公开检索。唯一看似有中文的 Malta Sirens 页面把 `Sirens` 自动译成普通词“警报”，不符合球队惯用名标准；JQ007 的埃及对阵页反而将 `El Raja Marsa` 原样保留为英文，未作为中文名证据。其余命中没有形成精确 team ID + 英文身份 + 可核验简体队名的可靠交叉记录。因此新增 canonical 为 0，未改共享库，也没有虚构译名。
- 展示回归：M1 `test_m1_telegram_display.py` 与 `test_m1_telegram_display_repair.py` 共 11/11 PASS。MR1 通过 `FOOTBALL_DISPLAY_REGISTRY_DIR` 挂载该共享 master 的 `test-football-display-names.js` 为 2/2 PASS，确认 MR1 可读同一 canonical registry 且不触碰策略字段。另将非纯展示的 `test-v6-ah-display-repair-v5.js` 一并执行时出现 1 项既有 fixture 断言不符（期望 0、实际 1）；单独共享 resolver/显示测试通过，本轮未改 MR1 文件。
- 本轮没有正式 TG 发送或历史消息编辑，历史编辑成功数保持 0。已经存在的修复回执不可据本地 formatter 测试推断为 Telegram 编辑成功；需逐条使用原账本 provider message ID 并获得 Telegram API 成功回执。当前 blocker 仍是缺少 132 个球队的可信简体中文标准名来源（其中 team ID 4931 的 provider identity 是无效字面值 `0`），以及历史消息编辑需由既有授权运行链执行。策略、赛事范围、盘口、订单、账本、结算和通知规则均未修改。

## 2026-10-15 正式范围中文名续补与 Telegram 回执（第111批）
- 从共享仓库最新 master 继续；PR [#27](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/27) 已合并，提交 `81782bd80a080fcedc721e0cc6d06e4df6dfe080`。为 TotalCorner `team_id 48448`（`FK Kabel Novi Sad`）新增 canonical `卡贝尔`；Baidu 简体诺维萨德词条明确列出“卡贝尔队（FK Kabel）”，Tips.Dog 简体球队档案另列“卡比勒”，官方俱乐部站核对 Novi Sad 身份。映射限于该 team ID，别名保留两种中文写法；来源及核验说明进入唯一共享 `display_names.json`。M1 formal ledger 中没有此 ID 的历史 Pick。
- 重新生成后的正式范围为2,468个 ID、2,358个 canonical、110个 unresolved（95.54%）：M1 1,540/1,553（99.16%）；M1 OU-R1 52/52（100%）；MR1 AH 1,838/1,921（95.68%）；MR1 AI declared mirror of M1 1,540/1,553（99.16%）。MR1 AI observed confidence≥50 cohort 为181/182（99.45%）。完整 unresolved 名单、ID、赛事上下文和原因只保存在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`；不以机器音译补齐。
- 验证：`python3 -m unittest test_m1_telegram_display.py test_m1_telegram_display_repair.py` 14/14 PASS；`git diff --check` PASS。M1 formatter 新回归用例按 team ID 将 FK Kabel 解析为“卡贝尔”，方向随中文队名；未触及模型字段。MR1 挂载共享 registry 的 `test-football-display-names.js` 2/2 PASS，额外按真实 ID 48448 隔离渲染为“塞尔维亚甲级联赛 卡贝尔 vs FK Radnicki Novi Beograd”；MR1 AI `test-v7-ai-picks-telegram.js` 3/3 PASS。均未改 MR1 源码。
- 合并后串行运行三个既有 name-only 历史修复工作流，均只尝试编辑账本原 provider message ID，不重发：M1 run [38661914201](https://github.com/ljm198964-alt/quant-runner/actions/runs/38661914201) PASS，41条已匹配、0需编辑、99条缺原发送文本、100条无可用映射、0失败；该修复程序遍历 M1 formal notifications，M1 OU-R1 在此共享 M1 显示链内。MR1 AH run [38662204237](https://github.com/ljm198964-alt/quant-runner/actions/runs/38662204237) PASS，125条已处理、0需编辑、0未解析、0失败。MR1 AI run [38662311395](https://github.com/ljm198964-alt/quant-runner/actions/runs/38662311395) workflow PASS，但实际编辑0：9条旧 message ID 均收到 Telegram `400 message to edit not found`，另192条 unresolved。没有重发任何历史 Pick，也没有发送测试消息；本轮 Telegram 实际编辑成功数为0。
- 已完成的生产链接检查仅证明当前共享中文 registry 和现存编辑器可运行；不宣称所有正式消息已经中文。未来消息的 M1、M1 OU-R1、MR1 AH、MR1 AI 继续使用同一 canonical registry；剩余110个无可靠译名的 ID 仍可能按原 fallback 显示英文。模型、策略、赔率、比赛范围、Pick、结算、发送规则均未修改。

## 2026-10-15 正式范围中文名继续补齐（第112批）
- 延续共享 `master`。PR [#28](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/28) 合并提交 `1bd0ab5815105a633253a8d91a3fe909bfae16cb`，新增 TotalCorner `team_id 65036 FC Hoyvik → 霍伊维克FC`；Sofascore 简中球员资料使用该俱乐部中文名，并以 Sofascore 精确英文球队档案的 Faroe Islands 1. Deild 身份与 TotalCorner league_id 10635 交叉核验。PR [#29](https://github.com/ljm198964-alt/totalcorner-research-bridge/pull/29) 合并提交 `2b76721aaa408e38b6578e1476dc3ba6e164d9b5`，新增 `team_id 43875 KF Kika → KF Kika队`；Tips.GG 简中球队档案明确显示该名称并标注科索沃，和 TotalCorner Kosovo Division 1 / league_id 10808 一致。两项均只写入各自 ID，不做音译或身份合并。
- 最新共享 master 为 `2b76721aaa408e38b6578e1476dc3ba6e164d9b5`。正式范围2,468 IDs：2,360 canonical、108 unresolved（95.62%）。M1 1,541/1,553（99.23%）；M1 OU-R1 52/52（100%）；MR1 AH 1,840/1,921（95.78%）；MR1 AI declared mirror of M1 1,541/1,553（99.23%）；MR1 AI observed confidence≥50 cohort 181/182（99.45%）。完整 unresolved 名单及逐项原因仍只在共享 `data/football_display_names/formal_scope_coverage.json#unresolved_records`。
- 展示回归：M1 formatter/history repair 16/16 PASS；MR1 mounted shared-registry + MR1 AI formatter 5/5 PASS。隔离解析分别确认 team ID 65036 输出“法罗群岛足球甲级联赛 霍伊维克FC vs …”，team ID 43875 输出“科索沃甲级联赛 KF Kika队 vs …”。M1 formal ledger 未找到这两个 ID 的已发送 Pick；MR1 V6 formal、MR1 AI sent ledger / prospective ledger 搜索也未找到对应记录，故本批没有历史 TG 待编辑项，不重跑编辑器。未来消息将由既有共享 registry 自动解析。
- 本批只改共享展示数据、curator、coverage 和测试；历史 Telegram 实际编辑0，未重发任何消息。策略、盘口、赛事范围、订单、结算及通知规则均未修改。其余108个缺乏可核验简体中文名称的队继续 unresolved，不用机器音译凑覆盖率。

## 2026-10-15 正式范围余项来源复核（第113批）
- 以共享 master `2b76721aaa408e38b6578e1476dc3ba6e164d9b5` 的108项 unresolved 为对象继续定向搜索。Tips.GG 简中 `KF Vjosa` 球队页虽然带中文界面，但标题和正文仍保留官方拉丁名；Sofascore 简中 `Al Masry Salloum` 页面亦保留英文队名；Sofascore/LiveScore 的 `Proleter 023` 页面保留英文品牌；其余被查的埃及低级别队、马其顿/塞尔维亚队仅找到外文身份或联赛记录。均不足以形成可信简体 canonical，因此新增0、正式未匹配维持108。
- 本批检查没有修改共享 JSON、formatter、策略或账本，也未触发 Telegram 编辑/发送。完整候选和未匹配原因仍以共享 `formal_scope_coverage.json#unresolved_records` 为准；后续继续按正式 team ID 和比赛级身份核对，不把地点转写或机器翻译当中文来源。
