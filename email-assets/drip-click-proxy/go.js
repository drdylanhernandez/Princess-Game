const SCHEDULERS = {
  gilbert: "https://www.gilbert.axisspineandsport.com/schedule-an-appointment-gilbert/",
  phoenix: "https://www.phoenix.axisspineandsport.com/schedule-an-appointment-phoenix/",
  tempe: "https://www.tempe.axisspineandsport.com/schedule-an-appointment-tempe/",
};

const FIELD_CLICKED = "Clicked Scheduling Link";

function pickScheduler(clinic, dest) {
  if (dest && /^https:\/\/(www\.)?(gilbert|phoenix|tempe)\.axisspineandsport\.com\//i.test(dest)) {
    return dest;
  }
  const key = String(clinic || "").toLowerCase().trim();
  return SCHEDULERS[key] || SCHEDULERS.phoenix;
}

function appendUtm(url, params) {
  try {
    const u = new URL(url);
    for (const [k, v] of Object.entries(params)) {
      if (v) u.searchParams.set(k, v);
    }
    return u.toString();
  } catch {
    return url;
  }
}

async function markClicked(lid) {
  const token = process.env.AIRTABLE_TOKEN;
  const base = process.env.AIRTABLE_BASE_ID || "appbrqCxWYmOjiWDk";
  const table = process.env.AIRTABLE_TABLE_ID || "tblqBRg8stRWVEusj";
  if (!token || !lid || !/^rec[a-zA-Z0-9]+$/.test(lid)) {
    return { ok: false, reason: !token ? "no_token" : "bad_lid" };
  }
  const url = `https://api.airtable.com/v0/${base}/${table}/${lid}`;
  const res = await fetch(url, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ fields: { [FIELD_CLICKED]: true } }),
  });
  if (!res.ok) {
    const text = await res.text();
    return { ok: false, reason: `airtable_${res.status}`, detail: text.slice(0, 200) };
  }
  return { ok: true };
}

exports.handler = async (event) => {
  const q = event.queryStringParameters || {};
  const lid = (q.lid || q.lead || q.id || "").trim();
  const clinic = (q.clinic || q.city || q.loc || "phoenix").trim();
  const step = (q.step || q.e || "e1").trim().toLowerCase();
  const dest = q.dest || "";

  let clickResult = { ok: false, reason: "skipped" };
  try {
    clickResult = await markClicked(lid);
  } catch (e) {
    clickResult = { ok: false, reason: "exception", detail: String(e).slice(0, 120) };
  }

  const baseSched = pickScheduler(clinic, dest);
  const finalUrl = appendUtm(baseSched, {
    utm_source: "email",
    utm_medium: "drip",
    utm_campaign: `lead-${step}`,
    utm_content: lid || "unknown",
    utm_term: clinic.toLowerCase(),
  });

  if (q.debug === "1") {
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ finalUrl, clickResult, lid, clinic, step }),
    };
  }

  return {
    statusCode: 302,
    headers: {
      Location: finalUrl,
      "Cache-Control": "no-store",
    },
    body: "",
  };
};
