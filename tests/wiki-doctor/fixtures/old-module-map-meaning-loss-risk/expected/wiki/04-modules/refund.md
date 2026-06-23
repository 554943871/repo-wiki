# Refund Module

Related reading: [Refund flow](../02-flows/refund.md).

## Old Module Map

Legacy note: Support, Refund UI, Refund Processor, and Payment are connected by "refund stuff"; the note does not name boundary ports or connector direction.

Evidence: `docs/refund-notes.md#legacy-map`

Uncertainty:

- Payment owns reversals?
- Refund Processor may be external.
- The old note says "API or job" but does not confirm which one is the module boundary port.
