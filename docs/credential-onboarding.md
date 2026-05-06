# Credential Onboarding

The repo commits provider names, environment variable names, scopes, and call
plans. It never commits actual API keys.

## Setup Flow

1. Copy `.env.example` to `.env` or configure the same names in a secret
   manager.
2. Fill only the providers you want to test first.
3. Keep live calls disabled until the provider adapter or payment adapter is
   explicitly marked live-enabled in code.
4. Use dry-run mode to verify provider selection, request fields, credential
   gates, audit traces, asset manifests, and escrow call plans.

## Provider Credentials

| Environment Variable | Used For |
|---|---|
| `OPENAI_API_KEY` | OpenAI Responses and GPT Image 2 |
| `BANANA_API_KEY` | Banana image generation/editing |
| `SEEDANCE_API_KEY` | Seedance video generation |
| `KLING_API_KEY` | Kling video generation |
| `RENOISE_API_KEY` | Renoise video production toolkit |
| `SUNO_API_KEY` | Suno music generation |
| `ELEVENLABS_API_KEY` | ElevenLabs voiceover/TTS/dubbing |
| `GITHUB_TOKEN` | GitHub repo and pull request workflows |
| `VERCEL_TOKEN` | Vercel preview/deployment workflows |
| `WORDPRESS_API_TOKEN` | WordPress site operations |
| `SHOPIFY_ACCESS_TOKEN` | Shopify store/theme operations |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Google Ads keyword/campaign drafts |
| `STRIPE_SECRET_KEY` | Stripe Connect payment/escrow scaffold |

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_credentials.py'
python3 scripts/validate_catalog.py
python3 -m unittest discover -s tests -p 'test_provider_runtime.py'
python3 -m unittest discover -s tests -p 'test_payments.py'
```

Expected local behavior:

- Missing provider keys are reported, not silently ignored.
- Non-dry-run provider calls fail when their required key is absent.
- Configured keys produce call plans, not live network calls, until the adapter
  is deliberately enabled.
- `.env.example` contains empty placeholders only.
