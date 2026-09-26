import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# 1. 准备数据（MNIST 手写数字数据集，会自动下载）
transform = transforms.ToTensor()
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True)

# 2. 定义一个简单的神经网络（3层全连接）
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(28*28, 128),   # 输入 28x28 像素 → 隐藏层 128 个神经元
            nn.ReLU(),                # 激活函数
            nn.Linear(128, 10)        # 输出 10 个类别（数字 0-9）
        )
    def forward(self, x):
        return self.fc(x.view(-1, 28*28))  # 把图片拉平成一维

model = Net()
optimizer = optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss()

# 3. 训练一轮
for epoch in range(1):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()             # 清空梯度
        output = model(data)              # 前向传播
        loss = loss_fn(output, target)    # 计算损失
        loss.backward()                   # 反向传播
        optimizer.step()                  # 更新参数
        if batch_idx % 200 == 0:
            print(f'批次 {batch_idx}, 损失: {loss.item():.4f}')

print('训练完成！')