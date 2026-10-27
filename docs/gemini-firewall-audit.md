**Gemini 防火墙清单核对**

原始核对日期：2026-10-16；分流范围更新：2026-10-28；[Google 官方文档](https://knowledge.workspace.google.com/admin/generative-ai/gemini-app/gemini-app-firewall-settings)标注更新日期为 2026-10-22

官方列出 34 个需要在防火墙放行的主机，并说明即使管理员关闭相应服务，也应允许这些主机。本仓库维护域名分流，不能将防火墙放行要求等同于地区限制，也不能按 URL 路径识别 Gemini 请求

截至 2026-10-28，官方清单的 34 个主机均不再由 AI 专用规则接管：25 个入口或共享主机使用 Google / WARP 或通用静态资源路由，3 个视频主机保留媒体策略，6 个广告或统计主机沿用原策略；不新增共享父域后缀。Google 清单中的 `i.ytimg.com`、`+.ggpht.com` 与 `+.youtube.com` 覆盖三个视频主机，配套 Rules 的 YouTube 清单也已覆盖

2026-10-24 从 AI 移除 11 个共享字体、图片和静态 CDN 精确主机，表中逐项标明；它们仍可由 Google / Proxy 通用规则覆盖，移除 AI 规则并不代表拦截，也不保证直连。当前 dler-server 的 `warp-google` 明确排除 `gstatic.com`，其余目标是否走 WARP 取决于是否启用该功能及有无优先出口；本次未修改 dler-server、Google 清单或节点配置

2026-10-28 将剩余 11 个官方主机对应的 AI 规则注释保留，同时注释旧 Bard 入口和 `+.gemini.google`，共 13 条；不删除记录，方便恢复。Gemini 网页与 Chrome 内置入口使用 Google / WARP 路由，`csp.withgoogle.com` 补入 WARP 精确清单，其余已由 Google 父域覆盖。共享主机不能按 URL 区分产品，同主机的非 Gemini 请求也会恢复通用分流

Chrome 内置 Gemini 的 [Chromium 官方配置](https://chromium.googlesource.com/chromium/src/+/HEAD/chrome/common/chrome_features.cc) 使用 `gemini.google.com/glic`，资格状态接口为 `geminiweb-pa.googleapis.com/v1/glicStatus`，后者原本就由 `+.googleapis.com` 覆盖；Chrome DevTools 的 `aida.googleapis.com` 是另一项服务，继续保留 AI 出口

企业版保留更具体的 `+.business.gemini.google`，覆盖 `business.gemini.google` 及其认证子域；普通根域、分享和网页入口由 WARP 后缀覆盖。AI Studio、Gemini API、Antigravity、Notebook、Opal、Labs 等现有 AI 规则不变；手机端专用后端也不在本次网页 / Chrome 清理范围内

`www.google.com`、`www.googleapis.com`、`www.gstatic.com` 按用户要求移出 AI，继续由现有 Google / Proxy 通用规则覆盖

6 个广告或统计主机不加入 AI 清单，沿用已有策略。Rules 的 Clash/Surge AdBlock 包含 `doubleclick.net` 后缀，且位于 AI 规则之前；启用广告拦截时，三个 DoubleClick 主机仍可能被阻止。因此本次更新不是对 Google 全量防火墙放行要求的完整实现，不能保证所有 Gemini 功能可用；若遇到相关功能异常，应结合请求日志检查拦截策略

| 官方主机 | 当前处理 |
|---|---|
| `lh5.googleusercontent.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `www.googleapis.com` | 按用户要求移出 AI，保留通用 Google / Proxy 分流 |
| `ssl.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `fonts.googleapis.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `play.google.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `ogs.google.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `www.google.com` | 按用户要求移出 AI，保留通用 Google / Proxy 分流 |
| `apis.google.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `jnn-pa.googleapis.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `waa-pa.clients6.google.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `i.ytimg.com` | 保留 YouTube 分流；服务端 Google 新增精确规则 |
| `yt3.ggpht.com` | 保留 YouTube 分流；服务端 Google 已覆盖 |
| `lh3.googleusercontent.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `maps.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `lh3.google.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `ogads-pa.clients6.google.com` | 广告或统计共享主机，保留现有策略 |
| `csp.withgoogle.com` | 2026-10-28 注释 AI 规则，新增 WARP 精确规则 |
| `www.googletagmanager.com` | 广告或统计共享主机，保留现有策略 |
| `www.youtube.com` | 保留 YouTube 分流；服务端 Google 已覆盖 |
| `fonts.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `maps.googleapis.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `static.doubleclick.net` | 广告或统计共享主机，保留现有策略 |
| `www.gstatic.com` | 按用户要求移出 AI，保留通用 Google / Proxy 分流 |
| `gemini.google.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `td.doubleclick.net` | 广告或统计共享主机，保留现有策略 |
| `googleads.g.doubleclick.net` | 广告或统计共享主机，保留现有策略 |
| `www.google-analytics.com` | 广告或统计共享主机，保留现有策略 |
| `optimizationguide-pa.googleapis.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `encrypted-tbn0.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `encrypted-tbn1.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `encrypted-tbn2.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `encrypted-tbn3.gstatic.com` | 2026-10-24 移出 AI，共享静态资源恢复通用分流 |
| `streetviewpixels-pa.googleapis.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |
| `content-autofill.googleapis.com` | 2026-10-28 注释 AI 规则，由 Google / WARP 接管 |

本次 `services/AI.list` 生效规则从 158 条变为 146 条（注释 13 条，新增 1 条更具体的企业版规则），全目录 590 个域名模式、40 处登记重叠。服务 ID、其他受限产品规则与节点选区不变；本次仅修改服务端规则仓库，不宣称客户端静态清单已同步

验证包括构建、目录及归属检查、单元测试，以及服务端真实解析器与路由优先级验证；未执行账号登录、模型调用或线上节点刷新。清单刷新不改变已有 TCP 连接，需要重新建立连接；节点若保留旧的内联 AI 条目或另行绑定 Google 通用解锁出口，仍按 unlock 优先级处理
