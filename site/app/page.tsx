import { CloudShader } from "@/components/cloud-shader";

const REPO = "https://github.com/RahulSinghai606/MICRO1_HACKATHON";
const HERO_VIDEO =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260803_192301_9231ed6b-c55c-4a48-909c-4ebe11cf2e11.mp4";

const kpis = [
  { n: "100%", l: "decision accuracy", s: "vs 81.3% single-prompt baseline" },
  { n: "0", l: "defective invoices approved", s: "baseline silently approved 30%" },
  { n: "−29%", l: "cost per invoice", s: "$0.020 vs $0.028 — and ~0.16% of manual cost" },
  { n: "64", l: "gold-labeled cases", s: "32 main + 32 held-out (seed 43): both 100%" },
];

const pipeline = [
  { t: "OCR", d: "Mistral OCR reads 32 rendered invoice images. Raw output committed for reproducibility." },
  { t: "Extraction agent", d: "LLM turns OCR markdown into strict JSON. Forbidden from 'fixing' numbers — printed numbers are the evidence." },
  { t: "Matching agent", d: "Investigates with deterministic tools: PO lookup, GRN totals across partial deliveries, duplicate search, arithmetic checker. The LLM never does math." },
  { t: "Independent verifier", d: "A deterministic match engine recomputes every check. Disagreement → one feedback round → deterministic evidence wins." },
  { t: "Human sign-off", d: "Approval queue (web UI). Payments post only to a sandbox ledger after a qualified reviewer approves. Then a signed audit packet." },
];

const changelog = [
  { v: "Baseline", r: "81.3% acc · missed 30% of defects", d: "One prompt, full ERP dump. Missed every arithmetic error and both missing goods-receipts. LLMs fail at math and at absence." },
  { v: "v1 · Scoped context", r: "90.6% acc · cost −67%", d: "Extraction agent + retrieve only the referenced PO/GRN/vendor. Needle-in-haystack misses were context failures." },
  { v: "v1b · CoT math — REMOVED", r: "87.5% acc · exact match ↓ to 68.8%", d: "Asked the model to recompute digit by digit. Worse, and 2.2× the cost. Negative result kept runnable in the repo." },
  { v: "v2 · Deterministic tools", r: "100% acc · 0 missed defects", d: "Arithmetic moved out of the model into tools. The single biggest jump." },
  { v: "v3 · Verifier", r: "100% on every metric", d: "Independent engine recomputes everything; fixed the last taxonomy confusions via feedback rounds." },
  { v: "Final · Memory + HITL", r: "100% + human checkpoint", d: "Vendor alias memory, approval queue, sandbox ledger, audit packet an AP manager signs." },
];

function ArrowIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="inline-block">
      <path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function Home() {
  return (
    <main className="min-h-screen bg-[#05070d] text-white antialiased">
      {/* ---------- HERO ---------- */}
      <section className="relative h-screen w-full overflow-hidden">
        <video
          className="absolute inset-0 h-full w-full object-cover"
          src={HERO_VIDEO}
          autoPlay
          loop
          muted
          playsInline
        />
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-[#05070d] via-black/20 to-transparent" />

        <div className="relative z-10 flex h-full flex-col px-5 sm:px-8 lg:px-12">
          <nav className="flex items-center justify-between py-6">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/10 backdrop-blur-lg">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M20 6L9 17l-5-5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <span className="text-lg font-semibold tracking-tight">matchpoint</span>
            </div>
            <div className="hidden items-center gap-1 rounded-full bg-white/10 px-1.5 py-1.5 backdrop-blur-lg md:flex">
              {[["#problem", "Problem"], ["#how", "How it works"], ["#results", "Results"], ["#changelog", "Changelog"]].map(([h, l]) => (
                <a key={h} href={h} className="rounded-full px-4 py-1.5 text-sm font-medium text-white/80 transition-colors hover:bg-white/10 hover:text-white">
                  {l}
                </a>
              ))}
            </div>
            <a
              href={REPO}
              target="_blank"
              rel="noreferrer"
              className="rounded-full px-5 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90"
              style={{ background: "linear-gradient(to bottom, #2B2B2B, #101010)" }}
            >
              View source <ArrowIcon />
            </a>
          </nav>

          <div className="mt-auto flex flex-col gap-8 pb-10 sm:pb-14 lg:flex-row lg:items-end lg:justify-between lg:pb-16">
            <div className="max-w-2xl">
              <p className="mb-4 inline-block rounded-full bg-white/10 px-4 py-1.5 text-xs font-medium uppercase tracking-widest text-white/70 backdrop-blur-lg">
                micro1 Agentic Workflows Hackathon
              </p>
              <h1 className="text-4xl font-semibold leading-[1.08] tracking-tight drop-shadow-[0_2px_20px_rgba(0,0,0,0.75)] sm:text-5xl lg:text-[3.6rem]">
                Agents that close the books.
                <br />
                <span className="text-emerald-300/90">Humans that sign them.</span>
              </h1>
              <p className="mt-5 max-w-xl text-base leading-relaxed text-white/85 drop-shadow-[0_1px_8px_rgba(0,0,0,0.8)]">
                Matchpoint three-way-matches supplier invoices against purchase orders and
                goods receipts — catching the arithmetic errors, phantom deliveries, duplicates
                and swapped bank accounts that a single LLM prompt silently approves.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <a
                  href={`${REPO}#readme`}
                  target="_blank"
                  rel="noreferrer"
                  className="rounded-full bg-white px-6 py-3 text-sm font-semibold text-black transition-opacity hover:opacity-90"
                >
                  Read the evidence
                </a>
                <a
                  href="#results"
                  className="rounded-full bg-white/10 px-6 py-3 text-sm font-medium text-white backdrop-blur-lg transition-colors hover:bg-white/20"
                >
                  81.3% → 100%, measured
                </a>
              </div>
            </div>

            <div className="flex flex-col gap-4 sm:flex-row lg:gap-5">
              <div className="flex flex-col justify-between rounded-2xl border border-white/10 bg-black/40 p-5 backdrop-blur-xl sm:w-64 sm:p-6">
                <div className="text-4xl font-semibold tracking-tight text-emerald-300">0 / 20</div>
                <p className="mt-3 text-sm leading-relaxed text-white/70">
                  defective invoices slipped through the final agent — the baseline approved 6 of
                  them, including every arithmetic error.
                </p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/40 p-5 backdrop-blur-xl sm:w-64 sm:p-6">
                <div className="mb-3 flex items-center gap-2">
                  <div className="flex h-6 w-6 items-center justify-center rounded bg-emerald-400 text-xs font-bold text-black">M</div>
                  <span className="text-sm font-semibold">The audit packet</span>
                </div>
                <p className="text-sm leading-relaxed text-white/80">
                  Every flag backed by a deterministic check, every payment behind a human
                  signature — the report an AP specialist actually signs.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ---------- PROBLEM ---------- */}
      <section id="problem" className="mx-auto max-w-5xl px-5 py-24 sm:px-8">
        <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">The bottleneck is real money</h2>
        <div className="mt-10 grid gap-4 sm:grid-cols-3">
          {[
            ["$12.88–19.83", "cost per manually processed invoice", "Ardent Partners, AP Metrics That Matter 2025"],
            ["9.2 days", "average invoice cycle time; over 60% of invoices still need human touch", "Ardent Partners 2025"],
            ["76%", "of US organizations hit by payments fraud in 2025 — over a third of attacks are fake bank-change requests", "AFP Payments Fraud Survey 2026"],
          ].map(([n, l, s]) => (
            <div key={l} className="rounded-2xl border border-white/15 bg-white/[0.07] p-6">
              <div className="text-3xl font-semibold tracking-tight text-emerald-300">{n}</div>
              <p className="mt-2 text-sm leading-relaxed text-white/70">{l}</p>
              <p className="mt-3 text-xs text-white/40">{s}</p>
            </div>
          ))}
        </div>
        <p className="mt-8 max-w-3xl text-base leading-relaxed text-white/70">
          An accounts-payable specialist must match every invoice against the purchase order and
          the goods receipt, then screen duplicates, tax math and remit-to bank details — 10 to 15
          minutes per invoice, hundreds per month. One miss is money that doesn&apos;t come back.
        </p>
      </section>

      {/* ---------- HOW ---------- */}
      <section id="how" className="border-t border-white/5 bg-[#0a101d] py-24">
        <div className="mx-auto max-w-5xl px-5 sm:px-8">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
            Five stages. The LLM never does arithmetic.
          </h2>
          <div className="mt-10 grid gap-4 md:grid-cols-5">
            {pipeline.map((s, i) => (
              <div key={s.t} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <div className="mb-3 flex h-7 w-7 items-center justify-center rounded-full bg-white/10 text-xs font-bold">
                  {i + 1}
                </div>
                <div className="text-sm font-semibold">{s.t}</div>
                <p className="mt-2 text-xs leading-relaxed text-white/60">{s.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------- RESULTS ---------- */}
      <section id="results" className="relative overflow-hidden py-24">
        <div className="absolute inset-0 opacity-50">
          <CloudShader
            className="h-full w-full"
            speed={0.6}
            count={4}
            cloudColor="#3d4f6e"
            skyTopColor="#05070d"
            skyBottomColor="#0d1526"
          />
        </div>
        <div className="relative z-10 mx-auto max-w-5xl px-5 sm:px-8">
        <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">Measured, not vibes</h2>
        <p className="mt-3 max-w-3xl text-white/70">
          Same 32 gold-labeled invoices, same model, same written AP policy for baseline and agent.
          Then a held-out batch (seed 43) the system never saw during development.
        </p>
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {kpis.map((k) => (
            <div key={k.l} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <div className="text-4xl font-semibold tracking-tight">{k.n}</div>
              <div className="mt-1 text-sm font-medium text-white/90">{k.l}</div>
              <p className="mt-2 text-xs leading-relaxed text-white/50">{k.s}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 overflow-x-auto rounded-2xl border border-white/10">
          <table className="w-full min-w-[640px] text-left text-sm">
            <thead className="bg-white/5 text-white/60">
              <tr>
                {["Metric", "Baseline (1 prompt)", "Matchpoint final", "Held-out batch (final)"].map((h) => (
                  <th key={h} className="px-5 py-3 font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {[
                ["Decision accuracy", "81.3%", "100%", "100%"],
                ["Exact match (decision + all codes)", "75.0%", "100%", "100%"],
                ["Discrepancy F1", "0.79", "1.00", "1.00"],
                ["Missed-defect rate", "30%", "0%", "0%"],
                ["False-hold rate (clean invoices)", "0%", "0%", "0%"],
                ["Est. cost per invoice", "$0.028", "$0.020", "$0.020"],
              ].map((row) => (
                <tr key={row[0]}>
                  {row.map((c, i) => (
                    <td key={i} className={"px-5 py-3 " + (i === 0 ? "text-white/70" : i === 1 ? "text-white/50" : "font-semibold")}>
                      {c}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        </div>
      </section>

      {/* ---------- CHANGELOG ---------- */}
      <section id="changelog" className="border-t border-white/5 bg-[#0a101d] py-24">
        <div className="mx-auto max-w-5xl px-5 sm:px-8">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">The changelog is the story</h2>
          <p className="mt-3 max-w-3xl text-white/70">
            Every stage stays runnable (<code className="rounded bg-white/10 px-1.5 py-0.5 text-xs">make agent-v1 … make agent-final</code>),
            every number lives in a committed results file, and full agent trajectories ship with the repo.
          </p>
          <div className="mt-10 space-y-3">
            {changelog.map((c) => (
              <div key={c.v} className="flex flex-col gap-2 rounded-2xl border border-white/10 bg-white/5 p-5 sm:flex-row sm:items-baseline sm:gap-6">
                <div className="w-56 shrink-0 text-sm font-semibold">{c.v}</div>
                <div className="w-64 shrink-0 text-sm text-emerald-300/90">{c.r}</div>
                <p className="text-sm leading-relaxed text-white/60">{c.d}</p>
              </div>
            ))}
          </div>

          <div className="mt-12 rounded-2xl border border-white/10 bg-gradient-to-br from-white/10 to-white/[0.03] p-8">
            <div className="text-xs font-semibold uppercase tracking-widest text-white/40">Hot take</div>
            <p className="mt-3 max-w-3xl text-xl font-medium leading-relaxed">
              The most reliable agent is the one with the smallest possible LLM surface area.
              Every measured gain came from taking a responsibility <em>away</em> from the model —
              and our ablation proved it: extraction plus a for-loop scored the same 100% at a
              fifth of the cost. Spend the LLM only where the world is unstructured.
            </p>
          </div>
        </div>
      </section>

      {/* ---------- FOOTER ---------- */}
      <footer className="mx-auto max-w-5xl px-5 py-16 sm:px-8">
        <div className="flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
          <div>
            <div className="text-lg font-semibold">matchpoint</div>
            <p className="mt-1 text-sm text-white/50">
              Synthetic data only · sandboxed payments · human sign-off on every action.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <a href={REPO} target="_blank" rel="noreferrer" className="rounded-full bg-white/10 px-5 py-2.5 text-sm font-medium backdrop-blur-lg transition-colors hover:bg-white/20">
              GitHub <ArrowIcon />
            </a>
            <a href={`${REPO}/blob/main/REPRODUCE.md`} target="_blank" rel="noreferrer" className="rounded-full bg-white/10 px-5 py-2.5 text-sm font-medium backdrop-blur-lg transition-colors hover:bg-white/20">
              Reproduce it <ArrowIcon />
            </a>
          </div>
        </div>
        <p className="mt-10 text-xs text-white/30">
          Built for the micro1 Agentic Workflows Hackathon. Baseline and agent share the same model,
          policy and evaluation cases; all claims trace to committed evidence files.
        </p>
      </footer>
    </main>
  );
}
