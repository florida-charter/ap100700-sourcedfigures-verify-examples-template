#!/usr/bin/env bash
set -euo pipefail

test -f .fcg/repo.yaml
test -f LICENSE
test -f CLAUDE.md
test -f llms-install.md
test -f .github/dependabot.yml
grep -q 'All rights reserved' LICENSE
grep -q 'No license is granted' LICENSE
grep -q 'Florida Charter Group LLC' LICENSE
grep -q 'package-ecosystem: "github-actions"' .github/dependabot.yml
grep -q 'Informational only. Not investment, legal or tax advice.' llms-install.md

repository=${GITHUB_REPOSITORY:-$(git remote get-url origin)}
repo_name=${repository##*/}
repo_name=${repo_name%.git}
ap_id=$(printf '%s' "$repo_name" | sed -E 's/^(ap[0-9]+).*/\1/' | tr '[:lower:]' '[:upper:]')
test "${repo_name##*-}" = template
grep -Fqx "ap_id: ${ap_id}" .fcg/repo.yaml
grep -Fqx "repo: ${repo_name}" .fcg/repo.yaml
grep -Fqx 'type: template' .fcg/repo.yaml
python3 scripts/damm_id.py verify AP100700
test "$(python3 scripts/damm_id.py check 10070)" = "100700"
