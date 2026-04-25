import pandas as pd
import numpy as np
from neuroCombat import neuroCombat
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import func_plot as fp

df = pd.read_csv('../data/data_raw.csv')
df.loc[df.sex=='M','sex'] = 1 
df.loc[df.sex=='F','sex'] = 2 
df.loc[df.DX=='SCZ','DX'] = 1 
df.loc[df.DX=='CTR','DX'] = 0 
df.age = df.age.round(0)
site = df['site'].astype(str).str[:2]
df.insert(0,'site_num',np.array(site).astype(int))

region_list = fp.region_list
df_ct = df[region_list]

# missing data for one person should be less than 7 (10%)
df_ct = df_ct[df_ct.isna().sum(axis=1) < 7]
df_tmp = pd.concat([df[['site_num','DX','age','sex','ICV']].loc[df_ct.index], df_ct], axis=1).reset_index(drop=True)

data_combat = np.zeros((len(df_tmp),68))
data_combat[data_combat==0] = np.nan

for i in range(68):
  print(i+1, region_list[i])
  tmp_tmp = df_tmp[['site_num','DX','age','sex']+[region_list[i]]].dropna()

  data_combat[:,i][tmp_tmp.index] = neuroCombat(dat=np.vstack(((np.ones(len(tmp_tmp)),tmp_tmp[fp.region_list[i]].astype(float)))), 
                           covars=tmp_tmp[['site_num','DX','age','sex']].reset_index(drop=True), batch_col='site_num',
                           categorical_cols=['DX','sex'])['data'][1]

df_tmp[region_list] = data_combat

icv_combat = np.zeros(len(df_tmp))
icv_combat[icv_combat==0] = np.nan
tmp_tmp = df_tmp[['site_num','DX','age','sex','ICV']].dropna()
icv_combat[tmp_tmp.index] = neuroCombat(dat=np.vstack(((np.ones(len(tmp_tmp)),tmp_tmp['ICV'].astype(float)))), 
                           covars=tmp_tmp[['site_num','DX','age','sex']].reset_index(drop=True), batch_col='site_num',
                           categorical_cols=['DX','sex'])['data'][1]

df_tmp['ICV'] = icv_combat

imp = IterativeImputer(max_iter=10, random_state=0)
imp.fit(df_tmp)
impute = imp.transform(df_tmp)

df_impute = pd.DataFrame(impute,columns=df_tmp.columns)
# np_ct = np.array(df_impute[region_list],dtype=float)

df_impute = pd.concat([df[['site','ID', 'AO', 'IQ', 'CPZ', 'sans_total']].loc[df_ct.index].reset_index(drop=True),
            df_impute], axis=1)

df_impute.loc[df_impute.sex>1.5,'sex']=2
df_impute.loc[df_impute.sex<1.5,'sex']=1

df_impute.to_csv('../data/df_impute.csv', index=None)