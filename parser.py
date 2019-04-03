import sys
import ply.yacc as yacc
from lexer import lexer
from tokens import tokens

precedence = (
  ('left', 'plus', 'minus'),
  ('left', 'times', 'divide'),
  ('left', 'dot')
)

def describe_as_identifier(p, index):
  node = Node()
  node._repr = (p.lineno(index), p[index])
  return node

class Node:
  def __init__(self):
    self._repr = ()
  
  def __repr__(self):
    return repr(self._repr)

class ClassNode(Node):
  """
  single_class : class type class_inherit class_body semi
  """
  def __init__(self, p):
    super().__init__()
    self._repr = (
      describe_as_identifier(p, 2),
      p[3],
      p[4])

class InheritNode(Node):
  """
  class_inherit : inherits type
                |
  """  
  def __init__(self, p):
    super().__init__()
    if len(p) <= 1:
      self._repr = ("no_inherits",)  
    else:
      self._repr = ('inherits', describe_as_identifier(p, 2))

class BindingNode(Node):
  """
  binding : identifier colon type
          | identifier colon type larrow expr      
  """  
  def __init__(self, p):
    super().__init__()
    if len(p) == 4:
      self._repr = (
        'let_binding_no_init', 
        describe_as_identifier(p, 1), 
        describe_as_identifier(p, 3))
    else:
      self._repr = (
        'let_binding_init', 
        describe_as_identifier(p, 1),
        describe_as_identifier(p, 3),
        p[5])

class CaseEltNode(Node):
  """
  case_elt : identifier colon type rarrow expr semi
  """
  def __init__(self, p):
    super().__init__()
    self._repr = (
      describe_as_identifier(p, 1),
      describe_as_identifier(p, 3),
      p[5])
  
class FeatureNode(Node):
  """
  feature : identifier colon type 
          | identifier colon type larrow expr
          | identifier lparen formal_list rparen colon type method_body
  """
  def __init__(self, p):
    super().__init__()
    if len(p) == 4:
      self._repr = (
        'attribute_no_init', 
        describe_as_identifier(p, 1),
        describe_as_identifier(p, 3))
    elif len(p) == 6:
      self._repr = (
        'attribute_init', 
        describe_as_identifier(p, 1),
        describe_as_identifier(p, 3),
        p[5])
    elif len(p) == 8:
      self._repr = (
        'method', 
        describe_as_identifier(p, 1),
        p[3],
        describe_as_identifier(p, 6), 
        p[7])

class FormalNode(Node):
  """
  formal : identifier colon type
  """
  def __init__(self, p):
    super().__init__()
    self._repr = (
      describe_as_identifier(p, 1),
      describe_as_identifier(p, 3))
  
class ExprNode(Node):
  """
  expr : identifier larrow expr
       | identifier dispatch_body
       | expr dot identifier dispatch_body
       | expr at type dot identifier dispatch_body
       | if expr then expr else expr fi
       | while expr loop expr pool
       | lbrace expr semi expr_block_tail rbrace
       | let binding binding_tail in expr
       | case expr of case_elts esac
       | new type
       | isvoid expr
       | not expr
       | tilde expr
       | expr plus expr
       | expr minus expr
       | expr times expr
       | expr divide expr
       | expr lt expr
       | expr le expr
       | expr equals expr
       | identifier
       | true
       | false
       | integer
       | string
  """
  def __init__(self, subclass, p):
    super().__init__()
    self._repr = [p.lineno(1), subclass]

    subexpr = []
    if subclass == 'assign':
      subexpr = [describe_as_identifier(p, 1), p[3]]
    elif subclass == 'self_dispatch':
      subexpr = [describe_as_identifier(p, 1), p[2]]
    elif subclass == 'dynamic_dispatch':
      subexpr = [p[1], describe_as_identifier(p, 3), p[4]]
    elif subclass == 'static_dispatch':
      subexpr = [p[1], describe_as_identifier(p, 3), 
      describe_as_identifier(p, 5), p[6]]
    elif subclass == 'if':
      subexpr = [p[2], p[4], p[6]]
    elif subclass in ('while', 'case'):
      subexpr = [p[2], p[4]]
    elif subclass == 'block':
      subexpr = [[p[2]] + p[4]]
    elif subclass == 'let':
      subexpr = [[p[2]] + p[3], p[5]]
    elif subclass == 'new':
      subexpr = [describe_as_identifier(p, 2)]
    elif subclass in ('isvoid', 'not', 'tilde'):
      subexpr = [p[2]]
      if subclass == 'tilde':
        self._repr[1] = 'negate'
    elif subclass in (
      'plus', 'minus', 'times', 
      'divide', 'lt', 'le', 'equals'):
      subexpr = [p[1], p[3]]
      if subclass == 'equals':
        self._repr[1] = 'eq'
    elif subclass == 'identifier':
      subexpr = [describe_as_identifier(p, 1)]
    elif subclass in ('integer', 'string'):
      subexpr = [p[1]]
    elif subclass in ('true', 'false'):
      pass
      
    self._repr = tuple(self._repr + subexpr)
  
def p_program(p):
  'program : class_list single_class'
  p[0] = p[1] + [p[2]]

def p_class_list_empty(p):
  'class_list :'
  p[0] = []

def p_class_list(p):
  'class_list : class_list single_class'
  p[0] = p[1] + [p[2]]

def p_single_class(p):
  'single_class : class type class_inherit class_body semi'
  p[0] = ClassNode(p)

def p_class_inherit(p):
  '''
  class_inherit : inherits type
                |
  '''
  p[0] = InheritNode(p)

def p_class_body(p):
  'class_body : lbrace feature_list rbrace'
  p[0] = p[2]

def p_feature_list_empty(p):
  'feature_list :'
  p[0] = []

def p_feature_list(p):
  'feature_list : feature semi feature_list'
  p[0] = [p[1]] + p[3]

def p_feature(p):
  '''
  feature : identifier colon type 
          | identifier colon type larrow expr
          | identifier lparen formal_list rparen colon type method_body
  '''
  p[0] = FeatureNode(p)

def p_formal_list_empty(p):
  'formal_list :'
  p[0] = []

def p_formal_list(p):
  'formal_list : formal formal_tail'
  p[0] = [p[1]] + p[2]

def p_formal_tail(p):
  'formal_tail : comma formal formal_tail'
  p[0] = [p[2]] + p[3]

def p_formal_tail_empty(p):
  'formal_tail :'
  p[0] = []

def p_formal(p):
  'formal : identifier colon type'
  p[0] = FormalNode(p)

def p_method_body(p):
  'method_body : lbrace expr rbrace'
  p[0] = p[2]

def p_expr_assign(p):
  'expr : identifier larrow expr'
  p[0] = ExprNode('assign', p)#('assign', p[1], p[3])

def p_expr_self_dispatch(p):
  'expr : identifier dispatch_body'
  p[0] = ExprNode('self_dispatch', p)#('self_dispatch', p[1], p[2])

def p_expr_dynamic_dispatch(p):
  'expr : expr dot identifier dispatch_body'
  p[0] = ExprNode('dynamic_dispatch', p)#('dynamic_dispatch', p[1], p[3], p[4])

def p_expr_static_dispatch(p):
  'expr : expr at type dot identifier dispatch_body'
  p[0] = ExprNode('static_dispatch', p)#('static_dispatch', p[1], p[3], p[5], p[6])

def p_dispatch_body(p):
  'dispatch_body : lparen expr_list rparen'
  p[0] = p[2]

def p_expr_list_empty(p):
  'expr_list :'
  p[0] = []

def p_expr_list(p):
  'expr_list : expr expr_tail'
  p[0] = [p[1]] + p[2]

def p_expr_tail_empty(p):
  'expr_tail :'
  p[0] = []

def p_expr_tail(p):
  'expr_tail : comma expr expr_tail'
  p[0] = [p[2]] + p[3]

def p_expr_if(p):
  'expr : if expr then expr else expr fi'
  p[0] = ExprNode('if', p)#('if', p[2], p[4], p[6])

def p_expr_while(p):
  'expr : while expr loop expr pool'
  p[0] = ExprNode('while', p)#('while', p[2], p[4])

def p_expr_block(p):
  'expr : lbrace expr semi expr_block_tail rbrace'
  p[0] = ExprNode('block', p)#('block', [p[2]] + p[4])

def p_expr_block_tail_empty(p):
  'expr_block_tail :'
  p[0] = []

def p_expr_block_tail(p):
  'expr_block_tail : expr semi expr_block_tail'
  p[0] = [p[1]] + p[3]

def p_let(p):
  'expr : let binding binding_tail in expr'
  p[0] = ExprNode('let', p)#('let', [p[2]] + p[3], p[5])

def p_let_binding_no_init(p):
  '''binding : identifier colon type
             | identifier colon type larrow expr'''
  p[0] = BindingNode(p)

def p_binding_tail_empty(p):
  'binding_tail :'
  p[0] = []

def p_binding_tail(p):
  'binding_tail : comma binding binding_tail'
  p[0] = [p[2]] + p[3]

def p_expr_case(p):
  'expr : case expr of case_elts esac'
  p[0] = ExprNode('case', p)#('case', p[2], p[4])

def p_expr_case_elts(p):
  'case_elts : case_elt_head case_elt'
  p[0] = p[1] + [p[2]]

def p_case_elt(p):
  'case_elt : identifier colon type rarrow expr semi'
  p[0] = CaseEltNode(p)

def p_case_elt_head_empty(p):
  'case_elt_head :'
  p[0] = []

def p_case_elt_head(p):
  'case_elt_head : case_elt_head case_elt'
  p[0] = p[1] + [p[2]]

def p_expr_new(p):
  'expr : new type'
  p[0] = ExprNode('new', p)#('new', p[2])

def p_expr_uniop(p):
  '''expr : isvoid expr
          | not expr
          | tilde expr'''
  p[0] = ExprNode(p.slice[1].type, p)

def p_expr_biop(p):
  '''expr : expr plus expr
          | expr minus expr
          | expr times expr
          | expr divide expr
          | expr lt expr
          | expr le expr
          | expr equals expr'''
  p[0] = ExprNode(p.slice[2].type, p)

def p_expr_paren(p):
  'expr : lparen expr rparen'
  p[0] = p[2]

def p_expr_identifier(p):
  'expr : identifier'
  p[0] = ExprNode('identifier', p)

def p_expr_true(p):
  'expr : true'
  p[0] = ExprNode('true', p)

def p_expr_false(p):
  'expr : false'
  p[0] = ExprNode('false', p)

def p_expr_integer(p):
  'expr : integer'
  p[0] = ExprNode('integer', p)

def p_expr_string(p):
  'expr : string'
  p[0] = ExprNode('string', p)

def p_error(p):
  print(f"Syntax error in input: {p.value}")

parser = yacc.yacc()

def print_elt(elt):
  if isinstance(elt, Node):
    print_node(elt)
  elif isinstance(elt, list):
    print_list(elt)
  else:
    print(elt)

def print_node(node):
  l = node._repr
  for item in l:
    print_elt(item)

def print_list(l):
  print(len(l))
  for item in l:
    print_elt(item)

if __name__ == '__main__': 
  data = sys.stdin.readlines()
  sys.stdin = open('/dev/tty')
  result = parser.parse(' '.join(data), tracking=True)
  #print(result)
  print_elt(result)