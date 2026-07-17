# Buggy Snippet C: Misplaced Break
for char in "hello":
    print(char) # This will print 'h', 'e', 'l' then break
    if char == 'l':
        print("Found 'l', stopping!")
        break