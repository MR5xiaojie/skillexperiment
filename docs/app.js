"use strict";

(() => {
  const metricKeys = ["content", "format", "coverage", "step", "evidence", "tool", "negative", "boundary", "termination"];
  const search = document.querySelector("#model-search");
  const harness = document.querySelector("#harness-filter");
  const metricSelect = document.querySelector("#metric-select");
  const tableHead = document.querySelector("#table-head");
  const tableBody = document.querySelector("#table-body");
  const message = document.querySelector("#data-message");
  const count = document.querySelector("#result-count");
  const chart = document.querySelector("#metric-chart");
  const reset = document.querySelector("#reset-filters");
  let metrics = [];
  let configurations = [];
  let sortKey = "";
  let sortDirection = "descending";

  function element(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  }

  function formatScore(value) {
    return `${value.toFixed(2)}%`;
  }

  function harnessClass(value) {
    return value === "Codex" ? "codex" : "claude-code";
  }

  function buildHeaders() {
    tableHead.replaceChildren();
    const columns = [{ key: "model", label: "Model" }, { key: "harness", label: "Harness" }, ...metrics];
    for (const column of columns) {
      const th = element("th");
      th.scope = "col";
      th.dataset.key = column.key;
      th.setAttribute("aria-sort", "none");
      const button = element("button");
      button.type = "button";
      button.append(document.createTextNode(column.label));
      const indicator = element("span", "sort-icon", "↕");
      indicator.setAttribute("aria-hidden", "true");
      button.append(indicator);
      button.setAttribute("aria-label", `Sort by ${column.label}`);
      if (column.description) button.title = column.description;
      button.addEventListener("click", () => {
        sortDirection = sortKey === column.key && sortDirection === "descending" ? "ascending" : "descending";
        if (sortKey !== column.key && ["model", "harness"].includes(column.key)) sortDirection = "ascending";
        sortKey = column.key;
        render();
      });
      th.append(button);
      tableHead.append(th);
    }
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    const filtered = configurations.filter(row => row.model.toLocaleLowerCase().includes(query) && (!harness.value || row.harness === harness.value));
    const rows = [...filtered];
    if (sortKey) rows.sort((a, b) => {
      const comparison = typeof a[sortKey] === "number" ? a[sortKey] - b[sortKey] : a[sortKey].localeCompare(b[sortKey]);
      return sortDirection === "ascending" ? comparison : -comparison;
    });
    tableBody.replaceChildren();
    for (const row of rows) {
      const tr = element("tr");
      const modelCell = element("td", "", row.model);
      const harnessCell = element("td");
      harnessCell.append(element("span", `harness-badge ${harnessClass(row.harness)}`, row.harness));
      tr.append(modelCell, harnessCell);
      for (const metric of metrics) {
        const td = element("td");
        const value = element("span", "score-value", formatScore(row[metric.key]));
        value.style.setProperty("--tint", String(0.025 + row[metric.key] / 100 * 0.25));
        td.append(value);
        tr.append(td);
      }
      tableBody.append(tr);
    }
    for (const th of tableHead.children) {
      const active = th.dataset.key === sortKey;
      th.setAttribute("aria-sort", active ? sortDirection : "none");
      th.querySelector(".sort-icon").textContent = active ? (sortDirection === "ascending" ? "↑" : "↓") : "↕";
    }
    const sortedMetric = metrics.find(metric => metric.key === sortKey)?.label || (sortKey === "model" ? "Model" : "Harness");
    count.textContent = `${rows.length} of ${configurations.length} configurations${sortKey ? ` · ${sortedMetric}, ${sortDirection}` : ""}`;
    message.hidden = rows.length > 0;
    message.textContent = "No configurations match these filters. Try another model or reset the view.";
    reset.hidden = !query && !harness.value && !sortKey;
    renderChart(filtered);
  }

  function renderChart(rows) {
    const key = metricSelect.value;
    const metric = metrics.find(item => item.key === key);
    if (!metric) return;
    document.querySelector("#metric-description").textContent = metric.description;
    chart.setAttribute("aria-label", `${metric.label} scores by configuration`);
    chart.replaceChildren();
    if (!rows.length) {
      chart.append(element("p", "chart-empty", "No matching configurations to compare."));
      return;
    }
    for (const row of [...rows].sort((a, b) => b[key] - a[key])) {
      const item = element("div", "chart-row");
      item.setAttribute("role", "listitem");
      item.setAttribute("aria-label", `${row.model}, ${row.harness}: ${formatScore(row[key])}`);
      const label = element("div", "chart-label", row.model);
      label.append(element("small", "", row.harness));
      const track = element("div", "bar-track");
      track.setAttribute("aria-hidden", "true");
      const bar = element("div", `bar-fill ${harnessClass(row.harness)}`);
      bar.style.width = `${row[key]}%`;
      track.append(bar);
      item.append(label, track, element("span", "chart-value", formatScore(row[key])));
      chart.append(item);
    }
  }

  async function initialize() {
    try {
      const response = await fetch("./data/scores.json");
      if (!response.ok) throw new Error(`Data request failed (${response.status})`);
      const data = await response.json();
      if (!Array.isArray(data.metrics) || !Array.isArray(data.configurations) || data.configurations.length === 0) throw new Error("Unexpected score data");
      metrics = metricKeys.map(key => data.metrics.find(metric => metric.key === key));
      if (metrics.some(metric => !metric || typeof metric.label !== "string" || typeof metric.description !== "string")) throw new Error("Missing metric definitions");
      configurations = data.configurations;
      if (configurations.some(row => typeof row.model !== "string" || !["Codex", "Claude Code"].includes(row.harness) || metricKeys.some(key => typeof row[key] !== "number" || !Number.isFinite(row[key]) || row[key] < 0 || row[key] > 100))) throw new Error("Invalid score values");
      document.querySelectorAll('[data-configuration-count]').forEach(node => { node.textContent = configurations.length; });
      metricSelect.replaceChildren();
      for (const metric of metrics) {
        const option = element("option", "", metric.label);
        option.value = metric.key;
        metricSelect.append(option);
      }
      buildHeaders();
      search.addEventListener("input", render);
      harness.addEventListener("change", render);
      metricSelect.addEventListener("change", render);
      reset.addEventListener("click", () => {
        search.value = "";
        harness.value = "";
        sortKey = "";
        sortDirection = "descending";
        render();
        search.focus();
      });
      render();
    } catch (error) {
      count.textContent = "Score data unavailable";
      message.hidden = false;
      message.replaceChildren(document.createTextNode("The interactive results could not load. "));
      const link = element("a", "", "Download the published CSV");
      link.href = "./data/configuration_scores.csv";
      message.append(link, document.createTextNode(" to see every score."));
      search.disabled = true;
      harness.disabled = true;
      metricSelect.disabled = true;
      chart.append(element("p", "chart-empty", "The comparison will appear when score data is available."));
      console.error("Unable to load configuration scores:", error);
    }
  }

  initialize();
})();
