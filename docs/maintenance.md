# 规则维护指南

## 修改清单

- 在 [`catalog.json`](../catalog.json) 中登记服务 ID、路径和状态。服务 ID 和清单路径用于配置引用，修改已有条目时需考虑兼容性
- 普通服务直接修改 `services/` 中的清单。已拆分的服务在 `parts/` 修改源文件，再运行 `python3 scripts/build.py` 生成完整清单和组合清单
- 域名使用小写，每行一条，按字典序排列。已知只需匹配一个主机时使用精确模式。确认整个域及子域均属于目标范围后，再使用 `+.` 后缀规则
- 共享平台或归属待确认的条目放入 `review/`，停运服务的存档放入 `legacy/`。生成这两类条目的配置时须显式指定 `--include-review`
- 更新 [服务目录](catalog.md)或[子清单目录](subsets.md)中受影响的行。Google 搜索、YouTube 和 Gemini 的独立清单在 [`warp-google/`](../warp-google/) 单独维护，YouTube 视频域名在 [`warp-youtube/`](../warp-youtube/) 单独维护

## 匹配范围

同一个匹配模式应只有一个来源。父域与其他服务的具体子域有意重叠时，在 [`policy/overlaps.json`](../policy/overlaps.json) 记录双方服务、模式和理由，并确认使用端会按预期处理。Google 旗下服务统一归入 Google 清单，已被 `+.google.com`、`+.googleapis.com` 或 `+.gemini.google` 覆盖的子域不再单独列出

规则按域名匹配，同一主机上的不同 URL 路径会命中同一条规则。共享登录、API 和 CDN 域名应按实际用途控制范围。服务的防火墙放行清单可以用于核对依赖，是否为某个依赖指定出口需单独判断

[`policy/removed-domains.txt`](../policy/removed-domains.txt) 记录已移除的域名，校验器会拒绝重新加入同名条目。确需恢复时，复核用途与解析结果后同步更新该文件

## 规则来源

- Gemini 的入口、共享依赖和企业版规则见 [Gemini 防火墙清单核对](gemini-firewall-audit.md)，其他 AI 服务的地区依据见 [AI 服务香港可用范围复核](ai-hong-kong-audit.md)
- Antigravity 企业版的 `businessaicode`、`aiplatform` 和 `discoveryengine` 精确主机来自 [官方网络清单](https://antigravity.google/docs/enterprise#network-allowlists-and-mtls-endpoints)。部分 API 与其他 Google Cloud 产品共享主机
- Disney+ 的登录、内容和播放主机参照 [官方登录页](https://www.disneyplus.com/identity/login)及 [Web SDK 配置](https://client-sdk-configs.bamgrid.com/bam-sdk/v7.0/disney-svod-3d9324fc/browser/v35.6/windows/chrome/prod.json)。共享身份主机上的其他登录请求也会命中
- 存档状态依据 [GYAO 公告](https://support.yahoo-net.jp/SccGyao/s/)和 [Funimation 停运说明](https://help.crunchyroll.com/hc/en-us/articles/22843839604500-Funimation-End-of-Services)

## 验证

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

GitHub Actions 还会核对生成的 YAML 与 [`examples/`](../examples/) 是否一致。接入新清单时，在使用端验证下载和命中，再验证实际出口和所需功能
