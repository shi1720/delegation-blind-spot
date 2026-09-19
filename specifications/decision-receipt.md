# Decision receipt: a proposed measurement contract

Status: research design proposal, not a deployed standard or a claim of first use of the term.

A decision receipt records why an observation is relevant to a declared decision. It must not relabel an agent-generated explanation as a customer statement or verified outcome. The live receipt experiment in this release tests only extracting the largest already supplied weight, not the complete contract below.

## Required distinctions

| Field | Purpose |
| --- | --- |
| Decision ID and contrast version | Names the comparison the evidence is intended to inform. |
| Agent, interface and prompt versions | Defines the calibrated observation channel. |
| Assigned probe and assignment mechanism | Preserves the measurement condition instead of pooling incompatible channels. |
| Observation type and value | Separates an executed action from a supplied preference, model inference or confirmed outcome. |
| Evidence provenance | States whether information came from an input, an independent customer response or model inference. |
| Missing or refused | Retains absent information as an outcome rather than silently deleting it. |
| Calibration reference and validity window | Makes transport assumptions inspectable. |
| Allowed use and retention | Records the operational constraint; recording it is not proof of permission or privacy protection. |

The record below is a synthetic example. There is no customer identity or assertion of customer confirmation.

```json
{
  "schema_version": "research-proposal-0.1",
  "synthetic": true,
  "decision": {
    "id": "capacity-versus-flexibility",
    "contrast_version": "finite-bank-v2"
  },
  "measurement": {
    "kind": "supplied_preference_report",
    "value": "capacity",
    "evidence_source": "explicit_synthetic_input_weights",
    "customer_confirmed": false,
    "missing": false
  },
  "channel": {
    "agent_snapshot": "recorded-in-run-manifest",
    "prompt_version": "explicit-preference-receipt-v1",
    "probe_id": "largest-supplied-weight",
    "assignment": "frozen-follow-up-task-subset"
  },
  "scope": {
    "supports": "calibration of this declared observation channel",
    "does_not_establish": [
      "authentic human preferences",
      "future product satisfaction",
      "willingness to pay",
      "privacy guarantees"
    ]
  }
}
```

## Evaluation before deployment

1. Establish that the contrast represents an actual customer outcome, using an appropriate independent design.
2. Obtain genuine customer evidence and consent where needed. Do not substitute simulated personas.
3. Test whether receipts preserve relevant information beyond ordinary action logging at a matched measurement budget.
4. Measure elicitation burden, missingness, incentives to misreport, calibration drift and decision regret.
5. Separate a parser extracting known structured fields from a model inferring unknown preferences. Prefer direct extraction when the evidence is already structured.
6. Revalidate the channel and contrast when the product question, agent, interface or population changes.

The mathematical diagnostic can reveal ambiguity within the supplied model. It cannot certify that an incorrect taxonomy or poorly measured outcome is meaningful.
