#message first element equal 
with open('README.md') as fp:
    for line in fp:
        if (line[0] == "*" or line[0] == "#"):
            pass
        else:
            print(line)
