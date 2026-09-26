import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# 1. 准备数据
transform = transforms.ToTensor()
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True)
test_data = datasets.MNIST(root='./data', train=False, transform=transform)

# 2. 搭一个简单模型
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

# 3. 快速训练（只跑一小部分数据，够用就行）
optimizer = optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss()

for batch_idx, (data, target) in enumerate(train_loader):
    optimizer.zero_grad()
    output = model(data.view(-1, 784))
    loss = loss_fn(output, target)
    loss.backward()
    optimizer.step()
    

# 4. 从测试集里随便拿 5 张图，让模型猜
print("模型预测结果：")
for i in range(5):
    image, true_label = test_data[i]
    prediction = model(image.view(1, 784))
    guessed = prediction.argmax().item()
    print(f"第 {i+1} 张图 → 真实数字: {true_label}，模型猜: {guessed}")


# ===== 算准确率 =====
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for image, true_label in test_data:
        prediction = model(image.view(1, 784))
        guessed = prediction.argmax().item()
        if guessed == true_label:
            correct += 1
        total += 1

accuracy = correct / total * 100
print(f"在 {total} 张测试图上的准确率: {accuracy:.2f}%")