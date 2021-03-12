

# Program Flow Testing

if not isinstance(value,str):
    raise TypeError('value is not a string')

if not isinstance(value,int):
    raise TypeError('value is not an Integer')

# While running Tests NOTE you should install pytest in configure test cases like this

assert isinstance(value,str), "Value can only be a string"
assert isinstance(value,int), "Value can only be an integer"

# TO learn how to install pytest and configure your testing environment see
# https://gists.github.com/freelance-solutions