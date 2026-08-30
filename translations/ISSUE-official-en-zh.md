# 回馈官方 Issue 草案（danielperna84/hass-configurator 加 zh-CN i18n）

> 用途：在官方仓库提 issue，建议加入中文支持 / 欢迎 open 中文汉化包。
> 提交方式：登录 GitHub 官方仓库 https://github.com/danielperna84/hass-configurator/issues 新建。
> 附项目链接（已公开）：https://github.com/dafeng-zh/file-editor-zh

---

## 标题（Title）
**Feature request: Add zh-CN (Chinese Simplified) localization / i18n support, and a ready-to-use Chinese translation**

## 正文（Body）

### 中文版
**Feature request：加入简体中文（zh-CN）界面汉化支持**

你好！我是一名中国用户，非常喜欢 HASS Configurator（HA 的 File editor）。但前端界面目前**仅支持英文单语言**，没有 i18n / 本地化机制，对庞大的中文 Home Assistant 社区使用不便。

我已完成一份**完整的简体中文汉化**，可作为参考或 PR 起点：
- **汉化成果**：界面用户可见文案 100% 中文（按钮、菜单、弹窗、toast、确认句、设置、提示语全覆盖，约 1727 个中文字符）
- **项目地址**：https://github.com/dafeng-zh/file-editor-zh （含完整对照表 translations/en-zh.json / .po，229 条）
- **一键安装/回退**脚本 + 从官方版复现的 `apply_zh.py`

**建议**：
1. 若官方愿意，可基于我的对照表直接集成一个 zh-CN 语言包
2. 或引入轻量 i18n 机制（如 `dev.html` + 语言文件 key-value），社区可持续维护多语言

**技术背景**：当前 `dev.html` 硬编码英文字符串、无 LANG 配置。可抽出为 `key: 原文` + 语言映射表，默认英文、按浏览器或设置切换。

如果您不方便实现，也希望这份汉化能帮到其他中文用户。欢迎参考或直接使用我的仓库。谢谢！

---

### English version
Hi! I'm a Chinese user of HASS Configurator (HA's "File editor"). The UI currently only supports English with no i18n/localization mechanism, which is inconvenient for the large Chinese HA community.

I have completed a **full Simplified Chinese (zh-CN) localization** that could serve as reference or a PR starting point:
- **Result**: 100% of user-visible UI text in Chinese (~1,727 Chinese characters: buttons, menus, dialogs, toasts, confirmations, settings, tooltips)
- **Repo**: https://github.com/dafeng-zh/file-editor-zh (with full translation tables `translations/en-zh.json` / `.po`, 229 entries, plus one-click install/rollback scripts and a reproducible `apply_zh.py`)

**Suggestion**:
1. If you're open to it, integrate a zh-CN language pack based on my translation tables.
2. Or introduce a lightweight i18n mechanism (e.g. `key: source` mapping with a language table) so the community can maintain multiple languages sustainably.

Currently `dev.html` hardcodes English strings with no LANG config; it could be refactored to a `key → source` + language map, defaulting to English and switchable per browser/settings.

If you prefer not to implement it, I hope this translation still helps other Chinese users. Thanks for the great addon!

---

## 可选补充（作为评论/PR 提供）
- 完整翻译文件可直接下载：`translations/en-zh.json`
- 若需要，可提供 `dev.html` 的 i18n 改造 diff（最小侵入）
