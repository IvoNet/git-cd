#!/usr/bin/env bash

GCD_DIR="${HOME}/.gcd"
CACHE_FILE="${GCD_DIR}/gcd.cache"

GIT_HTTP_LOW_SPEED_LIMIT=1000
GIT_HTTP_LOW_SPEED_TIME=5

# first zap all unknown git
../bin/gcd-zap

if [[ ! -f  "${CACHE_FILE}" ]]; then
    echo "No gcd cache file was found..."
    exit 1
fi

IDX=0
while IFS= read -r line
do
  ((IDX++))
  echo "$IDX ${line}"
  if [[ -d "${line}/.git" ]]; then
      git -C "${line}" ls-remote 2>&1 >/dev/null
      if [[ $? -eq 0 ]]; then
        git -C "${line}" pull &
      fi
  fi
  if ((IDX > 7)); then
      IDX=0
      wait
  fi
done < "${CACHE_FILE}"
