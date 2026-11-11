# proxy-unlock-defined

按服务维护的域名分流规则集，覆盖 Netflix、Disney+、BBC、Google、YouTube 和常见 AI 服务。每份清单可以独立引用，出口由使用端配置

[服务目录](docs/catalog.md) · [子清单目录](docs/subsets.md) · [维护指南](docs/maintenance.md) · [Google / Gemini 专用清单](warp-google/README.md)

## 选择清单

| 路径 | 用途 |
| --- | --- |
| [`services/`](services/) | 110 份常规服务清单，包含按服务合并的完整清单 |
| [`parts/`](parts/) · [`subsets/`](subsets/) | 可独立使用的源子清单，以及从源子清单生成的组合 |
| [`review/`](review/) · [`legacy/`](legacy/) | 2 份共享或待核查合集、2 份停运服务的存档，按需显式启用 |
| [`warp-google/`](warp-google/) | 独立维护的 Google 搜索、YouTube 和 Gemini 清单，可单独接入 |
| [`catalog.json`](catalog.json) | 服务 ID、清单路径、状态和组合关系 |

服务目录共收录 760 个唯一域名模式。规则校验覆盖文件格式和匹配范围，实际可用性取决于出口、账号及服务的地区政策

## 规则格式

每行写一个域名模式，允许空行和以 `#` 开头的注释

```text
# 精确匹配一个主机
api.example.com
# 匹配域名本身及任意层级的子域名
+.example.net
```

清单仅接受域名，支持精确匹配和 `+.` 后缀匹配

## 引用清单

从服务目录打开所需文件，复制 GitHub 的 **Raw** 地址，在支持上述格式的工具中加载。同一服务按需选择完整清单或互不重叠的子清单

仓库也提供 `proxy-unlock` YAML 片段生成器。使用 Python 3.10 或更高版本运行以下命令，将生成的 `rules` 合并到现有配置，`=` 右侧填写已有出口或代理组名称

```bash
python3 scripts/render.py --service Netflix=SG --service Disney=SG
python3 scripts/render.py --service CanalPlus_MyCanal=DE --service CanalPlus_Core=FR
```

默认生成跟随 `main` 的清单地址。需要固定内容时可加 `--ref <commit-sha>`，引用当前可访问的提交。完整示例见 [服务配置](examples/defined.yml)和[子清单配置](examples/subsets.yml)

## 维护规则

直接修改普通服务清单。已拆分的服务在 `parts/` 修改源文件，再重新生成完整清单和组合清单

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

校验会检查非法域名、重复匹配、跨服务后缀重叠和生成文件是否同步。允许的跨服务覆盖记录在 [`policy/overlaps.json`](policy/overlaps.json)，提交前也应同步更新相关目录说明
