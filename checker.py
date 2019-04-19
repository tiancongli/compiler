from copy import copy
from tools import Model


SELF_TYPE = 'SELF_TYPE'
OBJECT_TYPE = 'Object'
IO_TYPE = 'IO'
INT_TYPE = 'Int'
STRING_TYPE = 'String'
BOOL_TYPE = 'Bool'

def get_list_print(l):
  ret = f'{len(l)}\n'
  for item in l:
    ret += f'{item}\n'
  return ret[:-1]

def print_error_msg(line, msg):
  print(f'ERROR: {line}: Type-Check: {msg}')
  exit()

def check_self_type(itype):
  if itype.name == SELF_TYPE:
    print_error_msg(itype.line, 'mistake SELF_TYPE')

def check_self(var):
  if var.name == 'self':
    print_error_msg(var.line, 'mistake self')

class Identifier(Model):
  def __init__(self, line, name, desc=None): pass
  def __str__(self):
    return f'{self.line}\n{self.name}'

class Inherit(Model):
  def __init__(self, line, name, desc): pass
  def __str__(self):
    if self.desc == 'no_inherits':
      return str(self.desc)
    else:
      return f'{self.desc}\n{self.line}\n{self.name}'

class LetBinding(Model):
  def __init__(self, name, var, var_type, value=None): pass
  def __str__(self):
    ret = f'{self.name}\n{self.var}\n{self.var_type}\n'
    if self.value:
      ret += str(self.value)
    return ret

class ExprType(Model):
  def __init__(self, type_name, self_type_class=None): pass
  
  def is_self_type(self, self_type_class=None):
    if self.type_name == SELF_TYPE and self.self_type_class == self_type_class:
      return True
    else:
      return False

EXPR_IO = ExprType(IO_TYPE)
EXPR_INT = ExprType(INT_TYPE)
EXPR_BOOL = ExprType(BOOL_TYPE)
EXPR_STRING = ExprType(STRING_TYPE)
EXPR_OBJECT = ExprType(OBJECT_TYPE)
EXPR_SELF = ExprType(SELF_TYPE)

class Expr(Model):
  def __init__(self, line, name, sub_part, static_type=None): pass
  
  def is_self_type(self, self_type_class=None):
    if not self.static_type:
      print_error_msg(0, 'expr not type checked')
    return self.static_type.is_self_type(self_type_class)

  def __str__(self):
    return (f'{self.line}\n{self.static_type.type_name}\n{self.name}\n'
           f'{self.sub_part}')

class AssignExpr(Model):
  def __init__(self, var, rhs): pass
  def __str__(self):
    return f'{self.var}\n{self.rhs}'

class DynamicDispatchExpr(Model):
  def __init__(self, e, method, args): pass
  def __str__(self):
    return f'{self.e}\n{self.method}\n{get_list_print(self.args)}'

class SelfDispatchExpr(Model):
  def __init__(self, method, args): pass
  def __str__(self):
    return f'{self.method}\n{get_list_print(self.args)}'


class StaticDispatchExpr(Model):
  def __init__(self, e, parent_type, method, args): pass
  def __str__(self):
    return (f'{self.e}\n{self.parent_type}\n{self.method}\n'
            f'{get_list_print(self.args)}')


class IfExpr(Model):
  def __init__(self, if_e, then_e, else_e): pass
  def __str__(self):
    return f'{self.if_e}\n{self.then_e}\n{self.else_e}'

class WhileExpr(Model):
  def __init__(self, predicate, body): pass
  def __str__(self):
    return f'{self.predicate}\n{self.body}'

class BlockExpr(Model):
  def __init__(self, body): pass
  def __str__(self):
    return f'{get_list_print(self.body)}'

class NewExpr(Model):
  def __init__(self, class_name): pass
  def __str__(self):
    return str(self.class_name)

class UniOpExpr(Model):
  def __init__(self, e): pass
  def __str__(self):
    return str(self.e)

class BiOpExpr(Model):
  def __init__(self, x, y): pass
  def __str__(self):
    return f'{self.x}\n{self.y}'

class ConstantExpr(Model):
  def __init__(self, value): pass

  def __str__(self):
    return str(self.value)

class IdentifierExpr(Model):
  def __init__(self, var): pass
  def __str__(self):
    return str(self.var)

class LetExpr(Model):
  def __init__(self, bindings, body): pass
  def __str__(self):
    return f'{get_list_print(self.bindings)}\n{self.body}'

class CaseExpr(Model):
  def __init__(self, e, elts): pass
  def __str__(self):
    return f'{self.e}\n{get_list_print(self.elts)}'

class CaseElt(Model):
  def __init__(self, var, var_type, body): pass
  def __str__(self):
    return f'{self.var}\n{self.var_type}\n{self.body}'

class Formal(Model):
  def __init__(self, name_id, formal_type): pass
  def __str__(self):
    return f'{self.name_id}\n{self.formal_type}'

class AttrFeature(Model):
  def __init__(self, feature_name, name_id, attr_type, desc, init_expr=None,
               defined_class=None): pass
  def __str__(self):
    ret = f'{self.feature_name}\n{self.name_id}\n{self.attr_type}'
    if self.init_expr:
      ret += f'\n{self.init_expr}'
    return ret

class MethodFeature(Model):
  def __init__(self, feature_name, name_id, formals, ret_type, body,
               defined_class=None): pass

  def __str__(self):
    return (f'{self.feature_name}\n{self.name_id}\n'
            f'{get_list_print(self.formals)}\n{self.ret_type}\n{self.body}')

  def diff(self, other):
    if len(self.formals) != len(other.formals):
      self.name_id.desc = "diff len of params"
      return self.name_id
    for i, formal in enumerate(self.formals):
      if formal.formal_type.name != other.formals[i].formal_type.name:
        formal.formal_type.desc = f"param {formal.name_id.name} change type to {formal.formal_type.name}"
        return formal.formal_type
    if self.ret_type.name != other.ret_type.name:
      self.ret_type.desc = f"ret type change to {self.ret_type.name}"
      return self.ret_type
    

class CoolClass(Model):
  def __init__(self, name_id, inherit, features, attrs, methods): pass

  def __str__(self):
    return f'{self.name_id}\n{self.inherit}\n{get_list_print(self.features)}'

def get_line():
  return ast_list.pop(0)

def read_identifier():
  line_no = int(get_line())
  id_name = get_line()
  return Identifier(line_no, id_name)

def read_inherit(class_name):
  inherit_type = get_line()
  if inherit_type == 'no_inherits':
    if class_name == OBJECT_TYPE:
      return None
    else:
      return Inherit(0, OBJECT_TYPE, inherit_type)
  else:
    line_no = int(get_line())
    id_name = get_line()
    return Inherit(line_no, id_name, inherit_type)

def read_binding():
  binding_name = get_line()
  if binding_name == 'let_binding_no_init':
    var = read_identifier()
    var_type = read_identifier()
    return LetBinding(binding_name, var, var_type)
  else:
    var = read_identifier()
    var_type = read_identifier()
    value = read_expr()
    return LetBinding(binding_name, var, var_type, value)

def read_expr():
  line_no = int(get_line())
  expr_name = get_line()
  sub_part = ()
  if expr_name == 'assign':
    var = read_identifier()
    rhs = read_expr()
    sub_part = AssignExpr(var, rhs)
  elif expr_name == 'dynamic_dispatch':
    e = read_expr()
    method = read_identifier()
    args_no = int(get_line())
    args = [read_expr() for i in range(args_no)]
    sub_part = DynamicDispatchExpr(e, method, args)
  elif expr_name == 'static_dispatch':
    e = read_expr()
    parent_type = read_identifier()
    check_self_type(parent_type)
    method = read_identifier()
    args_no = int(get_line())
    args = [read_expr() for i in range(args_no)]
    sub_part = StaticDispatchExpr(e, parent_type, method, args)
  elif expr_name == 'self_dispatch':
    method = read_identifier()
    args_no = int(get_line())
    args = [read_expr() for i in range(args_no)]
    sub_part = SelfDispatchExpr(method, args)
  elif expr_name == 'if':
    if_e = read_expr()
    then_e = read_expr()
    else_e = read_expr()
    sub_part = IfExpr(if_e, then_e, else_e)
  elif expr_name == 'while':
    predicate = read_expr()
    body = read_expr()
    sub_part = WhileExpr(predicate, body)
  elif expr_name == 'block':
    exprs_no = int(get_line())
    body = [read_expr() for i in range(exprs_no)]
    sub_part = BlockExpr(body)
  elif expr_name == 'new':
    class_name = read_identifier()
    sub_part = NewExpr(class_name)
  elif expr_name in ('isvoid', 'not', 'negate'):
    e = read_expr()
    sub_part = UniOpExpr(e)
  elif expr_name in ('plus', 'times', 'minus', 'divide', 'lt', 'eq', 'le'):
    x = read_expr()
    y = read_expr()
    sub_part = BiOpExpr(x, y)
  elif expr_name in ('integer', 'string'):
    constant = get_line()
    sub_part = ConstantExpr(constant)
  elif expr_name == 'identifier':
    var = read_identifier()
    sub_part = IdentifierExpr(var)
  elif expr_name in ('true', 'false'):
    return ConstantExpr(expr_name)
  elif expr_name == 'let':
    binding_no = int(get_line())
    bindings = [read_binding() for i in range(binding_no)]
    body = read_expr()
    sub_part = LetExpr(bindings, body)
  elif expr_name == 'case':
    e = read_expr()
    elts_no = int(get_line())
    elts = [read_case_elt() for i in range(elts_no)] 
    sub_part = CaseExpr(e, elts)
  else:
    raise Exception('unknown expr name')
  return Expr(line_no, expr_name, sub_part)


def read_case_elt():
  var = read_identifier()
  var_type = read_identifier()
  check_self_type(var_type)
  body = read_expr()
  return CaseElt(var, var_type, body)

def read_formal():
  formal_name = read_identifier()
  formal_type = read_identifier()
  check_self(formal_name)
  check_self_type(formal_type)
  return Formal(formal_name, formal_type)


def read_feature():
  feature_name = get_line()
  name = read_identifier()
  if feature_name == 'attribute_no_init':
    attr_type = read_identifier()
    return AttrFeature(feature_name, name, attr_type, 'no_initializer')
  elif feature_name == 'attribute_init':
    attr_type = read_identifier()
    init_expr = read_expr()
    return AttrFeature(feature_name, name, attr_type, 'initializer', init_expr)
  else:
    formals_no = int(get_line())
    formals = [read_formal() for i in range(formals_no)]
    ret_type = read_identifier()
    body = read_expr()
    return MethodFeature(feature_name, name, formals, ret_type, body)


def read_class():
  class_name = read_identifier()
  check_self_type(class_name)
  inherit = read_inherit(class_name.name)
  feature_no = int(get_line())
  features = [read_feature() for i in range(feature_no)]
  for feature in features:
    feature.defined_class = class_name.name
  attrs = [feature for feature in features if feature.feature_name != 'method']
  methods = [feature for feature in features if feature.feature_name == 'method']
  return CoolClass(class_name, inherit, features, attrs, methods)


#################### running ###################
ast_file = 'hello-world.cl-ast'#sys.argv[-1]
checker_file = ast_file.replace('cl-ast', 'cl-type')

ast_list = []
with open(ast_file) as f:
  ast_list = [line.strip() for line in f.readlines()]

class_no = int(get_line())
ast = {}
input_classes = []
for class_item in [read_class() for i in range(class_no)]:
  if class_item.name_id.name in ast:
    print_error_msg(class_item.name_id.line, f'dup class {class_item.name_id.name}')
  ast[class_item.name_id.name] = class_item
  input_classes.append(class_item)

base_ast = {
  OBJECT_TYPE: CoolClass(Identifier(0, OBJECT_TYPE), None, [], [], [
    MethodFeature('method', Identifier(0, 'abort'), [],
                  Identifier(0, OBJECT_TYPE), None, OBJECT_TYPE),
    MethodFeature('method', Identifier(0, 'type_name'), [],
                  Identifier(0, STRING_TYPE), None, OBJECT_TYPE),
    MethodFeature('method', Identifier(0, 'copy'), [],
                  Identifier(0, SELF_TYPE), None, OBJECT_TYPE)
  ]),
  IO_TYPE: CoolClass(Identifier(0, IO_TYPE), Identifier(0, OBJECT_TYPE), [], [], [
    MethodFeature('method', Identifier(0, 'out_string'), [
      Formal(Identifier(0, 'x'), Identifier(0, STRING_TYPE))
    ], Identifier(0, SELF_TYPE), None, IO_TYPE),
    MethodFeature('method', Identifier(0, 'out_int'), [
      Formal(Identifier(0, 'x'), Identifier(0, INT_TYPE))
    ], Identifier(0, SELF_TYPE), None, IO_TYPE),
    MethodFeature('method', Identifier(0, 'in_string'), [],
                  Identifier(0, STRING_TYPE), None, IO_TYPE),
    MethodFeature('method', Identifier(0, 'in_int'), [],
                  Identifier(0, INT_TYPE), None, IO_TYPE)
  ]),
  INT_TYPE: CoolClass(Identifier(0, INT_TYPE), Identifier(0, OBJECT_TYPE), [], [], []),
  STRING_TYPE: CoolClass(Identifier(0, STRING_TYPE), Identifier(0, OBJECT_TYPE), [], [], [
    MethodFeature('method', Identifier(0, 'length'), [],
                  Identifier(0, INT_TYPE), None, STRING_TYPE),
    MethodFeature('method', Identifier(0, 'concat'), [
      Formal(Identifier(0, 's'), Identifier(0, STRING_TYPE))
    ], Identifier(0, STRING_TYPE), None, STRING_TYPE),
    MethodFeature('method', Identifier(0, 'substr'), [
      Formal(Identifier(0, 'i'), Identifier(0, INT_TYPE)), Formal(Identifier(0, 'l'), Identifier(0, INT_TYPE))
    ], Identifier(0, STRING_TYPE), None, STRING_TYPE)
  ]),
  BOOL_TYPE: CoolClass(Identifier(0, BOOL_TYPE), Identifier(0, OBJECT_TYPE), [], [], [])
}


entire_classes = sorted(list(base_ast.keys()) + list(ast.keys()))
entire_ast = {**ast, **base_ast}


############### error checking ##################

def check_inherit_from_Int(class_item):
  inherit = class_item.inherit
  if inherit:
    if inherit.name == INT_TYPE:
      print_error_msg(inherit.line, f'inheriting from forbidden class {inherit.name}')
    if inherit.name not in entire_classes:
      print_error_msg(inherit.line, f'inheriting from undefined class {inherit.name}')

def check_inherit_cycle(chain):
  class_name = chain[-1]
  if class_name in base_ast:
    # no inheritance cycle in base classes
    return 
  class_item = ast[class_name]
  inherit = class_item.inherit
  if inherit:
    if inherit.name in chain:
      print_error_msg(0, f'Inheritance cycle {chain}')
    check_inherit_cycle(chain + [inherit.name])

def check_dup_features(class_item):
  attrs = []
  methods = []
  for attr in class_item.attrs:
    if attr.name_id.name in attrs:
      print_error_msg(attr.name_id.line, 
      f'class {class_item.name_id.name} duplicate feature(field) {attr.name_id.name}')
    attrs.append(attr.name_id.name)
  
  for method in class_item.methods:
    if method.name_id.name in methods:
      print_error_msg(method.name_id.line, 
      f'class {class_item.name_id.name} duplicate feature(method) {method.name_id.name}')
    methods.append(method.name_id.name)
      
def check_overload(class_item, parent_id):
  if parent_id is None: 
    return
  parent = entire_ast[parent_id.name]
  for i, method in enumerate(class_item.methods):
    pmethod = parent.methods[i]
    if method.name_id.name == pmethod.name_id.name:
      diff = method.diff(parent.methods[i])
      if diff:
        print_error_msg(diff.line, 
        f'class {class_item.name_id.name} overloads method {method.name_id.name}, {diff.desc}')
  check_overload(class_item, parent.inherit)

def check_main():
  if 'Main' not in ast:
    print_error_msg(0, 'class Main not found')
  for method in ast['Main'].methods:
    if method.name_id.name == 'main':
      return
  print_error_msg(0, 'class Main method main not found')

def check_dup_formal(class_item):
  for method in class_item.methods:
    formal_names = []
    for formal in method.formals:
      if formal.name_id.name in formal_names:
        print_error_msg(formal.name_id.line, 
        f'class {class_item.name_id.name}, method {method.name_id.name} has dup formal {formal.name_id.name}')
      formal_names.append(formal.name_id.name)


check_main()

for class_item in ast.values():
  check_inherit_from_Int(class_item)

  check_inherit_cycle([class_item.name_id.name])

  check_dup_features(class_item)

  # cool doesnt allow overload
  check_overload(class_item, class_item.inherit)

  check_dup_formal(class_item)


############### type checking ##################
def get_parents(ctype):
  """
  store parents in a list
  with the order, current to oldest
  include the current type
  """
  def get_parrent(ctype):
    class_item = entire_ast[ctype]
    if class_item.inherit:
      parents.append(class_item.inherit.name)
      get_parrent(class_item.inherit.name)

  parents = [ctype]
  get_parrent(ctype)
  return parents
      

def is_subtype(parent, child):
  if parent.type_name == SELF_TYPE and child.type_name == SELF_TYPE:
    return True
  elif parent.type_name == SELF_TYPE and child.type_name != SELF_TYPE:
    return False
  elif parent.type_name != SELF_TYPE and child.type_name == SELF_TYPE:
    return is_subtype(parent, ExprType(child.self_type_class))
  else:
    return parent.type_name in get_parents(child.type_name)

def bilub(x, y):
  if x.type_name == SELF_TYPE and y.type_name == SELF_TYPE:
    return x
  elif x.type_name == SELF_TYPE and y.type_name != SELF_TYPE:
    return bilub(ExprType(x.self_type_class), y)
  elif x.type_name != SELF_TYPE and y.type_name == SELF_TYPE:
    return bilub(ExprType(y.self_type_class), x)
  else:
    x_parents = get_parents(x)
    y_parents = set(get_parents(y))
    for x_parent in x_parents:
      if x_parent in y_parents:
        return ExprType(x_parent)


def lub(**subtypes):
  if len(subtypes) == 1:
    return subtypes[0]
  else:
    return bilub(subtypes[0], lub(**subtypes[1:]))

def dispatch_check(o, m, c, sub_expr, class_name):
  if (class_name, sub_expr.method.name) not in m:
    print_error_msg(sub_expr.method.line,
    f'unknown method {sub_expr.method.name}')

  param_types = m[(class_name, sub_expr.method.name)]
  if len(param_types) - 1 != len(sub_expr.args):
    print_error_msg(sub_expr.method.line, 
    'wrong actual arguments number')

  for i, param_type in enumerate(param_types[:-1]):
    actual_type = type_check(o, m, c, sub_expr.args[i])
    if not is_subtype(param_type, actual_type):
      print_error_msg(sub_expr.method.line,
      f'wrong actual argument type, expect {param_type.type_name}, but {actual_type.type_name}')
  return param_types[-1]

def type_check(o, m, c, expr):
  sub_expr = expr.sub_part
  if expr.name == 'identifier':
    if sub_expr.var.name not in o:
      print_error_msg(sub_expr.var.line, 'unknown identifier')
    expr.static_type = o[sub_expr.var.name]
  elif expr.name == 'integer':
    expr.static_type = EXPR_INT
  elif expr.name == 'string':
    expr.static_type = EXPR_STRING
  elif expr.name in ('true', 'false'):
    expr.static_type = EXPR_BOOL
  elif expr.name == 'new':
    expr.static_type = ExprType(sub_expr.class_name.name, c)
  elif expr.name == 'assign':
    if sub_expr.var.name not in o:
      print_error_msg(sub_expr.var.line, 
      f'unknown identifier {sub_expr.var.name}')
    var_type = o[sub_expr.var.name]
    rhs_type = type_check(o, m, c, sub_expr.rhs)
    if not is_subtype(var_type, rhs_type):
      print_error_msg(expr.line, 
      f"assgin not conform, {rhs_type.type_name} to {var_type.type_name}")
    expr.static_type = rhs_type
  elif expr.name == 'dynamic_dispatch':
    e_type = type_check(o, m, c, sub_expr.e)
    if sub_expr.e.is_self_type(c):
      # sub_expr.e is self_type occur in class c
      e_type = ExprType(c)
    ret_type = dispatch_check(o, m, c, sub_expr, e_type.type_name)
    if ret_type.type_name == SELF_TYPE:
      expr.static_type = sub_expr.e.static_type
    else:
      expr.static_type = ret_type
  elif expr.name == 'static_dispatch':
    e_type = type_check(o, m, c, sub_expr.e)
    parent_type = ExprType(sub_expr.parent_type.name)
    if not is_subtype(parent_type, e_type):
      print_error_msg(expr.line, 
      f'static dispatch type not conform, {parent_type.type_name} < {e_type.type_name}')
    
    ret_type = dispatch_check(o, m, c, sub_expr, parent_type.type_name)
    if ret_type.type_name == SELF_TYPE:
      expr.static_type = sub_expr.e.static_type
    else:
      expr.static_type = ret_type
  elif expr.name == 'self_dispatch':
    ret_type = dispatch_check(o, m, c, sub_expr, c)
    if ret_type.type_name == SELF_TYPE:
      expr.static_type = ExprType(SELF_TYPE, c)
    else:
      expr.static_type = ret_type
  elif expr.name in ('plus', 'times', 'minus', 'divide'):
    x_type = type_check(o, m, c, sub_expr.x)
    y_type = type_check(o, m, c, sub_expr.y)
    if x_type.type_name != INT_TYPE or y_type.type_name != INT_TYPE:
      print_error_msg(expr.line, f"wrong type for {expr.name}")
    expr.static_type = EXPR_INT
  elif expr.name == 'if':
    if_type = type_check(o, m, c, sub_expr.if_e)
    then_type = type_check(o, m, c, sub_expr.then_e)
    else_type = type_check(o, m, c, sub_expr.else_e)
    if if_type.type_name != BOOL_TYPE:
      print_error_msg(expr.line, 'wrong type for if')
    expr.static_type = lub(then_type, else_type)
  elif expr.name == 'block':
    body_type = None
    for sub_block in sub_expr.body:
      body_type = type_check(o, m, c, sub_block)
    expr.static_type = body_type
  elif expr.name == 'let':
    def binding_check(binding):
      e_type = ExprType(binding.var_type.name)
      if binding.var_type.name == SELF_TYPE:
        e_type.self_type = c
      if binding.value:
        value_type = type_check(o_let, m, c, binding.value)
        if not is_subtype(e_type, value_type):
          print_error_msg(expr.line, 
          f"let init type wrong, actually got {value_type.type_name}")
      o_let[binding.var.name] = e_type

    o_let = copy(o)
    for binding in sub_expr.bindings:
      binding_check(binding)
    expr.static_type = type_check(o_let, m, c, sub_expr.body)
  elif expr.name == 'case':
    type_check(o, m, c, sub_expr.e)
    body_types = []
    for case_elt in sub_expr.elts:
      o_case = copy(o)
      o_case[case_elt.var.name] = ExprType(case_elt.var_type.name)
      body_types.append(type_check(o_case, m, c, case_elt.body))
    expr.static_type = lub(**body_types)
  elif expr.name == 'while':
    predicate_type = type_check(sub_expr.predicate)
    if predicate_type.type_name != BOOL_TYPE:
      print_error_msg(expr.line, "wrong type for while predicate")
    type_check(sub_expr.body)
    expr.static_type = EXPR_OBJECT
  elif expr.name == 'isvoid':
    type_check(sub_expr.e)
    expr.static_type = EXPR_BOOL
  elif expr.name == 'not':
    if type_check(sub_expr.e).type_name != BOOL_TYPE:
      print_error_msg(expr.line, 'wrong type for not')
    expr.static_type = EXPR_BOOL
  elif expr.name == 'negate':
    if type_check(sub_expr.e).type_name != INT_TYPE:
      print_error_msg(expr.line, 'wrong type for neg')
    expr.static_type = EXPR_INT
  elif expr.name in ('lt', 'eq', 'le'):
    x_type = type_check(sub_expr.x)
    y_type = type_check(sub_expr.y)
    if x_type.type_name in (INT_TYPE, STRING_TYPE, BOOL_TYPE) \
      or y_type.type_name in (INT_TYPE, STRING_TYPE, BOOL_TYPE):
      if x_type.type_name != y_type.type_name:
        print_error_msg(expr.line, 
        f'{expr.name} op types wrong, {x_type.type_name}, {y_type.type_name}')
    expr.static_type = EXPR_BOOL

  return expr.static_type

def generate_m(current_class_name, actual_class_name):
  class_item = entire_ast[actual_class_name]
  if class_item.inherit:
    generate_m(current_class_name, class_item.inherit.name)
  for method in class_item.methods:
    m[(current_class_name, method.name_id.name)] = [
      ExprType(formal.formal_type.name)
      for formal in method.formals
    ] + [ExprType(method.ret_type.name)]

################## generate global m ##############
m = {}
for class_name in entire_ast:
  generate_m(class_name, class_name)

def generate_o(current_class_name, actual_class_name):
  class_item = ast[actual_class_name]
  if class_item.inherit in ast:
    generate_o(current_class_name, class_item.inherit.name)
  for attr in class_item.attrs:
    o[attr.name_id.name] = ExprType(attr.attr_type.name)

  if current_class_name == actual_class_name:
    o['self'] = ExprType(SELF_TYPE, current_class_name)
  
for class_name, class_item in ast.items():
  ########### generate oc #############
  o = {}
  c = class_name
  generate_o(c, c)

  for attr in class_item.attrs:
    if attr.init_expr:
      e_type = type_check(o, m, c, attr.init_expr)
      if not is_subtype(ExprType(attr.attr_type.name, c), e_type):
        print_error_msg(attr.name_id.line, 
        f'attr type not conform, actually got {e_type.type_name}')


  for method in class_item.methods:
    ######### generate current method o ###########
    om = copy(o)
    for formal in method.formals:
      om[formal.name_id.name] = ExprType(formal.formal_type.name)

    body_type = type_check(o, m, c, method.body)
    if not is_subtype(ExprType(method.ret_type.name, c), body_type):
      print_error_msg(method.name_id.line, 
      f'method type not conform, actually got {body_type.type_name}')
    




############### print class map #################
def get_class_attrs(class_name):
  if class_name not in ast:
    # base classes
    return []
  else:
    # user defined classes
    attrs = []
    class_item = ast[class_name]
    inherit = class_item.inherit
    if inherit is not None:
      attrs += get_class_attrs(inherit.name)
    attrs += class_item.attrs
    return attrs

print("class_map")
print(len(entire_classes))
for class_name in entire_classes:
  print(class_name)
  if class_name in base_ast:
    print(0)
  else:
    attrs = get_class_attrs(class_name)
    print(len(attrs))
    for attr in attrs:
      print(attr.desc)
      print(attr.name_id.name)
      print(attr.attr_type.name)
      if attr.init_expr:
        print(attr.init_expr)



############### print impl map ###############
def get_class_methods(class_name):
  methods = []
  class_item = entire_ast[class_name]
  inherit = class_item.inherit
  if inherit is not None:
    methods += get_class_methods(inherit.name)
  methods += class_item.methods
  return methods

def get_sorted_class_methods(class_name):
  methods = get_class_methods(class_name)
  if not methods:
    return []

  boundaries = [0]

  defined_class = methods[0].defined_class
  i = 0
  for method in methods:
    if method.defined_class not in base_ast:
      break
    elif method.defined_class != defined_class:
      boundaries.append(i)
      defined_class = method.defined_class
    i += 1
  boundaries.append(i)

  ret = []
  for i in range(len(boundaries)):
    if i == len(boundaries) -1:
      break
    start = boundaries[i]
    end = boundaries[i+1]
    ret += sorted(methods[start: end], key=lambda x: x.name_id.name)

  ret += methods[boundaries[i]:]
  return ret


def print_base_method(method):
  print(0)
  print(method.ret_type.name)
  print('internal')
  print(f'{method.defined_class}.{method.name_id.name}')

print("implementation_map")
print(len(entire_classes))
for class_name in entire_classes:
  print(class_name)
  methods = get_sorted_class_methods(class_name)
  print(len(methods))
  for method in methods:
    print(method.name_id.name)
    print(len(method.formals))
    for formal in method.formals:
      print(formal.name_id.name)
    print(method.defined_class)
    if method.defined_class in base_ast:
      print_base_method(method)
    else:
      print(method.body)

################## print parent map #################
print("parent_map")
print(len(entire_classes) -1)
for class_name in entire_classes:
  if class_name == OBJECT_TYPE:
    continue
  print(class_name)
  class_item = entire_ast[class_name]
  print(class_item.inherit.name)

#################### print annotated ast ###############
print(get_list_print(input_classes))
