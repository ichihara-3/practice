#!/usr/bin/env bash -eu

BASEDIR="$(cd "$(dirname "$(readlink $0)")/../"; pwd)"
today="$(date "+%Y-%m-%d")"

cd "${BASEDIR}"

echo "Today is : ${today}"
echo "--------------------------------"
mkdir -p "${today}"

if ! [[ -f "${today}/README.md" ]]; then
  echo "# ${today}" > "${today}/README.md"
fi

echo "Ready to work!"
