# Web Alpha

The web alpha is a static buyer-facing prototype for the Agent Fiverr
marketplace/workroom flow.

## Implemented

- Service catalog with 20 MVP service agents.
- Category navigation and filters for category, capability, and provider.
- Selected-service workroom panel.
- Brief field rendering and autofill.
- Basic/Standard/Premium quote package selector.
- Price, SLA, platform fee, and escrow hold summary.
- Provider dry-run status list.
- Mock escrow checkout button.
- Desktop and mobile responsive layouts.

## Run

```bash
python3 -m http.server 8127 --directory web
```

Open:

```text
http://127.0.0.1:8127/
```

The app is also static-file friendly:

```text
web/index.html
```

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_web_static.py'
python3 -m http.server 8127 --directory web
curl -fsS http://127.0.0.1:8127/ | head
curl -fsS http://127.0.0.1:8127/app.js | grep -c 'slug:'
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --screenshot=/tmp/agent-fiverr-alpha-headless.png --window-size=1440,1000 http://127.0.0.1:8127/
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --screenshot=/tmp/agent-fiverr-alpha-mobile.png --window-size=390,900 http://127.0.0.1:8127/
```

Latest rendered screenshot evidence:

- Desktop: `/tmp/agent-fiverr-alpha-headless.png`
- Mobile: `/tmp/agent-fiverr-alpha-mobile-2.png`

