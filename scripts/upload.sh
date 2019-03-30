#!/bin/bash

LOCAL='./'
REMOTE='/opt/swiper'

USER='root'
HOST='47.102.223.108'

# 上传
rsync -crvP --exclude={.git,.venv,logs,__pycache__} $LOCAL $USER@$HOST:$REMOTE/

# 远程调用重启脚本
ssh $USER@$HOST "$REMOTE/scripts/restart.sh"
