import sys

filename='filename'
tmp = sys.argv[0].split('/')
tmp.pop()
tmp += [filename]
tmp = '/'.join(tmp)
print(tmp)
