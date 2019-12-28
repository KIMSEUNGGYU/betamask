import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
sys.path.append(os.path.abspath(path))

from unittest import TestCase

from lib.helper import run
from src.point import Point

class PointTest(TestCase):
    def exercise1(self):
        print("********** [타원곡선 상의 점인지 확인] **********")
        try:
            print("점 (-1, -1)이 타원곡선 상(y^2 = x^3 + 5x + 7) 상의 존재하나요? ")
            Point(-1, -1, 5, 7)
            print("타원곡선 상에 존재합니다.")
        except:
            print("타원곡선 상에 존재하지 않습니다.")

        try:
            print("점 (-1, -2)이 타원곡선 상(y^2 = x^3 + 5x + 7) 상의 존재하나요? ")
            Point(-1, -2, 5, 7)
            print("타원곡선 상에 존재합니다.")
        except:
            print("타원곡선 상에 존재하지 않습니다.")

    def exercise2(self):
        # [연습문제 2.1]
        print("********** [타원곡선 상의 점인지 확인] **********")
        try:
            print("점 (2, 4)이 타원곡선 상(y^2 = x^3 + 5x + 7) 상의 존재하나요? ")
            Point(2, 4, 5, 7)
            print("타원곡선 상에 존재합니다.")
        except:
            print("타원곡선 상에 존재하지 않습니다.")

        try:
            print("점 (-1, -1)이 타원곡선 상(y^2 = x^3 + 5x + 7) 상의 존재하나요? ")
            Point(-1, -1, 5, 7)
            print("타원곡선 상에 존재합니다.")
        except:
            print("타원곡선 상에 존재하지 않습니다.")

        try:
            print("점 (18, 77)이 타원곡선 상(y^2 = x^3 + 5x + 7) 상의 존재하나요? ")
            Point(18, 77, 5, 7)
            print("타원곡선 상에 존재합니다.")
        except:
            print("타원곡선 상에 존재하지 않습니다.")

        try:
            print("점 (5, 7)이 타원곡선 상(y^2 = x^3 + 5x + 7) 상의 존재하나요? ")
            Point(5, 7, 5, 7)
            print("타원곡선 상에 존재합니다.")
        except:
            print("타원곡선 상에 존재하지 않습니다.")

    def exercise3(self):
        print("********** [타원곡선 상의 덧셈] 점과 역원, 항등원과의 덧셈**********")
        point1 = Point(-1, -1, 5, 7)
        point2 = Point(-1, 1, 5, 7)
        inf = Point(None, None, 5, 7)
        print("(-1, -1) + inf = ", point1 + inf)
        print("inf + (-1, 1) = ", inf + point2)
        print("(-1, -1) + (-1, 1) = ", point1 + point2)

    def exercise4(self):
        # [연습 문제 2.4]
        print("********** [타원곡선 상의 덧셈] 서로 다른 두 점(x1 != x2)의 덧셈 **********")
        print("타원곡선 상(y^2 = x^3 + 5x + 7) 상에서 두 점 (2, 5) (-1, -1) 덧셈")
        x1, y1 = 2, 5
        x2, y2 = -1, -1
        s = (y2 - y1) / (x2 - x1)
        x3 = pow(s, 2) - x1 - x2
        y3 = s * (x1 - x3) - y1
        print("x3:", x3)
        print("y3:", y3)

    def exercise5(self):
        # [연습 문제 2.4]
        print("********** [타원곡선 상의 덧셈] 서로 다른 두 점(x1 != x2)의 덧셈 **********")
        print("타원곡선 상(y^2 = x^3 + 5x + 7) 상에서 두 점 (2, 5) (-1, -1) 덧셈")
        point1 = Point(2, 5, 5, 7)
        point2 = Point(-1, -1, 5, 7)
        print("(2, 5) + (-1, -1) = ", point1 + point2)

    def exercise6(self):
        # [연습 문제 2.6]
        print("********** [타원곡선 상의 덧셈] 같은 두 점(x1 == x2)의 덧셈 **********")
        print("타원곡선 상(y^2 = x^3 + 5x + 7) 상에서 두 점 (-1, -1) (-1, -1) 덧셈")
        x1, y1 = -1, -1
        a = 5

        s = (3 * pow(x1, 2) + a) / (2 * y1)
        x3 = pow(s, 2) - 2 * x1
        y3 = (s * (x1 - x3)) - y1
        print("x3:", x3)
        print("y3:", y3)

    def exercise7(self):
        # [연습 문제 2.6]
        print("********** [타원곡선 상의 덧셈] 같은 두 점(x1 == x2)의 덧셈 **********")
        print("타원곡선 상(y^2 = x^3 + 5x + 7) 상에서 두 점 (-1, -1) (-1, -1) 덧셈")
        point1 = Point(-1, -1, 5, 7)
        point2 = Point(-1, -1, 5, 7)
        print("(-1, -1) + (-1, -1) = ", point1 + point2)

    def test_ne(self):
        print("********** [타원곡선 상의 점이 다른지 확인] **********")
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        self.assertTrue(a != b)
        self.assertFalse(a != a)

    def test_add0(self):
        print("********** [타원곡선 상의 점 덧셈] - 점과 항등원, 역원의 덧셈 **********")
        a = Point(x=None, y=None, a=5, b=7)
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        self.assertEqual(a + b, b)
        self.assertEqual(b + a, b)
        self.assertEqual(b + c, a)

    def test_add1(self):
        print("********** [타원곡선 상의 점 덧셈] - 서로 다른 두 점의 덧셈 **********")
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + b, Point(x=2, y=-5, a=5, b=7))

    def test_add2(self):
        print("********** [타원곡선 상의 점 덧셈] - 같은 두 점의 덧셈 **********")
        a = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=77, a=5, b=7))



## 책 예제 테스트 코드 구현
# run(PointTest("exercise1"))         # 타원곡선 상의 점인지 확인
# run(PointTest("exercise2"))         # 타원곡선 상의 점인지 확인
# run(PointTest("exercise3"))         # 타원곡선 상의 점인지 확인
# run(PointTest("exercise4"))         # 타원곡선 상의 서로 다른 두 점 덧셈
# run(PointTest("exercise5"))         # 타원곡선 상의 서로 다른 두 점 덧셈 - 함수
# run(PointTest("exercise6"))         # 타원곡선 상의 같은 두 점 덧셈
# run(PointTest("exercise7"))         # 타원곡선 상의 같은 두 점 덧셈 - 함수

## 유한체 클래스 기능 테스트셈
# run(PointTest("test_ne"))         # 타원곡선 상의 점이 다른지 확인
# run(PointTest("test_add0"))       # 점과 항등원, 역원의 덧셈
# run(PointTest("test_add1"))       # 서로 다른 두 점의 덧셈
# run(PointTest("test_add2"))       # 같은 두 점의 덧셈


