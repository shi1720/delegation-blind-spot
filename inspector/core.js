(function(root){
'use strict';
const SCHEMAS = {
 primary_action:{label:'Primary / action only',description:'Selected product type plus failures; no continuous menu details.'},
 primary_context:{label:'Primary / context + action',description:'Selected product type paired with the recorded context regime, plus failures.'},
 matched_action:{label:'Follow-up / matched actions',description:'Original actions for exactly the selected follow-up task IDs and observation counts.'},
 receipt:{label:'Follow-up / preference receipt',description:'Leading attribute in explicitly supplied weights. Twelve distinct prompts, repeatedly queried.'}
};
function select(data,model,domain,cohort,schema){
 const rows=data.rows.filter(r=>r.model===model&&r.domain===domain&&r.cohort===cohort&&r.schema===schema);
 if(rows.length!==1)throw new Error('Selection does not identify exactly one recorded condition.');
 return rows[0];
}
function decisionLabel(row){
 if(row.lower>1e-8)return 'Capacity supported';
 if(row.upper< -1e-8)return 'Flexibility supported';
 return 'Decision unresolved';
}
function witnessValue(row,side){return row[side+'_witness'].reduce((s,p,i)=>s+p*row.class_contrasts[i],0);}
function format(x,digits=4){return (x>=0?'+':'')+x.toFixed(digits);}
const api={SCHEMAS,select,decisionLabel,witnessValue,format};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.InspectorCore=api;
})(typeof window!=='undefined'?window:globalThis);
