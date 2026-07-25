import assert from "node:assert/strict";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the complete academic dashboard", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /Facebook Engagement &amp; Network Visual Analytics/);
  assert.match(html, /S\. M\. Monowar Kayser/);
  assert.match(html, /7,050/);
  assert.match(html, /network_color_toggle_dashboard\.html/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
});

test("published assets are present", async () => {
  const { access } = await import("node:fs/promises");
  const required = [
    "public/report.pdf",
    "public/images/g_ppi_layout_comparison.png",
    "public/interactive/network_color_toggle_dashboard.html",
    "public/interactive/domain_graph.html",
  ];
  await Promise.all(required.map((path) => access(new URL(path, projectRoot))));
});
