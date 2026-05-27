# GitHub Labels Definition
# Create these labels in your repo before the pipeline goes live.
# Format: name | color | description

## Status labels (workflow state)
status: triage        | #e4e669 | Newly submitted, pending mod review
status: approved      | #0075ca | Reviewed and added to approved database
status: rejected      | #d93f0b | Rejected — duplicate, insufficient evidence, or out of scope
status: needs-info    | #d876e3 | Returned to submitter for clarification
status: debunked      | #bfd4f2 | Previously approved, subsequently disproven

## Platform labels
platform: twitter     | #1da1f2 | Observed on X / Twitter
platform: discord-public   | #5865f2 | Observed in a public Discord server
platform: discord-leaked   | #5865f2 | From leaked or shared Discord logs
platform: twitch      | #9146ff | Observed in Twitch chat or donations
platform: youtube     | #ff0000 | Observed in YouTube chat or comments
platform: reddit      | #ff4500 | Observed on Reddit
platform: other       | #cccccc | Other platform

## Narrative cluster labels
cluster: lawsuit          | #f9d0c4 | Related to ongoing lawsuit narrative
cluster: sexual-misconduct | #f9d0c4 | Sexual misconduct allegations
cluster: financial        | #f9d0c4 | Financial corruption / profit-motive claims
cluster: association      | #f9d0c4 | Complicity-by-association framing
cluster: platform-manipulation | #f9d0c4 | Claims about platform/algorithm manipulation
cluster: uncategorized    | #eeeeee | Does not fit existing clusters

## Tactic labels
tactic: always-on-offense     | #c5def5 | Tactic 1
tactic: isolated-rigor        | #c5def5 | Tactic 2
tactic: schroedingers-joke    | #c5def5 | Tactic 3
tactic: unilateral-principles | #c5def5 | Tactic 4
tactic: no-win-framing        | #c5def5 | Tactic 5
tactic: victim-reversal       | #c5def5 | Tactic 6 — DARVO
tactic: moving-goalposts      | #c5def5 | Tactic 7
tactic: permission-structures | #c5def5 | Tactic 8
tactic: maximize-minimize     | #c5def5 | Tactic 9
tactic: fragmentation         | #c5def5 | Tactic 10
tactic: narrative-laundering  | #c5def5 | Tactic 11
