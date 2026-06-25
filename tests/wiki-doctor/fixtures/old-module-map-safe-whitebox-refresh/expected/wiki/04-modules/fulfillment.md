# Fulfillment Module

Fulfillment accepts paid checkout orders and starts stock reservation work.

Related reading: [Checkout flow](../02-flows/checkout.md) and [Inventory model](../05-models/inventory.md).

## 模块边界图（Module Boundary Map）

![Fulfillment Module whitebox component diagram](./assets/fulfillment.whitebox.svg)

Source model: [`fulfillment.whitebox.yaml`](./fulfillment.whitebox.yaml) for the complete diagram and generated derived views.

### Boundary Derived Whitebox View

Reader purpose: Boundary view isolates who can call Fulfillment and which boundary ports they use.

![Fulfillment Module Boundary Derived Whitebox View](./assets/fulfillment.whitebox.boundary.svg)

### Assembly Derived Whitebox View

Reader purpose: Assembly view isolates the internal persistence and audit chain after intake accepts an order.

![Fulfillment Module Assembly Derived Whitebox View](./assets/fulfillment.whitebox.assembly.svg)

Generated derived views are reader aids from the same source model; only reader-purpose views are embedded here, and none replace the complete diagram.

Current Whitebox facts preserve these confirmed boundary details:

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

Evidence:

- Evidence: `src/fulfillment/FulfillmentController.ts`
- Evidence: `src/fulfillment/StatusController.ts`
- Evidence: `src/fulfillment/OrderIntake.ts`
- Evidence: `src/fulfillment/InventoryClient.ts`
- Evidence: `src/fulfillment/CarrierClient.ts`
- Evidence: `src/fulfillment/Notifier.ts`
- Evidence: `src/fulfillment/OrderWriter.ts`
- Evidence: `src/fulfillment/AuditLogger.ts`

Uncertainty preserved:

- Manual cancellation follow-up is mentioned as a future boundary candidate, not confirmed. It stays out of the source model until confirmed.
