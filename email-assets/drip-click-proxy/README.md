# Axis lead-drip click proxy

## Live URL (after Netlify deploy on axis-offers-59)
`https://offers.axisspineandsport.com/go?lid={recId}&clinic={gilbert|phoenix|tempe}&step={e1|e2|e3}`

## Behavior
1. PATCH Airtable Advertising Leads `Clicked Scheduling Link` = true
2. 302 to city scheduler with UTMs (`utm_source=email&utm_medium=drip&utm_campaign=lead-{step}&utm_content={lid}&utm_term={clinic}`)

## Deploy
1. Netlify site: **axis-offers-59** (offers.axisspineandsport.com)
2. Upload folder from workspace `files/ops/drip-attribution/drip-click-proxy/` (or zip `axis-drip-click-proxy.zip`)
   - Keep existing offer LP files if you merge deploys; this package is proxy-only and will replace site root if dropped alone. Prefer adding `netlify/functions/go.js` + redirects to the existing offers deploy.
3. Site settings → Environment variables:
   - `AIRTABLE_TOKEN` = PAT with `data.records:write` on base `appbrqCxWYmOjiWDk`
   - optional `AIRTABLE_BASE_ID=appbrqCxWYmOjiWDk`
   - optional `AIRTABLE_TABLE_ID=tblqBRg8stRWVEusj`
4. Test: `/go?lid=recXXXX&clinic=phoenix&step=e1&debug=1` → JSON with `clickResult` and `finalUrl`

## Function source
`go.js` in this folder (same as workspace files/ops/drip-attribution/drip-click-proxy/netlify/functions/go.js)
