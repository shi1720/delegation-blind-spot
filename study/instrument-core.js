(function (root) {
  'use strict';
  const OPTIONS = Object.freeze([
    Object.freeze({ id: 'garden', name: 'Garden House', price: 130, quiet: 9, minutes: 25 }),
    Object.freeze({ id: 'central', name: 'Central House', price: 130, quiet: 5, minutes: 5 }),
    Object.freeze({ id: 'courtyard', name: 'Courtyard House', price: 130, quiet: 7, minutes: 15 })
  ]);
  function score(option, quietWeight) {
    if (!Number.isFinite(quietWeight) || quietWeight < 0 || quietWeight > 100) throw new Error('Invalid preference');
    return quietWeight / 100 * option.quiet / 10 + (1 - quietWeight / 100) * (30 - option.minutes) / 30;
  }
  function recommendation(quietWeight) {
    // Neutral tie break by stable identifier, declared in the protocol.
    return [...OPTIONS].sort((a, b) => score(b, quietWeight) - score(a, quietWeight) || a.id.localeCompare(b.id))[0].id;
  }
  function assign(randomUniform) {
    if (!(randomUniform >= 0 && randomUniform < 1)) throw new Error('Invalid random draw');
    return randomUniform < 0.5 ? 'unaided' : 'reference_aided';
  }
  function validateExport(record) {
    if (record.record_type !== 'instrument_preview_not_human_evidence') throw new Error('Only preview exports allowed');
    if (record.human_participation_verified !== false) throw new Error('Cannot verify human participation');
    if (!['unaided', 'reference_aided'].includes(record.assignment.arm)) throw new Error('Invalid arm');
    if (!OPTIONS.some(o => o.id === record.choice.option_id)) throw new Error('Invalid choice');
    if (record.config.mode !== 'preview_only') throw new Error('Participant collection is not implemented');
    return true;
  }
  const api = { OPTIONS, score, recommendation, assign, validateExport };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.InstrumentCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
