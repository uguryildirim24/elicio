# WP17c — research v5: the JLC edge rule, FPC assembly sides, a router, a screw (lane w5, Antigravity)

Read `tasks/phase1-common.md`, `docs/fab/L7-research-v4.md` §3–§4 (your
own JLC notes), `docs/fab/board-v2.md` §12 (the JLC terms sentence:
"component body to board edge ≥ 2.5 mm; tooling holes, edge rails and
fiducials required for assembly") and `docs/fab/open-questions.md` Q71,
Q76, Q77, Q78. Lane `w5`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w5`, branch `lane/w5` at main
after the round 6 merge. Start line (coordinator restarts you by
copy-paste):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1

Why: the packing lane cannot place the board on the island if the 2.5 mm
is measured from the board's own outline; it can if it is measured from
the assembly panel's rail edge. The answer is on JLC's pages, not in our
arithmetic. Web reads only. No sign-up, no quote, no upload, no purchase,
no vendor contact; free tools only.

Deliver `docs/fab/L8-research-v5.md`, each claim with the URL, the read
date and the verbatim sentence; anything you could not read on the page
tagged UNVERIFIED:

1. **JLC assembly edge rule.** From the assembly terms page, the
   panelization help article, the "PCB assembly capabilities" page and the
   flex (FPC) assembly page: is the ≥ 2.5 mm from component body to the
   board's outline, or to the panel's rail edge; does JLC add edge rails
   (process edges) itself when a design has none, for rigid and for FPC
   assembly; the minimum component-to-outline distance once rails exist;
   how JLC depanels FPC (mouse bites, laser, V-cut) and what that costs in
   edge distance; whether a 2.5 mm wide tab strip with a Ø5.0 pad is an
   assembly problem at all when the parts sit elsewhere.
2. **FPC assembly sides.** Does JLC assemble both sides of a 2-layer
   polyimide flex; any restriction on part height, size or count on flex;
   the stiffener rules for a double-sided FPC assembly (the extra-fee
   threshold you already quoted, restated with the page).
3. **A router that writes a file on this Mac.** Freerouting newest release
   (2.4.x or later): does headless mode write a SES on macOS with Java 21;
   exact CLI flags; the issue tracker entries on the 2.1.0 headless hang;
   any other free autorouter with a KiCad 10 path (KiCad's own
   pcbnew Python, an ORCA-style plugin, or the DSN route through another
   free tool). Report only; the board lane installs.
4. **The tail screw (Q71).** M2.5 titanium screws sold in ones or small
   packs with a page price (McMaster-Carr, Bolt Depot, Amazon, a bicycle
   or RC shop): thread length 4 to 6 mm, pan or button head, Grade 2 or 5;
   and the pilot hole HP or JLC3DP recommends for an M2.5 self-tapping
   into MJF PA12 (for Q73's island bosses too). Prices are for the ledger;
   nothing is bought.

Gates: the file exists with the four sections, every number carries its
page quote or UNVERIFIED, no other file touched, `git status --short`
empty. Commit `research(v5): JLC edge rule and FPC sides, router, screw`.
Report `.reports/WP17c-report.md` (untracked) with the one-paragraph
answer to item 1 first. Closing steps per the common file with `<PKG>` =
`WP17c`, `<lane>` = `w5`, also when you fail.
