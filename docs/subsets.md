**子清单目录**

原有完整服务 URL 继续有效；按需选择完整清单、独立子清单或组合清单，避免重复加载同一域名

子清单内没有出口选择，`region` 由节点配置指定；待核查集合拆分仅保留原有范围，不代表已确认业务归属

| 配置生成器选择键 | 所属服务 | 状态 | URL 路径 | 模式数 |
|---|---|---|---|---:|
| `CanalPlus_Core` | CanalPlus | imported | [parts/CanalPlus/Core.list](../parts/CanalPlus/Core.list) | 4 |
| `CanalPlus_MyCanal` | CanalPlus | imported | [parts/CanalPlus/MyCanal.list](../parts/CanalPlus/MyCanal.list) | 2 |
| `DAZN_CloudFront` | DAZN | imported | [parts/DAZN/CloudFront.list](../parts/DAZN/CloudFront.list) | 2 |
| `DAZN_Core` | DAZN | imported | [parts/DAZN/Core.list](../parts/DAZN/Core.list) | 6 |
| `HBOGOAsia_Base` | HBOGOAsia | imported | [parts/HBOGOAsia/Base.list](../parts/HBOGOAsia/Base.list) | 9 |
| `HBOGOAsia_Extended` | HBOGOAsia | imported | [parts/HBOGOAsia/Extended.list](../parts/HBOGOAsia/Extended.list) | 8 |
| `MyTVSuper_Analytics` | MyTVSuper | imported | [parts/MyTVSuper/Analytics.list](../parts/MyTVSuper/Analytics.list) | 2 |
| `MyTVSuper_Core` | MyTVSuper | imported | [parts/MyTVSuper/Core.list](../parts/MyTVSuper/Core.list) | 2 |
| `Now_NowE` | Now | imported | [parts/Now/NowE.list](../parts/Now/NowE.list) | 2 |
| `Now_NowTV` | Now | imported | [parts/Now/NowTV.list](../parts/Now/NowTV.list) | 2 |
| `Shared_GoMPulse` | Shared | review | [parts/Shared/GoMPulse.list](../parts/Shared/GoMPulse.list) | 1 |
| `Shared_ThePlatform` | Shared | review | [parts/Shared/ThePlatform.list](../parts/Shared/ThePlatform.list) | 1 |
| `Unclassified_Japanese` | Unclassified | review | [subsets/Unclassified/Japanese.list](../subsets/Unclassified/Japanese.list) | 16 |
| `Unclassified_JapaneseSites` | Unclassified | review | [parts/Unclassified/JapaneseSites.list](../parts/Unclassified/JapaneseSites.list) | 15 |
| `Unclassified_NStatic` | Unclassified | review | [parts/Unclassified/NStatic.list](../parts/Unclassified/NStatic.list) | 1 |
| `Unclassified_RakutenMagazine` | Unclassified | review | [parts/Unclassified/RakutenMagazine.list](../parts/Unclassified/RakutenMagazine.list) | 1 |
| `Unclassified_SharedHosts` | Unclassified | review | [parts/Unclassified/SharedHosts.list](../parts/Unclassified/SharedHosts.list) | 7 |
| `Unclassified_Usercentrics` | Unclassified | review | [parts/Unclassified/Usercentrics.list](../parts/Unclassified/Usercentrics.list) | 1 |
| `ViuTV_Core` | ViuTV | imported | [parts/ViuTV/Core.list](../parts/ViuTV/Core.list) | 1 |
| `ViuTV_LiveCDN` | ViuTV | imported | [parts/ViuTV/LiveCDN.list](../parts/ViuTV/LiveCDN.list) | 1 |

`Unclassified_Japanese` 是 JapaneseSites 与 RakutenMagazine 的组合；需要保留较小范围时仅使用 `Unclassified_JapaneseSites`

配置生成器中的选择键是便捷命名；已有节点可以保留自己的服务键，只替换 URL 与 region

```yaml
proxy-unlock:
  defined:
    CanalPlus_DE:
      url: https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/parts/CanalPlus/MyCanal.list
      region: DE
    CanalPlus_FR:
      url: https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/main/parts/CanalPlus/Core.list
      region: FR
```

这两个服务键可分别指定其他本机出口；示例中的地区名称仅为使用示例，不是清单内置策略

已拆分服务的完整清单与组合清单均由 `python3 scripts/build.py` 生成；维护时只编辑对应 `parts/` 源文件，校验器会阻止源文件间重复及生成文件过期
