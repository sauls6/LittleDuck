@echo off
echo === Ejecutando pruebas del analizador sintáctico ===

set TEST_FILES=^
test_min_valid.txt ^
test_missing_program.txt ^
test_missing_semi.txt ^
test_missing_main.txt ^
test_missing_end.txt ^
test_vars_simple.txt ^
test_vars_multiple.txt ^
test_vars_bad_type.txt ^
test_vars_missing_semi.txt ^
test_vars_missing_type.txt ^
test_func_simple.txt ^
test_func_params.txt ^
test_func_local_vars.txt ^
test_func_empty.txt ^
test_func_bad_params.txt ^
test_assign_simple.txt ^
test_condition.txt ^
test_cycle.txt ^
test_func_call.txt ^
test_print.txt ^
test_print_multiple.txt ^
test_expr_simple.txt ^
test_expr_compare.txt ^
test_expr_nested.txt ^
test_expr_paren_error.txt ^
test_expr_bad_order.txt ^
test_complete_valid.txt ^
test_mixed_statements.txt ^
test_complex_expr.txt ^
test_mixed_errors.txt ^
test_advanced.txt

for %%F in (%TEST_FILES%) do (
    echo.
    echo === Ejecutando prueba: %%F ===
    python parser_runner.py tests/parser/%%F
)

echo.
echo === Pruebas completadas ===
if "%1" neq "nopause" pause
