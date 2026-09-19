(function(){
'use strict';
const data=window.INSPECTOR_DATA, core=window.InspectorCore;
const el=id=>document.getElementById(id);
function svgNode(tag,attrs,text){const n=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,String(v)));if(text!==undefined)n.textContent=text;return n;}
function chart(row){
 const min=-.05,max=.065,width=Math.max(280,Math.min(650,el('interval-chart').clientWidth)),left=25,right=width-25;
 const x=v=>left+(v-min)/(max-min)*(right-left);
 const svg=svgNode('svg',{viewBox:'0 0 '+width+' 90','aria-hidden':'true'});
 svg.append(svgNode('line',{x1:left,x2:right,y1:38,y2:38,stroke:'#d2dce1','stroke-width':2}));
 [-.04,-.02,0,.02,.04,.06].forEach(v=>{svg.append(svgNode('line',{x1:x(v),x2:x(v),y1:32,y2:45,stroke:v===0?'#516c76':'#d2dce1','stroke-width':v===0?2:1}));svg.append(svgNode('text',{x:x(v),y:68,'text-anchor':'middle',fill:'#556972','font-size':11,'font-family':'system-ui'},v===0?'0':core.format(v,2)));});
 const color=row.decision==='unresolved'?'#846329':'#176776';
 svg.append(svgNode('line',{x1:x(row.lower),x2:x(row.upper),y1:38,y2:38,stroke:color,'stroke-width':6,'stroke-linecap':'round'}));
 for(const v of [row.lower,row.upper])svg.append(svgNode('circle',{cx:x(v),cy:38,r:5,fill:color,stroke:'white','stroke-width':2}));
 const target=el('interval-chart');target.replaceChildren(svg);target.setAttribute('aria-label','Recorded contrast interval '+core.format(row.lower)+' to '+core.format(row.upper)+'. Zero separates flexibility from capacity.');
}
function update(){
 const row=core.select(data,el('model').value,el('domain').value,el('cohort').value,el('schema').value);
 el('schema-description').textContent=core.SCHEMAS[row.schema].description;
 el('decision').textContent=core.decisionLabel(row);el('decision').classList.toggle('resolved',row.decision!=='unresolved');
 el('interval-text').textContent='['+core.format(row.lower)+', '+core.format(row.upper)+']';
 el('decision-detail').textContent=row.decision==='unresolved'?'The evidence admits both negative and positive contrasts. This report does not select an investment.':'Within the supplied uncertainty model, both endpoints favor capacity. This is a conditional synthetic result, not a customer-validated recommendation.';
 if(row.decision==='flexibility')el('decision-detail').textContent='Within the supplied uncertainty model, both endpoints favor flexibility. This is a conditional synthetic result, not a customer-validated recommendation.';
 el('calibration').textContent=row.calibration_n+' ('+row.calibration_by_class[0]+'/class)';
 el('field').textContent=row.field_n;el('failures').textContent=row.field_failures;
 el('comparison-warning').textContent=row.followup?'Exploratory follow-up after primary results. Compare receipt with matched actions, not the larger primary sample. Equal counts do not equalize cost or burden.':'Primary study. A change of logging schema can change uncertainty-box conservatism; a wider interval alone does not imply less intrinsic information.';
 chart(row);
 el('witnesses').replaceChildren();
 row.class_attributes.forEach((name,i)=>{
  const tr=document.createElement('tr'),heading=document.createElement('th');heading.scope='row';heading.textContent=name+' first';tr.append(heading);
  const contrast=document.createElement('td');contrast.textContent=core.format(row.class_contrasts[i]);tr.append(contrast);
  for(const side of ['lower','upper']){const cell=document.createElement('td');cell.className='mix-cell '+side;const p=row[side+'_witness'][i];cell.append(document.createTextNode((100*p).toFixed(1)+'%'));const bar=document.createElement('span');bar.className='mix-bar';const fill=document.createElement('span');fill.style.width=(100*p)+'%';bar.append(fill);cell.append(bar);tr.append(cell);}
  el('witnesses').append(tr);
 });
 el('lower-value').textContent=core.format(core.witnessValue(row,'lower'));el('upper-value').textContent=core.format(core.witnessValue(row,'upper'));
 el('snapshot').textContent=row.model_snapshot;el('source').textContent=row.source;
 el('source-hash').textContent=data.sources.find(s=>s.path===row.source).sha256;
 el('violation').textContent=row.solver_violation.toExponential(3);
}
window.addEventListener('resize',update);
for(const id of ['model','domain','cohort','schema'])el(id).addEventListener('change',update);
el('reset').addEventListener('click',()=>{el('model').value='mini';el('domain').value='cloud';el('cohort').value='A';el('schema').value='primary_action';update();});
update();
})();
