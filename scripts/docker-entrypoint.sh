#!/usr/bin/env bash

set -euo pipefail

WORKSPACE=/workspace
ZMK_DIR="$WORKSPACE/zmk"

cd $ZMK_DIR

if [ ! -d ".west" ]; then
    echo "Initializing west workspace..."
    west init -l app && west update
fi

west zephyr-export

if [ -f "build_trackball_local.sh" ]; then
    bash $WORKSPACE/scripts/build_trackball_local.sh
else
    bash $WORKSPACE/scripts/build_trackball.sh
fi

FIRMWARE="$ZMK_DIR/build/zephyr/zmk.uf2"

echo ""
echo "Build successful!"
echo "Firmware: $FIRMWARE"

if [ -d "/output" ]; then
    cp "$FIRMWARE" /output/zmk.uf2
    echo "Firmware copied to /output/zmk.uf2"
fi
echo ""
