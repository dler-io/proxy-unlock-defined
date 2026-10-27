# warp-google 专用域名清单

[domains.list](domains.list) 供支持在线清单的 `oix-server` 的 `warp-google` 功能使用，选择出口和健康检查由服务端处理

默认地址：

```text
https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/warp-google/domains.list
```

该目录独立于 `catalog.json`，不作为 `proxy-unlock` 服务导入，不参与普通服务的域名归属去重，也不由 `scripts/render.py` 或 `scripts/build.py` 生成；现有 `services/Google.list` 和 AI 服务保持各自用途

清单范围：

- Google 搜索国家域名：按 [Google 官方 supported_domains](https://www.google.com/supported_domains) 的 2026-10-28 快照列出 187 个域名，并补回 Gemini 官方页面 CSP 中的 11 个搜索别名，使用明确的后缀规则，不使用 `google.*` 标签通配
- YouTube 入口、短链接、无 Cookie 播放器和 Kids；`googlevideo.com` 默认只列出精确主机 `redirector.googlevideo.com`
- Gemini 网页、API 和 AI Studio：`gemini.google.com`、`aistudio.google.com` 由 `+.google.com` 覆盖，API 由 `+.googleapis.com` 覆盖；另用 `+.gemini.google` 覆盖根域、分享和企业版认证子域
- Gemini App 唤起：官方 `gemini.google.com` 页面使用 `gemini.app.google` 深链，保留该服务及子域
- Canvas / AI Studio 预览：保留 `+.scf.usercontent.goog`，用途和动态子域结构见 [Google SafeContentFrame 说明](https://bughunters.google.com/blog/beyond-sandbox-domains-rendering-untrusted-web-content-with-safecontentframe)
- Gemini 开发入口保留精确 `ai.google.dev`；Gemini Enterprise 保留官方网络清单中的 `auth.cloud.google`、`vertexaisearch.cloud.google`、`notebooklm.cloud.google`、`payments.cloud.google`，见[官方接入文档](https://docs.cloud.google.com/gemini/enterprise/docs/private-ui-access)
- Gemini 的实验 Gems 编辑器保留 `+.opal.google`，见[官方集成说明](https://blog.google/innovation-and-ai/models-and-research/google-labs/mini-apps-opal-gemini-app-experiment/)；[官方 FAQ](https://developers.google.com/opal/faq)说明该实验计划于 2026-11-17 关闭，本清单不扩展到其他 Labs 产品
- 共享服务域 `googleapis.com`、`googleusercontent.com`、`ggpht.com`：Google 的 [Gemini 主机清单](https://knowledge.workspace.google.com/admin/security/firewall-and-proxy-settings#gemini-hosts) 列有这些域下的 API、图片或内容主机，现阶段保留后缀覆盖以免遗漏动态主机；这也会覆盖使用同域的其他 Google 请求

已确认的 Gemini 子域包括 [share.gemini.google](https://share.gemini.google/)（Google 分享短链）、[business.gemini.google](https://support.google.com/g/answer/16938246?hl=en)（企业版入口）及其登录跳转目标 `auth.business.gemini.google`；不能只精确匹配根域

11 个搜索别名为 `google.co.im`、`google.co.je`、`google.com.ai`、`google.com.cn`、`google.com.tn`、`google.gp`、`google.hk`、`google.ms`、`google.ng`、`google.tk`、`google.vg`，来源为 `https://gemini.google.com/` 响应的 `script-src` CSP。2026-10-28 实查其中 10 个返回搜索界面或跳转，`google.com.cn` 仅确认官方 CSP 引用，本次未成功完成 HTTPS 请求，不据此宣称可用

不纳入 `gmail.com`、`android.com`、`googleapis.cn`、`xn--ngstr-lra8j.com`，也不接管整个 `.google`、`.goog`、`.youtube` 顶级域；`gstatic.com`、`i.ytimg.com`、`gvt1.com` 及默认视频 CDN 保持原有路由，其中 `gstatic.com` 涵盖常用联网探测与测速主机。Google 官方搜索列表中的 `google.cn` 仍保留

移除 `gmail.com` 不代表 Gmail 所有请求都不再经 WARP，`mail.google.com` 等共享父域下的请求仍会匹配。清单支持 Google 与 Gemini 域名分流，不保证产品可用地区、账号资格或订阅权益；Google/YouTube 出口检查通过也不等于 Gemini 可用

服务端应保留用户路由和显式解锁的现有优先级。账户级 YouTube 视频 CDN 开关由服务端额外增加 `+.googlevideo.com`，不写入本清单。在线版本仅使用本清单和现有按 URL 缓存，不在服务端保存另一份内置副本；首次没有有效缓存时按原有路由，成功下载后热更新生效，下载失败保留最后有效缓存。旧版本服务端继续使用各自内置规则，只有已实现在线加载的版本才会读取此地址；清单发布与服务端升级需分别验证，不能把规则校验通过视为实际解锁验证

维护时直接编辑 `domains.list`，非注释行按字典序排列且不得重复，格式限于精确主机和 `+.` 后缀规则。`scripts/check.py` 单独校验该清单，允许与普通服务规则重叠，但不放宽普通清单校验

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```
