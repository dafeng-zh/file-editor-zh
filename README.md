# file-editor-zh · Home Assistant「文件编辑器」中文汉化包

> 极简版一句话：**把 HA 的 File editor 插件界面彻底汉化成中文，一键安装，重启不丢。**

把 Home Assistant 官方 **File editor**（`core_configurator` 6.0.0，HASS Configurator）前端界面**完整汉化为中文**，并解决 supervisor「重启即回滚英文」的持久化难题。

> 界面用户可见文案 **100% 中文（约 1727 个中文字符）**：按钮、菜单、弹窗、toast、确认句、设置面板、网络状态、主题标签、工具栏提示全部覆盖。

---

## ✨ 特性

- **全量汉化**：不只按钮菜单，连完整确认弹窗（"确定要关闭当前文件吗？未保存的更改将丢失。"）、错误提示 toast、网络状态标签、主题切换按钮、撤销/重做悬浮提示都汉化了
- **持久生效**：解决 supervisor 用预构建镜像重建容器导致 docker cp 改动丢失的问题 —— 通过 `docker commit` 覆盖镜像 tag 固化
- **可回退**：安装前自动备份原镜像 tag，一条命令回退英文原版
- **可复现**：附带 `apply_zh.py` 一键汉化脚本 + 229 条中英对照表（JSON/PO），可从官方英文版复现
- **安全白名单替换**：只替换用户可见文案，避开代码标识符、Ace 主题名/语言名、快捷键、品牌、示例值，JS 语法零破坏（node --check 验证）

---

## 📦 仓库结构

```
file-editor-zh/
├── releases/
│   ├── dev.orig.html      # 官方原版前端(权威源, 152547B)
│   └── dev.html           # 汉化成品(1727 中文字符)
├── translations/
│   ├── en-zh.json         # 229 条中英对照(机器可读)
│   ├── en-zh.po           # gettext 格式对照
│   └── _zh_map.py         # 内嵌替换规则源
├── install/
│   ├── install_zh.sh      # 一键安装(备份+注入+commit+重启+验证)
│   └── rollback_zh.sh     # 一键回退英文版
└── apply_zh.py            # 从官方版复现汉化的脚本
```

---

## 🚀 快速安装

```bash
git clone <你的仓库地址> hass-configurator-zh
cd hass-configurator-zh
sudo bash install/install_zh.sh
```

脚本自动完成：
1. 备份当前镜像 tag（`*.pre-zh-<时间戳>`，可回退）
2. 将汉化 `dev.html` 注入运行中的 addon 容器
3. `docker commit` 覆盖镜像 tag `:6.0.0`（持久化关键步骤）
4. 重启 `core_configurator` addon
5. 验证容器 healthy + 中文生效

### 环境变量
| 变量 | 默认 | 说明 |
|---|---|---|
| `CONTAINER` | `app_core_configurator` | addon 容器名 |
| `IMAGE` | `homeassistant/aarch64-addon-configurator:6.0.0` | 镜像名+tag（架构/版本不同可覆盖） |

### 手动汉化（不用脚本）
```bash
# 1. 注入前端文件到运行容器
docker cp releases/dev.html app_core_configurator:/usr/lib/python3.12/site-packages/hass_configurator/dev.html
# 2. 提交为镜像覆盖 tag(持久化, 否则重启回滚英文)
docker commit -m "zh-CN" app_core_configurator homeassistant/aarch64-addon-configurator:6.0.0
# 3. 重启 addon(HA 界面重启 File editor, 或 docker restart app_core_configurator)
```

---

## ↩️ 回退英文原版

```bash
bash install/rollback_zh.sh homeassistant/aarch64-addon-configurator:6.0.0.pre-zh-20260830-234126
docker restart app_core_configurator
```
（用 `docker images | grep configurator` 找到安装时的备份 tag）

---

## 🔍 为什么用 docker commit（持久化原理）

- HA addon 由 supervisor 管理，**重启/重建时用预构建镜像重新创建容器**，直接 `docker cp` 进容器的文件改动会**丢失**。
- 官方 core addon 不接受本地 rebuild（"Local and store versions differ, use Update"）。
- 但 supervisor 的 `apps.json` 里 **configurator 镜像按 tag 引用（无 digest 锁定）** → 只要 `docker commit` 把容器现状固化成镜像并**覆盖同名 tag**，supervisor 下次启动就会用到汉化镜像，**持久生效**。

---

## 🛠 从官方版复现汉化

```bash
python3 apply_zh.py            # 读 releases/dev.orig.html → 生成 releases/dev.html
python3 apply_zh.py 你的dev.html -o out.html
```

脚本从 `translations/_zh_map.py`（内嵌）+ 内建 EXTRA 规则精确替换，输出约 1727 中文字符的界面文件。

---

## ✅ 汉化原则与保留项

**只汉化用户可见 UI 文案**（按钮/菜单/弹窗/toast/确认句/设置项/提示语），**刻意保留不汉化**：
- Ace 编辑器**主题配色名**（Monokai/Twilight/Tomorrow Night/Solarized 等，汉化后用户认不出主题）
- Ace **语言/语法模式名**（python/yaml/javascript 等，编辑器内部模式标识）
- **快捷键**（Ctrl-K、Shift-Left 等，会同步显示按键）
- 品牌/库名（Home Assistant、HASS Configurator、Ace Editor、Git）
- 输入**示例值**（ws 地址、sensor.example 等占位符）
- CSS 类名 / DOM id / JS 事件/变量名

**质量校验**：替换后 `node --check` 验证 JS 语法完整、HTML 标签均衡（script/div/a/option 开闭一致）。

---

## 🐛 本机已验证环境

- Armbian (arm64) + Docker + HA supervisor
- HA addon: `core_configurator` 6.0.0 (File editor)
- 镜像: `homeassistant/aarch64-addon-configurator:6.0.0`
- 前端文件路径: `/usr/lib/python3.12/site-packages/hass_configurator/dev.html`
- 汉化结果: 1727 中文字符, 容器 healthy, 重启不丢

---

## 📝 汉化过程记录（完整方法论）

完整过程见当日日志摘要，核心教训：
1. 提取候选文本的正则**必须含 `?`/`.`/`:` 等标点**，否则含标点的完整长句（确认弹窗、地址标签）全部漏判
2. 替换含 `<` 的句子时小心吞掉相邻 HTML 标签的 `<`（会断链），改坏要重建完整段落而非局部 patch
3. 过滤/替换类改动要**贯穿所有消费该字符串的环节**（HTML 文本 / JS 字符串 / toast 变体 / 对象值 label 都要覆盖）

---

## 🤝 回馈与扩展

- **用得上请 Star/Fork**，帮助更多中文 Home Assistant 用户
- 想改进：直接提 issue/PR，或补充其他 addon 的汉化
- 官方英文项目: [danielperna84/hass-configurator](https://github.com/danielperna84/hass-configurator)（官方无 i18n，本包为社区汉化替代方案）

## 📜 License

MIT — 汉化替换内容基于官方 [hass-configurator](https://github.com/danielperna84/hass-configurator)（MIT）的 `dev.html` 构建。

---

## ❓ 常见问题 (FAQ)

**Q: 装完后界面还是英文/显示旧英文（如 "Theme: Dark"）？**
A: 是浏览器缓存了汉化前的旧页面。**强制刷新**即可：`Ctrl+Shift+R`（Windows/Linux）或 `Cmd+Shift+R`（Mac）。代码里已是中文（如「主题：深色」），刷新后即显示。

**Q: 为什么重启 addon 后汉化还在？**
A: 因为安装脚本用 `docker commit` 把汉化固化成镜像层并覆盖原 tag，supervisor 重建容器用的就是中文镜像，所以重启不丢。若用 `docker cp` 直接改而不 commit，重启会还原英文。

**Q: 汉化会影响功能吗？**
A: 不会。只替换用户可见文案，避开代码标识符/Ace 主题名/语言名/快捷键/品牌/示例值，JS 语法经 `node --check` 验证零破坏。
