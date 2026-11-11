# Gemini 防火墙清单核对

以下对照 Google 的 Gemini 防火墙主机清单与本仓库的分流规则，核对范围以 2026-10-28 的官方清单为准。防火墙清单用于确认网络可达性，分流清单用于选择匹配范围，两者用途不同。[Google 官方主机清单](https://knowledge.workspace.google.com/admin/generative-ai/gemini-app/gemini-app-firewall-settings)

- 普通 Gemini 网页、分享和 App 唤起由 [Google 服务清单](../services/Google.list)覆盖
- Chrome 内置 Gemini 使用 `gemini.google.com/glic`，资格状态接口由 `+.googleapis.com` 覆盖。Chrome DevTools 的 `aida.googleapis.com` 也由 Google 清单的 `+.googleapis.com` 覆盖。[Chromium 配置](https://chromium.googlesource.com/chromium/src/+/HEAD/chrome/common/chrome_features.cc)
- 自 2026-11-11 起，Google 旗下服务统一归入 [Google 服务清单](../services/Google.list)：包括 Gemini 网页与企业版、AI Studio、Gemini API、Antigravity / Code Assist、NotebookLM、Jules、Opal、DeepMind、Labs 和 DevTools。原 AI 清单的 48 条有效规则迁出，其中 36 条由 Google 清单已有父域覆盖，另外 12 条作为独立域名保留
- `business.gemini.google` 及认证子域由 `+.gemini.google` 覆盖；产品专用的 `google.com` 与 `googleapis.com` 子域由对应父域覆盖。清理 AI 清单中原先注释的网页与共享接口条目，共享 CSP 主机 `csp.withgoogle.com` 不恢复收录
- 迁移后需加载 Google 清单并配置适合目标产品的出口；仅加载 AI 清单不再涵盖这些产品。归属调整不改变产品地区或账号资格要求；独立 [WARP 清单](../warp-google/README.md)保留原 Google 搜索、YouTube 入口和 Gemini 业务范围；视频 CDN 范围由独立的 [YouTube 清单](../warp-youtube/README.md)维护，并由面板的「YouTube 后台播放兼容」账户设置控制；`redirector.googlevideo.com` 仍保留在 Google 清单中
- 原 WARP 清单中的地区搜索域名、`auth.cloud.google`、`notebooklm.cloud.google`、`payments.cloud.google`、`vertexaisearch.cloud.google` 和交互预览域 `+.scf.usercontent.goog` 同步迁入 Google 清单，让 Google 服务清单也覆盖这些既有业务入口；交互预览不按静态 CDN 排除
- 图片、字体、内容托管及其他共享依赖可沿用使用端的通用分流，广告与统计主机的可达性取决于使用端的策略

| 官方主机 | 当前处理 |
|---|---|
| `lh5.googleusercontent.com` | 共享静态资源，沿用通用分流 |
| `www.googleapis.com` | 由 Google 清单覆盖 |
| `ssl.gstatic.com` | 共享静态资源，沿用通用分流 |
| `fonts.googleapis.com` | 共享字体接口，由 Google 清单覆盖 |
| `play.google.com` | 由 Google 清单覆盖 |
| `ogs.google.com` | 由 Google 清单覆盖 |
| `www.google.com` | 由 Google 清单覆盖 |
| `apis.google.com` | 由 Google 清单覆盖 |
| `jnn-pa.googleapis.com` | 由 Google 清单覆盖 |
| `waa-pa.clients6.google.com` | 由 Google 清单覆盖 |
| `i.ytimg.com` | YouTube 缩略图，沿用通用分流 |
| `yt3.ggpht.com` | 共享图片，沿用通用分流 |
| `lh3.googleusercontent.com` | 共享静态资源，沿用通用分流 |
| `maps.gstatic.com` | 共享静态资源，沿用通用分流 |
| `lh3.google.com` | 共享内容接口，由 Google 清单覆盖 |
| `ogads-pa.clients6.google.com` | 广告或统计主机，由 Google 清单覆盖 |
| `csp.withgoogle.com` | 共享 CSP 依赖，沿用通用分流 |
| `www.googletagmanager.com` | 广告或统计主机，由使用端处理 |
| `www.youtube.com` | 由 Google 清单覆盖 |
| `fonts.gstatic.com` | 共享静态资源，沿用通用分流 |
| `maps.googleapis.com` | 由 Google 清单覆盖 |
| `static.doubleclick.net` | 广告或统计主机，由使用端处理 |
| `www.gstatic.com` | 共享静态资源，沿用通用分流 |
| `gemini.google.com` | 由 Google 清单覆盖 |
| `td.doubleclick.net` | 广告或统计主机，由使用端处理 |
| `googleads.g.doubleclick.net` | 广告或统计主机，由使用端处理 |
| `www.google-analytics.com` | 广告或统计主机，由使用端处理 |
| `optimizationguide-pa.googleapis.com` | 由 Google 清单覆盖 |
| `encrypted-tbn0.gstatic.com` | 共享静态资源，沿用通用分流 |
| `encrypted-tbn1.gstatic.com` | 共享静态资源，沿用通用分流 |
| `encrypted-tbn2.gstatic.com` | 共享静态资源，沿用通用分流 |
| `encrypted-tbn3.gstatic.com` | 共享静态资源，沿用通用分流 |
| `streetviewpixels-pa.googleapis.com` | 由 Google 清单覆盖 |
| `content-autofill.googleapis.com` | 由 Google 清单覆盖 |

清单覆盖仅表示域名可被匹配。若同时加载多份清单，应验证重叠规则的实际出口，并分别检查账号登录和所需功能
