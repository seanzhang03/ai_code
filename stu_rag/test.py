import jieba
a="苹果公司发布了新款iPhone 15，搭载A17芯片和潜望式长焦镜头"
words = jieba.lcut(a)
print(words)