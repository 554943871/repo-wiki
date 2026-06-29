# Shipping Module

Related reading: [Shipping flow](../02-flows/shipping.md).

## Old Module Map

The old map says Checkout API calls Shipping Planner through Create Shipment.

Evidence: `src/shipping/routes.ts` before the route cleanup.

Uncertainty: Current code may now route through Delivery Orchestrator. Refreshing the map requires comparing the wiki with current code before deciding the external entry point or connector direction.
