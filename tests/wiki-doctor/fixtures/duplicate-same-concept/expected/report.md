# Expected Wiki Doctor Report

Mode: default safe rewrite.

Gate note: `wiki/07-drift.md` is already in the standard empty state.

Classification: `safe_guidance_rewrite`.

Actions: `safe_page_merge`, `safe_file_rename`, `safe_page_delete`, `update_canonical_index`.

Changed pages:

- `wiki/04-modules/billing.md`: merged duplicate same-concept content from `wiki/04-modules/billing-module.md`.
- `wiki/04-modules/README.md`: updated the Billing owner page to `./billing.md`.
- `wiki/02-flows/checkout.md`: updated the internal link to `../04-modules/billing.md`.

Unique information preserved:

- supports recurring invoice retries
- does not own tax-rate policy
- Evidence: `src/billing/BillingRetryJob.ts`
- Evidence: `src/billing/BillingController.ts`

Deleted or renamed pages:

- `wiki/04-modules/billing-module.md` was removed after its unique information was migrated.
