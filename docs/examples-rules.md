# Examples and the verify-facts action

Python `examples/python/check_fact.py` and JavaScript
`examples/javascript/check_fact.mjs` call `POST /mcp` method `tools/call`
name `check_fact`. The key comes from `POST /signup` on the Free tier. The
caller supplies the official record. The snippets do not fetch a source
agency and do not print the email or the key.

`llms-install.md` at the repository root is the Cline install note. No
production origin is written down. Directory listings are not submitted
from this repository.

`examples/verify-facts/action.yml` is the composite action named
`verify facts`. It runs the Python snippet. Exit status is non-zero when
any verdict is not `matches` or the host rejects the call. The sample file
is `examples/verify-facts.json` and uses the H.15 10-year cell 5.28 percent
on 2026-10-07. `examples/verify-facts/workflow-example.yml` is a sample and
is not registered under `.github/workflows`.

The Free-tier run of these same snippets is `tests/test_examples.py` in
`ap100700-sourcedfigures-verify-api-service`. That test signs up a Free key
on the local app and runs the Python snippet, the JavaScript snippet, and
the action command.
