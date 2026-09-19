(function () {
  'use strict';
  const core = window.InstrumentCore;
  const config = window.STUDY_CONFIG;
  const el = id => document.getElementById(id);
  const started = performance.now();
  let stepStarted = started;
  let step = 0;
  let record = null;
  const stepNames = ['INFORMATION', 'PREFERENCES', 'CHOICE', 'OUTCOMES', 'EXPORT'];
  function draw() {
    const n = new Uint32Array(1);
    window.crypto.getRandomValues(n);
    return n[0] / 4294967296;
  }
  function identifier() {
    const n = new Uint8Array(16);
    window.crypto.getRandomValues(n);
    return Array.from(n, b => b.toString(16).padStart(2, '0')).join('');
  }
  function error(text) { el('error').textContent = text; }
  function go(next) {
    if (record) record.elapsed_seconds_by_step[stepNames[step].toLowerCase()] = Math.round((performance.now() - stepStarted) / 100) / 10;
    el('step-' + step).classList.add('hidden');
    step = next;
    el('step-' + step).classList.remove('hidden');
    el('progress').textContent = 'STEP ' + (step + 1) + ' OF 5 / ' + stepNames[step];
    error('');
    stepStarted = performance.now();
    const heading = el('step-' + step).querySelector('h2');
    heading.tabIndex = -1;
    heading.focus();
    window.scrollTo({top: 0, behavior: 'auto'});
  }
  function exportJson(value, suffix) {
    const blob = new Blob([JSON.stringify(value, null, 2) + '\n'], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'PREVIEW-NOT-HUMAN-DATA-' + record.preview_id.slice(0, 8) + '-' + suffix + '.json';
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  el('start').addEventListener('click', function () {
    if (!el('acknowledge').checked) return error('Please acknowledge the preview information first.');
    if (!config || config.mode !== 'preview_only') return error('This version supports previews only. Participant collection requires a separately reviewed protocol and instrument.');
    if (!window.crypto || !window.crypto.getRandomValues) return error('This browser cannot provide the required random assignment.');
    record = {
      schema_version: '0.1.0',
      record_type: 'instrument_preview_not_human_evidence',
      human_participation_verified: false,
      informed_research_consent_collected: false,
      preview_information_acknowledged: true,
      preview_id: identifier(),
      config: {...config},
      assignment: {arm: core.assign(draw()), probability: 0.5, source: 'browser_crypto_getRandomValues'},
      recommendation: null,
      preferences: {}, choice: {}, outcomes: {}, elapsed_seconds_by_step: {}
    };
    go(1);
  });
  el('quiet-weight').addEventListener('input', () => { el('quiet-output').textContent = el('quiet-weight').value + ' / 100'; });
  el('preferences-next').addEventListener('click', function () {
    if (!el('preference-certainty').value) return error('Please select how certain you feel about your preference.');
    record.preferences = {quiet_weight: Number(el('quiet-weight').value), certainty: el('preference-certainty').value};
    const order = [...core.OPTIONS];
    for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(draw() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; }
    record.choice.display_order = order.map(o => o.id);
    const container = el('options');
    container.replaceChildren();
    order.forEach(o => {
      const label = document.createElement('label'); label.className = 'option';
      const radio = document.createElement('input'); radio.type = 'radio'; radio.name = 'hotel'; radio.value = o.id;
      const name = document.createElement('strong'); name.textContent = ' ' + o.name;
      const attributes = document.createElement('div'); attributes.className = 'attributes';
      [o.price + ' credits', 'Quietness ' + o.quiet + '/10', o.minutes + ' min to meeting'].forEach(t => { const span = document.createElement('span'); span.textContent = t; attributes.appendChild(span); });
      label.append(radio, name, attributes); container.appendChild(label);
    });
    if (record.assignment.arm === 'reference_aided') {
      const id = core.recommendation(record.preferences.quiet_weight);
      const option = core.OPTIONS.find(o => o.id === id);
      record.recommendation = {source: 'deterministic_reference_chooser', version: '0.1.0', option_id: id, formula: 'w*(quiet/10)+(1-w)*((30-minutes)/30)', tie_break: 'stable_option_id_ascending'};
      el('aid').textContent = 'Rule-based decision aid: ' + option.name + '. This recommendation combines your stated quietness weight with normalized quietness and travel time. It is a simple reference rule, not a live AI. You may choose any hotel.';
      el('aid').classList.remove('hidden');
    }
    go(2);
  });
  el('choice-next').addEventListener('click', function () {
    const choice = document.querySelector('input[name="hotel"]:checked');
    if (!choice) return error('Please select a hotel.');
    record.choice.option_id = choice.value;
    go(3);
  });
  el('outcomes-next').addEventListener('click', function () {
    const ids = ['fit', 'improvement', 'clarity', 'burden'];
    if (ids.some(id => !el(id).value)) return error('Please complete the four short follow-up questions.');
    record.outcomes = {self_reported_fit: Number(el('fit').value), future_improvement: el('improvement').value, clarity: el('clarity').value, self_reported_burden: Number(el('burden').value)};
    record.elapsed_seconds_total = Math.round((performance.now() - started) / 100) / 10;
    core.validateExport(record);
    el('summary').textContent = 'Assigned condition: ' + (record.assignment.arm === 'unaided' ? 'unaided choice' : 'rule-based reference aid') + '. Selected hotel: ' + core.OPTIONS.find(o => o.id === record.choice.option_id).name + '. Reported fit: ' + record.outcomes.self_reported_fit + '/5. Record type: instrument preview, not human evidence.';
    go(4);
  });
  el('export-full').addEventListener('click', function () { core.validateExport(record); exportJson(record, 'full'); });
  el('export-actions').addEventListener('click', function () {
    core.validateExport(record);
    exportJson({schema_version: record.schema_version, record_type: record.record_type, human_participation_verified: false, preview_id: record.preview_id, protocol_id: config.protocolId, assignment: record.assignment, observed_choice: record.choice, data_view: 'action_only_preview_no_preferences_or_outcomes'}, 'actions');
  });
  el('clear').addEventListener('click', function () { record = null; window.location.reload(); });
})();
