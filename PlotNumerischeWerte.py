import matplotlib.pyplot as plt

reproduction = [1.0, 58.7, 117.4, 188.6, 333.0, 425.8, 675.4, 1607.2, 2087.0, 2275.4, 2113.4, 2328.9, 3218.9, 3253.7, 4103.8, 5197.2, 4395.5, 4250.5, 4628.4, 5143.1, 4516.3, 5294.6, 5046.6, 5366.7, 5003.3, 5482.0, 5108.2, 5381.3, 5095.7, 5253.2, 5432.9, 5476.3, 5303.2, 5362.6, 5634.4, 5134.1, 5810.7, 5628.2, 5469.6, 5819.0, 5644.4, 5702.4, 6001.3, 5861.3, 6504.3, 5912.8, 6196.4, 5899.8, 6256.6, 6394.9]
x_axis = [i for i in range(len(reproduction))]
plt.plot(x_axis, reproduction, label="Extinct")
plt.legend()
plt.savefig("ExtinctHealing4Kolonien")