# %%
import math
import numpy as np
import torch
import random
import matplotlib.pyplot as plt
#电脑现在使用matplotlib会使内核挂掉，就不使用了

# %%
#定义正态分布
def normal(x,mu,sigma):
    p=1/math.sqrt(2*math.pi*sigma*sigma)
    return p*np.exp(-0.5/sigma**2 *(x-mu)**2)

x=np.arange(-7,7,0.01)
params=[(0,1),(0,2),(3,1)]
y=np.arange(-7,7,0.01)
plt.plot(x,y)

# %%
#制造数据集 y=Xw+b+噪声
def synthetic_data(w, b, num_examples): 
    X = torch.normal(0, 1, (num_examples, len(w)))
    y = torch.matmul(X, w) + b
    y += torch.normal(0, 0.01, y.shape)
    return X, y.reshape((-1, 1))

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 100)



# %%
#如何获取小批量的X，y
def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    # 这些样本是随机读取的，没有特定的顺序
    random.shuffle(indices)
    for i in range(0, num_examples, batch_size):
        batch_indices = torch.tensor(
            indices[i: min(i + batch_size, num_examples)])
            #注意yield
        yield features[batch_indices],labels[batch_indices]

batch_size=10

# %%
#初始化w,b
w = torch.normal(0, 0.01, size=(2,1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# %%
#定义模型wx+b
def liner(X,w,b):
    return torch.matmul(X,w)+b

# %%
#定义均方损失
def squared_loss(y_hat, y): 
    return (y_hat - y.reshape(y_hat.shape)) ** 2 / 2

# %%
lr = 0.03
num_epochs = 3
net = liner
loss = squared_loss
sgd=torch.optim.SGD([w,b],lr)


# %%
for epoch in range(num_epochs):
    for X, y in data_iter(batch_size, features, labels):
        l = loss(net(X, w, b), y) # X和y的⼩批量损失
        # 因为l形状是(batch_size,1)，⽽不是⼀个标量。l中的所有元素被加到⼀起，
        # 并以此计算关于[w,b]的梯度
        sgd.zero_grad()
        l.sum().backward()
        sgd.step() # 使⽤参数的梯度更新参数
    with torch.no_grad():
        train_l = loss(net(features, w, b), labels)
        print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')
print([true_w,true_b])
print([w,b])


