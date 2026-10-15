[![CI](https://github.com/florida-charter/ap100700-sourcedfigures-verify-examples-template/actions/workflows/check.yml/badge.svg)](https://github.com/florida-charter/ap100700-sourcedfigures-verify-examples-template/actions/workflows/check.yml)
[![Maintained by Florida Charter Group LLC](https://img.shields.io/badge/Maintained%20by-Florida%20Charter%20Group%20LLC-172238?labelColor=172238&color=D8B55C)](https://github.com/orgs/florida-charter/repositories)

# SourcedFigures Verify examples (`ap100700-sourcedfigures-verify-examples-template`)

Copy-paste calls for [SourcedFigures Verify](https://github.com/florida-charter/ap100700-sourcedfigures-verify-api-service).
A Free key from `POST {origin}/signup` checks a claim the caller already has
an official record for. The snippets print the period, the claimed value, and
the verdict. They do not print the email or the key.

Informational only. Not investment, legal or tax advice.

## Files

| Path | Role |
| --- | --- |
| `llms-install.md` | Cline install note. `{origin}` is not filled in. |
| `examples/python/check_fact.py` | Python `tools/call` for `check_fact`. |
| `examples/javascript/check_fact.mjs` | The same call in JavaScript. |
| `examples/verify-facts/action.yml` | Composite action named `verify facts`. |
| `examples/verify-facts.json` | Sample H.15 10-year cell, 5.28 percent on 2026-10-07. |

## Run

```bash
export VERIFY_BASE_URL="{origin}"
export VERIFY_API_KEY="<free key>"
python3 examples/python/check_fact.py
node examples/javascript/check_fact.mjs
```

`VERIFY_FACTS_FILE` defaults to `examples/verify-facts.json`. A verdict other than
`matches`, or a rejected call, exits non-zero.

## Action

```yaml
uses: florida-charter/ap100700-sourcedfigures-verify-examples-template/examples/verify-facts@main
with:
  base_url: ${{ vars.VERIFY_BASE_URL }}
  api_key: ${{ secrets.VERIFY_API_KEY }}
```

`examples/verify-facts/workflow-example.yml` is a sample. It is not registered
under `.github/workflows` in this repository.

&copy;2026 Florida Charter Group LLC.
