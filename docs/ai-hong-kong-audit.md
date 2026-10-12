# AI Suite 香港可用范围复核

核查日期：2026-10-12

本次同时检查已有 AI Suite 的入口、模型接口、登录依赖和常见未收录服务，并同步 Rules 仓库的 Clash、Surge、Egern、sing-box 四种格式与本仓库 `services/AI.list`

新增依据为服务官方地区说明，或官方明确声明适用的模型供应商地区限制；网站能打开、支持付款、模型部署在某地区，都不等于香港用户能使用所有模型。第三方清单仅用于发现候选项，不作为新增限制的唯一依据

## 本次新增

| 服务 | 依据 | 新增模式 |
| --- | --- | --- |
| Cohere | [SaaS 协议](https://cohere.com/saas-agreement)明确将香港、澳门列入 Restricted Location；[官方 SDK](https://github.com/cohere-ai/cohere-python/blob/main/src/cohere/environment.py)使用 `api.cohere.com`，[旧版官方条款](https://cohere.com/terms-of-use)仍记录 `cohere.ai` 服务域名 | `+.cohere.ai`、`+.cohere.com` |
| Chrome DevTools AI assistance | [官方启用说明](https://developer.chrome.com/docs/devtools/ai-assistance/get-started)在本次香港出口访问时显示 HK 不受支持；[Chromium 地区名单](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/browser/devtools/aida_client.cc)也未列 `hk`，[请求实现](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/browser/devtools/aida_service_handler.cc)确认 AIDA 主机 | `aida.googleapis.com` |
| TRAE 国际版 | [当前支持地区](https://docs.trae.ai/ide/supported-countries-and-regions)未列香港；[网络配置说明](https://docs.trae.ai/ide/troubleshoot-general-issues)列出 `*.trae.ai`、`*.traeapi.us`、`*.mchost.guru` 等依赖 | `+.trae.ai`、`+.traeapi.us`、`trae-api-sg.mchost.guru`、`trae-api-us.mchost.guru` |

TRAE 的两个 `mchost.guru` 精确主机来自[官方社区中的国际版网络答复](https://forum.trae.cn/t/topic/19250)，该答复由社区自动助手提供，并非正式接口规范；本次另行确认两者均能解析。结合正式文档的父域清单，只纳入这两个国际接口，未扩大到 `+.mchost.guru`，避免同时改变国内版等业务的出口

TRAE [2026 年 2 月订阅 FAQ](https://forum.trae.cn/t/topic/59)曾列香港可订阅，本次以当前产品支持名单为准，不据旧付款名单推断服务可用。网络文档中的 Open VSX、Supabase、Vercel 属于共享平台，不因出现在防火墙清单就把整个平台加入 AI 出口

新增共 7 个模式，AI 清单增至 136 个，全目录增至 579 个；服务或合集总数仍为 114，因为新增产品归入现有 `AI` 合集

## 已有覆盖与接口检查

| 服务或范围 | 本次结论 |
| --- | --- |
| OpenAI / ChatGPT / Codex / Sora | [OpenAI API 地区名单](https://developers.openai.com/api/docs/supported-countries)未列香港；现有 OpenAI、ChatGPT、Sora 服务后缀已覆盖这些产品，不重复添加其子域 |
| ChatGPT Voice | 重新读取[官方 IP 清单](https://openai.com/chatgpt-voice.json)，23 个 IPv4 `/32` 与四种客户端规则一致，未新增或删除 IP；本仓库域名清单不能代替客户端 UDP/IP 规则 |
| Claude / Claude Code / Cowork | [Anthropic 地区名单](https://www.anthropic.com/supported-countries)未列香港；现有 `anthropic.com`、`claude.ai`、`claude.com`、`claudeusercontent.com` 后缀保留 |
| Google AI Studio / Gemini API | [官方支持地区](https://ai.google.dev/gemini-api/docs/available-regions)未列香港；现有 AI Studio 入口与 Generative Language API 规则保留 |
| Antigravity / Project Genie | [Antigravity FAQ](https://antigravity.google/docs/faq)与 [Project Genie FAQ](https://labs.google/fx/faq)未列香港；前一批已补入两个 daily-cloudcode 主机和 `labs.google`，本次不重复添加 |
| Cursor | 按[网络清单](https://cursor.com/docs/enterprise/network-configuration)及[登录域名说明](https://cursor.com/help/troubleshooting/sign-in-domains)比对，已覆盖列出的模型、下载、托管计算机及新旧登录域名；保留[模型地区限制](https://cursor.com/docs/account/regions)下的分流 |
| Kiro | 按[官方网络清单](https://kiro.dev/docs/privacy-and-security/firewalls/)比对，现有 `+.kiro.dev` 覆盖多层子域，以及 runtime、management、telemetry 服务；旧 Q 的美国、欧洲主机也已覆盖。未把 AWS 通用身份、计费、遥测和企业租户全部并入 AI |
| GitHub Copilot | 比对[官方 allowlist](https://docs.github.com/en/copilot/reference/copilot-allowlist-reference)，已有 Copilot 服务后缀和专用精确主机保留；通用 GitHub 登录页面、软件包仓库、Azure 本地语音模型下载与企业 GHE 租户不据此整体扩大分流 |
| Gemini in Android Studio | [地区名单](https://developer.android.com/studio/gemini/availability)未列香港；这与 Gemini 网页版是不同产品，不能用网页版支持状态替代。新增 AIDA 主机的直接接口证据来自 Chrome DevTools，不声称已实测 Android Studio |

已有 Apple Intelligence、Augment、Cerebras、Chorus、DIA、Dify、Groq、Jasper、JetBrains AI、Meta AI、Microsoft Copilot、Mistral、NotebookLM、Opal、OpenArt、OpenRouter、Perplexity、Windsurf、Zed 等规则在本次保持不变；保留不代表重新确认它们全部不支持香港，本轮重点是补漏而非重定义整个 AI 合集

## 核查后未新增的候选项

| 候选项 | 依据或证据边界 |
| --- | --- |
| Raycast | [官方 FAQ](https://www.raycast.com/faq)列出的全球服务例外不含香港，未新增 |
| ElevenLabs | [官方限制地区说明](https://help.elevenlabs.io/hc/en-us/articles/22497891312401-Do-you-restrict-access-to-the-service-and-platform-for-any-specific-countries)未把香港列入限制，未新增 |
| Google Flow | [官方支持地区](https://support.google.com/flow/answer/16353544?hl=en)列有香港；与同在 `labs.google` 下的 Project Genie 区分。已有共享 Labs 入口仍会同时覆盖 Flow 路径 |
| Poe | [购买 FAQ](https://help.poe.com/hc/en-us/articles/19945140063636-Poe-Purchases-FAQs)列有香港；这只确认订阅范围，未找到足以认定整站香港不可用的新证据 |
| Google Stitch | 官网 “Where is Stitch available?” 答复仅称在 Gemini 支持地区向 18 岁以上用户开放，未明确指向哪份 Gemini 地区名单；[旧社区回复](https://discuss.ai.google.dev/t/sorry-stitch-is-unavailable/87225?page=3)与部分用户反馈不一致，暂不依据旧反馈认定当前香港不可用 |
| NVIDIA NIM | [官方 OTP 不支持国家配置](https://build.nvidia.com/api/runtime/config/otp-unsupported-countries.yaml)未列 HK；这只是验证手机号的范围，不据此声称所有模型均可用，也没有据此新增 |
| IBM watsonx.ai | [IBM Cloud 个人使用限制](https://cloud.ibm.com/docs/account?topic=account-account-getting-started)未列香港，未把个人注册限制误当成所有推理接口的香港限制 |
| Factory / Devin / Warp / Amp / Replit / Lovable / v0 / Qoder / Qodo / Cline / Kilo / Fireworks / Ollama / Upstage / Inception / AI21 / Runway / Midjourney | 定向检索未取得足以新增的当前香港限制证据；是否集成 Claude、GPT 或 Gemini 不能单独证明这些平台按终端用户 IP 实施相同限制，未盲目加入 |

## 排除与验证边界

- `g.ai` 在本次读取时重定向至 Google 搜索，不按旧第三方 AI Studio 分类新增
- TRAE 故障文档里的 `trae.com.ai` 经 Google、Cloudflare DNS 均返回 NXDOMAIN，不新增
- `traeapi.us` 根域返回 NOERROR 但没有 A 记录，不把这一结果误判为其所有子域不可用；保留官方明确列出的服务后缀
- `antigravity-unleash.goog` 出现在第三方规则与二进制分析中，但本次未取得官方接口用途及必要性说明，不仅凭域名存在或名称相似新增
- Antigravity 企业版的 `businessaicode`、`discoveryengine` 及 Gemini Code Assist Standard/Enterprise 的 `cloudaicompanion` 有官方网络清单，但未取得这些企业产品对香港用户一律不可用的独立证据，未套用个人版地区名单扩大到共享 Cloud API
- 新增精确主机以及 Cohere 新旧 API、TRAE 网站均经 Google 和 Cloudflare DNS 复核有 A 记录；该结果仅证明解析状态
- 四种客户端格式与服务端 AI 域名清单须保持集合一致，无重复、无同服务父子冗余；AIDA 对 Google 通用后缀的覆盖关系在 `policy/overlaps.json` 中单独登记
- 规则格式、目录测试、DNS 和官方地区说明都不能证明具体账号已成功登录、模型调用已成功或目标节点已刷新；本次未进行带账号的业务调用

这份记录是核查日期的候选服务审计，不是对互联网全部 AI 服务或将来地区政策的永久保证
