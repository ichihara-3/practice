#!/usr/bin/env bash
# Write Code Everyday
# ceating a directory with today's date and open it in Vim
# Today is : 2023-08-19
# --------------------------------
# Creating directory : 2023-08-19
# Ready to work!

VERSION="0.0.1"


BASEDIR="$(cd "$(dirname "$0")/../" || exit 1; pwd)"

cd "${BASEDIR}"
echo "Let's start today's exercise!"

# read options from args
whle IFS= read -r -d '' arg; do
  case "$arg" in
    -h|--help)
      echo "Usage: wce.sh [OPTION]..."
      echo "Write Code Everyday"
      echo "  -h, --help      display this help and exit"
      echo "  -v, --version   output version information and exit"
      exit 0
      ;;
    -v|--version)
      echo "Write Code Everyday ${VERSION}"
      exit 0
      ;;
    copy)
      echo "copying..."
      if [[ $2 == "" ]]; then
        # yesterday's date
        copyfrom="$(date -v-1d +%Y-%m-%d)"
      else
        copyfrom="$2"
      fi
      shift 2
      ;;
    *)
      echo "wce.sh: invalid option -- '$arg'"
      echo "Try 'wce.sh --help' for more information."
      exit 1
      ;;
  esac
done < <(printf '%s\0' "$@")

# get today's date
today="$(date +%Y-%m-%d)"
