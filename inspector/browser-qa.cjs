'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const packageRoot=process.env.PLAYWRIGHT_PACKAGE_ROOT;
const {chromium}=packageRoot?require(require.resolve('playwright',{paths:[packageRoot]})):require('playwright');
const out=path.join(__dirname,'qa-artifacts');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 const report={test_data_only:true,browser:await browser.version(),cases:[],network_requests:[],page_errors:[],console_errors:[]};
 for(const spec of [{name:'desktop',width:1440,height:1100},{name:'mobile',width:390,height:844}]){
  const context=await browser.newContext({viewport:{width:spec.width,height:spec.height}}),page=await context.newPage();
  page.on('pageerror',e=>report.page_errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.console_errors.push(m.text());});
  page.on('request',r=>{if(/^https?:/.test(r.url()))report.network_requests.push(r.url());});
  await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);
  assert.equal(await page.locator('#decision').innerText(),'Decision unresolved');
  await page.screenshot({path:path.join(out,spec.name+'-primary.png'),fullPage:true});
  const rowCount=await page.evaluate(()=>window.INSPECTOR_DATA.rows.length);assert.equal(rowCount,72);
  await page.locator('#model').focus();await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.id),'domain');
  await page.locator('#schema').selectOption('receipt');
  assert.equal(await page.locator('#decision').innerText(),'Capacity supported');
  assert.equal(await page.locator('#calibration').innerText(),'160 (40/class)');
  assert.equal(await page.locator('#field').innerText(),'80');
  assert.match(await page.locator('#comparison-warning').innerText(),/Exploratory/);
  await page.screenshot({path:path.join(out,spec.name+'-receipt.png'),fullPage:true});
  await page.locator('#schema').selectOption('matched_action');assert.equal(await page.locator('#decision').innerText(),'Decision unresolved');
  for(const model of ['mini','nano'])for(const domain of ['cloud','travel','workflow'])for(const cohort of ['A','B','C'])for(const schema of ['primary_action','primary_context','matched_action','receipt']){
   await page.locator('#model').selectOption(model);await page.locator('#domain').selectOption(domain);await page.locator('#cohort').selectOption(cohort);await page.locator('#schema').selectOption(schema);
   const expected=await page.evaluate(({model,domain,cohort,schema})=>{const c=window.InspectorCore,r=c.select(window.INSPECTOR_DATA,model,domain,cohort,schema);return{decision:c.decisionLabel(r),interval:'['+c.format(r.lower)+', '+c.format(r.upper)+']',lo:c.format(c.witnessValue(r,'lower')),hi:c.format(c.witnessValue(r,'upper'))};},{model,domain,cohort,schema});
   assert.equal(await page.locator('#decision').innerText(),expected.decision);assert.equal(await page.locator('#interval-text').innerText(),expected.interval);assert.equal(await page.locator('#lower-value').innerText(),expected.lo);assert.equal(await page.locator('#upper-value').innerText(),expected.hi);
  }
  await page.locator('summary').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('details').getAttribute('open'),'');
  assert.match(await page.locator('#snapshot').innerText(),/gpt-5.4-nano-2026-03-17/);assert.match(await page.locator('#source-hash').innerText(),/^[a-f0-9]{64}$/);
  await page.locator('#reset').click();assert.equal(await page.locator('#model').inputValue(),'mini');assert.equal(await page.locator('#schema').inputValue(),'primary_action');
  const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,local:localStorage.length,session:sessionStorage.length,evaluationKeys:JSON.stringify(window.INSPECTOR_DATA).includes('true_contrast')||JSON.stringify(window.INSPECTOR_DATA).includes('true_population')}));
  assert.equal(state.overflow,false);assert.equal(state.local,0);assert.equal(state.session,0);assert.equal(state.evaluationKeys,false);
  report.cases.push({viewport:spec.name,conditions_checked:72,keyboard_navigation:true,reset:true,no_horizontal_overflow:true,no_evaluation_truth:true});await context.close();
 }
 assert.deepEqual(report.network_requests,[]);assert.deepEqual(report.page_errors,[]);assert.deepEqual(report.console_errors,[]);
 await browser.close();fs.writeFileSync(path.join(out,'browser-qa-results.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1);});
