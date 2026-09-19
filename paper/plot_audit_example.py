"""Compact, data-derived view of one recorded audit; not a usability result."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
ROOT=Path(__file__).resolve().parents[1]
record=next(r for r in json.loads((ROOT/'results/model-study-mini/analysis.json').read_text())['reports'] if (r['domain'],r['cohort'],r['log_schema'])==('cloud','positive','action_only'))
d=np.array(record['known_synthetic_class_contrasts']);lo=np.array(record['lower_witness_population']);hi=np.array(record['upper_witness_population'])
assert np.isclose(d@lo,record['lower']) and np.isclose(d@hi,record['upper'])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'pdf.fonttype':42,'ps.fonttype':42})
fig=plt.figure(figsize=(6.8,2.05),facecolor='white')
a=fig.add_axes([.065,.30,.38,.43]); b=fig.add_axes([.56,.30,.41,.43])
a.axvline(0,color='#8E969C',ls=':',lw=1)
a.plot([record['lower'],record['upper']],[.5,.5],color='#966F28',lw=4,solid_capstyle='round')
a.scatter([record['lower'],record['upper']],[.5,.5],s=28,color='#966F28',zorder=3)
a.set_xlim(-.045,.065);a.set_ylim(0,1);a.set_yticks([]);a.set_xticks([-.04,0,.04],labels=['−0.04','0','+0.04']);a.set_xlabel('Capacity minus flexibility utility',labelpad=3)
a.set_title('Decision unresolved',loc='left',fontsize=10,weight='bold',pad=12)
a.text(record['lower'],.73,f"{record['lower']:.4f}",ha='center',fontsize=8)
a.text(record['upper'],.73,f"+{record['upper']:.4f}",ha='center',fontsize=8)
for side in ['top','right','left']:a.spines[side].set_visible(False)
colors=['#74579B','#A8ADB3','#267B88','#DDAB70'];labels=['Capacity','Affordability','Portability','Support']
for y,p in [(1,lo),(0,hi)]:
 left=0
 for v,c in zip(p,colors):
  b.barh(y,v,left=left,color=c,height=.44)
  if v>.08:b.text(left+v/2,y,f'{v*100:.1f}%',ha='center',va='center',color='white' if c in colors[:1]+colors[2:3] else '#26313A',fontsize=8)
  left+=v
b.set_title('Compatible endpoint populations',loc='left',fontsize=10,weight='bold',pad=12)
b.set_xlim(0,1);b.set_ylim(-.5,1.5);b.set_xticks([]);b.set_yticks([1,0],labels=['Lower','Upper']);b.tick_params(axis='y',length=0)
for spine in b.spines.values():spine.set_visible(False)
fig.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],loc='lower right',bbox_to_anchor=(.98,.04),ncol=4,frameon=False,fontsize=7,handlelength=1,columnspacing=.9)
fig.text(.065,.95,'Recorded example: Mini / cloud / cohort A / primary actions',fontsize=8,color='#42545F')
fig.text(.065,.02,'320 calibration observations; 160 field observations. Synthetic outcomes. Witnesses are not estimates.',fontsize=7,color='#42545F')
out=ROOT/'paper/generated';fig.savefig(out/'audit-example.pdf',bbox_inches='tight');fig.savefig(out/'audit-example.png',dpi=180,bbox_inches='tight')
print('Wrote figure from recorded audit endpoints and witnesses.')
