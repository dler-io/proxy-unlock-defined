# proxy-unlock-defined

按服务统一维护 proxy-unlock 域名规则，节点通过 `defined.<服务>.url` 引用清单，通过 `region` 选择本机出口

清单源于 2026-09-29 清理后的规则：114 个服务或合集、559 个唯一域名模式，其中 110 个普通服务、2 个待核查合集、2 个已知停运服务历史合集；导入状态不代表已验证当前解锁或播放能力

[完整服务目录](docs/catalog.md) · [维护与迁移说明](docs/maintenance.md)

目录用途：

- `services/`：按服务去重的域名清单，保留 Netflix、Disney、AI 服务键
- `review/`：共享域名和原 Other/Reads 中未确认归属的条目，须明确归属和出口后启用
- `legacy/`：已知停运的 GYAO、Funimation 历史条目，默认不启用
- `parts/`：需要分开选区或仅加载部分范围的服务子清单，域名在此维护
- `subsets/`：由多个子清单自动组合的清单，不手工编辑
- `catalog.json`：稳定的服务 ID、文件路径和状态
- `policy/`：已删除条目记录，以及允许的更具体子域覆盖
- `scripts/`：离线校验和配置片段生成器，使用 Python 3.10+ 标准库

清单每行一个模式：

```text
# 域名本身和所有层级子域名
+.netflix.com
# 仅此主机
api.example.com
```

仓库统一使用精确域名与 `+.` 后缀模式；不接受 USER-AGENT、DOMAIN-KEYWORD 等规则类型

接入示例：

```yaml
proxy-unlock:
  rule-interval: 600
  defined:
    Netflix:
      url: https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/services/Netflix.list
      region: SG
    Disney:
      url: https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/services/Disney.list
      region: SG
    AI:
      url: https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/services/AI.list
      region: AI
```

这是一段配置片段，合并到现有 `proxy-unlock` 节点下，保留该节点已有的 `rules` 出口定义；`region: SG` 和 `region: AI` 分别要求本机有同名 `match`，不存在时可能回退直连

也可生成配置片段：

```bash
python3 scripts/render.py --service Netflix=SG --service Disney=SG --service AI=AI
```

默认 URL 跟随 `main`；灰度接入或需要固定版本时，增加 `--ref <commit-sha>`，确认后再切回 `main` 自动更新

同一服务中不同域名需要固定使用不同出口时，可以引用互不重复的子清单，例如：

```bash
python3 scripts/render.py --service CanalPlus_MyCanal=DE --service CanalPlus_Core=FR
```

输出示例见 [examples/subsets.yml](examples/subsets.yml)，可用子清单见 [子清单目录](docs/subsets.md)；`region` 既可指定单个出口，也可指定已有的代理组

已有完整服务 URL 保持可用，选择完整清单或所需子清单即可；同一配置不要同时加载完整清单与其子清单

更新规则时，普通服务修改对应文件；已拆分的服务只修改 `parts/`，再生成完整清单和组合清单：

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

校验脚本会检查非法域名、重复归属、根域与 `+.` 的同义冲突、未经登记的跨服务子域重叠、已删除名称重新引入，以及生成清单是否同步；GitHub Actions 另检查配置示例，校验通过不等于出口已解锁

共享规则说明：

- 同一个精确或后缀匹配模式只在一份源清单中维护，完整清单与组合清单由脚本生成
- `+.google.com` 与 AI 的具体子域、BBC 与 BritBox 等更具体覆盖保留，逐项记录于 `policy/overlaps.json`
- `theplatform.com`、`go-mpulse.net` 从原重复业务中抽出放入 `review/Shared.list`，不自动选择地区
- AI 保留为现有业务合集，其中共享登录、验证码、支付和 API 主机仍会影响同主机上的其他请求

服务规则中没有服务器地址、端口、账号、密码或节点配置；出口和用户选区由部署端维护
