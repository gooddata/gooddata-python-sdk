---
name: commit
description: Create a commit following this repo's conventional-commit format with the jira and risk trailers. Use when committing changes. Triggers on "commit", "commit this", "save changes", "ready to commit".
disable-model-invocation: true
---

## Workflow

1. `git diff --cached --stat`. If nothing is staged, run `git status` and ask what to stage —
   never stage everything on the user's behalf.

2. `git diff --cached` to understand what actually changed.

3. `git log --oneline -5` to match the surrounding style.

4. Propose a ticket. Try the branch name first:

   ```bash
   git branch --show-current | grep -oiE '[a-z]+-[0-9]+' | head -1 | tr '[:lower:]' '[:upper:]'
   ```

   No match means `jira: trivial`. Show whichever you picked; do not guess a real ticket ID.

5. Draft:

   ```
   <type>(<scope>): <subject>

   <body>

   jira: <TICKET-ID>
   risk: nonprod|low|high
   ```

   - **type** — `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`,
     `revert`, `ci`, `build`
   - **scope** — optional; when present it must be one of the package names listed in
     `.gitlint`
   - **subject** — imperative, no trailing period, whole line ≤ 70 characters
   - **body** — why, wrapped at 72. Rationale belongs here, not in a code comment
   - **jira** — required, lowercase; `jira: trivial` when no ticket applies
   - **risk** — lowercase; ask if unsure. `nonprod` = tests/docs/CI only, `low` = routine
     change to shipped code, `high` = breaking or risky behavior change

6. Show the draft and wait for approval.

7. Commit with a heredoc so the trailers keep their own lines:

   ```bash
   git commit -m "$(cat <<'MSG'
   <the message>
   MSG
   )"
   ```

## Important

- `jira:` and `risk:` must be consecutive lines in the final paragraph. A blank line above a
  trailing `Co-Authored-By:` orphans them from the trailer block.
- Never guess the risk level — ask.
- Never skip the confirmation step.
- One logical change per commit. Review feedback goes into the commit whose scope it belongs
  to: `git commit --fixup=<sha>` then `git rebase -i --autosquash <sha>^`.
- The commit-msg hook runs gitlint. If it rejects the message, fix the message rather than
  bypassing the hook.
