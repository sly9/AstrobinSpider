#!/bin/env python3

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import json
from os import listdir
from os.path import isfile, join
import os.path
from os import path

onlyfiles = [f for f in listdir('image_data/') if isfile(join('image_data/', f))]
print(onlyfiles)

images = None

images_dict = {}
for filename in onlyfiles:
    try:
        with open('./image_data/'+filename) as f:
            image_meta = json.load(f)
        images_dict[image_meta['hash']] = image_meta
    except:
        print('Load %s failed' % filename)
with open('./images.json','w') as f:
    json.dump(images_dict, f)
with open('./images.json') as f:
    images = json.load(f)
    
raw_array = []
radius = []
for a in images:
    image_meta = images[a]
    if 'ra' in image_meta and 'dec' in image_meta and 'radius' in image_meta:
        if image_meta['ra'] is not None:
            raw_array.append([image_meta['ra'], image_meta['dec']])
            radius.append(float(image_meta['radius']))
        #print('"https://astrobin.com/%s",%s,%s,%s' % (image_meta['hash'], image_meta['ra'], image_meta['dec'],image_meta['radius']))




# #############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X0 = np.asarray(raw_array)


print(type(X))
X = StandardScaler().fit_transform(X0)

# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.05, min_samples=5).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# #############################################################################
# Plot result


import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]


fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

for i in range(len(radius)):
    #print('Processing a point..')
    #print('has cluster? ' + str(core_samples_mask[i]))
    #print('label: %s' % labels[i])
    #print('color: %s' % str(colors[labels[i]]))
    #print('x: %f, y: %s' % (float(X0[i,0]), float(X0[i,1])))
    alpha = 1
    x = float(X0[i,0])
    y = float(X0[i,1])
    color = colors[labels[i]]
    if not core_samples_mask[i]:
        color = (0.8,0.8,0.8,1)
    if radius[i] > 5:
        alpha = 5 / radius[i]
    circle = plt.Circle((x, y), radius[i] * 0.75, color=color,linewidth=1, alpha=alpha)
    ax.add_patch(circle)

ax.set_aspect(aspect=1)
plt.xlim([0, 360])
plt.ylim([-90, 90])

fig.set_size_inches(12, 6)
ax.set_axis_off()
plt.set_cmap('hot')

#fig.savefig('test.svg', dpi=300, orientation='landscape', format='svg', transparent=True, bbox_inches='tight', pad_inches = 0)
fig.savefig('test.png', dpi=300, orientation='landscape', format='png', transparent=True, bbox_inches='tight', pad_inches = 0)
