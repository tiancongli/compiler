from tokens import tokens, keywords
import ply.lex as lex
import sys
import re

t_at = r'@'
t_colon = r':'
t_comma = r','
t_divide = r'/'
t_dot = r'\.'
t_equals = r'='
t_integer = r'[0-9]+'
t_larrow = r'<-'
t_lbrace = r'{'
t_le = r'<='
t_lparen = r'\('
t_lt = r'<'
t_minus = r'-'
t_plus = r'\+'
t_rarrow = r'=>'
t_rbrace = r'}'
t_rparen = r'\)'
t_semi = r';'
t_tilde = r'~'
t_times = r'\*'

def t_type(t):
  r'[A-Z][a-zA-Z_0-9]*'
  if t.value == 'Class':
    t.type = 'class'
  return t

def t_newline(t):
  r'(\n|(\r\n))+'
  t.lexer.lineno += 1

def t_comment(t):
  r'\(\*(?:\*(?!\))|[^*])*\*\)'
  t.lexer.lineno += len(re.findall(r'\n|(?:\r\n)', t.value))
  pass

def t_inline_cmt(t):
  r'--.*'
  pass
  
def t_string(t):
  r'".*?"'
  t.value = t.value[1:-1]
  return t

def t_identifier(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  if t.value in keywords:
    t.type = t.value
  elif t.value[0].isupper():
    t.type = "type"
  return t


t_ignore  = ' \t'


def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()
