import splitfolders, sys

input = sys.argv[1]
output = sys.argv[2]

if len(sys.argv) == 3:
    rat = (.7, .2, .1)
splitfolders.ratio('./ARIA/'+input, output="./"+output, seed=1337, ratio=rat)
