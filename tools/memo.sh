#!/usr/bin/env bash

# date command is different between GNU and BSD
# GNU: date "+%Y-%m-%d" -d "1 day ago"
# BSD: date -v-1d "+%Y-%m-%d"
function get_yesterday() {
    if [[ "$(uname)" == "Darwin" ]]; then
        date -v-1d "+%Y-%m-%d"
    else
        date "+%Y-%m-%d" -d "1 day ago"
    fi
}

# variables
today="$(date "+%Y-%m-%d")"
yesterday="$(get_yesterday)"
directory="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)/memo"
filename="${directory}/${today}.md"
yesterdayfilename="${directory}/${yesterday}.md"


function usage() {
  echo "Usage: memo.sh [start|save]"
  exit 1
}


function start() {
  if [[ ! -d "${directory}" ]]; then
      mkdir -p "${directory}"
  fi

  if [[ ! -f "${filename}" ]]; then
      touch "${filename}"

    # copy file if yesterday file exists
    # so that you can write memo from yesterday

    if [[ -f "${yesterdayfilename}" ]]; then
        echo "## ${yesterday}" >> "${filename}"
        cat "${yesterdayfilename}" >> "${filename}"
    fi
  fi

  vim "${filename}"

  save
}

function save() {
  if [[ ! -f "${filename}" ]]; then
      echo "No memo file for today"
      exit 1
  fi

  git add "${filename}"
  git commit -m "Add memo for ${today}"
  git push origin main
}


function main() {
  if [[ "$1" == "start" ]] || [[ -z "$1" ]] ; then
      start
  elif [[ "$1" == "save" ]]; then
      save
  else
    echo "Invalid argument"
    usage
  fi
}


main "$@"
