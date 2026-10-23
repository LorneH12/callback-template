# Comment "CALLBACK" auto-reply

The hook: every video ends with **Comment "CALLBACK"**. On Instagram, an automation DMs the template link and the free checklist. TikTok and YouTube can't DM from a comment, so they get a public auto-reply plus a pinned comment pointing to the link in bio.

## What each platform allows (checked Oct 2026)
| Platform | Comment → DM | How |
|---|---|---|
| Instagram | Yes, through Meta's official API (ManyChat or similar) | One automated message per comment, within 7 days of it |
| TikTok | No for most US accounts (public reply only) | Keyword auto-reply under the comment, plus a pinned comment and the bio link |
| YouTube Shorts | No DMs | Pinned comment with the link; heart and reply manually |

## Instagram setup (ManyChat, about 15 minutes, done by Lorne)
1. Make the Instagram account Professional (Creator or Business) and turn on **Settings › Messages › Allow access to messages** (Connected tools).
2. Create a ManyChat account with the business email and connect Instagram through Meta's login. Read the permission screen. ManyChat is a service connected to Instagram, not something installed into Claude.
3. New automation › **Instagram: User comments on your post or reel**
   - Post: "Any post or reel" (or select each Callback reel)
   - Keywords: `CALLBACK`, `Callback`, `callback`, `CALL BACK`, `call back` (match: "contains")
4. **Public reply** (rotate these so they don't look spammy):
   - "Sent! Check your DMs 📩"
   - "Just DM'd you the link 👊"
   - "On its way to your inbox. If you don't see it, check Message requests."
5. **Optional follow check:** ManyChat's "Follow to DM" check was in beta as of Oct 11, 2026. If you turn it on, the flow asks non-followers to follow, then tap a button to get the link. Keep the message friendly and always give a way through: never hide the link from someone who doesn't follow, because Meta's rules on follow-gating are unclear.
6. **DM message 1** (the one automated message Meta allows):
   > Here you go 👇
   > **Callback**, the Framer website template I built for local service businesses: tap-to-call on every screen, prices up front and a quote form people finish.
   > See it live: https://exuberant-experiences-208278.framer.app
   > Get it ($29): [GUMROAD CALLBACK LINK]
   > Free: the Website Money-Leak Checklist (21 checks for your current site): [GUMROAD CHECKLIST LINK]
   > Questions? Just reply here; a real person answers.
   - Buttons: "See the live demo" · "Get Callback $29" · "Free checklist"
7. **If they reply:** that opens a normal conversation (Meta's 24-hour window). Lorne answers, or Claude drafts replies for him to send.
8. Turn the automation on, then test it from a personal account by commenting CALLBACK on one reel.

## TikTok
- Pinned comment on every video: "Comment CALLBACK and I'll reply with the details 👇 The link's in my bio."
- Keyword auto-reply (TikTok Business Suite or an approved tool), public: "Link's in my bio 👆 Tap Callback for the template and the free checklist."
- Bio link: the product page (it has the demo, the checkout and the checklist).

## YouTube Shorts
- Pinned comment: "Template + free checklist: [product page link]. Comment CALLBACK if you want help picking a trade layout."
- Description: the product page link on the first line.

## Wording rules
- Every reply and DM says what it is: our own template that we sell.
- Only promise what's real: the link, the demo and the checklist. No "only 3 left" unless it's true.
- Don't DM anyone who didn't comment the keyword. Never buy followers or comments.
- The flash-sale version of the DM (Days 8–9): add "First 10 people: code CALLBACK1 makes it $1" while the code still has uses.

## Videos
- Instagram versions (end with Comment "CALLBACK"): `out/*-ig.mp4`
- TikTok and YouTube versions (end with "Link in bio"): `out/*.mp4` without `-ig`
