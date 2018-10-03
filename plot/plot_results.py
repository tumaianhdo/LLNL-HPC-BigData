#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv

data_name = 'results.csv'
with open(data_name, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# print data
data[0][0]='lustre'
# print data

lustre = [x[2:6] for x in data if x[0] == 'lustre']
print lustre
nvm = [x[2:6] for x in data if x[0] == 'nvm']
print nvm

total_lustre = [int(x[0]) for x in lustre]
print total_lustre
total_nvm = [int(x[0]) for x in nvm]
print total_nvm
sim_lustre = [int(x[1]) for x in lustre]
print sim_lustre
sim_nvm = [int(x[1]) for x in nvm]
print sim_nvm
ana_lustre = [int(x[2]) for x in lustre]
print ana_lustre
ana_nvm = [int(x[2]) for x in nvm]
print ana_nvm
# total_in_lustre = [int(x[0]) for x in in_lustre]
# total_post_nvm = [int(x[0]) for x in post_nvm]
# total_post_lustre = [int(x[0]) for x in post_lustre]

# syn_in_nvm = [int(x[1]) for x in in_nvm]
# syn_in_lustre = [int(x[1]) for x in in_lustre]
# syn_post_nvm = [int(x[1]) for x in post_nvm]
# syn_post_lustre = [int(x[1]) for x in post_lustre]

# ana_in_nvm = [int(x[2])+int(x[4])+int(x[6]) for x in in_nvm]
# print ana_in_nvm
# ana_in_lustre = [int(x[2])+int(x[4])+int(x[6]) for x in in_lustre]
# ana_post_nvm = [int(x[2]) for x in post_nvm]
# ana_post_lustre = [int(x[2]) for x in post_lustre]

# sum_in_nvm = [int(x[1])+int(x[2])+int(x[4])+int(x[6]) for x in in_nvm]
# print sum_in_nvm
# sum_in_lustre = [int(x[1])+int(x[2])+int(x[4])+int(x[6]) for x in in_lustre]
# sum_post_nvm = [int(x[1])+int(x[2]) for x in post_nvm]
# sum_post_lustre = [int(x[1])+int(x[2]) for x in post_lustre]

# clean_in_nvm = [int(x[3])+int(x[5])+int(x[7]) for x in in_nvm]
# print clean_in_nvm
# clean_in_lustre = [int(x[3])+int(x[5])+int(x[7]) for x in in_lustre]
# clean_post_nvm = [int(x[3]) for x in post_nvm]
# clean_post_lustre = [int(x[3]) for x in post_lustre]



label = ['6GB', '60GB', '600GB']
plt.figure()
plt.subplot()
# x = np.arange(0,6,2.5)
res = 100
x = [6, 60, 600]
# x1 = np.linspace(np.min(x),np.max(x),res)

# variables = [total_lustre, total_nvm]

# for var in variables:
# 	plt.figure()
# 	y1 = np.linspace(var[0],var[-1],res)
# 	print var
# 	plt.plot(x1, y1, marker='x')
# 	plt.plot(x, var, marker='o')
# 	plt.xlim([0,750])

# plt.figure()
plt.plot(x, total_lustre, label='Total_lustre', marker='o')
plt.plot(x, total_nvm, label='Total_nvm', marker='o')
plt.plot(x, sim_lustre, label='Simulation_lustre', marker='o')
plt.plot(x, sim_nvm, label='Simulation_nvm', marker='o')
plt.plot(x, ana_lustre, label='Analysis_lustre', marker='o')
plt.plot(x, ana_nvm, label='Analysis_nvm', marker='o')

cc = 0
for val in x:
	plt.plot([val]*2, [0, total_lustre[cc]], 'k--')
	cc += 1

plt.xticks(list(plt.xticks()[0]) + x)
plt.xlim(0,650)
plt.ylim(0,np.max(total_lustre)+100)
# plt.show()


# plt.plot(x, total_lustre, label='Total_lustre', marker='o')
# plt.plot(x, total_nvm, label='Total_nvm', marker='o')
# plt.plot(x, sim_lustre, label='Simulation_lustre', marker='o')
# plt.plot(x, sim_nvm, label='Simulation_nvm', marker='o')
# plt.plot(x, ana_lustre, label='Analysis_lustre', marker='o')
# plt.plot(x, ana_nvm, label='Analysis_nvm', marker='o')
# plt.bar(x-0.15, clean_in_lustre, width=0.2, bottom=sum_in_lustre, label='in-situ + lustre Clean up')
# plt.bar(x-0.15, ana_in_lustre, width=0.2, bottom=syn_in_lustre, label='in-situ + lustre Cumulative Analysis')
# plt.bar(x-0.15, clean_in_lustre, width=0.2, bottom=sum_in_lustre, label='in-situ + lustre Clean up')

# plt.bar(x+0.15, total_post_nvm, width=0.2, label='post-processing + nvm Total', color='g')
# plt.bar(x+0.35, syn_post_nvm, width=0.2, label='post-processing + nvm Synthetic Simulation')
# plt.bar(x+0.35, ana_post_nvm, width=0.2, bottom=syn_post_nvm, label='post-processing + nvm Cumulative Analysis')
# plt.bar(x+0.35, clean_post_nvm, width=0.2, bottom=sum_post_nvm, label='post-processing + nvm Clean up')

# plt.bar(x+0.65, total_post_lustre, width=0.2, label='post-processing + lustre Total', color='r')
# plt.bar(x+0.85, syn_post_lustre, width=0.2, label='post-processing + lustre Synthetic Simulation')
# plt.bar(x+0.85, ana_post_lustre, width=0.2, bottom=syn_post_lustre, label='post-processing + lustre Cumulative Analysis')
# plt.bar(x+0.85, clean_post_lustre, width=0.2, bottom=sum_post_lustre, label='post-processing + lustre Clean up')
plt.xlabel('Data Size (GB)')
plt.title('8 nodes')
plt.ylabel('TIME (s)')
plt.legend(loc='best')
# plt.xticks(x, label)

# plt.subplot(1,2,2)

# x = np.arange(0,6,2.5)

# plt.bar(x-0.85, total_in_nvm, width=0.2, label='in-situ + nvm Total', color='b')

# plt.bar(x-0.35, total_in_lustre, width=0.2, label='in-situ + lustre Total', color='c')

# plt.bar(x+0.15, total_post_nvm, width=0.2, label='post-processing + nvm Total', color='g')

# plt.bar(x+0.65, total_post_lustre, width=0.2, label='post-processing + lustre Total', color='r')
# plt.title('GLOBAL')
# plt.ylabel('TIME (s)')
# plt.legend(loc='best')
# plt.xticks(x, label)

plt.show()

