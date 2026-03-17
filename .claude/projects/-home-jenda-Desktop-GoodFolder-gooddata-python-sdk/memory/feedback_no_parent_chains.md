---
name: no-parent-chains
description: User dislikes chained .parent.parent.parent path navigation - considers it bad practice
type: feedback
---

Avoid chaining `.parent.parent.parent` for path resolution — it's fragile and hard to read.

**Why:** The user called it "really stupid" and "bad practice." It's brittle when directory structure changes.

**How to apply:** Use explicit path construction, environment variables, or package-relative resource loading instead of long `.parent` chains.
