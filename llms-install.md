# SourcedFigures Verify

Informational only. Not investment, legal or tax advice.

## Install

This file is the Cline `llms-install.md` for this public examples repository.
No production origin is recorded here. Replace `{origin}` when one exists.
Do not submit a directory listing from this file.

- Transport: streamable HTTP
- URL: `{origin}/mcp`
- Signup: `POST {origin}/signup` with a JSON body whose only field is `email`
- Header on `tools/call`: `Authorization: Bearer <key>`
- `initialize` and `tools/list` need no key

## Snippets

- `examples/python/check_fact.py`
- `examples/javascript/check_fact.mjs`

Both read `VERIFY_BASE_URL`, `VERIFY_API_KEY`, and `VERIFY_FACTS_FILE`
(default `examples/verify-facts.json`). A fact that does not match exits non-zero.
The key comes from `POST {origin}/signup`, which issues the Free tier.

## Action

`examples/verify-facts` is the composite action named `verify facts`. It runs
the Python snippet. The caller passes `base_url`, `api_key`, and `facts_file`.

```yaml
uses: florida-charter/ap100700-sourcedfigures-verify-examples-template/examples/verify-facts@main
```
