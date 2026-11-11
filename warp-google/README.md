# Google 视频专用域名清单

[`domains.list`](domains.list) 仅包含 `+.googlevideo.com`，匹配根域及所有层级的子域，包括 `redirector.googlevideo.com` 和视频分发主机

```text
https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/warp-google/domains.list
```

该清单独立于 [服务目录](../docs/catalog.md)，可以单独加载。出口选择和规则优先级由使用端决定

Google 搜索、YouTube 网页与短链接、Gemini 及其他 Google 旗下服务由 [Google 服务清单](../services/Google.list)处理，本清单不再收录这些入口、API 或共享静态资源。若同时加载两份清单，`redirector.googlevideo.com` 存在覆盖交集，应在使用端确认实际优先级

运行 `python3 scripts/check.py` 校验清单。修改清单后需确认使用端已刷新，实际出口和播放效果需另行验证
