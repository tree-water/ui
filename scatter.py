import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 生成随机数据
def generate_data():
    return np.random.rand(10)

# 更新散点图的数据
def update(frame):
    data = generate_data()
    scat.set_offsets(np.c_[np.arange(len(data)), data])
    return scat,

# 初始化散点图
fig, ax = plt.subplots()
ax.set_ylim(0, 1)
scat = ax.scatter([], [])

# 创建动画
ani = FuncAnimation(fig, update, frames=range(100), interval=200, blit=True)

plt.show()
