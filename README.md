# Growth sprint kit

Reusable AI skills for a timed customer-acquisition strategy exercise, plus a prospecting pipeline.

| Path | What it is |
|---|---|
| `START.md` | **One file holding all three skills.** Paste it into any Claude or ChatGPT chat, or ask the chat to read its URL. |
| `skills/` | The three skills as folders: `outra-acquisition-sprint`, `growth-unit-economics` (with `scripts/growth_calc.py`), `strategy-red-team` |
| `dist/*.zip` | The same skills zipped, ready to upload to claude.ai (Settings → Capabilities → Skills) |
| `pack/KNOWLEDGE.md` | The full method and public evidence with sources |
| `prospector-src/` | A pipeline: Meta Ad Library → stack check → AI agency research → scored prospects |

## Use on any machine

**A. Any Claude or ChatGPT chat, with no login to your own account needed:**
- If the chat can browse, say:
  > Read https://raw.githubusercontent.com/duncmckenna/growth-sprint-kit/main/START.md and follow it.
- Otherwise, open that URL in the browser, copy everything (Cmd/Ctrl+A, then C) and paste it into the chat. Do the same with `pack/KNOWLEDGE.md` if you need the full method.

**B. Terminal:**
```bash
git clone https://github.com/duncmckenna/growth-sprint-kit.git
# or, without git:
curl -L -o kit.zip https://github.com/duncmckenna/growth-sprint-kit/archive/refs/heads/main.zip && unzip kit.zip
```

**C. Claude Code on that machine:** install the skills, then start Claude Code:
```bash
mkdir -p ~/.claude/skills && cp -r growth-sprint-kit/skills/* ~/.claude/skills/
claude   # then: "start the sprint"
```

**D. claude.ai:** download `dist/*.zip` and upload each one under Settings → Capabilities → Skills.
