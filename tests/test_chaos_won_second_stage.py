from support_functions.chaos_won_second_stage import (
    make_full_asc_diagonal, make_full_desc_diagonal,
    make_array_for_element, make_column, check_single_line,
    second_stage
)

ar = [
    [0, 2, 0, 1, 1, 1],
    [1, 1, 2, 1, 1, 1],
    [0, 0, 2, 2, 1, 2],
    [0, 0, 0, 0, 2, 1],
    [0, 1, 1, 0, 2, 1],
    [0, 1, 1, 1, 0, 0],
]


def test_make_array_for_element_0_1():
    i = 0
    j = 1
    row = [0, 2, 0, 1, 1, 1]
    col = [2, 1, 0, 0, 1, 1]
    diag = [2, 2, 2, 2, 1]
    lines = make_array_for_element(ar, i, j)
    assert len(lines) == 3
    assert row == lines[0]
    assert col == lines[1]
    assert diag == lines[2]


def test_make_array_for_element_2_2():
    i = 2
    j = 2
    row = [0, 0, 2, 2, 1, 2]
    col = [0, 2, 2, 0, 1, 1]
    desc_diag = [0, 1, 2, 0, 2, 0]
    asc_diag = [1, 1, 2, 0, 0]
    lines = make_array_for_element(ar, i, j)
    assert len(lines) == 4
    assert row == lines[0]
    assert col == lines[1]
    assert desc_diag == lines[2]
    assert asc_diag == lines[3]


def test_make_array_for_element_4_4():
    i = 4
    j = 4
    row = [0, 1, 1, 0, 2, 1]
    col = [1, 1, 1, 2, 2, 0]
    desc_diag = [0, 1, 2, 0, 2, 0]
    lines = make_array_for_element(ar, i, j)
    assert len(lines) == 3
    assert row == lines[0]
    assert col == lines[1]
    assert desc_diag == lines[2]


def test_make_array_for_element_5_1():
    i = 5
    j = 1
    row = [0, 1, 1, 1, 0, 0]
    col = [2, 1, 0, 0, 1, 1]
    asc_diag = [1, 1, 0, 1, 1]
    lines = make_array_for_element(ar, i, j)
    assert len(lines) == 3
    assert row == lines[0]
    assert col == lines[1]
    assert asc_diag == lines[2]


def test_make_array_for_element_4_5():
    i = 3
    j = 5
    row = [0, 0, 0, 0, 2, 1]
    col = [1, 1, 2, 1, 1, 0]
    lines = make_array_for_element(ar, i, j)
    assert len(lines) == 2
    assert row == lines[0]
    assert col == lines[1]


def test_make_column_0():
    col = 0
    assert [0, 1, 0, 0, 0, 0] == make_column(ar, col)


def test_make_column_1():
    col = 1
    assert [2, 1, 0, 0, 1, 1] == make_column(ar, col)


def test_make_column_2():
    col = 2
    assert [0, 2, 2, 0, 1, 1] == make_column(ar, col)


def test_make_full_desc_diagonal_0_0():
    i = 0
    j = 0
    diagonal = [0, 1, 2, 0, 2, 0]
    assert diagonal == make_full_desc_diagonal(ar, i, j)


def test_make_full_desc_diagonal_2_5():
    i = 2
    j = 5
    diagonal = [1, 1, 2]
    assert diagonal == make_full_desc_diagonal(ar, i, j)


def test_make_full_desc_diagonal_4_1():
    i = 4
    j = 1
    diagonal = [0, 1, 1]
    assert diagonal == make_full_desc_diagonal(ar, i, j)


def test_make_full_asc_diagonal_3_2():
    i = 4
    j = 1
    diagonal = [1, 1, 2, 0, 1, 0]
    assert diagonal == make_full_asc_diagonal(ar, i, j)


def test_make_full_asc_diagonal_1_1():
    i = 1
    j = 1
    diagonal = [0, 1, 0]
    assert diagonal == make_full_asc_diagonal(ar, i, j)


def test_make_full_asc_diagonal_5_3():
    i = 5
    j = 3
    diagonal = [1, 2, 1]
    assert diagonal == make_full_asc_diagonal(ar, i, j)


def test_check_single_line_false():
    line = [1, 1, 2, 0, 0, 1]
    assert check_single_line(line, 1) is False
    assert check_single_line(line, 2) is False


def test_check_single_line_true_for_1():
    line = [1, 1, 0, 0, 0, 1]
    assert check_single_line(line, 1) is False
    assert check_single_line(line, 2) is False


def test_check_single_line_true_for_2():
    line = [1, 2, 0, 0, 0, 0]
    assert check_single_line(line, 1) is False
    assert check_single_line(line, 2) is True


def test_check_single_line_5_elements():
    line = [1, 2, 0, 0, 2]
    assert check_single_line(line, 1) is False
    assert check_single_line(line, 2) is False


def test_check_single_line_5_elements_all_1():
    line = [1, 1, 1, 1, 1]
    assert check_single_line(line, 1) is True


def test_check_single_line_6_elements_no_1():
    line = [2, 0, 2, 0, 2, 0]
    assert check_single_line(line, 2) is True


def test_check_single_line_changing_1_2():
    line = [1, 2, 1, 2, 1, 2]
    assert check_single_line(line, 1) is False
    assert check_single_line(line, 2) is False


def test_check_single_line_one_2_no_win():
    line = [1, 1, 2, 1, 1, 1]
    assert check_single_line(line, 1) is False
    assert check_single_line(line, 2) is False


def test_second_stage_chaos_not_won():
    board = [
        [0, 2, 0, 1, 1, 1],
        [1, 1, 2, 1, 1, 1],
        [0, 0, 2, 2, 1, 2],
        [0, 0, 0, 0, 2, 1],
        [0, 1, 1, 0, 2, 1],
        [0, 1, 1, 1, 0, 0],
    ]
    assert second_stage(board) is False


def test_second_stage_chaos_won():
    board = [
        [0, 2, 0, 1, 1, 1],
        [1, 1, 2, 1, 1, 1],
        [0, 0, 2, 2, 1, 2],
        [2, 2, 1, 2, 2, 1],
        [0, 1, 1, 0, 2, 1],
        [2, 1, 1, 1, 2, 2],
    ]
    assert second_stage(board) is True


def test_second_stage_chaos_won_second_variant():
    board = [
        [2, 1, 0, 2, 0, 0],
        [0, 1, 1, 2, 0, 0],
        [2, 1, 2, 1, 2, 1],
        [1, 1, 2, 1, 0, 0],
        [2, 2, 2, 0, 1, 2],
        [0, 2, 0, 1, 0, 0],
    ]
    assert second_stage(board) is True


def test_second_stage_chaos_won_third_variant():
    board = [
        [0, 0, 2, 1, 0, 0],
        [0, 2, 2, 1, 0, 1],
        [2, 0, 2, 1, 1, 0],
        [0, 1, 2, 1, 0, 2],
        [1, 0, 1, 2, 2, 0],
        [0, 2, 0, 2, 1, 0],
    ]
    assert second_stage(board) is True
