# dooby-fbi-origin-timeline — claims red-team

`/analyze-claims` pass (claude mode) over `dooby-fbi-origin-timeline.md`. Grades the load-bearing
*truth-claims* (not the verbatim quotes — those are mechanically checked by
`scripts/agentic/verify_quotes_clips.py`, currently 0-FAIL). Advisory only; source doc unchanged.

**teal;deer:** the doc is strong where it's **quote-grounded** (H1/H3/H4 descriptions) or
**primary-sourced** (H2 pipeline mechanics, 764 reality) — those are A/B. Every attackable seam is
the *same shape*: **inferring fabrication or intent from absence of evidence** (Markle
"embellishment," CCleaner "implausible," police→FBI "escalation," "no FBI portal exists"). None are
wrong, but each overstates a notch past what the evidence licenses. Fix = downgrade absence-of-
evidence from "likely false" to "unverified/unsupported," and label intent-reads as inferences.
Do that & the doc is unembarrassable.

## triage
- 🔴 high-risk (fix before deploying): **C2** (H2 "no FBI secure portal — is not a thing")
- 🟡 medium: **C5** (Markle "likely embellishment"), **C6** (CCleaner "FBI wouldn't"), **C4** (police→FBI "drift" as deliberate)
- 🟢 low / solid: **C1** (H1 possession), **C3** (H3 proof loop), **C7** (764 real), **C8** (2022 antecedent)

---

## per-claim

### C2 — 🔴 "the FBI provides no secure portal for civilians to upload CSAM; the pipeline is backwards"
- **support:** primary sources — NCMEC Take It Down hashes on-device & never uploads the image ([FAQ](https://takeitdown.ncmec.org/faq/)); CyberTipline is the public intake ([report.cybertip.org](https://report.cybertip.org/)); FBI public reporting is tips.fbi.gov / 1-800-CALL-FBI, not a CSAM upload channel. Take It Down / CyberTipline doing the *opposite* of what he describes is solidly sourced.
- **refutation / attack:** "no FBI secure portal exists for a civilian" is an **unprovable negative**. In a live investigation an agent *can* set up a secure transfer with a cooperating witness — rare, but you can't prove it never happens. An opponent says "you don't know what the FBI did in his specific case." → you've overclaimed.
- **fallacy:** appeal to ignorance (absence of a documented path ≠ proof none existed for him).
- **grade:** B+ (would be A if scoped to the documented channels).
- **fix:** change "is not a thing" → **"is not a documented or standard intake path — the public channels are the CyberTipline / tips.fbi.gov, and Take It Down by design never transmits the image."** Keep the verified mechanics; drop the absolute negative.

### C5 — 🟡 "the Meghan-Markle UK-arrest credit is unverified, likely embellishment"
- **support:** real far-right threats against Markle + UK prosecutions exist (CBS / Neil Basu); real UK arrests of 764-adjacent extremists exist (Finnigan). No public record connects *Dooby* to them.
- **refutation:** "likely embellishment" leans on absence of evidence — the arrests he means could be real but not publicly attributable to a private tipster. Calling it "likely embellishment" is a stronger claim than "unverified," and it's the one he'd attack.
- **grade:** B (the *unverified* part is A; the *likely-embellishment* characterization is C).
- **fix:** keep "unverified — no public record links him to it"; **drop or soften "likely embellishment"** to "treat as unsupported until a name/source surfaces." (Same fix already applied conceptually to the 105-year claim — be consistent.)

### C6 — 🟡 "CCleaner-as-FBI-directed-wipe is implausible"
- **support:** CCleaner is a consumer tool, not forensic; no FBI rec; forensics firms recover evidence despite it ([Magnet](https://www.magnetforensics.com/resources/oh-no-the-suspect-ran-ccleaner-to-get-rid-of-the-evidence/)).
- **refutation:** "the FBI wouldn't coach a civilian to destroy CSAM" is a **plausibility inference**, not a documented fact. Defensible, but state it as inference.
- **grade:** B.
- **fix:** label the "FBI wouldn't" line `(inference)`; the tool-mismatch (consumer vs forensic) is the harder, keep-it point.

### C4 — 🟡 "police (2022/2025) → FBI (2026): a deliberate escalation/drift"
- **support:** quote-verified — 2022 "law enforcement," Dec 2025 "police," June 2026 "FBI."
- **refutation:** the *pattern* is real; the *deliberate-escalation* read is an inference. Innocent reading: he uses "police/FBI/law enforcement" loosely & interchangeably. Opponent: "he's not escalating, he's a sloppy talker."
- **grade:** B.
- **fix:** present as an **observed pattern** + name the benign explanation, then say why escalation is the better read (FBI framing intensifies as stakes/scrutiny rise). Don't assert intent flatly.

### C1 — 🟢 "downloaded vs screenshotted is the same act (CSAM on device)"
- **support:** he admits *retention* in both cases; possession-in-fact is identical regardless of acquisition.
- **refutation (minor):** there's a real-world distinction in *intent/transience* (incidental exposure vs deliberate hoarding) — but he concedes deliberate retention, so it doesn't rescue him.
- **grade:** A− (it's possession-in-fact, not a legal verdict on his liability).
- **fix:** add "(possession-in-fact, not a legal conclusion)" so you're not asserting criminal liability.

### C3 — 🟢 "the proof is reactive & perpetually deferred (closed loop)"
- quote-grounded description of his own statements (verified). **A.** no change.

### C7 — 🟢 "764 is a real designated network; real UK member arrests exist"
- primary/secondary sourced (Wikipedia, ISD, GNET; Finnigan). **A.** no change.

### C8 — 🟢 "VID4 (2022) holds the earliest infiltrate→report→arrest story; 'terroristic threats' prefigures the Markle claim"
- quote-verified; the "prefigures" already carries the qualifier (different/anti-nazi context, not the same incident — per the Codex pass). **A−.** keep the qualifier.

---

## systemic pattern
Every 🟡/🔴 is **absence-of-evidence dressed as positive disproof**. The doc's *factual* spine
(verified quotes + NCMEC/FBI primary sources + 764 reality) is genuinely strong — so don't let the
weakest links be over-stated inferences an opponent can flip into "you also overclaim." One global
edit pass — *downgrade "likely false / isn't a thing / is escalating" → "unverified / undocumented /
observed pattern,"* and tag plausibility-reads `(inference)` — closes every seam without weakening
the real case. The mechanics (H2) and the behavior (H1/H3/H4) carry it; the speculation doesn't need to.
