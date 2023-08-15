#!/usr/bin/env bash -eu

BASEDIR="$(cd "$(dirname "$(readlink $0)")/../"; pwd)"
today="$(date "+%Y-%m-%d")"
targetdate="${today}"
OPTIONS="$(getopt -o c:d:h -- "$@")"

eval set -- "${OPTIONS}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c)
      # copy from other day
      copyfrom="$2"
      shift 2
      ;;
    -d)
      # specify date
      targetdate="$2"
      shift 2
      ;;
    -h)
      # usage
      echo "Usage: $0 [-c <copyfrom>] [-d <targetdate>] [-h]"
      exit 0
      ;;
    *)
      shift
      ;;
  esac
done

cd "${BASEDIR}"

echo "Today is : ${today}"
echo "--------------------------------"
if [[ -n "${copyfrom:-}" ]]; then
  echo "Copy from : ${copyfrom}"
  cp -R "${copyfrom}" "${targetdate}"
  echo "# ${targetdate}" > "${targetdate}/README.md"
else
  echo "Creating directory : ${targetdate}"
  mkdir -p "${targetdate}"
  if ! [[ -f "${targetdate}/README.md" ]]; then
  echo "# ${targetdate}" > "${targetdate}/README.md"
  fi
fi
echo "Ready to work!"
