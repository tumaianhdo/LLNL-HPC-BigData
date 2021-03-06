#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv

data_name = 'time.csv'
with open(data_name, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

print data
data[0][0]='in-situ'
print data

in_nvm = [x[3:11] for x in data if x[0] == 'in-situ' and x[1] == 'nvm']
print in_nvm
in_lustre = [x[3:11] for x in data if x[0] == 'in-situ' and x[1] == 'lustre']
print in_lustre
post_nvm = [x[3:7] for x in data if x[0] == 'post-processing' and x[1] == 'nvm']
print post_nvm
post_lustre = [x[3:7] for x in data if x[0] == 'post-processing' and x[1] == 'lustre']
print post_lustre

total_in_nvm = [int(x[0]) for x in in_nvm]
print total_in_nvm
total_in_lustre = [int(x[0]) for x in in_lustre]
total_post_nvm = [int(x[0]) for x in post_nvm]
total_post_lustre = [int(x[0]) for x in post_lustre]

syn_in_nvm = [int(x[1]) for x in in_nvm]
syn_in_lustre = [int(x[1]) for x in in_lustre]
syn_post_nvm = [int(x[1]) for x in post_nvm]
syn_post_lustre = [int(x[1]) for x in post_lustre]

ana_in_nvm = [int(x[2])+int(x[4])+int(x[6]) for x in in_nvm]
print ana_in_nvm
ana_in_lustre = [int(x[2])+int(x[4])+int(x[6]) for x in in_lustre]
ana_post_nvm = [int(x[2]) for x in post_nvm]
ana_post_lustre = [int(x[2]) for x in post_lustre]

sum_in_nvm = [int(x[1])+int(x[2])+int(x[4])+int(x[6]) for x in in_nvm]
print sum_in_nvm
sum_in_lustre = [int(x[1])+int(x[2])+int(x[4])+int(x[6]) for x in in_lustre]
sum_post_nvm = [int(x[1])+int(x[2]) for x in post_nvm]
sum_post_lustre = [int(x[1])+int(x[2]) for x in post_lustre]

clean_in_nvm = [int(x[3])+int(x[5])+int(x[7]) for x in in_nvm]
print clean_in_nvm
clean_in_lustre = [int(x[3])+int(x[5])+int(x[7]) for x in in_lustre]
clean_post_nvm = [int(x[3]) for x in post_nvm]
clean_post_lustre = [int(x[3]) for x in post_lustre]



label = ['8GB', '64GB', '512GB']
plt.figure()
plt.subplot(1,2,1)
x = np.arange(0,6,2.5)

plt.bar(x-0.85, total_in_nvm, width=0.2, label='in-situ + nvm Total', color='b')
plt.bar(x-0.65, syn_in_nvm, width=0.2, label='in-situ + nvm Synthetic Simulation')
plt.bar(x-0.65, ana_in_nvm, width=0.2, bottom=syn_in_nvm, label='in-situ+nvm Cumulative Analysis')
plt.bar(x-0.65, clean_in_nvm, width=0.2, bottom=sum_in_nvm, label='in-situ+nvm Clean up')

plt.bar(x-0.35, total_in_lustre, width=0.2, label='in-situ + lustre Total', color='c')
plt.bar(x-0.15, syn_in_lustre, width=0.2, label='in-situ + lustre Synthetic Simulation')
plt.bar(x-0.15, ana_in_lustre, width=0.2, bottom=syn_in_lustre, label='in-situ + lustre Cumulative Analysis')
plt.bar(x-0.15, clean_in_lustre, width=0.2, bottom=sum_in_lustre, label='in-situ + lustre Clean up')

plt.bar(x+0.15, total_post_nvm, width=0.2, label='post-processing + nvm Total', color='g')
plt.bar(x+0.35, syn_post_nvm, width=0.2, label='post-processing + nvm Synthetic Simulation')
plt.bar(x+0.35, ana_post_nvm, width=0.2, bottom=syn_post_nvm, label='post-processing + nvm Cumulative Analysis')
plt.bar(x+0.35, clean_post_nvm, width=0.2, bottom=sum_post_nvm, label='post-processing + nvm Clean up')

plt.bar(x+0.65, total_post_lustre, width=0.2, label='post-processing + lustre Total', color='r')
plt.bar(x+0.85, syn_post_lustre, width=0.2, label='post-processing + lustre Synthetic Simulation')
plt.bar(x+0.85, ana_post_lustre, width=0.2, bottom=syn_post_lustre, label='post-processing + lustre Cumulative Analysis')
plt.bar(x+0.85, clean_post_lustre, width=0.2, bottom=sum_post_lustre, label='post-processing + lustre Clean up')
# plt.xlabel('Type')
plt.title('GLOBAL')
plt.ylabel('TIME (s)')
plt.legend(loc='best')
plt.xticks(x, label)

plt.subplot(1,2,2)

x = np.arange(0,6,2.5)

plt.bar(x-0.85, total_in_nvm, width=0.2, label='in-situ + nvm Total', color='b')

plt.bar(x-0.35, total_in_lustre, width=0.2, label='in-situ + lustre Total', color='c')

plt.bar(x+0.15, total_post_nvm, width=0.2, label='post-processing + nvm Total', color='g')

plt.bar(x+0.65, total_post_lustre, width=0.2, label='post-processing + lustre Total', color='r')
plt.title('GLOBAL')
plt.ylabel('TIME (s)')
plt.legend(loc='best')
plt.xticks(x, label)

plt.show()
