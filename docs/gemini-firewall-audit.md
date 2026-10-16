**Gemini 防火墙清单核对**

核对日期：2026-10-16；[Google 官方文档](https://knowledge.workspace.google.com/admin/generative-ai/gemini-app/gemini-app-firewall-settings)标注更新日期为 2026-10-13

官方列出 34 个需要在防火墙放行的主机，并说明即使管理员关闭相应服务，也应允许这些主机。本仓库维护域名分流，不能将防火墙放行要求等同于地区限制，也不能按 URL 路径识别 Gemini 请求

本次为 AI 增加 19 个精确主机，加上原有 3 个覆盖项，共 22 个官方主机由 AI 清单覆盖；不新增共享父域后缀。Google 清单另补 `i.ytimg.com`，现有 `+.ggpht.com` 与 `+.youtube.com` 覆盖另两个视频主机；配套 Rules 的 YouTube 清单已覆盖这三个主机，无需重复添加

Play、地图、字体、静态资源及用户图片使用共享主机，新增规则会让这些主机的其他业务请求也使用 AI 出口。这是按照本次指定依赖清单作出的出口选择，不代表它们自身不支持香港；同一父域下未列出的主机维持原策略

`www.google.com`、`www.googleapis.com`、`www.gstatic.com` 按用户要求移出 AI，继续由现有 Google / Proxy 通用规则覆盖

6 个广告或统计主机不加入 AI 清单，沿用已有策略。Rules 的 Clash/Surge AdBlock 包含 `doubleclick.net` 后缀，且位于 AI 规则之前；启用广告拦截时，三个 DoubleClick 主机仍可能被阻止。因此本次更新不是对 Google 全量防火墙放行要求的完整实现，不能保证所有 Gemini 功能可用；若遇到相关功能异常，应结合请求日志检查拦截策略

| 官方主机 | 本次处理 |
|---|---|
| `lh5.googleusercontent.com` | 新增 AI 精确规则 |
| `www.googleapis.com` | 按用户要求移出 AI，保留通用 Google / Proxy 分流 |
| `ssl.gstatic.com` | 新增 AI 精确规则 |
| `fonts.googleapis.com` | 新增 AI 精确规则 |
| `play.google.com` | 新增 AI 精确规则 |
| `ogs.google.com` | 新增 AI 精确规则 |
| `www.google.com` | 按用户要求移出 AI，保留通用 Google / Proxy 分流 |
| `apis.google.com` | AI 已覆盖，保留 |
| `jnn-pa.googleapis.com` | 新增 AI 精确规则 |
| `waa-pa.clients6.google.com` | AI 已覆盖，保留 |
| `i.ytimg.com` | 保留 YouTube 分流；服务端 Google 新增精确规则 |
| `yt3.ggpht.com` | 保留 YouTube 分流；服务端 Google 已覆盖 |
| `lh3.googleusercontent.com` | 新增 AI 精确规则 |
| `maps.gstatic.com` | 新增 AI 精确规则 |
| `lh3.google.com` | 新增 AI 精确规则 |
| `ogads-pa.clients6.google.com` | 广告或统计共享主机，保留现有策略 |
| `csp.withgoogle.com` | 新增 AI 精确规则 |
| `www.googletagmanager.com` | 广告或统计共享主机，保留现有策略 |
| `www.youtube.com` | 保留 YouTube 分流；服务端 Google 已覆盖 |
| `fonts.gstatic.com` | 新增 AI 精确规则 |
| `maps.googleapis.com` | 新增 AI 精确规则 |
| `static.doubleclick.net` | 广告或统计共享主机，保留现有策略 |
| `www.gstatic.com` | 按用户要求移出 AI，保留通用 Google / Proxy 分流 |
| `gemini.google.com` | AI 已覆盖，保留 |
| `td.doubleclick.net` | 广告或统计共享主机，保留现有策略 |
| `googleads.g.doubleclick.net` | 广告或统计共享主机，保留现有策略 |
| `www.google-analytics.com` | 广告或统计共享主机，保留现有策略 |
| `optimizationguide-pa.googleapis.com` | 新增 AI 精确规则 |
| `encrypted-tbn0.gstatic.com` | 新增 AI 精确规则 |
| `encrypted-tbn1.gstatic.com` | 新增 AI 精确规则 |
| `encrypted-tbn2.gstatic.com` | 新增 AI 精确规则 |
| `encrypted-tbn3.gstatic.com` | 新增 AI 精确规则 |
| `streetviewpixels-pa.googleapis.com` | 新增 AI 精确规则 |
| `content-autofill.googleapis.com` | 新增 AI 精确规则 |

四种客户端 AI 域名集合与 `services/AI.list` 同步为 155 条；ChatGPT Voice 的 23 个 IP 规则未修改。Google 父域与新增 AI 精确主机的 18 处重叠均登记在 `policy/overlaps.json`，不修改现有服务 ID 或节点选区

验证包括构建、目录及归属检查、单元测试、四种客户端集合比对与差异检查；未执行账号登录、模型调用或线上节点刷新
