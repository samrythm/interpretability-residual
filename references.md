import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.family':'serif','font.size':9,
                     'axes.edgecolor':'#444','axes.labelcolor':'#222','text.color':'#222',
                     'xtick.color':'#444','ytick.color':'#444'})
INK='#333333'; MID='#8a8a8a'; LITE='#d8d8d8'

rng=np.random.default_rng(7); N=200_000
p=rng.beta(2,8,N); ci=rng.beta(6,14,N); ch=rng.beta(2,38,N)
t=rng.beta(14,6,N); f=rng.beta(5,15,N); ec=rng.beta(2,98,N)
lb=lambda pp,a,b: np.minimum(pp*a,(1-pp)*b)
ln=p*ci; s=t*p+f*(1-p); n=1-s
po=(t*p)/s; pn=((1-t)*p)/n
voi=ln-(s*lb(po,ci,ch)+n*lb(pn,ci,ch)+ec)

# ---- Figure 1: two panels ----
fig,(a1,a2)=plt.subplots(1,2,figsize=(9.4,3.4),dpi=150)
a1.hist(voi,bins=130,range=(-0.06,0.16),color=MID,edgecolor='none')
a1.axvline(0,color=INK,lw=1.2,ls='--')
a1.set_xlabel('Value of information'); a1.set_ylabel('density')
a1.set_title(f'(a)  VoI under parameter uncertainty\nP(worth funding) = {(voi>0).mean():.2f}',fontsize=9.5)
a1.set_yticks([]); a1.spines[['top','right','left']].set_visible(False); a1.grid(alpha=.15,axis='x')

ratios=np.linspace(1.2,12,300)
cih=0.30; chs=cih/ratios
pstar=chs/(cih+chs)
a2.plot(ratios,pstar,color=INK,lw=1.8)
a2.scatter([6],[0.05/(0.30+0.05)],s=26,color=INK,zorder=5)
a2.annotate('baseline 6:1\np* = 0.14',xy=(6,0.143),xytext=(7.0,0.30),fontsize=8.3,
            arrowprops=dict(arrowstyle='->',color=INK,lw=.9))
a2.set_xlabel('Harm asymmetry  $c_{ignore}/c_{hedge}$'); a2.set_ylabel('Belief threshold  $p^*$')
a2.set_title('(b)  The threshold is a function of harm asymmetry,\nnot of the chosen prior',fontsize=9.5)
a2.spines[['top','right']].set_visible(False); a2.grid(alpha=.15)
plt.tight_layout(); plt.savefig('f1.png',dpi=150,bbox_inches='tight'); plt.close()

# ---- Figure 2: separation floor vs prior (honest contingency) ----
def sepfloor(pr,cig=.30,che=.05,ecx=.02):
    lo,hi=0.001,0.99
    def v(g):
        tt,ff=.5+g/2,.5-g/2
        l0=pr*cig; ss=tt*pr+ff*(1-pr); nn=1-ss
        aa=(tt*pr)/ss; bb=((1-tt)*pr)/nn
        return l0-(ss*min(aa*cig,(1-aa)*che)+nn*min(bb*cig,(1-bb)*che)+ecx)
    for _ in range(80):
        m=(lo+hi)/2
        if v(m)<=1e-9: lo=m
        else: hi=m
    return (lo+hi)/2

prs=np.linspace(0.06,0.40,160)
fl=[sepfloor(x) for x in prs]
fig,ax=plt.subplots(figsize=(5.6,3.1),dpi=150)
ax.plot(prs,fl,color=INK,lw=1.8)
ax.fill_between(prs,fl,1.0,alpha=.10,color=MID)
ax.axhline(0.13,color=INK,lw=1,ls=':')
ax.text(0.305,0.155,'IOI residual \u2248 0.13',fontsize=8,color=INK)
ax.set_xlabel('Prior credence the residual persists')
ax.set_ylabel('Required metric separation\n(TPR \u2212 FPR)')
ax.set_title('Required measurement quality is prior-dependent',fontsize=9.5)
ax.set_ylim(0,1); ax.spines[['top','right']].set_visible(False); ax.grid(alpha=.15)
ax.text(0.10,0.80,'study not\ninformative enough',fontsize=8,color='#666')
plt.tight_layout(); plt.savefig('f2b.png',dpi=150,bbox_inches='tight'); plt.close()

# ---- Figure 3: theory of change chain ----
fig,ax=plt.subplots(figsize=(9.4,1.65),dpi=150)
ax.axis('off')
steps=['Residual\nbenchmark','Residual estimate\nreported with\ncompleteness','Updated confidence\nin circuit-based\nauditing','Research and\nfunding\nprioritisation','Audit claims\nmatched to\nactual coverage']
xs=np.linspace(0.055,0.945,len(steps))
for i,(x,txt) in enumerate(zip(xs,steps)):
    ax.text(x,0.5,txt,ha='center',va='center',fontsize=8.2,color=INK,
            bbox=dict(boxstyle='round,pad=0.5',facecolor='#f4f4f4',edgecolor='#bbb',lw=.8))
    if i<len(steps)-1:
        ax.annotate('',xy=(xs[i+1]-0.082,0.5),xytext=(x+0.082,0.5),
                    arrowprops=dict(arrowstyle='-|>',color='#777',lw=1.0))
ax.set_xlim(0,1); ax.set_ylim(0,1)
plt.tight_layout(); plt.savefig('f3.png',dpi=150,bbox_inches='tight'); plt.close()
print("figures ok")
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif'})
INK='#2b2b2b'
fig,ax=plt.subplots(figsize=(9.4,1.75),dpi=150); ax.axis('off')
steps=[('Current\ninterpretability','circuits, SAEs,\ncausal methods'),
       ('Completeness\nmetric','what the circuit\nexplains'),
       ('Residual','$R = 1-$completeness\nwith uncertainty'),
       ('Decision model','Bayesian VoI\nover thresholds'),
       ('Funding\ndecision','measure now, or\nfix metrics first')]
xs=[0.055,0.28,0.5,0.72,0.945]
for i,(x,(a,b)) in enumerate(zip(xs,steps)):
    ax.text(x,0.62,a,ha='center',va='center',fontsize=9,color=INK,weight='bold',
            bbox=dict(boxstyle='round,pad=0.55',facecolor='#f5f5f5',edgecolor='#aaa',lw=.9))
    ax.text(x,0.16,b,ha='center',va='center',fontsize=7.2,color='#6a6a6a',style='italic')
    if i<4:
        ax.annotate('',xy=(xs[i+1]-0.075,0.62),xytext=(x+0.075,0.62),
                    arrowprops=dict(arrowstyle='-|>',color='#777',lw=1.1))
ax.set_xlim(0,1); ax.set_ylim(0,1)
plt.tight_layout(); plt.savefig('f0.png',dpi=150,bbox_inches='tight')
print('pipeline ok')
