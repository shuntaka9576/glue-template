#/bin/bash
RYE_VERSION=0.24.0
curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
source "$HOME/.rye/env"
rye config --set-bool behavior.use-uv=true
