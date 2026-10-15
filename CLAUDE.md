# CLAUDE.md — `ap100700-sourcedfigures-verify-examples-template`

Public examples for SourcedFigures Verify (FCG AP100700, Damm-valid). Callers
copy the Python snippet, the JavaScript snippet, and the `verify facts`
composite action. This repository does not serve traffic and does not deploy.

The suffix is `-template` because a caller clones or copies these files as a
starting point. It is not a service and it has no OpenTofu.

## State now

`llms-install.md` is the Cline install note. `{origin}` stays unfilled. No
production host is recorded. Nothing in this repository is submitted to a
directory.

The snippets and the action are the same programs exercised by
`tests/test_examples.py` in `ap100700-sourcedfigures-verify-api-service`.
That test signs up a Free key and requires a `matches` verdict.

## Before any change

1. A Jira ticket in the **`DEV`** project.
2. Branch from `main`: `feature/DEV-<n>-<short-slug>`.
3. Commits: `feature/DEV-<n>: [verify] <short description>`.

## Hard rules

- **No `.tf` files and no `infra/` directory.**
- **No secrets, no API key, and no production origin in the tree.**
- Fork pull requests do not run on the self-hosted runner. The `check` job
  runs only for a push, or for a pull request whose head is this repository.
- Verdict wording stays `matches`, `does_not_match`, or `unverifiable`.

## Layout

```
.fcg/repo.yaml                 # ap_id, repo, type: template
llms-install.md                # Cline install note
examples/python/check_fact.py
examples/javascript/check_fact.mjs
examples/verify-facts/         # composite action and a sample workflow
docs/examples-rules.md
scripts/damm_id.py
```

## Commands

```bash
python3 scripts/damm_id.py verify AP100700
prek run --all-files
```

&copy;2026 Florida Charter Group LLC.
