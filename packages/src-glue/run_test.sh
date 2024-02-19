#!/bin/bash
if [ "$(uname)" == 'Darwin' ]; then
  shopt -s expand_aliases
  alias docker='finch'
elif [ "$(expr substr $(uname -s) 1 5)" == 'Linux' ]; then
  echo "Linux"
else
  echo "Your platform ($(uname -a)) is not supported."
  exit 1
fi

docker compose exec -T -u glue_user -w /home/glue_user/workspace/jupyter_workspace glue.dev.summary bash -c "\
  /home/glue_user/.local/bin/pytest $1"
