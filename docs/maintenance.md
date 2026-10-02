**维护与迁移**

服务 ID 是节点配置及用户选区的稳定键，例如 Netflix、Disney、AI；新增服务可以增加 ID，重命名已有 ID 时需要同步面板和节点，不能仅改文件名

清单按服务划分，出口不写进清单；VideoMarket、Molotov 已从多个地区段提取为各自唯一清单，具体使用 JP、JP_S 或 FR 等出口由节点显式配置

初次导入保留清理后全部 559 个唯一模式，不把共享与归属不明的条目伪装成单一业务：`review/Shared.list` 有 2 个共享平台模式，`review/Unclassified.list` 有 25 个未分类模式；两份文件及其子清单均需要显式 `--include-review` 才能被配置生成器引用

8 个服务或合集已拆分为 19 份源子清单，分别维护于 `parts/<服务>/`；`catalog.json` 的 `parts` 声明完整清单由哪些源组成，`subsets` 声明需要额外组合的子集

维护拆分服务时只修改源子清单，再运行 `python3 scripts/build.py`，提交源文件和生成结果；完整服务 URL 保持原样，`scripts/check.py` 会拒绝过期的生成文件、子清单间重复规则及父子域名范围重叠，避免分别绑定出口时意外覆盖

多出口不要求在节点内联维护域名：完整服务使用多个候选出口时，`region` 指向本机代理组；不同域名必须固定走不同出口时，为各个子清单分别设置 `url + region`，示例和完整路径见 [子清单目录](subsets.md)

子清单名称表达域名分组，不规定出口地区；节点可保留现有服务键，仅替换其 URL，避免改变用户选区键

GYAO 和 Funimation 共 3 个模式放入 `legacy/`，依据 [Yahoo 官方说明](https://support.yahoo-net.jp/SccGyao/s/) 和 [Crunchyroll 官方说明](https://help.crunchyroll.com/hc/en-us/articles/22843839604500-Funimation-End-of-Services)；其他迁入服务的状态为 `imported`，不作为现时可用性证明

迁移步骤：

1. 选择要迁移的服务，确认节点上相应出口存在且能实际连接
2. 将清单 URL 和 `region` 加入现有 `defined`，保留现有 `rules` 出口定义
3. 从旧的地区段删除已经迁移的相同域名，避免服务间重复；不要把新的 Molotov 等服务与旧 DE/FR 大列表重叠加载
4. 对原来应在某节点直连的服务，可继续不在该节点定义它；不要为了清单齐全而强行绑定代理
5. 验证首轮下载与 `/config/unlock` 运行时状态，再验证目标域名的真实出口与业务访问
6. 完成灰度验证后扩展到其他节点

在此配置方式下，远程 URL 和内联 `domain` / `ip-cidr` 会相加合并，不是覆盖；迁移后若保留旧内联列表，远程删除域名也不能让旧条目消失

远程刷新失败会保留已有快照；首次启动若无缓存且源不可达，不能假定远程规则已经生效；一次刷新中某个源失败会让该次快照更新整体失败，因此待核查服务应按需启用

同一后缀下允许更具体的业务子域覆盖，但必须在 `policy/overlaps.json` 精确列出双方服务与模式并说明原因；相同模式不得用例外名单绕过重复归属校验

更新规则后执行 `python3 scripts/build.py`、`python3 scripts/check.py`，再运行测试；不在 CI 中自动根据一次 DNS 查询删规则，DNS 健康和实际业务播放应单独验证

`policy/removed-domains.txt` 当前保留 41 个已确认删除且尚未恢复的 NXDOMAIN 名称，阻止维护时误加回同名规则；它不阻止已存在的父域后缀覆盖，也不是运行时拒绝连接列表；确需恢复时应先复核并同步更新记录

2026-10-02 更新：AI 清单按 [SKK Apple Intelligence](https://github.com/SukkaW/Surge/blob/master/Source/non_ip/apple_intelligence.conf) 补齐 4 个 Siri / Apple Relay 精确域名，并按 [Cursor 登录域名说明](https://cursor.com/help/troubleshooting/sign-in-domains) 恢复 `accounts.spacex.ai`；该域名在 2026-09-29 清理时为 NXDOMAIN，本次通过 Google 和 Cloudflare DNS 复核后从删除记录中移除，AI 清单增至 121 条，全目录增至 564 条

给服务增加条目时保持小写、逐行排序；同服务已经有 `+.example.com` 时不再重复写 `example.com`；明确主机使用精确匹配，服务专属域名按需使用 `+.`，避免扩大到整个共享 CDN

新仓库已提供稳定清单地址，但创建仓库不会自动替换既有节点配置或热重载线上服务
