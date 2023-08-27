#!/bin/bash

# wce.sh start -- start to Write Code Everyday Session
# wce.sh finish -- finish the session, commit and push to GitHub
# wce.sh suspend -- suspend the session, git stash the changes
# wce.sh resume -- resume the session, git stash pop the changes
# wce.sh status -- show the status of the session
# wce.sh info -- show the info of all sessions

WCE_FILE="$HOME/.wce"
WCE_COUNT_FILE="$HOME/.wce_count"
WCE_SUSPEND_FILE="$HOME/.wce_suspend"
WCE_WORKING_DIR="$(cd "$(readlink -f "$(dirname "$0")")/../" || exit 1; pwd)"
TODAY="$(date +%Y-%m-%d)"
PS1_ORIGINAL="${PS1}"

function help() {
    echo "Usage: wce.sh [start|finish|suspend|resume|status|info]"
    exit 1
}

function start() {
    cd "${WCE_WORKING_DIR}" || exit 1
    if [[ -f "${WCE_FILE}" ]]; then
        echo "Error: session already started"
        exit 1
    fi
    echo "${TODAY}" > "${WCE_FILE}"
    if [[ ! -f "${WCE_COUNT_FILE}" ]]; then
        echo "0" > "${WCE_COUNT_FILE}"
        days=0
    fi
    days=$(($(cat "${WCE_COUNT_FILE}") + 1))

    if [[ ! -d "${TODAY}" ]]; then
        mkdir "${TODAY}"
    fi
    if ! [[ -f "${TODAY}/README.md" ]]; then
      echo "# ${TODAY}" > "${TODAY}/README.md"
    fi

    echo "Today is ${TODAY}"
    echo "${days}" > "${WCE_COUNT_FILE}"
    echo "Write Code Everyday: The day ${days}"
    echo "Session started!"
    export PS1="wce[${TODAY}]: ${PS1_ORIGINAL}"
}

function finish() {
  if [[ ! -f "${WCE_FILE}" ]]; then
      echo "Error: session not started"
      exit 1
  fi
  if [[ -f "${WCE_SUSPEND_FILE}" ]]; then
      echo "Error: session suspended"
      exit 1
  fi
  if [[ $(cat "${WCE_FILE}") != "${TODAY}" ]]; then
      echo "Error: session not started today"
      echo "First run 'wce.sh cancel' to cancel the session"
      exit 1
  fi
  git add .
  read -r -p "Commit message: " message
  git commit -a -m "wce[${TODAY}]: ${message}"
  # ask wanna push?
  read -r -p "Push to GitHub? [y/N] " response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then git push
  fi
  echo "Session finished"
  rm "${WCE_FILE}"
  export PS1="${PS1_ORIGINAL}"
}

function cancel() {
  if [[ ! -f "${WCE_FILE}" ]]; then
      echo "Error: session not started"
      exit 1
  fi
  if [[ -f "${WCE_SUSPEND_FILE}" ]]; then
      echo "Error: session suspended"
      exit 1
  fi
  echo "Canceling session: ${TODAY}"
  rm "${WCE_FILE}"
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

function status() {
  if [[ ! -f "${WCE_FILE}" ]]; then
    echo "Not Started"
  elif [[ -f "${WCE_SUSPEND_FILE}" ]]; then
    echo "Suspended"
  else
    echo "Started"
  fi
  echo "Today is ${TODAY}"
  git status
}

function info() {
  if [[ ! -f "${WCE_COUNT_FILE}" ]]; then
    echo "No session info"
    exit 1
  else
    days="$(cat "${WCE_COUNT_FILE}")"
  fi
  echo "Write Code Everyday: The day ${days}"
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
      cancel)
        cancel
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
