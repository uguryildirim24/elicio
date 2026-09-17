# WP2 — Gauge script and order 1 files (lane w2)

Read `tasks/phase1-common.md` first. Lane `w2`, worktree
`/home/user/projects/elicio/.worktrees/w2`, branch `lane/w2`.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec sections: plan §3 in full (3.1 tool and files, 3.2 frames and path,
3.3 parameters and checks, 3.4 caliper protocol, 3.5 construction in order,
3.6 print rules, acceptance policy, outputs, 3.7 passive fit acceptance),
§5, §9 row WP2, §10 open items 1 to 4. `docs/fab/L1-cad.md` for build123d
background only.

Owns: `scripts/cad/` (new), `docs/fab/cad/v1/` (new, including
`manifest.json`), `tests/test_cad.py` (new), the `cad` optional-dependency
group in `pyproject.toml`.

Deliver:

1. `scripts/cad/bte_fit_shell.py` (or the path §3.1 names, if different):
   a build123d script that takes the §3.3 parameters (defaults are the
   reference-ear build, every one overridable from the command line or a
   small JSON), applies the §3.4 measurement mapping including the computed
   chord gate (M1) and CREASE_BOW from the arc-chord formula clamped 1 to 8
   (open item 1), builds the body in the §3.5 order in the body frame, the
   lid, the tail with the reference pocket, WIRE_CHANNEL with its physical
   opening reported per open item 4, the hook with HOOK_PRELOAD, and the
   MOCK_CONTACTS behaviour §3.3 describes.
2. Every check §3.3 and §3.6 name, run before export, failing loudly with
   the parameter and the number. The VARIANT × HOOK_PRELOAD matrix only;
   anything else fails before export.
3. Outputs under `docs/fab/cad/v1/`: the five files and six parts §3.6
   lists (STEP, STL and 3MF as it specifies), plus `manifest.json` with the
   parameter set, each file's SHA-256, the check results, the manufacturing
   exceptions (E1 to E5) and interference values, and the clamped
   CREASE_BOW. Open item 3 (manifest schema and hash rule) is WP3's, so keep
   the manifest simple and documented in a docstring; WP3 may extend it.
4. `tests/test_cad.py`: stdlib unittest; skips cleanly when build123d is
   not installed; when it is, regenerates the reference build into a temp
   dir and asserts identical file hashes against the committed manifest,
   and asserts the failing cases fail (M1 below the gate, a parameter
   outside the matrix).
5. A `README.md` in `scripts/cad/` with the exact commands: install, build
   the reference set, build from Rolf's measurements, run the checks.

Do not render or draw; WP3 does that from your STEP. Do not order anything.
If build123d has no Python 3.13 wheel, use 3.12 per the common file. If a
§3.5 step cannot be built as written, build the closest geometry that
passes the §3.3 checks, and put the exact sentence and your reading under
"Needs a decision".

Acceptance (plan §9 row WP2): all §3.3 checks pass; exceptions and
interference in the manifest; identical regeneration. Gates: unit tests
green including yours; the script run twice yields identical hashes.

Report: `.reports/WP2-report.md`. Closing steps per the common file with
`<PKG>` = `WP2`, `<lane>` = `w2`.
