# YouTube 视频专用域名清单

[`domains.list`](domains.list) 仅包含 `+.googlevideo.com`，覆盖根域、视频分发子域与 `redirector.googlevideo.com`，不包含网页、图片或其他共享静态资源

```text
https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/warp-youtube/domains.list
```

本清单独立于服务目录和 [`warp-google`](../warp-google/README.md)。支持该功能的使用端自动加载本清单，仅由面板上的「YouTube 后台播放兼容」账户设置控制，不增加 `warp-youtube` 节点开关，也不依赖 `warp-google` 开关。`redirector.googlevideo.com` 同时保留在 Google 清单中，仍可由 `warp-google` 独立接管。域名命中、出口优先级和回退行为由使用端决定

运行 `python3 scripts/check.py` 检查格式与重复项。新增清单不代表旧版使用端会自动加载，需要支持独立规则源的版本
