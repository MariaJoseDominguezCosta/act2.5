import ply.yacc as yacc
from lexer import tokens

# Tabla de símbolos
symbol_table = {}
errores = []

# Reglas gramaticales
def p_program(p):
    '''program : declarations statements'''
    p[0] = ('program', p[1], p[2])

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaration(p):
    '''declaration : INT ID EQUALS NUM SEMICOLON'''
    p[0] = ('declaration', p[2], p[4])
    if p[2] in symbol_table:
        errores.append(f"Semantic error: Variable '{p[2]}' already declared")
    else:
        symbol_table[p[2]] = p[4]

def p_statements(p):
    '''statements : statements statement
                | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_assign(p):
    '''statement : ID EQUALS expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])
    if p[1] not in symbol_table:
        errores.append(f"Semantic error: Variable '{p[1]}' not declared")
    else:
        # Actualiza el valor de la variable en la tabla de símbolos
        symbol_table[p[1]] = evaluate_expression(p[3])

def p_statement_do_while(p):
    '''statement : DO statements ENDDO WHILE condition ENDWHILE'''
    p[0] = ('do_while', p[2], p[5])

def p_expression_plus(p):
    '''expression : NUM PLUS expression
                | ID PLUS expression
                | expression PLUS NUM
                | expression PLUS ID'''
    p[0] = ('plus', p[1], p[3])
    validate_expression(p[1])
    validate_expression(p[3])

def p_expression_times(p):
    '''expression : NUM TIMES expression
                | ID TIMES expression
                | expression TIMES NUM
                | expression TIMES ID'''
    p[0] = ('times', p[1], p[3])
    validate_expression(p[1])
    validate_expression(p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_num(p):
    '''expression : NUM'''
    p[0] = p[1]

def p_expression_id(p):
    '''expression : ID'''
    p[0] = p[1]
    if p[1] not in symbol_table:
        errores.append(f"Semantic error: Variable '{p[1]}' not declared")

def p_condition(p):
    '''condition : LPAREN ID DOUBLEEQUALS NUM RPAREN'''
    p[0] = ('condition', p[2], p[4])
    if p[2] not in symbol_table:
        errores.append(f"Semantic error: Variable '{p[2]}' not declared")

# Función para evaluar expresiones
def evaluate_expression(expr):
    if isinstance(expr, tuple):
        if expr[0] == 'plus':
            val1 = get_value(expr[1])
            val2 = get_value(expr[2])
            return val1 + val2
        elif expr[0] == 'times':
            val1 = get_value(expr[1])
            val2 = get_value(expr[2])
            return val1 * val2
    elif isinstance(expr, int):
        return expr
    elif isinstance(expr, str):
        return get_value(expr)

# Función para obtener el valor de una variable o número
def get_value(token):
    if isinstance(token, int):
        return token
    elif token in symbol_table:
        return symbol_table[token]
    else:
        errores.append(f"Semantic error: Variable '{token}' not declared")
        return None

# Función para validar expresiones
def validate_expression(token):
    if isinstance(token, str) and token not in symbol_table:
        errores.append(f"Semantic error: Variable '{token}' not declared")

# Manejo de errores
# Regla para errores de sintaxis
def p_error(p):
    if p:
        error_message = (
            f"Error de sintaxis en la posición {p.lexpos}: Token '{p.value}' inesperado"
        )
    else:
        error_message = "Error de sintaxis: se expera un token"
    raise SyntaxError(error_message)


# Instanciar el analizador
parser = yacc.yacc()


# Función para analizar una expresión
def parse(expression):
    global symbol_table
    global errores

    # Reiniciar tabla de símbolos y errores
    error_message = None  # Inicializa la variable error_message
    resultado = None  # Inicializa la variable resultado
    try:
        resultado = parser.parse(expression)
        if resultado is not None:
            return str(resultado) + " ,Sintaxis correcta"
        else:
            return "Sintaxis correcta"

    except SyntaxError as e:
        error_message = str(e)
        print("Error:", error_message)
        return error_message
