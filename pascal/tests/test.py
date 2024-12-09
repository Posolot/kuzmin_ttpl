import pytest
from ..main.Interpreter import Interpreter
from ..main.Token import TokenType,Token
from ..main.Ast import Node, Number, BinOp, UnaryOp, Variable, Assignment, Statement, Empty, StatementList, ComplexStatement, Program

@pytest.fixture
def interpreter() -> Interpreter:
    return Interpreter()


class UnknownNode:
    pass


class TestInterpreter:

    def test_empty_program(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_single_assignment(self, interpreter):
        result = interpreter.eval("BEGIN x := 10; END.")
        assert result == {"x": 10.0}

    def test_arithmetic_operations(self, interpreter):
        result = interpreter.eval("BEGIN x := 10; y := x + 2 * (3 - 1); END.")
        assert result == {"x": 10.0, "y": 14.0}

    def test_nested_blocks(self, interpreter):
        result = interpreter.eval("""
        BEGIN 
            BEGIN 
                x := 5; 
            END; 
            y := x + 2; 
        END.
        """)
        assert result == {"x": 5.0, "y": 7.0}

    def test_variable_reassignment(self, interpreter):
        result = interpreter.eval("BEGIN x := 1; x := x + 5; END.")
        assert result == {"x": 6.0}

    def test_unary_operations(self, interpreter):
        result = interpreter.eval("BEGIN x := -10; y := +x; z := -x; END.")
        assert result == {"x": -10.0, "y": -10.0, "z": 10.0}

    def test_variable_not_defined_error(self, interpreter):
        with pytest.raises(NameError, match="Variable 'z' is not defined"):
            interpreter.eval("BEGIN x := 10; y := z + 1; END.")

    def test_invalid_operator_error(self, interpreter):
        # Здесь нужно отключить закомментированный блок в `_visit_binop` для теста.
        interpreter._visit_binop = lambda node: (Exception(f"invalid operator: {node.op.value}"))
        with pytest.raises(Exception, match="Bad Token: ?"):
            interpreter.eval("BEGIN x := 10; y := x ? 5; END.")

    def test_missing_end_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid statement"):
            interpreter.eval("BEGIN x := 10; y := 5;; END.")

    def test_invalid_syntax_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            interpreter.eval("BEGIN x := 10 + ; END.")

    def test_empty_statement_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid statement"):
            interpreter.eval("BEGIN ; END.")

    def test_division_by_zero(self, interpreter):
        with pytest.raises(ZeroDivisionError):
            interpreter.eval("BEGIN x := 10 / 0; END.")

    def test_empty_nested_blocks(self, interpreter):
        result = interpreter.eval("""
        BEGIN 
            BEGIN 
            END; 
        END.
        """)
        assert result == {}

    def test_complex_expression(self, interpreter):
        result = interpreter.eval("BEGIN x := 2 + 3 * (4 - 1) / 3; END.")
        assert result == {"x": 5.0}

    def test_unary_op_node(self, interpreter):
        result = interpreter.eval("BEGIN x := -5; END.")
        assert result == {"x": -5.0}

    def test_compound_node(self, interpreter):
        result = interpreter.eval("""
        BEGIN
            BEGIN
                x := 10;
            END;
            y := x + 1;
        END.
        """)
        assert result == {"x": 10.0, "y": 11.0}

    def test_undefined_variable_error(self, interpreter):
        with pytest.raises(NameError, match="Variable 'z' is not defined"):
            interpreter.eval("BEGIN x := 1; y := z; END.")

    def test_invalid_statement(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid statement"):
            interpreter.eval("BEGIN 123 := x; END.")

    def test_invalid_character_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Bad Token: @"):
            interpreter.eval("BEGIN x := 5 @ 3; END.")

    def test_missing_end(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid token order"):
            interpreter.eval("BEGIN x := 10;")

    def test_extra_token_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            interpreter.eval("BEGIN x := 10 + ; END.")

    def test_without_end(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            interpreter.eval("BEGIN x := 10 + ;")

    def test_token_str(self, interpreter):
        token = Token(TokenType.NUMBER, '10')
        assert str(token) == "(TokenType.NUMBER: 10)"

    def test_invalid_number_of_points(self,interpreter):
        with pytest.raises(SyntaxError, match="Invalid number of points"):
            interpreter.eval('123.45.6')

    def test_unknown_node_error(self, interpreter):
        unknown_node = UnknownNode()
        with pytest.raises(Exception, match="Unkown node in tree: UnknownNode"):
            interpreter.visit(unknown_node)


def test_number_str():
    token = Token(TokenType.NUMBER, "42")
    number = Number(token)
    assert str(number) == "(TokenType.NUMBER: 42)"


def test_binop_str():
    left = Number(Token(TokenType.NUMBER, "5"))
    right = Number(Token(TokenType.NUMBER, "3"))
    op = Token(TokenType.OPERATOR, "+")
    binop = BinOp(left, op, right)
    assert str(binop) == "((TokenType.NUMBER: 5) + (TokenType.NUMBER: 3))"


def test_unaryop_str():
    expr = Number(Token(TokenType.NUMBER, "10"))
    op = Token(TokenType.OPERATOR, "-")
    unaryop = UnaryOp(op, expr)
    assert str(unaryop) == "((TokenType.OPERATOR: -)(TokenType.NUMBER: 10))"


def test_variable_str():
    name = Token(TokenType.VARIABLE, "x")
    variable = Variable(name)
    assert str(variable) == "Variable((TokenType.VARIABLE: x))"


def test_assignment_str():
    var = Token(TokenType.VARIABLE, "y")
    expr = Number(Token(TokenType.NUMBER, "7"))
    assignment = Assignment(var, expr)
    assert str(assignment) == "Assignment((TokenType.VARIABLE: y) := (TokenType.NUMBER: 7))"


def test_statement_str():
    value = Number(Token(TokenType.NUMBER, "9"))
    statement = Statement(value)
    assert str(statement) == "Statement((TokenType.NUMBER: 9))"


def test_empty_str():
    empty = Empty()
    assert str(empty) == "Empty"


def test_statement_list_str():
    first = Statement(Number(Token(TokenType.NUMBER, "1")))
    second = Statement(Number(Token(TokenType.NUMBER, "2")))
    statement_list = StatementList(first, second)
    assert str(statement_list) == "StatementList(Statement((TokenType.NUMBER: 1)) SEMI Statement((TokenType.NUMBER: 2)))"

    statement_list_no_second = StatementList(first, None)
    assert str(statement_list_no_second) == "StatementList(Statement((TokenType.NUMBER: 1)))"


def test_complex_statement_str():
    statement_list = StatementList(
        Statement(Number(Token(TokenType.NUMBER, "1"))),
        Statement(Number(Token(TokenType.NUMBER, "2")))
    )
    complex_statement = ComplexStatement(statement_list)
    assert str(complex_statement) == "ComplexStatement(StatementList(Statement((TokenType.NUMBER: 1)) SEMI Statement((TokenType.NUMBER: 2))))"


def test_program_str():
    comp_statement = ComplexStatement(StatementList(
        Statement(Number(Token(TokenType.NUMBER, "1"))),
        None
    ))
    program = Program(comp_statement)
    assert str(program) == "Program: ComplexStatement(StatementList(Statement((TokenType.NUMBER: 1))))"
