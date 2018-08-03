#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv

data_name = 'local.csv'
with open(data_name, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

print data
data[0][0]='in-situ'
print data

in_nvm = [x[3:5] for x in data if x[0] == 'in-situ' and x[1] == 'nvm']
print in_nvm
in_lustre = [x[3:4] for x in data if x[0] == 'in-situ' and x[1] == 'lustre']
print in_lustre
post_nvm = [x[3:5] for x in data if x[0] == 'post-processing' and x[1] == 'nvm']
print post_nvm
post_lustre = [x[3:4] for x in data if x[0] == 'post-processing' and x[1] == 'lustre']
print post_lustre

nvm_in_nvm = [float(x[0]) for x in in_nvm]
print nvm_in_nvm
nvm_post_nvm = [float(x[0]) for x in post_nvm]
print nvm_post_nvm

hdfs_in_nvm = [float(x[1]) for x in in_nvm]
print hdfs_in_nvm
hdfs_post_nvm = [float(x[1]) for x in post_nvm]
print hdfs_post_nvm

lustre_in_lustre = [float(x[0]) for x in in_lustre]
print lustre_in_lustre
lustre_post_lustre = [float(x[0]) for x in post_lustre]
print lustre_post_lustre



label = ['8GB', '64GB', '512GB']
plt.figure()
plt.subplot()
# plt.subplot(1,2,1)
x = np.arange(0,6,2.5)

# plt.bar(x-0.85, total_in_nvm, width=0.2, label='in-situ + nvm Total', color='b')
# plt.bar(x-0.65, syn_in_nvm, width=0.2, label='in-situ + nvm Synthetic Simulation')
# plt.bar(x-0.65, ana_in_nvm, width=0.2, bottom=syn_in_nvm, label='in-situ+nvm Cumulative Analysis')
# plt.bar(x-0.65, clean_in_nvm, width=0.2, bottom=sum_in_nvm, label='in-situ+nvm Clean up')

plt.bar(x-0.45, nvm_in_nvm, width=0.2, label='in-situ + nvm nvm_write', color='c')
plt.bar(x-0.45, hdfs_in_nvm, width=0.2, label='in-situ + nvm hdfs_write', bottom=nvm_in_nvm)
plt.bar(x-0.15, lustre_in_lustre, width=0.2, label='in-situ + lustre lustre_write')
# plt.bar(x-0.15, ana_in_lustre, width=0.2, bottom=syn_in_lustre, label='in-situ + lustre Cumulative Analysis')
# plt.bar(x-0.15, clean_in_lustre, width=0.2, bottom=sum_in_lustre, label='in-situ + lustre Clean up')

plt.bar(x+0.15, nvm_post_nvm, width=0.2, label='post-processing + nvm nvm_write', color='g')
plt.bar(x+0.15, hdfs_post_nvm, width=0.2, label='post-processing + nvm hdfs_write', bottom=nvm_post_nvm)
plt.bar(x+0.45, lustre_post_lustre, width=0.2, label='post-processing + lustre lustre_write')
# plt.bar(x+0.35, ana_post_nvm, width=0.2, bottom=syn_post_nvm, label='post-processing + nvm Cumulative Analysis')
# plt.bar(x+0.35, clean_post_nvm, width=0.2, bottom=sum_post_nvm, label='post-processing + nvm Clean up')

# plt.bar(x+0.65, total_post_lustre, width=0.2, label='post-processing + lustre Total', color='r')
# plt.bar(x+0.85, syn_post_lustre, width=0.2, label='post-processing + lustre Synthetic Simulation')
# plt.bar(x+0.85, ana_post_lustre, width=0.2, bottom=syn_post_lustre, label='post-processing + lustre Cumulative Analysis')
# plt.bar(x+0.85, clean_post_lustre, width=0.2, bottom=sum_post_lustre, label='post-processing + lustre Clean up')
# # plt.xlabel('Type')
plt.title('LOCAL')
plt.ylabel('TIME (s)')
plt.legend(loc='best')
plt.xticks(x, label)

# plt.subplot(1,2,2)

# x = np.arange(0,6,2.5)

# plt.bar(x-0.85, total_in_nvm, width=0.2, label='in-situ + nvm Total', color='b')

# plt.bar(x-0.35, total_in_lustre, width=0.2, label='in-situ + lustre Total', color='c')

# plt.bar(x+0.15, total_post_nvm, width=0.2, label='post-processing + nvm Total', color='g')

# plt.bar(x+0.65, total_post_lustre, width=0.2, label='post-processing + lustre Total', color='r')
# plt.ylabel('TIME (s)')
# plt.legend(loc='best')
# plt.xticks(x, label)

plt.show()
