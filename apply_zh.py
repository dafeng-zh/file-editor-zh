#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hass-configurator 一键汉化脚本 (Home Assistant "File editor" / core_configurator 6.0.0)
用法:
  python3 apply_zh.py <原始dev.html路径> -o <输出路径>
  无参数则默认: 读取同目录 releases/dev.orig.html -> 输出 releases/dev.html
原理: 精确替换用户可见 UI 文案(白名单), 避开代码标识符/主题名/语言名/快捷键/品牌/示例值。
"""
import ast, json, os, re, sys, argparse

# ---------- 内嵌补充规则(不在这两批替代里, 单独维护, 保证可复现到成品) ----------
EXTRA = [
  # 品牌名+中文说明(外部链接)
  ("Material Icons","Material 图标"),
  # 弹窗确认(含标点完整句)
  ('Do you really want to save?','确实要保存吗？'),
  ('Are you sure you want to initialize a repository at the current path?','确定要在当前路径初始化仓库吗？'),
  ('Are you sure you want to push your commited changes to the configured remote / origin?','确定要将已提交的更改推送到配置的远程仓库 / origin 吗？'),
  ('Are you sure you want to stash your changes?','确定要暂存你的更改吗？'),
  ('Are you sure you want to close the current file? Unsaved changes will be lost.','确定要关闭当前文件吗？未保存的更改将丢失。'),
  ('to the index?','到暂存区吗？'),
  ('Do you want to check the configuration?','要检查配置吗？'),
  ('Do you want to reload the automations?','要重新加载自动化模块吗？'),
  ('Do you want to reload the scripts?','要重新加载脚本吗？'),
  ('Do you want to reload the groups?','要重新加载分组吗？'),
  ('Do you want to reload the core?','要重新加载核心吗？'),
  ('Do you really want to restart Home Assistant?','确实要重启 Home Assistant 吗？'),
  ('from the list of allowed networks?','从允许的网络列表中移除吗？'),
  ('to the list of allowed networks?','添加到允许的网络列表吗？'),
  ('This requires a browser, such as Google Chrome or Firefox, that supports the Page Visibility API.','这需要一个支持页面可见性 API 的浏览器（如 Google Chrome 或 Firefox）。'),
  # toast/提示
  ("'Error:  Please provide a filename'","'错误： 请提供文件名'"),
  ('\\"Error:  Please provide a filename\\"','\\"错误： 请提供文件名\\"'),
  ("'Could not save theme preference'","'无法保存主题偏好'"),
  ("'Socket connected'","'WebSocket 已连接'"),
  ("'Socket closed'","'WebSocket 已关闭'"),
  ('idle Fingers','闲置手指'),
  # 网络状态弹窗地址标签
  ('Your address:&nbsp;','你的地址：&nbsp;'),
  ('Listening address:&nbsp;','监听地址：&nbsp;'),
  ('Home Assistant API address:&nbsp;','Home Assistant API 地址：&nbsp;'),
  # 错误toast前缀
  ('<div><pre>Error: "','<div><pre>错误： "'),
  # 主题切换按钮 label(JS 对象值)
  ("'Theme: Auto'","'主题：自动'"),
  ("'Theme: Light'","'主题：浅色'"),
  ("'Theme: Dark'","'主题：深色'"),
  ("|| 'Theme'","|| '主题'"),
  # 工具栏悬浮提示(data-tooltip)
  ('"Undo"','"撤销"'),
  ('"Redo"','"重做"'),
  ('"Fold"','"折叠"'),
  ('"(Un)comment"','"注释/取消注释"'),
  # 关于弹窗完整重建(修正破损句)
  ('>Web-based file editor designed to modify configuration files of <的配置文件','>基于 Web 的文件编辑器，用于修改 <的配置文件'),
]

def parse_zh_map(path):
    """从 zh_map.py(存有 >X<标签型 + JS字符串型对照) 解析 MAP 列表"""
    pairs=[]
    if not os.path.exists(path): return pairs
    src=open(path,encoding='utf-8').read()
    tree=ast.parse(src)
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for t in node.targets:
                if isinstance(t,ast.Name) and t.id=='MAP':
                    for el in node.value.elts:
                        if isinstance(el,ast.Tuple) and len(el.elts)==2:
                            try:
                                a=ast.literal_eval(el.elts[0]); b=ast.literal_eval(el.elts[1])
                                if isinstance(a,str) and isinstance(b,str) and a!=b and any('\u4e00'<=c<='\u9fff' for c in b):
                                    pairs.append((a,b))
                            except: pass
    return pairs

def main():
    here=os.path.dirname(os.path.abspath(__file__))
    ap=argparse.ArgumentParser()
    ap.add_argument('src',nargs='?',default=None)
    ap.add_argument('-o','--out',default=None)
    a=ap.parse_args()
    src=a.src or os.path.join(here,'releases','dev.orig.html')
    out=a.out or os.path.join(here,'releases','dev.html')
    zm=os.path.join(here,'translations','_zh_map.py')
    rules=parse_zh_map(zm) if os.path.exists(zm) else []
    rules+=EXTRA
    c=open(src,encoding='utf-8',errors='ignore').read()
    n=0; miss=[]
    for old,new in rules:
        k=c.count(old)
        if k: c=c.replace(old,new); n+=k
        else: miss.append(old)
    os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w',encoding='utf-8').write(c)
    zh=sum(1 for ch in c if '\u4e00'<=ch<='\u9fff')
    print(f'应用规则 {len(rules)} 条, 命中 {n} 处; 中文字符={zh}')
    print(f'输出: {out}')
    if miss: print('未命中 %d 条: %s'%(len(miss),miss[:8]))

if __name__=='__main__':
    main()
