#!/usr/bin/env bash
# 汉化回退: 恢复到汉化前镜像 tag
# 用法: bash rollback_zh.sh <备份tag>
set -euo pipefail
IMAGE="${IMAGE:-homeassistant/aarch64-addon-configurator:6.0.0}"
CONTAINER="${CONTAINER:-app_core_configurator}"
BACKUP="${1:?用法: rollback_zh.sh <备份tag> 例: homeassistant/aarch64-addon-configurator:6.0.0.pre-zh-20260830-2330}"
docker tag "$BACKUP" "$IMAGE"
echo "已回退镜像 tag → $IMAGE (来自 $BACKUP)"
echo "重启 addon 生效: docker restart $CONTAINER, 或 HA 界面重启 File editor"
