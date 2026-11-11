# Google / Gemini 专用域名清单

[`domains.list`](domains.list) 可用于给 Google 搜索、YouTube 和 Gemini 指定 WARP 出口。该清单独立于 [服务目录](../docs/catalog.md)，可以单独加载。出口选择和规则优先级由使用端决定

```text
https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/warp-google/domains.list
```

## 覆盖范围

| 类别 | 覆盖 |
| --- | --- |
| Google 搜索 | Google 官方搜索域名的 2026-10-28 快照，以及 Gemini 页面引用的 11 个搜索别名 |
| YouTube | 主站、短链接、隐私增强嵌入播放器、Kids 和视频重定向主机 |
| Gemini | 网页、分享、App 唤起、AI Studio、预览，以及部分企业版接口 |
| 共享 API | `+.googleapis.com` 涵盖 Gemini 相关接口，也会匹配同一父域下的其他 Google API |

搜索域名逐项列出，来源见 [Google 搜索域名列表](https://www.google.com/supported_domains)。额外的 11 个别名为 `google.co.im`、`google.co.je`、`google.com.ai`、`google.com.cn`、`google.com.tn`、`google.gp`、`google.hk`、`google.ms`、`google.ng`、`google.tk`、`google.vg`，来自 Gemini 页面响应的 `script-src`

Gemini 网页和 AI Studio 由 `+.google.com` 覆盖，分享和 App 唤起分别由 `+.gemini.google`、`+.gemini.app.google` 覆盖。预览域名和企业接口参照 [SafeContentFrame 说明](https://bughunters.google.com/blog/beyond-sandbox-domains-rendering-untrusted-web-content-with-safecontentframe)与 [Gemini Enterprise 网络文档](https://docs.cloud.google.com/gemini/enterprise/docs/private-ui-access)

## 与服务清单搭配

- [Google 服务清单](../services/Google.list)统一维护 Google 旗下服务；[AI 服务清单](../services/AI.list)不再单独收录这些服务。两份 Google 清单用途和范围不同，同时加载时应确认使用端的出口与优先级
- 本清单保留 Google 通用分流；完整的 `googlevideo.com` 视频 CDN 范围由使用端的账户级 YouTube 功能额外启用，不写入公共清单
- 共享图片、字体、内容托管和证书域名沿用使用端的其他规则。视频 CDN 仅收录 `redirector.googlevideo.com` 精确主机，`mail.google.com` 等子域仍会被 `+.google.com` 覆盖

直接修改 `domains.list`，保持域名逐行排序。运行 `python3 scripts/check.py` 单独校验该清单的格式和重复项
