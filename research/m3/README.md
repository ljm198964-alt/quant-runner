# M3 — 独立足球 AH / OU 研究

M3 是新的独立模型身份，**不是 M1/M2/MR1 的子模块**。此目录不读取这些模型的扫描、信号、账本或 Telegram；不从它们的结果推算 M3 交易战绩。

## 已确认范围
- 同一 M3 研究工程，分别输出亚洲让球 AH 与亚洲大小球 OU 概率和亚洲盘五状态期望回报。
- 研究候选开源软件：`martineastwood/penaltyblog`（进球分布，MIT）；`pkotengpoku/football-predictor`（LightGBM，大/小2.5，后续研究与许可复核）。
- 正式盘口来源继续严格遵循用户指定的 Crown。其他来源可用于历史比赛/球队特征研究，不能替代 Crown 下单盘口。
- **当前仅研究**。不存在已经获批的 M3 TG 发单、正式订单、策略 Gate、数量要求、时效门槛或发布条件。
- M1 OU 暂停、M1 AH 和 MR1 AH 的生产逻辑不受影响。

## 数据与模型独立性
M3 使用自己的历史比赛文件（`research/m3/data/`）和独立结果（`research/m3/results/`）。这些目录不自动填入 M1/MR1/M2 原账本数据。模型训练数据必须在赛前可得；日期、球队身份及官方 FT 证据要可追溯。

`python -m research.m3.probabilities --input <M3_JSON> --output <M3_JSON>` 支持独立模型给出的主客期望进球 `lambda_home`、`lambda_away`，计算 AH/OU 各盘口的五状态概率与给定 Crown 双边水位的期望回报。输入中的 lambda 在当前阶段来自外部 M3 模型推断，**不是本工具已经训练得到的概率模型**。这套通用结算计算器仅是两套开源模型之后的共同评价接口。

输入：
```json
{"fixture_id":"demo","lambda_home":1.5,"lambda_away":1.1,
 "ah":{"home_line":-0.25,"home_decimal":1.95,"away_decimal":1.95},
 "ou":{"total_line":2.5,"over_decimal":1.95,"under_decimal":1.95}}
```
示例仅用于接口验证，并非真实 Crown 报价。程序不读取其他模型目录、不请求盘口、不发送消息。

## 下一阶段
在独立 M3 输入中接入 penaltyblog 的训练/预测 API 和 LightGBM 的时间前推数据管道，核对开源库的具体版本、许可证、训练日志及 M3 独立样本外表现。使用有证据的 Crown 同期快照评价，不凭模拟输入声称盈利。
