################## Reflection
# Built in function: getattr()
class Object:
    dummy_field = 'hest'


print(getattr(Object, 'dummy_field'))

# Built in function: hasattr()
print(hasattr(Object, 'dummy_field')) # Expected True
print(hasattr(Object, 'hjkfdslad'))   # Expected False

# Built in function: type()
x = 1
print(type(x))
x = 'hest'
print(type(x))

# Built in function: isinstance()
print(isinstance(x, str)) # Expected True
print(isinstance(x, int)) # Expected False


