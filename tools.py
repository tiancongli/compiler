from inspect import signature, Parameter

def all_args_constructor(tclass):
  attrs = signature(tclass).parameters

  def __init__(self, *args, **kwargs):
    if len(args) > len(attrs) or any(map(lambda arg: arg not in attrs, kwargs.keys())):
      raise TypeError(f'{tclass.__name__} has invalid constructor parameters, {args}, {kwargs}, {attrs}')
    
    args = list(args)
    for attr in attrs:
      default_value = attrs[attr].default
      if args:
        self.__dict__[attr] = args.pop(0)
      elif attr in kwargs:
        self.__dict__[attr] = kwargs[attr]
      elif default_value != Parameter.empty:
        self.__dict__[attr] = default_value

  __init__.__doc__ = tclass.__init__.__doc__

  def __str__(self):
    return f"class {tclass.__name__}, attrs {self.__dict__}"

  tclass.__init__ = __init__
  if not hasattr(tclass, '__str__'):
    tclass.__str__ = __str__

  return tclass

class ModelMeta(type):
  def __init__(tclass, name, parents, class_attr):
    type.__init__(tclass, name, parents, class_attr)
    all_args_constructor(tclass)

class Model(object, metaclass=ModelMeta): pass