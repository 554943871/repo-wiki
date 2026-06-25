# Expected Wiki Doctor Report

Mode: default safe rewrite.

Gate note: `wiki/07-drift.md` is already in the standard empty state.

Classification: `safe_guidance_rewrite`.

Actions: `rewrite_page`, `add_table_or_diagram`.

Changed pages:

- `wiki/04-modules/fulfillment.md`: replaced the old Mermaid module map with a linked Whitebox Component Diagram while preserving links, evidence, and uncertainty.

Whitebox files refreshed:

- `wiki/04-modules/fulfillment.whitebox.yaml`: source model created from existing module-map facts.
- `wiki/04-modules/assets/fulfillment.whitebox.svg`: complete diagram rendered from the source model and linked first from the module page.
- `wiki/04-modules/assets/fulfillment.whitebox.boundary.svg`: non-empty Boundary Derived Whitebox View rendered from the same source model.
- `wiki/04-modules/assets/fulfillment.whitebox.delegation.svg`: non-empty Delegation Derived Whitebox View rendered from the same source model.
- `wiki/04-modules/assets/fulfillment.whitebox.assembly.svg`: non-empty Assembly Derived Whitebox View rendered from the same source model.
- `wiki/04-modules/assets/fulfillment.whitebox.interfaces.svg`: non-empty Interfaces Derived Whitebox View rendered from the same source model.

Reader-purpose Derived Whitebox Views embedded after the complete diagram:

- Boundary: isolates who can call Fulfillment and which boundary ports they use.
- Assembly: isolates the internal persistence and audit chain after intake accepts an order.

Generated but not embedded:

- Delegation and Interfaces views remain renderer-produced artifacts from the same source model, but they are not embedded because the complete diagram plus selected views already carry the needed reader path.

Information preserved:

- Checkout flow starts fulfillment through the Submit Fulfillment boundary port.
- Returns flow asks Fulfillment through the Cancel Fulfillment boundary port.
- Operations console reads fulfillment through the Fulfillment Status boundary port.
- Submit Fulfillment is delegated to Order Intake.
- Cancel Fulfillment is delegated to Cancellation Desk.
- Fulfillment Status is delegated to Status Projector.
- Order Intake delegates stock reservation needs to Inventory Client.
- Order Intake delegates label purchase needs to Carrier Client.
- Order Intake delegates notification dispatch needs to Notifier.
- Order Intake passes accepted orders to Order Writer.
- Order Writer publishes audit records to Audit Logger.
- Manual cancellation follow-up remains a future boundary candidate, not a diagram fact.
- Evidence anchors for FulfillmentController, StatusController, OrderIntake, InventoryClient, CarrierClient, Notifier, OrderWriter, and AuditLogger remain visible.
