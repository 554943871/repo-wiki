# Expected Wiki Doctor Report

Mode: default safe rewrite.

Gate note: `wiki/07-drift.md` is already in the standard empty state.

Classification: `evidence_grounded_update`.

Actions: `rewrite_page`, `write_evidence_grounded_fact`.

Reason: current route evidence directly supports the current Shipping entry point and owner.

Important outside-wiki files read:
- `src/shipping/routes.ts`

Changed pages:
- `wiki/04-modules/shipping.md`

Evidence-grounded facts written:
- Current shipment creation enters through `/delivery/shipments` and is owned by Delivery Orchestrator. Evidence: `src/shipping/routes.ts`.

No Whitebox Component Diagram files were generated because the route evidence updates the public entry fact but does not by itself identify enough legal Whitebox internals.
