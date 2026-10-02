import string

word_counts = {}

text = input("Enter sentence to count : ").lower().split()
text = [_.strip(string.punctuation) for _ in text if _.strip(string.punctuation)]
text.sort()

for i in text:
    try:
        word_counts[i] += 1
    except KeyError:
        word_counts[i] = 1

for word, value in word_counts.items():
    print(f"{word.title()} = {value}")