# Reduction : Answer to exercise 1

```python
import sys

def count_lines(filename):
    """Function that returns the number of lines
       of text in the file 'filename'"""

    lines = open(filename, "r").readlines()
    return len(lines)

# get all of the names of the plays from
# the command line
filenames = sys.argv[1:]

# map the count_lines function against all of the 
# files listed in "filenames"
results = map( count_lines, filenames )

# now print out the results (can also be a map)
def print_result( filename, nlines ):
    """Function to print out the number of lines"""
    print( "%s contains %d lines" % (filename, nlines) )

map( print_result, filenames, results )

def sum(x, y):
    """Return the sum of the two arguments"""
    return x+y

total = reduce( sum, results )

print("The total number of lines is %d." % total)
```

***

# [Previous](reduce.md) [Up](reduce.md) [Next](reduce.md)
