import pandas as pd
import numpy as np
import func_stats as fs
import func_plot as fp
from brainspace.gradient import GradientMaps
import networkx as nx

import warnings
warnings.filterwarnings("ignore")

df_impute = pd.read_csv('../data/df_impute.csv')
data_combat = np.array(df_impute[fp.region_list])


## calculate covariation
"""
cova_data = np.zeros((data_combat.shape[0], 68, 68))
std = data_combat[df_impute.DX == 0].std(axis=0)
for sub in range(data_combat.shape[0]):
    cova_data[sub] = fs.cova_indi(data_combat[sub], std)

np.save('../data/coviariation_indiviudal.npy', cova_data)
"""
spa=60 # top20%
cova_data = np.load('../data/coviariation_indiviudal.npy')

## calculate small-world topology

cova_data_spa = cova_data.copy()
for i in range(len(cova_data)):
  for j in range(68):
    cova_data_spa[i,j][cova_data_spa[i,j]<np.percentile(cova_data_spa[i,j], spa)]=0


length_indi = np.zeros((len(cova_data_spa),68))
cluster_indi = np.zeros((len(cova_data_spa),68))

for i in range(len(cova_data_spa)):
  G_graph = nx.from_numpy_array(cova_data_spa[i])
  sw = fs.regional_small_worldness(G_graph)
  tmp = np.array(list(sw[0].values()))
  cluster_indi[i] = (tmp-tmp.min())/(tmp.max() - tmp.min())
  tmp = np.array(list(sw[1].values()))
  length_indi[i] = (tmp-tmp.min())/(tmp.max() - tmp.min())
  print(i, cluster_indi[i][0], length_indi[i][0])
np.save('../data/coviariation_indiviudal_spa'+str(spa)+'.npy', cova_data_spa)
np.save('../data/length_indi_spa'+str(spa)+'.npy', length_indi)
np.save('../data/cluster_indi_spa'+str(spa)+'.npy', cluster_indi)


## calculate gradients
cova_data_spa = np.load('../data/coviariation_indiviudal_spa'+str(spa)+'.npy')
gm_ctr = np.loadtxt('../data/gm_ctr'+str(spa)+'.txt')
grad_indi = [None] * len(cova_data_spa)
for i in range(len(cova_data_spa)):
  gm = GradientMaps(approach='dm', kernel='normalized_angle', alignment='procrustes', random_state=0)
  grad_indi[i] = gm.fit(cova_data_spa[i], sparsity=0, reference=gm_ctr)

np.savetxt('../results/enigma_g1/'+str(spa)+'indi_g1.txt', 
           np.array([grad_indi[i].aligned_[:,0] for i in range(len(cova_data))]))

np.savetxt('../results/enigma_g2/'+str(spa)+'indi_g2.txt', 
           np.array([grad_indi[i].aligned_[:,1] for i in range(len(cova_data))]))