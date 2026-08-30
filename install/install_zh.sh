#!/usr/bin/env bash
# =====================================================================
# hass-configurator 汉化安装脚本
# 用法: sudo bash install_zh.sh
# 依赖: docker; 可选 supervisor (自动探测)
# =====================================================================
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTAINER="${CONTAINER:-app_core_configurator}"
IMAGE="${IMAGE:-homeassistant/aarch64-addon-configurator:6.0.0}"
SRC_DH="$HERE/releases/dev.html"
PKG=/usr/lib/python3.12/site-packages/hass_configurator/dev.html

cecho(){ printf "\033[1;32m%s\033[0m\n" "$*"; }
[ -f "$SRC_DH" ] || { echo "缺少 $SRC_DH"; exit 1; }
command -v docker >/dev/null || { echo "未安装 docker"; exit 1; }
docker ps --format '{{.Names}}' | grep -qx "$CONTAINER" || {
  echo "未找到容器 $CONTAINER(确认 addon 已在 HA 运行)"; exit 1; }

TS="$(date +%Y%m%d-%H%M%S)"
BACKUP="${IMAGE}.pre-zh-${TS}"
cecho "① 备份当前镜像 tag → $BACKUP"
docker tag "$IMAGE" "$BACKUP" || warn

cecho "② 注入汉化 dev.html → 容器 $CONTAINER"
docker cp "$SRC_DH" "$CONTAINER:$PKG"
docker exec "$CONTAINER" sh -c "echo 容器内中文字符:\$(grep -oE '[一-龥]' '$PKG' | wc -l)"

cecho "③ docker commit 覆盖镜像 tag $IMAGE (持久化, 重启不丢)"
docker commit -m "hass-configurator zh-CN 汉化 $(date +%F) $(hostname)" -a assistant \
  "$CONTAINER" "${IMAGE}.zh" >/dev/null
docker tag "${IMAGE}.zh" "$IMAGE"

cecho "④ 重启 addon (core_configurator)"
TOK="$(docker exec hassio_supervisor sh -c 'cat /data/homeassistant.json' 2>/dev/null \
  | python3 -c "import sys,json;print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || true)"
if [ -n "$TOK" ]; then
  curl -s -X POST http://172.30.32.2:80/addons/core_configurator/restart \
    -H "Authorization: Bearer $TOK" >/dev/null || echo "重启请求失败, 请手动在 HA 重启 addon"
  sleep 12
fi

cecho "⑤ 验证"
docker ps --format '{{.Names}}\t{{.Status}}' | grep "$CONTAINER" || true
docker exec "$CONTAINER" sh -c "echo 最终中文字符:\$(grep -oE '[一-龥]' '$PKG' | wc -l)" || true
cecho "✅ 完成! 回退: bash rollback_zh.sh $BACKUP"
cecho "   重启 addon: docker restart $CONTAINER (或 HA 界面重启 File editor)"
