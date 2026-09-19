'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const core=require('./core.js');const sandbox={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'data.js'),'utf8'),sandbox);
const data=sandbox.window.INSPECTOR_DATA;
assert.equal(data.rows.length,72);assert.equal(data.evaluation_truth_included,false);
for(const row of data.rows){
 assert.equal(core.select(data,row.model,row.domain,row.cohort,row.schema).id,row.id);
 assert(row.lower<=row.upper);assert(row.lower>=-.05&&row.upper<=.065);
 for(const side of ['lower','upper']){assert(Math.abs(core.witnessValue(row,side)-row[side])<1e-7);assert(Math.abs(row[side+'_witness'].reduce((a,b)=>a+b,0)-1)<1e-7);}
 assert.equal(core.decisionLabel(row),row.decision==='unresolved'?'Decision unresolved':row.decision==='capacity'?'Capacity supported':'Flexibility supported');
 assert(!('evaluation_only' in row));assert(!('true_contrast' in row));assert(!('true_population' in row));
 assert.equal(row.calibration_by_class.reduce((a,b)=>a+b,0),row.calibration_n);
}
assert.throws(()=>core.select(data,'unknown','cloud','A','receipt'));
assert.equal(core.select(data,'mini','cloud','A','receipt').decision,'capacity');
assert.equal(core.select(data,'mini','cloud','A','matched_action').decision,'unresolved');
console.log('All 72 selections, witness endpoints, decisions, denominators, and withheld-truth checks passed.');
