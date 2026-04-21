# train_model.py - Run once to train model and generate charts
import pandas as pd, pickle, numpy as np, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patches as mpatches
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_curve, auc, classification_report)
from feature_extraction import extract_features

print("="*55); print("   PhishGuard AI — Model Trainer & Evaluator"); print("="*55)

print("\n[1/5] Loading dataset...")
df = pd.read_csv('dataset.csv')
print(f"      Total: {len(df):,} | Safe: {(df.label==0).sum():,} | Phishing: {df.label.sum():,}")

print("\n[2/5] Extracting features...")
X = [extract_features(u) for u in df['url']]
y = df['label'].tolist()
FEAT_NAMES = ['URL Length','Has IP Address','Dot Count','Has @ Symbol',
              'Uses HTTPS','Suspicious Keywords','Hyphen Count','Subdomain Count']

print("\n[3/5] Training Logistic Regression model...")
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
model = LogisticRegression(max_iter=1000,random_state=42)
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]
fpr,tpr,_ = roc_curve(y_test,y_prob)
roc_auc = auc(fpr,tpr)
acc=accuracy_score(y_test,y_pred); prec=precision_score(y_test,y_pred)
rec=recall_score(y_test,y_pred); f1=f1_score(y_test,y_pred)
print(f"\n      Accuracy={acc*100:.2f}% | Precision={prec*100:.2f}% | Recall={rec*100:.2f}% | F1={f1*100:.2f}% | AUC={roc_auc:.4f}")
print("\n"+classification_report(y_test,y_pred,target_names=['Safe','Phishing']))

print("[4/5] Saving model.pkl...")
with open('model.pkl','wb') as f: pickle.dump(model,f)

print("[5/5] Generating performance chart...")
os.makedirs('static',exist_ok=True)
BG,SURF,SURF2,BORDR = '#0a0c10','#10141c','#161b26','#1e2738'
AMBER,GREEN,RED,TEXT,MUTED = '#f5a623','#39d98a','#ff4d6a','#e8ecf4','#6b7a99'

fig = plt.figure(figsize=(16,10),facecolor=BG)
fig.suptitle('PhishGuard AI — Model Performance Report',color=AMBER,fontsize=18,fontweight='bold',y=0.97,fontfamily='monospace')
gs = fig.add_gridspec(2,3,hspace=0.45,wspace=0.35,left=0.07,right=0.97,top=0.90,bottom=0.08)

def style_ax(ax):
    ax.set_facecolor(SURF); ax.tick_params(colors=TEXT)
    for s in ax.spines.values(): s.set_color(BORDR)

# Confusion Matrix
ax1=fig.add_subplot(gs[0,0]); style_ax(ax1)
cm=confusion_matrix(y_test,y_pred); ax1.imshow(cm,cmap='YlOrRd',aspect='auto')
for i in range(2):
    for j in range(2): ax1.text(j,i,str(cm[i,j]),ha='center',va='center',color='white',fontsize=22,fontweight='bold',fontfamily='monospace')
ax1.set_xticks([0,1]); ax1.set_yticks([0,1])
ax1.set_xticklabels(['Safe','Phishing'],color=TEXT,fontsize=11); ax1.set_yticklabels(['Safe','Phishing'],color=TEXT,fontsize=11,rotation=90,va='center')
ax1.set_xlabel('Predicted',color=MUTED); ax1.set_ylabel('Actual',color=MUTED)
ax1.set_title('Confusion Matrix',color=AMBER,fontsize=12,fontweight='bold',pad=10,fontfamily='monospace')

# ROC Curve
ax2=fig.add_subplot(gs[0,1]); style_ax(ax2)
ax2.plot(fpr,tpr,color=AMBER,lw=2.5,label=f'AUC = {roc_auc:.4f}')
ax2.plot([0,1],[0,1],color=BORDR,lw=1.5,linestyle='--'); ax2.fill_between(fpr,tpr,alpha=0.12,color=AMBER)
ax2.set_xlim([0,1]); ax2.set_ylim([0,1.02])
ax2.set_xlabel('False Positive Rate',color=MUTED); ax2.set_ylabel('True Positive Rate',color=MUTED)
ax2.set_title('ROC Curve',color=AMBER,fontsize=12,fontweight='bold',pad=10,fontfamily='monospace')
ax2.legend(facecolor=SURF2,edgecolor=BORDR,labelcolor=TEXT); ax2.grid(True,color=BORDR,linewidth=0.5,alpha=0.6)

# Feature Importance
ax3=fig.add_subplot(gs[0,2]); style_ax(ax3)
coefs=model.coef_[0]; colors=[RED if c>0 else GREEN for c in coefs]
ax3.barh(FEAT_NAMES,np.abs(coefs),color=colors,height=0.6,edgecolor='none')
ax3.set_xlabel('|Coefficient|',color=MUTED); ax3.tick_params(colors=TEXT,labelsize=9)
ax3.set_title('Feature Importance',color=AMBER,fontsize=12,fontweight='bold',pad=10,fontfamily='monospace')
ax3.grid(True,axis='x',color=BORDR,linewidth=0.5,alpha=0.6)
ax3.legend(handles=[mpatches.Patch(color=RED,label='→ Phishing'),mpatches.Patch(color=GREEN,label='→ Safe')],
           facecolor=SURF2,edgecolor=BORDR,labelcolor=TEXT,fontsize=8)

# Metrics bars
ax4=fig.add_subplot(gs[1,0]); style_ax(ax4); ax4.axis('off'); ax4.set_xlim(0,1); ax4.set_ylim(0,1)
ax4.set_title('Metrics Summary',color=AMBER,fontsize=12,fontweight='bold',pad=10,fontfamily='monospace')
for i,(nm,v) in enumerate({'Accuracy':acc,'Precision':prec,'Recall':rec,'F1 Score':f1,'ROC-AUC':roc_auc}.items()):
    yp=0.82-i*0.18; ax4.text(0.05,yp,nm,color=MUTED,fontsize=11,va='center')
    ax4.barh([yp],[v*0.6],left=0.35,height=0.12,color=GREEN if v>=0.95 else AMBER,alpha=0.85)
    ax4.text(0.97,yp,f'{v:.4f}',color=TEXT,fontsize=11,va='center',ha='right',fontfamily='monospace',fontweight='bold')

# Dataset Distribution
ax5=fig.add_subplot(gs[1,1]); style_ax(ax5)
sc=(df.label==0).sum(); pc=df.label.sum()
bars=ax5.bar(['Safe URLs','Phishing URLs'],[sc,pc],color=[GREEN,RED],width=0.5,edgecolor='none')
ax5.set_title('Dataset Distribution',color=AMBER,fontsize=12,fontweight='bold',pad=10,fontfamily='monospace')
ax5.set_ylabel('Count',color=MUTED); ax5.grid(True,axis='y',color=BORDR,linewidth=0.5,alpha=0.6)
for b,v in zip(bars,[sc,pc]): ax5.text(b.get_x()+b.get_width()/2,b.get_height()+30,f'{v:,}',ha='center',color=TEXT,fontsize=12,fontweight='bold',fontfamily='monospace')
ax5.set_ylim(0,max(sc,pc)*1.18)

# URL Length Distribution
ax6=fig.add_subplot(gs[1,2]); style_ax(ax6)
ax6.hist([len(u) for u,l in zip(df.url,df.label) if l==0],bins=40,color=GREEN,alpha=0.7,label='Safe',edgecolor='none')
ax6.hist([len(u) for u,l in zip(df.url,df.label) if l==1],bins=40,color=RED,alpha=0.7,label='Phishing',edgecolor='none')
ax6.set_title('URL Length Distribution',color=AMBER,fontsize=12,fontweight='bold',pad=10,fontfamily='monospace')
ax6.set_xlabel('URL Length (chars)',color=MUTED); ax6.set_ylabel('Frequency',color=MUTED)
ax6.legend(facecolor=SURF2,edgecolor=BORDR,labelcolor=TEXT,fontsize=9); ax6.grid(True,color=BORDR,linewidth=0.5,alpha=0.6)

plt.savefig('static/model_performance.png',dpi=150,bbox_inches='tight',facecolor=BG); plt.close()
print("      Saved → static/model_performance.png")
print("\n✅ Done! Run: python app.py\n")
