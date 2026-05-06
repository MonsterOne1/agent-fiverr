# Provider Strategy

Provider/API dependencies are service-level requirements, not hardcoded secrets.
This repo commits provider IDs, intended use, credential environment variable
names, and side-effect levels. Keys will be supplied later by the owner.

## Media Providers

| Task | Primary Providers | Notes |
|---|---|---|
| Video creation / repurposing | Seedance, Kling, Renoise, OpenAI Responses | Use Seedance/Kling for generation, Renoise for production workflow, OpenAI for storyboard/caption logic. |
| Poster / product image / brand design | Banana, GPT Image 2, OpenAI Responses | Use Banana/GPT Image 2 for generation/editing; store prompt and asset manifest. |
| Music / jingle / background tracks | Suno, OpenAI Responses | Use Suno for generation and OpenAI for brief, lyrics/structure, and rights notes. |
| Voiceover / TTS / dubbing | ElevenLabs, OpenAI Responses | Use ElevenLabs for voice assets; require voice/source notes in asset manifest. |

## Technical Providers

| Task | Primary Providers | Side-Effect Rule |
|---|---|---|
| Coding and PR work | GitHub, OpenAI Responses | PRs and repo mutations require buyer authorization. |
| Preview deploys | Vercel | Deploys require explicit authorization. |
| CMS/e-commerce tasks | WordPress, Shopify | Live store/account changes require explicit authorization. |

## Marketing and Research Providers

| Task | Primary Providers | Side-Effect Rule |
|---|---|---|
| SEO/GEO audit | Browser/Search, Google Ads, OpenAI Responses | Read-only audit can run; ad spend cannot. |
| Market research | Browser/Search, OpenAI Responses | Cite sources and label uncertainty. |
| Email/social campaigns | OpenAI Responses, optional image providers | Sending/publishing requires authorization. |

## Credential Handling

- Commit provider IDs and env var names only.
- Never commit keys, tokens, cookies, or buyer account credentials.
- Use `.env` locally, secret manager in hosted mode, or per-workspace provider auth.
- Treat webhook URLs and provider OAuth tokens as credentials.

