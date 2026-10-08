str1 = input("请输入字符串")
lower_str1 = str1.lower()
punctuation = '!.,;:"\'(){}[]'
for p in punctuation:
    lower_str1 = lower_str1.replace(p,'')
words = lower_str1.split()
words_count = {}
for w in words:
    words_count[w] = words_count.get(w,0) + 1
print(words_count)