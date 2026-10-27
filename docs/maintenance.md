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
2. 将清单 URL 和 `region` 合并到 `proxy-unlock.rules.<服务>`，保留现有 `nodes` / `groups` 出口定义和其他服务规则
3. 从旧的地区段删除已经迁移的相同域名，避免服务间重复；不要把新的 Molotov 等服务与旧 DE/FR 大列表重叠加载
4. 对原来应在某节点直连的服务，可继续不在该节点定义它；不要为了清单齐全而强行绑定代理
5. 验证首轮下载与 `/config/unlock` 运行时状态，再验证目标域名的真实出口与业务访问
6. 完成灰度验证后扩展到其他节点

在此配置方式下，远程 URL 和内联 `domain` / `ip-cidr` 会相加合并，不是覆盖；迁移后若保留旧内联列表，远程删除域名也不能让旧条目消失

同一轮刷新中，成功下载的源可以独立更新，失败源保留最后有效规则，不阻止其他源发布。首次启动若某个源无缓存且不可达，该源尚未生效；可通过 `/config/unlock` 的 `source_status` 核对各源状态，待核查服务仍应按需启用

同一后缀下允许更具体的业务子域覆盖，但必须在 `policy/overlaps.json` 精确列出双方服务与模式并说明原因；相同模式不得用例外名单绕过重复归属校验

更新规则后执行 `python3 scripts/build.py`、`python3 scripts/check.py`，再运行测试；不在 CI 中自动根据一次 DNS 查询删规则，DNS 健康和实际业务播放应单独验证

`policy/removed-domains.txt` 当前保留 41 个已确认删除且尚未恢复的 NXDOMAIN 名称，阻止维护时误加回同名规则；它不阻止已存在的父域后缀覆盖，也不是运行时拒绝连接列表；确需恢复时应先复核并同步更新记录

2026-10-02 更新：AI 清单按 [SKK Apple Intelligence](https://github.com/SukkaW/Surge/blob/master/Source/non_ip/apple_intelligence.conf) 补齐 4 个 Siri / Apple Relay 精确域名，并按 [Cursor 登录域名说明](https://cursor.com/help/troubleshooting/sign-in-domains) 恢复 `accounts.spacex.ai`；该域名在 2026-09-29 清理时为 NXDOMAIN，本次通过 Google 和 Cloudflare DNS 复核后从删除记录中移除，AI 清单增至 121 条，全目录增至 564 条

给服务增加条目时保持小写、逐行排序；同服务已经有 `+.example.com` 时不再重复写 `example.com`；明确主机使用精确匹配，服务专属域名按需使用 `+.`，避免扩大到整个共享 CDN

2026-10-12 更新：根据 Google 官方论坛的 [Antigravity 2.8.1 客户端日志](https://discuss.ai.google.dev/t/antigravity-2-8-1-macos-sign-in-never-starts-language-server-never-generates-an-oauth-url-no-browser-is-ever-opened/178878)和[较早版本登录日志](https://discuss.ai.google.dev/t/antigravity-blocco-login-e-modelli-su-rete-con-proxy-windows-11/110782)，为 AI 补充 `daily-cloudcode-pa.googleapis.com`、`daily-cloudcode-pa.sandbox.googleapis.com` 两个精确主机，并登记其对 Google 通用后缀的覆盖关系；两者经 Google、Cloudflare DNS 复核均有 A 记录，AI 清单增至 125 条，全目录增至 568 条；日志与 DNS 结果仅证明域名使用记录和解析状态，不代表当前所有版本均使用这些接口，也不代表账号资格或模型调用已验证

新仓库已提供稳定清单地址，但创建仓库不会自动替换既有节点配置或热重载线上服务

2026-10-12 香港可用范围补充：按 [Google Labs FAQ](https://labs.google/fx/faq) 为支持名单未列香港的 Project Genie 加入精确主机 `labs.google`；这是共享入口，同主机下其他 Labs 产品路径也会使用 AI 出口，不能按域名区分各产品路径。按 [Kiro FAQ](https://kiro.dev/faq/) 和[网络清单](https://kiro.dev/docs/privacy-and-security/firewalls/) 加入 `+.kiro.dev`、`q.eu-central-1.amazonaws.com`、`q.us-east-1.amazonaws.com`；Kiro 支持香港购买套餐，但模型仍遵循供应商地区要求，[Anthropic 支持名单](https://www.anthropic.com/supported-countries)未列香港，因此保留受限模型的 AI 分流，不表示 Kiro 全站均不支持香港。AWS 接口仅匹配上述两个精确主机；AI 清单增至 129 条，全目录增至 572 条，尚未实测账号登录和模型调用

2026-10-12 AI Suite 全面补漏：根据官方资料新增 Cohere、Chrome DevTools AI assistance、TRAE 国际版的 7 个模式，并同步四种客户端格式；AI 清单增至 136 条，全目录增至 579 条。地区依据、共享域名边界、已覆盖服务和未新增候选项见 [香港可用范围复核](ai-hong-kong-audit.md)

2026-10-16 Gemini 依赖更新：按 Google 官方防火墙清单增加 19 个 AI 精确共享主机，并为 Google 清单补充 `i.ytimg.com`；AI 清单增至 155 条，全目录增至 599 条。34 个官方主机的逐项归属、共享出口影响和广告拦截限制见 [Gemini 防火墙清单核对](gemini-firewall-audit.md)

2026-10-20 Antigravity 企业版：依据 [Google 官方网络清单](https://antigravity.google/docs/enterprise#network-allowlists-and-mtls-endpoints)，新增 `businessaicode`、`aiplatform`、`discoveryengine` 三组共 14 个精确主机，覆盖全球、美国、欧洲及官方列出的 mTLS 接口；加上原有 `cloudcode-pa.googleapis.com`，完整覆盖表中 15 个主机。AI 清单增至 169 条，全目录增至 613 条，62 处跨服务后缀重叠已登记。共享 API 主机上的其他 Google Cloud 业务也会使用 AI 出口；该清单不证明香港可用性或账号资格。官方要求这些端点 TCP 443 可达；企业使用 PSC、私有 DNS 或 VPC Service Controls 时仍需保留其私网路由，域名分流清单不代替企业网络配置。未验证企业账号登录、模型调用或线上节点刷新

2026-10-22 Muse from Meta：根据 [Meta 官方公告](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)补充 `+.muse.ai`，同步四种客户端格式；`api.meta.ai`、`dev.meta.ai` 已由 `+.meta.ai` 覆盖，不重复新增精确条目。检查 AI 清单未发现重复模式或同清单内被父域覆盖的冗余项；AI 清单为 170 条，全目录为 614 条，跨服务分流覆盖关系保持不变。公告说明发布时面向美国推出，不等同于已验证当前账号资格或完整业务访问

2026-10-23 xAI / Grok：按 [Cursor 官方登录域名说明](https://cursor.com/help/troubleshooting/sign-in-domains)，与 Rules 的 AI Suite 同步增加 `+.x.ai`、`+.grok.com`、`+.grokusercontent.com`、`+.grokipedia.com`；删除已被这些后缀覆盖的 `accounts.x.ai` 和 4 个 `auth.*` 精确条目，保留 `accounts.spacex.ai` 精确匹配。Grok 服务及共享登录使用 AI 出口；AI 清单为 169 条，全目录为 613 条，跨服务分流覆盖关系保持不变

2026-10-24 共享静态资源清理：从 AI 清单和四种客户端格式移除 11 个 Google 共享字体、图片和静态 CDN 精确主机，恢复通用分流，名单见 [Gemini 防火墙清单核对](gemini-firewall-audit.md)；受限 AI 服务入口、模型、登录及企业接口保持不变，Google 清单、dler-server 和节点配置不变。同步删除 11 条对应的覆盖记录；AI 清单为 158 条，全目录为 602 条，保留 51 处跨服务后缀重叠。本次只验证规则完整性，未实测业务登录、模型调用或线上节点刷新

2026-10-28 Gemini 网页 / Chrome 分流：将 13 条网页入口及共享主机的 AI 规则注释保留，企业版改用更具体的 `+.business.gemini.google`；有效 AI 条目为 146 条，全目录 590 个域名模式、40 处登记重叠。WARP 只补入 `csp.withgoogle.com` 精确规则；AI Studio、Gemini API、Antigravity、Notebook 等现有规则保持，unlock 仍优先于 WARP。变更依据和共享主机边界见 [Gemini 防火墙清单核对](gemini-firewall-audit.md)
