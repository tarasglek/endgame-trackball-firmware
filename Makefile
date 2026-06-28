KEYMAP_DOCS_DIR ?= docs/generated
KEYMAP_FILE ?= endgame-trackball-config/config/efogtech_trackball_0.keymap
KEYMAP_YAML ?= $(KEYMAP_DOCS_DIR)/efogtech_trackball_0.yaml
KEYMAP_SVG ?= $(KEYMAP_DOCS_DIR)/efogtech_trackball_0.svg
KEYMAP_DTS_LAYOUT ?= endgame-trackball-config/boards/arm/efogtech_trackball_0/buttons.dtsi

.PHONY: keymap-yaml keymap-svg keymap-docs

keymap-yaml:
	mkdir -p $(KEYMAP_DOCS_DIR)
	uvx --from keymap-drawer keymap parse -z $(KEYMAP_FILE) > $(KEYMAP_YAML)

keymap-svg: keymap-yaml
	uvx --from keymap-drawer keymap draw --dts-layout $(KEYMAP_DTS_LAYOUT) $(KEYMAP_YAML) > $(KEYMAP_SVG)

keymap-docs: keymap-svg
