# M3 三线并行核查｜2026-10-21 UTC

本记录为**现有正式研究产物的只读复算与缺口审计**，不是新增样本、成交策略、训练结果或模型升级。所有盘口交易价格仍只承认可验证的 Crown 数据。

## 1. 历史 OOS 误差研究（立即可推进）
- 使用现有 `research/m3/results/openfootball/latest_oos_stability.json`，每种模型有效评估11,254场。
- 固定OU 2.5，实际大球比例0.53874178。预测平均概率：Poisson 0.51785881，Dixon-Coles 0.51780442，Bivariate Poisson 0.51469300，分别低估 **2.0883、2.0937、2.4049个百分点**。这些是现有独立OOS诊断，不是 Crown EV。
- 相比Poisson，在league-season分块bootstrap的AH0三状态log loss差值95%区间：Dixon-Coles [-0.00047162, +0.00106992]；Bivariate [-0.00055059,+0.00083411]。两者均含零，现有样本不能证明复杂模型整体更好；禁止因此事后挑选模型、调整交易阈值或将固定2.5误差外推到任意Crown OU盘口。
- 新一轮应在**新增、未参与调参的真实未来赛果**到达后复核校准；如果源输入hash不变，本轮没有新的学习信息。

## 2. 赛程身份与Crown只读审计
- 现有 `research/m3/results/crown/latest_pairing_status.json`（2026-10-20T13:42:29Z）：M3可核验的同时期预测×Crown盘口AH=0、OU=0；未来自动采集未开启、授权范围未证明，因此EV、ROI、收益曲线与回撤为不可计算，**不是零**。
- OpenFootball前瞻数据只有无时区的日期，不等于可核验的赛前UTC kickoff。B1在该源缺失。
- 候选 `oladeeayo/open-matchday` 的 `BEL_1_pro-league` 存在当季 fixtures/results CSV，且结果的 source 标为 ESPN；但是仓库根目录LICENSE核验未找到，`time`语义不够严谨，不应加入M3或直接用来结算。须先验证原始提供方许可、fixture唯一身份、精确UTC与DST含义并保留采集时刻。
- 权限界限：已有TotalCorner Crown接口的存在不等于M3自动采集、留存和公开衍生结果得到授权。未进行新的Crown API请求。

## 3. 自动影子结算链路
- 既有 `m3-openfootball-shadow.yml` 每4小时UTC的第35分钟自动执行，并且含有后续FT匹配与append-only SETTLEMENT逻辑；无需为了制造活动而重复创建调度。
- 最新**可读取的持久化** `latest_shadow_performance.json`：generated 2026-10-20T14:00:44Z，4215条canonical预测、0条forward settlement、0条Crown市场报价。
- 源代码只对源日历日期在预测日+3天或更晚的赛程建立前瞻预测；首批2026-10-20预测最早2026-10-23，2026-10-21暂时0结算符合时间窗口。不能提前使用已有历史比分来补做伪前瞻结算。
- 如果首批赛事结束并经合法来源确认FT后仍然是0结算，应核对实际FT源更新UTC、fixture_identity_id、source日期、supersession及执行日志，以代码/数据证据定位原因；不要放宽时间规则冒充盈利。
- 影子模型只评估概率质量；未产生真实皇冠赔率前不得计算或描述Crown ROI，不给TG派单。

## 执行边界及下一次客观触发
1. 一旦确认新未来FT，先检查可匹配且此前真实记录的预测，再复算AH0/O2.5预测表现。
2. 在取得合规且时间匹配的Crown报价与精确UTC kickoff证据以前，只审计数据覆盖，不启用市场自动采集和收益计算。
3. 保持8种研究方案独立评估，M1/M2/MR1代码、账本、Telegram及用户冻结策略均不变。
