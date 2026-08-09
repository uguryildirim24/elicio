# Research migration provenance

This engineering slice treated the Claude Science Elicio project as read-only.
No files were written, renamed, or deleted under the Claude Science root.

## Final pipeline resolution

The final package was identified from completed packaging frame
d760b00c-128f-444b-8f3d-3453a3cd37f4. The artifact index shows that repeated
artifact IDs for the same package file resolve to the same SHA-256 checksum and
canonical storage path. This avoids selecting the earlier, smaller features.py
or splits.py artifacts.

| File | Final artifact version | SHA-256 |
|---|---|---|
| __init__.py | ba240296-2223-446a-be3e-0e6c6eaa6e6f | c58d7e1b6519d11d50d9805488ee978a17d54c8727519a3de3a27598783dfc89 |
| cli.py | 3f1fc0c5-b978-480f-90d2-8f2c907a0690 | 105828d953229dcc51ca817f326c0f8858c0a83ec492454561a459cf0b4fdc90 |
| config.py | 57744de0-d594-451a-b6f9-c589506ae140 | 900e41833583780beac794b1c9ec47d240ba16ddffde3fde161aecf49e96dc23 |
| load.py | f3ba4f33-053c-4679-91a1-b08137b39958 | 9ffdf591715316535ec6a2b73094dab676153acba2b9e7cac09f32a7fd6edf12 |
| features.py | 285d5a0e-0086-4398-ba04-f96b5f755d74 | fd33c64b45fcf0594e77610c91e3b7445f5ac9e55e38d5b7fea9f52d76f24625 |
| splits.py | d81408e8-c645-4870-a167-82ccf20ba24a | f0a2ee84cb097c4280b119407aa39cf3ebc64666dd32230a17d4f7d90ab9421c |
| models.py | 793cca06-279d-449a-9606-d4e9bbdd8715 | 19d983e39f1f0d7135db9abdcf0f376fc5149d99c477aa1a3132c55f89bd62c4 |
| net_models.py | 2005c77b-64c8-4f47-ba05-79f47acbdf0b | 47969c7b70fa6844e1db2085e8d691a8c3335b5da1ce94202bd5507c12e7f0bb |
| prepare_subjects.py | 6f30c990-a182-46c0-8c3e-d1980235c8df | 4b357493aca7189db8cd9c019cce8feba2c9ba2f6b954af9ea23f69933764ab6 |
| train_and_eval.py | 84688912-92f5-4470-a953-ac2e98149966 | a6cbef747fff9b497319368e04f7b95415298e5e33a6019762cfb4b20455503b |
| six_best_rest.py | ac154ef1-e1d2-47a0-87fb-2efbcaebe5ed | ffeaf61ddc96a72e6e6f7c8ed1c77e90f082983451c572c8dfdb2ecd2f539f86 |
| README.md | 784d1137-90f7-4944-b927-f027d2fb2548 | 7f2af40e555a474eaf6700c0c85d380208818128d4e254c0d7bbdba5baf1d35d |

The migrated code is under src/elicio/pipeline. Engineering changes were
limited to package-relative imports, command argument forwarding, shared
configuration use, a clear optional-dependency error, safe output-directory
handling, and routing both model entry points through cross_session_split.
The model architectures, feature formulas, windowing, channel selection, and
six-gesture selection remain the final research implementations.

## Simulated harness source

The source harness was the milestone0.py artifact:

- Artifact: b6cd0196-bde6-4c1d-a69d-00671774d132
- Version: e1e67efc
- SHA-256: 06d0a31f239bdefbce15823eedc5b93b4e1c1389db16c43690ce27f211e2abbe
- Stable event: (symbol, confidence, timestamp)

Its alphabet, risk levels, confidence floors, three-second confirmation window,
rest behavior, and deterministic demo script were migrated into
src/elicio/harness. The wrist_down print-only behavior was replaced with the
fixed-path local marker adapter. Other actions remain simulations.

## Result evidence checked

The final report artifact was version
5dc65755-20f3-47a6-b0fe-0ce8c5eb97ed. The latest eight-channel evidence was
also checked read-only:

    workspaces/97322daa-0e54-4e21-9ef3-6d37f68ed1d6/six_best_rest_8ch.py
    workspaces/97322daa-0e54-4e21-9ef3-6d37f68ed1d6/six_best_rest_8ch_summary.csv

That summary reports a Temporal CNN mean accuracy of 79.31 percent, median
accuracy of 84.29 percent, and 7 of 23 subjects at or above 90 percent. It is
public-dataset evidence, not personal or hardware end-to-end proof.
