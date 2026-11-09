# Workflow: Guided onboarding

**Goal:** learn who the person is before recommending who they should target or how they should position themselves. Start from existing evidence, not a long questionnaire.

## Step 1: Introduce the process and request optional source material

Explain that the process will be: **share context → review existing material → return a summary → confirm/correct → explore goals and audiences → build positioning**.

Invite the user to share whichever of these already exist:
- CV/résumé, with a note about whether it is current, partly outdated or unknown.
- Website or portfolio, if applicable.
- LinkedIn profile.
- Public profiles on Instagram, YouTube, TikTok, Facebook, X or other relevant channels.
- A short self-description, spoken or written, **instead of documents** if they prefer.

**All are optional.** Ask only once, in natural language, without a wall of required fields. Do not pressure users to share sensitive information or credentials. If the user offers a narrative first, listen and use it.

## Step 2: Ask permission, define the source boundary

Before examining supplied materials, explain which sources will be reviewed and how they inform the summary. Open only authorized links, documents, and publicly accessible pages. Do not attempt to log in, bypass privacy settings, collect third-party personal details or use unsupported scraping. An inaccessible page is not evidence of absence. Never assume a social username belongs to the user without confirmation.

For uploaded CVs and files, use the environment's supported file-reading tools. Keep any resulting private profile or notes **outside the public framework repository**. Do not post source documents, real URLs or user information to public issues, examples or commits.

## Step 3: Research and synthesize

Use [Researcher](../agents/researcher.md) to:
1. Identify experience, current work, projects, interests, recurring topics, strengths and visible positioning across provided sources.
2. Compare sources and flag contradictions, gaps, unclear dates, outdated CV information or differences between public profiles.
3. Distinguish verified public claims from user-reported details and hypotheses.
4. Analyze current presence, **not** personal characteristics inferred from appearance, followers, or private behavior.
5. Record citations/source references and review date **only in a private workspace**.

If sources cannot be accessed, say which ones and proceed from what is available. Do not invent a research result.

## Step 4: Return a draft profile and ask for validation

Before asking about target audiences or making positioning recommendations, summarize:
- **Who I understand you are:** professional background and activities.
- **What you're working toward:** aspirations, if provided.
- **What is already visible publicly:** communication channels and themes, only if actually reviewed.
- **What seems distinctive:** explicitly tentative observations.
- **What is uncertain/outdated/contradictory.**
- **What I could not access.**

Ask one direct question: **“Is this picture accurate? What would you correct or add?”**

Treat the summary as **DRAFT / NOT VERIFIED BY USER** until they confirm. Corrections take precedence over assumptions but may still need independent evidence for public claims.

## Step 5: Define goals and audiences

After confirmation, explore primary and secondary professional goals (e.g. employment, consulting, entrepreneurship, reputation) and then the audiences and markets that matter. The user may have multiple goals. Don't require a fixed business idea from someone still exploring.

## Step 6: Channels, positioning, and approval

Confirm desired channels, language, effort, topics to avoid and privacy boundaries. Run [Positioning Strategist](../agents/positioning-strategist.md). Present an evidence-led hypothesis and trade-offs; ask the owner to approve or revise it.

## Step 7: Establish a private workspace and launch a small experiment

Copy blank files from `templates/` **outside this public repository**. Store real sources, approved facts, positioning, drafts and decisions there. Choose up to three evidence-backed content ideas and enter [content cycle](content-cycle.md). No automatic publishing.

## Completion criteria
- Source scope/permission documented privately.
- Existing inputs reviewed as far as tools/access permit.
- Draft profile returned and user corrections captured.
- Audience, positioning and publishing claims never assumed from unconfirmed profile.
- Missing evidence and unresolved decisions explicitly tracked.

## Quality note from onboarding simulation
In an early conversational test, the assistant moved from the user's broad ambitions to audience questions before learning the user's background. This v0.2 sequence corrects that design flaw. The test scenario itself is **not** included here, to protect real-world privacy.
