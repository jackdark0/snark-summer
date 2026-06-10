# Coordinator Contradiction Pass

This pass looks for places where a coordinator-side position appears to conflict
with another position in the processed transcripts. It is a lead sheet, not a
final factual finding. Use it to prioritize audio verification and clip review.

## Method

- Use canonical names from `docs/actor-aliases.md` in authored prose.
- Preserve source wording inside quoted snippets.
- Treat auto-caption-only material as provisional until audio review.
- A strong contradiction needs two positions from the same speaker or same
  speaker-linked stream context. Cross-speaker tensions are listed only as
  follow-up leads.

## High-Confidence Leads

### CC-0001 | JSTLK | Reporting principle versus reporting campaign

**Position A:** In the May 19 transcript, JSTLK presents a broad anti-reporting
principle: he says he is "against reporting in general," that "snitching is
cowardly," and that outside extreme illegal-material cases "there is absolutely
no reason to report, let alone mass flag."

**Position B:** The same transcript later admits or defends reporting activity:
"I totally tried to report Destiny," "we're reporting this guy," "there's a big
difference" between bad and justified mass reporting, and "going after the
platforms is the good choice."

**Why this matters:** The principle is stated as general, then becomes conditional
once JSTLK frames the target as harmful enough. This is the cleanest
contradiction lead in the current corpus because both sides are in the same
stream.

**Sources:** `transcripts/processed/jstlk-mrow-kuihman-v-stale.txt` at 5:18,
6:14-6:21, 19:15-20:33, 31:12-33:47; EX-0043, EX-0044, EX-0053, EX-0054,
EX-0056.

**Confidence:** High. Audio verification still needed before promoting direct
quotes to `VERIFIED`.

### CC-0002 | JSTLK | Free-speech posture versus deplatforming threshold

**Position A:** In the Dec. 21 Ryle transcript, JSTLK says he is "pro free
speech," is happy that people were unbanned, runs relaxed chats, and tends not to
block or ban because he likes disagreement.

**Position B:** In the same Dec. 21 transcript and the May 19 transcript, he says
Destiny should be banned/demonetized and that YouTube may terminate the channel.

**Why this matters:** This is not an absolute contradiction because JSTLK states
exceptions for doxing, threats, and direct encouragement. The tension is that his
free-speech posture is broad in self-description, while the platform-enforcement
threshold becomes much lower once the target is framed as engaged in doxing.

**Sources:** `transcripts/ryle-kittenhouse/processed/20251221-D1Xh8ojDv48.txt`
at 1:16:08-1:18:22 and 5:33-9:50;
`transcripts/processed/jstlk-mrow-kuihman-v-stale.txt` at 31:12-33:47.

**Confidence:** Medium-high. Needs audio verification and careful framing as a
threshold shift, not a categorical contradiction.

### CC-0003 | JSTLK | Evidence standard for allies versus opponents

**Position A:** When discussing allies, JSTLK says he will "make the assumption"
that Nick Andros and Shimu "probably didn't do anything that bad."

**Position B:** In the next breath, criticism of the opposing side is treated as
something where "the facts are there" and critics should "go watch the debate."

**Why this matters:** The burden of proof shifts by side. Allies receive default
charity; opponents are told the evidence is already available and they should
research it.

**Sources:** `transcripts/processed/jstlk-mrow-kuihman-v-stale.txt` at
35:47-36:19; EX-0042.

**Confidence:** High as an asymmetric-standard lead. Audio verification needed
for exact quotation.

### CC-0004 | Kuihman | Coordinated boosting as astroturfing versus normal growth

**Position A:** In the May 28 Kuihman transcript, Whick's frame describes
coordinated, targeted, edited, out-of-context clips as astroturfed narratives.
Kuihman agrees that "coordinating to boost a false narrative using out of context
clips is wrong."

**Position B:** In the same stream, Kuihman says it is "fine and good to make
tweets and get your friends to boost them," calls clipping and friend-retweeting
"the game," and says "what's not wrong is coordinating to boost clips" where the
content is criticism or a mean joke.

**Why this matters:** Coordination is condemned or normalized based on whether
the speaker accepts the content as false or justified. That makes the standard
depend on the speaker's truth judgment rather than the coordination mechanism.

**Sources:** `transcripts/kuihman-live/processed/20260528-5P--7ZRZaz8.txt` at
17:43-18:32 and 30:47-31:40; EX-0059, EX-0070.

**Confidence:** High for a same-stream tension. Captions are auto-generated.

### CC-0005 | Kuihman | PII/doxing as moderation incident versus culture pattern

**Position A:** In Snark-side discussion, Kuihman says a PII post "happens in
every Discord of a certain size" and the measure is "how it's handled." The same
line appears again as "it's about how it's handled" and "it is not a doxing
server."

**Position B:** When describing opponent-side behavior, the framing becomes a
year-plus pattern of doxing/harassment culture rather than isolated moderation
incidents.

**Why this matters:** The same category of conduct changes scale depending on
whose side is being evaluated: isolated moderation problem for Snark-side PII;
broader culture/pattern for DGG-linked behavior.

**Sources:** `transcripts/kuihman-live/processed/20260524-iaGkqiDHY24.txt` at
3:44-3:52 and 1:16:50-1:17:05;
`transcripts/kuihman-live/processed/20260528-5P--7ZRZaz8.txt` at 22:05-22:49;
EX-0060, EX-0065.

**Confidence:** Medium-high. Strong as a standard-shift lead; needs direct
opponent-side quote verification before use as a concise contradiction.

### CC-0006 | Kuihman | Off-platform moderation rule versus exceptions

**Position A:** Kuihman says his usual policy is not moderating off-platform
behavior because "you simply cannot" and because it requires investigating DMs,
other servers, and outside evidence.

**Position B:** Immediately before that rule, he says there are things that will
make him "do something about something that happened off platform," including
someone reporting while he is trying to talk to them.

**Why this matters:** This is a weaker contradiction because he explicitly
frames it as an exception. It is still useful because the exception is broad and
interest-based: off-platform conduct is too hard to moderate generally, except
when it directly affects his ability to conduct conversations.

**Sources:** `transcripts/kuihman-live/processed/20260520-ye97og6PHWA.txt` at
4:23-5:31.

**Confidence:** Medium. Keep as an "exception tension" unless more direct
examples are found.

## Follow-Up Leads

| Actor | Lead | Next check |
|---|---|---|
| Nikandros / Shimu | Doxing definition narrows across the May 15 debate, but speaker attribution is not reliable enough from captions alone. | Audio-verify EX-0071 and EX-0083 before assigning contradiction to a person. |
| MrowLive | Current banked examples show joke framing and cross-platform relay, but not yet a clean same-speaker position A / position B contradiction. | Search Mrow transcripts for direct claims about tactics being wrong versus justified. |
| Ryle Kittenhouse | Current evidence mostly documents distribution and publication of other streams. | Separate channel/platform role from speaker claims before scoring contradictions. |

## Suggested Clip Targets

- CC-0001: May 19 JSTLK reporting cluster, 5:18-6:21 and 19:15-20:33.
- CC-0004: May 28 Kuihman coordination cluster, 17:43-18:32 and 30:47-31:40.
- CC-0005: May 24/May 28 Kuihman PII standard cluster, 3:44-3:52,
  1:16:50-1:17:05, and 22:05-22:49.
