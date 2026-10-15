// Call check_fact on the Free tier. The caller supplies the official record.

import { readFile } from "node:fs/promises";

const base = process.env.VERIFY_BASE_URL;
const key = process.env.VERIFY_API_KEY;
const file = process.env.VERIFY_FACTS_FILE ?? "examples/verify-facts.json";

if (!base || !key) {
  console.error("VERIFY_BASE_URL and VERIFY_API_KEY are required");
  process.exit(1);
}

const facts = JSON.parse(await readFile(file, "utf8"));
if (!Array.isArray(facts) || facts.length === 0) {
  console.error("facts file is empty");
  process.exit(1);
}

let failed = 0;
for (const fact of facts) {
  const response = await fetch(`${base.replace(/\/$/, "")}/mcp`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${key}`,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "check_fact", arguments: fact },
    }),
  });
  if (!response.ok) {
    console.error(`HTTP ${response.status}: ${await response.text()}`);
    process.exit(1);
  }
  const payload = await response.json();
  const result = payload.result;
  if (result.isError) {
    console.error(result.content[0].text);
    process.exit(1);
  }
  const verdict = String(result.structuredContent.verdict ?? "");
  const period = String(fact.claim_period ?? "");
  const value = String(fact.claim_value ?? "");
  console.log(`${period} ${value} ${verdict}`.trim());
  if (verdict !== "matches") {
    failed += 1;
  }
}
process.exit(failed === 0 ? 0 : 1);
