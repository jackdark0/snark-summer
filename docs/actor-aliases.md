# Actor and Entity Register

Use this register for authored analysis, candidate notes, score audits, and merge
edits. Do not normalize direct quotes, transcript text, source titles, filenames,
or URLs. If the source says "Queman" or "JTO" inside a quote, keep the source
wording and use the canonical name in surrounding prose.

## Classification Key

- `coordinator`: person treated as planning, directing, or routing campaign-side activity.
- `coordination hub`: venue, server, or channel where coordination appears to happen.
- `active participant`: person participating in campaign-side argument or amplification without enough evidence to classify as a coordinator.
- `amplifier / reviewer`: person or channel mainly repeating, reviewing, or distributing a frame.
- `target / team-adjacent`: person or community being targeted or aligned with the target side.
- `source / channel`: source label for media capture; do not infer a human speaker from the channel label alone.
- `unknown / needs-classification`: entity must be queued for user classification before authored analysis relies on the role.

| Canonical name | Classification | Known aliases / source variants | Prose rule | Notes |
|---|---|---|---|---|
| JSTLK | coordinator | JTO, Jtock, Jaystalk, jstlk | Use `JSTLK`. | Keep published video titles and transcript filenames as-is. |
| Kuihman | coordinator | Queman, Queenman, Quiman | Use `Kuihman`. | YouTube auto-captions frequently mishear the handle. |
| Nikandros | coordinator | Nick Andros | Use `Nikandros` when the person is identified by handle; keep `Nick Andros` in source wording. | `Shimu` appears in related transcript/source labels; do not collapse it into Nikandros without source confirmation. |
| Snark Server | coordination hub | Snark Discord, Snark server, Snark Left, Snark Left server, secret Snark Discord, "Secret" SNARK Discord | Use `Snark Server` for the coordination hub. | Major hub where coordinators coordinate. Treat hub-level claims as server/network claims unless the source identifies a specific person. |
| MrowLive | active participant / source channel | Mrow, mrowlive | Use `MrowLive` for the channel; use `Mrow` only when the source clearly means the speaker. | Existing source labels use both forms. |
| Dooby | active participant | Dooby | Use `Dooby`. | Adversary debate participant in the Dec. 2025 Wick TV debate and later coverage. |
| Aiden Underground | active participant | Aiden | Use `Aiden Underground` on first reference, then `Aiden`. | May 2026 Wick TV debate participant. |
| Dickers | active participant | Dickers | Use `Dickers`. | May 2026 Wick TV debate participant. |
| Chudlogic | amplifier / reviewer | Chud | Use `Chudlogic` for the channel/person unless source wording says `Chud`. | May 2026 reaction stream source; classification can vary by context. |
| Destiny | target / team-adjacent | Steven, Steven Bonnell, Steven Bunnel, DGG | Use `Destiny` for the creator; use `DGG` for the community. | Keep legal names as source wording when they appear in filings or transcript quotes. |
| Dan Saltman | target / team-adjacent | Dan | Use `Dan Saltman` when the surname matters; use `Dan` only when context is unambiguous. | Often appears as a target-side actor in Snark/DGG conflict coverage. |
| Foodshops | target / team-adjacent | Food Shops, FoodShop, Food Slops, Food Cops, Food Chops, Food Jobs | Use `Foodshops`. | Existing examples frame Foodshops as a Destiny-orbit / DGG-adjacent target of Snark-side coverage. Preserve derogatory variants in quotes and source titles. |
| Pisco | target / team-adjacent | Pisco | Use `Pisco`. | Existing Ryle titles and transcripts frame him as a Destiny-side/orbiter target. |
| Wicked Supreme | target / team-adjacent | Supreme | Use `Wicked Supreme`. | Existing examples discuss allegations against him as Destiny-side/orbiter collateral. Avoid collapsing generic "supreme" legal wording into the person without context. |
| Esports Batman | target / team-adjacent | Esports Batman | Use `Esports Batman`. | Existing examples pair him with Wicked Supreme in Destiny-side/orbiter dox-discussion context. |
| LonerBox | target / team-adjacent | Loner Box | Use `LonerBox`. | Existing examples treat him as target/team side, not adversary-side tactic actor. |
| Hutch | target / team-adjacent | Hutch | Use `Hutch`. | Existing examples treat him as target/team side. |
| Stardust | target / team-adjacent | Stardust | Use `Stardust`. | Existing examples treat her as target/team side. |
| Whick | target / team-adjacent | WhickTV, Whick TV | Use `Whick` for the person and `Whick TV` for the channel/source. | Debate/source labels may use `Whick TV`. |
| Purple Parry Gaming | source / channel | Purple Parry, purplepepsigaming, purpleparrygaming | Use `Purple Parry Gaming` for channel/source references. | Do not infer the human speaker from the channel label alone. |
| Ryle Kittenhouse | source / channel | Ryle | Use `Ryle Kittenhouse` for channel/source references. | Use `Ryle` only in short prose after the channel has been named. |

## Editing Rules

- Authored prose should use the canonical name.
- Direct quotes, transcript excerpts, video titles, channel titles, filenames, and
  URLs should preserve source wording.
- If an alias is useful for clarity, introduce it once in prose:
  `JSTLK (alias: JTO)` or `Kuihman (auto-caption variant: Queman)`.
- Do not infer that a source channel is the speaker unless the transcript or
  video context identifies the speaker.
- Do not attribute Snark Server hub-level activity to a specific coordinator
  unless the source identifies that person or the relationship is already
  documented in an accepted example.
- When merging candidates, add uncertain aliases to this file before broad
  cleanup. Do not silently normalize names that may refer to different people.

## Classification Trigger

When a transcript, candidate, or report introduces an actor/entity whose role
matters and is not in this register, stop before assigning a role in authored
analysis. Ask the user for classification. If the analysis is running in a batch
and cannot stop cleanly, add the item to `docs/actor-classification-queue.md`,
mark it `unknown / needs-classification`, and avoid role-based conclusions until
the user resolves it.
