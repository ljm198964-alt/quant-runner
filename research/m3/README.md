# M3 独立 AH / OU 研究

M3 是独立研究模型，不读取 M1、M2、MR1 的预测、订单、参数或账本。当前流程不产生正式交易信号、不发 Telegram、不自动提升模型，也没有增加交易 Gate。

## 研究入口与结果

- [完整研究验收报告](M3_RESEARCH_REPORT.md)
- [最新 penaltyblog OOS 报告](results/latest_penaltyblog_oos_report.json)
- [最新时间切分清单](results/latest_penaltyblog_oos_splits.json)
- [最新 V4 原版指标](results/latest_v4_original_metrics.csv)
- 历史报告、预测 CSV 与参数快照在 `results/history/`、`results/predictions/`、`results/model_parameters/`。

GitHub Actions 工作流 `.github/workflows/m3-independent-research.yml` 保持每 4 小时 UTC 运行，下载开源 Football Predictor V4 数据，按原项目流程执行 OU 模型，并对 penaltyblog 的 Poisson、Dixon-Coles、Bivariate Poisson 执行严格赛季前推 AH / OU 评估。每次运行记录输入文件 SHA-256、来源 commit、模型参数、预测文件哈希、时间切分、分数与前次报告比较；输入哈希相同会明确记录没有新增数据变化。

## 重要口径

Football-Data.co.uk 历史赛果仅提供日期（无精确开赛时间），训练集排除测试赛季首场比赛所在的整个 UTC 日期；训练仅使用更早赛季文件且比赛日期严格早于测试截止。该数据源文件中的赔率列不会被 penaltyblog 流程读取。未知训练球队不生成伪预测，而记录为未覆盖。

penaltyblog 目前的 AH 评价为 AH 0.0（主队 DNB）三状态概率；OU 评价为固定 O2.5。由于当前没有 Crown 的同期有效盘线和双边水位，二者只是模型概率诊断，不是具体 Crown 下注结果，ROI、收益和回撤均为空。其他来源的赔率不能代替 Crown。

Football Predictor V4 的 ROI 列只还原其上游研究阈值和原数据赔率，不能称作 Crown ROI，也不能作为 M3 正式交易规则。该上游仓库当前检出版本未发现显式许可证文件；M3 不复制其源代码，工作流按原项目入口运行，并将许可限制记录在报告中。

运行单元测试：

```bash
python -m unittest discover -s research/m3 -p 'test_*.py' -v
```
