# Artefact receipt — integrity ≠ QA ≠ publication ≠ authorization

Candidate receipt `contracts/artifact-receipt.schema.json`, validator `scripts/validate_artifact_receipt.py`. This is a small envelope across existing source, bundle, payload and renderer flows; it is **not a replacement for validate_bundle, check_prehitl, render_exec or a new event BUS**.

1. **Integrity**: `sha256` must describe actual bytes of the artifact. A source capture declares `selected_excerpt/excerpt_utf8` or `full_original/original_bytes`. An excerpt cannot impersonate the original.
2. **Persistence**: `prepared_not_published → published_unverified → published_verified` are distinct states; `blocked` is explicit. The final state requires independent readback **bytes** supplied to the validator and exact SHA-256 match. A URL, commit status or local write is not readback proof.
3. **QA**: `NOT_RUN/PASS/FAIL` belongs to a specific content/version. It does not change persistence and never approves a business decision.
4. **Authorization**: `UNREVIEWED/DEMO_ONLY/HITL_REFERENCED` is **metadata only**. `human_decision_ref` is not an authenticated approval; the actual committee gate remains in `contracts/decision-rules.md` and `docs/agent/gates.md`.
5. **Visibility**: raw captures and restricted content stay outside the public repository unless an explicit rights review authorizes use. Do not add new raw archives to `examples/`.

This validator **does not fetch a remote URL**. The publisher/session is responsible for retrieving readback bytes through its authorized connector and passing them to the validator. Without that independent action, leave `published_unverified`.

Negative NRT test missing readback, mismatched bytes, false original scope, QA ≠ authorization and HITL reference ≠ permission. Future producer integration and actual remote receipt acceptance remain under #47 / #29 / #10.

## Producteur réel raccordé (#47 — incrément)

Le renderer candidat `renderers/value_chain_preview/render.py --pdf` écrit désormais `artifact_receipt.json` **à partir des octets du PDF réellement généré**, et non d'une empreinte annoncée. Son `qa_state=PASS` exige un `qa.json` navigateur avec exactement trois pages et sans défaut détecté. Le reçu reste toujours `prepared_not_published` et `UNREVIEWED`, même après cette QA.

Le helper `scripts/prepare_artifact_receipt.py` sert aussi aux autres producteurs via arguments explicites. Le transport (API GitHub, stockage autorisé) doit être fait **après**, dans la session qui possède réellement les droits ; la promotion vers `published_verified` nécessite la relecture distante octet pour octet par `validate_artifact_receipt.py --readback-file`. Aucune CI verte ne réalise à elle seule ce transport.
