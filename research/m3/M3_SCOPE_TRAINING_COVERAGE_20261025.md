# M3 研究范围覆盖与现有训练数据调查（2026-10-25）

本文件仅为只读事实调查。未修改 M3 正式模型或 TG。

- 已从 M1 生产 `m1_runtime_policy.py` 和 MR1 AH 生产 `config/validation-spec.json` 恢复赛事范围，并在公开 M3 账本中写入同一来源规则的逐场对照，提交 e1a845b。
- 最新 M3 全量 TotalCorner 扫描 #40200056050：两日赛事 2,183 场，研究范围为 M1 或 MR1 AH 的赛事 303 场（两者共有165、仅M1 38、仅MR1 100），其中赛前至少90分钟的 83 场，涉及 47 个联赛。不能把83算作已有预测。
- 83场中频次最多的联赛：Norway Eliteserien 5、France Ligue 1 5、Argentina Liga Profesional 5、Portugal Primeira Liga 4、Norway Division 1 4、Colombia Primera A 4、Mexico Liga MX 4、Greece Super League 1 3。
- 发现 M1 已有正式联赛历史缓存目录 `data/m1_history_cache/<league_id>.json`（位于现有 M1 生产依赖仓库 totalcorner-research-bridge）。英超联赛ID 1的缓存于2026-10-25 14:27 UTC更新，包含1830条赛事，其中1757条 status=full，且具有联赛ID、主客球队ID、赛时、进球数，可成为M3补充训练的候选。仅检查了这一联赛文件，不能推定其余46联赛缓存完备。
- 复用缓存必须核查比分确为终场、开赛时区与严格训练截止、赛前球队ID对应及保存权限。不应把M1已存未来比赛或进行中比分当作历史训练。新数据训练线应与现有 OpenFootball Poisson／Dixon–Coles／Bivariate Poisson 基准身份独立。保持 M3 当前 TotalCorner 默认亚洲盘研究设置、不发正式TG。
- 本轮开始编写新的按TotalCorner联赛ID/球队ID训练 M3 模型适配器，但未提交、未运行生产；私有仓库接线工具调用受限。勿声明多联赛新模型已上线。下一步先处理这个阻塞、审核适配器并执行真实生产扫描与落账。
