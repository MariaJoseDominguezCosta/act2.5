import ply.lex as lex

# Lista de tokens
tokens = (
    'INT',
    'ID',
    'NUM',
    'DO',
    'ENDDO',
    'WHILE',
    'ENDWHILE',
    'EQUALS',
    'PLUS',
    'SEMICOLON',
    'TIMES',
    'LPAREN',
    'RPAREN',
    'DOUBLEEQUALS'
)

# Reglas de expresiones regulares para tokens simples
t_EQUALS    = r'='
t_PLUS      = r'\+'
t_SEMICOLON = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_TIMES = r'\*'
t_DOUBLEEQUALS = r'=='

# Definir tokens
def t_INT(t):
    r'int'
    return t

def t_DO(t):
    r'DO'
    return t

def t_ENDDO(t):
    r'ENDDO'
    return t

def t_WHILE(t):
    r'WHILE'
    return t

def t_ENDWHILE(t):
    r'ENDWHILE'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_space(t):
    r'\s+'
    t.lexer.lineno += len(t.value)
# Caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# instanciamos el analizador lexico
lexer = lex.lex()

def tokenize(data):
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
    return tokens