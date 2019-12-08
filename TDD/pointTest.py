from unittest import TestCase
import os
import sys
sys.path.append(os.path.abspath("/Users/SG/PycharmProjects/bitcoin/"))
from point import Point
from lib.helper import run

class PointTest(TestCase):
    def test_ne(self):
        print("####### [Point] test_ne #######")
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        self.assertTrue(a != b)
        self.assertFalse(a != a)

    def test_on_curve(self):
        print("####### [Point] test_on_curve #######")
        with self.assertRaises(ValueError):
            Point(x=-2, y=4, a=5, b=7)
        # these should not raise an error
        Point(x=3, y=-7, a=5, b=7)
        Point(x=18, y=77, a=5, b=6)

    def test_add0(self):
        print("####### [Point] test_add0 #######")
        a = Point(x=None, y=None, a=5, b=7)
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        self.assertEqual(a + b, b)
        self.assertEqual(b + a, b)
        self.assertEqual(b + c, a)

    def test_add1(self):
        print("####### [Point] test_add1 #######")
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + b, Point(x=2, y=-5, a=5, b=7))

    def test_add2(self):
        print("####### [Point] test_add2 #######")
        a = Point(x=-1, y=1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=-77, a=5, b=7))



run(PointTest("test_ne"))
run(PointTest("test_on_curve"))
run(PointTest("test_add0"))
run(PointTest("test_add1"))
run(PointTest("test_add2"))

## TEST 1 - 포인트 생성 가능 여부
# p1 = Point(2, 4, 5, 7)
# p2 = Point(-1, -1, 5, 7) # ok
# p3 = Point(18, 77, 5, 7) # ok
# p4 = Point(5, 7, 5, 7)

## TEST 2 - 항등원과 점 덧셈
# p1 = Point(-1, -1, 5, 7)
# p2 = Point(-1, 1, 5, 7)
# inf = Point(None, None, 5, 7)
# print(p1 + inf)
# print(inf + p2)
# print(p1 + p2) # error

## TEST 2 - 항등원과 점 덧셈