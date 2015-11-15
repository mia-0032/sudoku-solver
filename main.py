# -*- coding: utf-8 -*-
import math

matrix_0 = \
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

matrix_1 = \
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 3, 1, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 1, 2, 0, 0, 0, 5, 0, 0],
        [7, 0, 0, 0, 8, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 1, 2, 0]
    ]

matrix_2 = \
    [
        [6, 0, 5, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 7],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 2, 0, 9, 0, 8, 0, 0, 0],
        [0, 0, 4, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 6, 0],
        [0, 9, 0, 0, 0, 0, 8, 0, 0]
    ]


class Cell(object):
    def __init__(self, number, x, y):
        self.__x = x
        self.__y = y
        self.__group = self.__calculateGroup(x, y)

        if number > 0:
            self.__number = number
            self.__takable = None
        else:
            self.__number = None
            self.__takable = set(range(1, 10))

    def __calculateGroup(self, x, y):
        return int(math.floor(x / 3.0) + math.floor(y / 3.0) * 3)

    def removeTakableNumber(self, numbers):
        """指定した配列の指定した数を取りうる値配列から除去"""
        removed = False

        for number in numbers:
            if number in self.__takable:
                self.__takable.remove(number)
                removed = True

        if len(self.__takable) == 1:
            self.__number = list(self.__takable)[0]
        return removed

    def findOnlyTakableNumber(self, numbers):
        """他のマスの候補の値と比較して、このマスにしか存在しない数値があればその数値に決定する"""
        numbers = set(numbers)
        filtered = self.__takable - numbers
        if len(filtered) == 1:
            self.__number = list(filtered)[0]
            return True
        return False

    def isFixed(self):
        return self.__number is not None

    def __getX(self):
        return self.__x

    def __getY(self):
        return self.__y

    def __getGroup(self):
        return self.__group

    def __getNumber(self):
        return self.__number

    def __str__(self):
        if self.__number is None:
            return '0'
        return str(self.__number)

    x = property(__getX)
    y = property(__getY)
    group = property(__getGroup)
    number = property(__getNumber)


class SudokuSolver(object):
    def __init__(self, matrix):
        self.__matrix = [[Cell(matrix[y][x], x, y) for x in range(0, 9)] for y in range(0, 9)]

    def checkCells(self):
        results = list()

        for row in self.__matrix:
            for c in row:
                if c.isFixed():
                    continue
                results.append(self.__checkCell(c))

        return True in results

    def __checkCell(self, cell):
        results = [
            # 同じ列・行・グループにある数字を除去する
            cell.removeTakableNumber(self.__getRowNumbers(cell.y)),
            cell.removeTakableNumber(self.__getColumnNumbers(cell.x)),
            cell.removeTakableNumber(self.__getGroupNumbers(cell.group))
            # 同じ列・行・グループで他の部分に候補がなければ、その数字に決定する

        ]
        return True in results

    def __getRowNumbers(self, index):
        return set([row.number for row in self.__matrix[index] if row.isFixed()])

    def __getColumnNumbers(self, index):
        return set([row[index].number for row in self.__matrix if row[index].isFixed()])

    def __getGroupNumbers(self, index):
        group = set()
        for row in self.__matrix:
            for c in row:
                if c.group == index and c.isFixed():
                    group.append(c.number)
        return group

    def __str__(self):
        return '\n'.join([','.join([str(n) for n in m]) for m in self.__matrix])

    def __getMatrix(self):
        return [[n.number for n in m] for m in self.__matrix]

    matrix = property(__getMatrix)


class SudokuVerifier(object):
    def __init__(self, matrix):
        self.__matrix = matrix

    def verify(self):
        # 行のベリファイ
        for row in self.__matrix:
            numbers = set(row)
            if numbers != set(range(1, 10)):
                return False
        # 列のベリファイ
        for i in range(0, 9):
            numbers = list()
            for row in self.__matrix:
                numbers.append(row[i])
            if set(numbers) != set(range(1, 10)):
                return False
        # グループのベリファイ
        for i in range(0, 9):
            numbers = list()
            rows = range(int(math.floor(i / 3.0)) * 3, int(math.floor(i / 3.0)) * 3 + 3)
            columns = range((i % 3) * 3, (i % 3) * 3 + 3)
            for y in rows:
                for x in columns:
                    numbers.append(self.__matrix[y][x])
            if set(numbers) != set(range(1, 10)):
                return False
        return True


def main(matrix):
    solver = SudokuSolver(matrix)
    while(True):
        if not solver.checkCells():
            break
    print(solver)
    verifier = SudokuVerifier(solver.matrix)
    print(verifier.verify())

if __name__ == '__main__':
    main(matrix_0)
    main(matrix_1)
    main(matrix_2)