#!/bin/bash

# wce.sh start -- start to Write Code Everyday Session
# wce.sh finish -- finish the session, commit and push to GitHub
# wce.sh suspend -- suspend the session, git stash the changes
# wce.sh resume -- resume the session, git stash pop the changes
# wce.sh status -- show the status of the session
# wce.sh info -- show the info of all sessions

WCE_FILE="$HOME/.wce"
WCE_SUSPEND_FILE="$HOME/.wce_suspend"
TODAY="$(date +%Y-%m-%d)"
PS1_ORIGINAL="${PS1}"

function help() {
    echo "Usage: wce.sh [start|finish|suspend|resume|status|info]"
    exit 1
}

function start() {
    if [ -f "${WCE_FILE}" ]; then
        echo "Error: session already started"
        exit 1
    fi
    touch "${WCE_FILE}"
    echo "Today is ${TODAY}"
    echo "Session started"
    export PS1="wce[${TODAY}]: ${PS1_ORIGINAL}"
}

function finish() {
  if [[ ! -f "${WCE_FILE}" ]]; then
      echo "Error: session not started"
      exit 1
  fi
  git add .
  read -r -p "Commit message: " message
  git commit -a -m "wce[${TODAY}]: ${message}"
  # ask wanna push?
  read -r -p "Push to GitHub? [y/N] " response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
      git push
  fi
  echo "Session finished"
  export PS1="${PS1_ORIGINAL}"
}

function suspend() {
  if [[ ! -f "${WCE_FILE}" ]]; then
      echo "Error: session not started"
      exit 1
  fi
  if [[ -f "${WCE_SUSPEND_FILE}" ]]; then
      echo "Error: session already suspended"
      exit 1
  fi
  echo "${TODAY}" > "${WCE_SUSPEND_FILE}"
  git stash
  echo "Session suspended"
  export PS1="${PS1_ORIGINAL}"
}

function resume() {
  if [[ ! -f "${WCE_FILE}" ]]; then
      echo "Error: session not started"
      exit 1
  fi
  if [[ ! -f "${WCE_SUSPEND_FILE}" ]]; then
      echo "Error: session not suspended"
      exit 1
  fi
  TODAY="$(cat "${WCE_SUSPEND_FILE}")"
  rm "${WCE_SUSPEND_FILE}"
  git stash pop
  echo "Session resumed"
}

function main() {
  if [[ $# -eq 0 ]]; then
      help
  fi
  case "$1" in
      start)
          start
          ;;
      finish)
          finish
          ;;
      suspend)
          suspend
          ;;
      resume)
          resume
          ;;
      status)
          status
          ;;
      info)
          info
          ;;
      *)
          help
          ;;
      esac
}

main "$@"
