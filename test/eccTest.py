import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
sys.path.append(os.path.abspath(path))

from unittest import TestCase

from lib.helper import run
from src.point import Point
from src.fieldElement import FieldElement

class ECCTest(TestCase):
    def test_on_curve(self):
        print("********** [타원곡선 상에 점이 유한체로 구성된 점들이 있는지 확인] **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add(self):
        print("********** [타원곡선 상에 점이 덧셈 연산 테스트] **********")
        # tests the following additions on curve y^2=x^3-7 over F_223:
        # (192,105) + (17,56)
        # (47,71) + (117,141)
        # (143,98) + (76,66)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        additions = (
            # (x1, y1, x2, y2, x3, y3)
            (192, 105, 17, 56, 170, 142),
            (47, 71, 117, 141, 60, 139),
            (143, 98, 76, 66, 47, 71),
        )

        # loop over additions
        # initialize x's and y's as FieldElements
        # create p1, p2 and p3 as Points
        # check p1+p2==p3
        for (x1, y1, x2, y2, x3, y3) in additions:
            xx1 = FieldElement(x1, prime)
            yy1 = FieldElement(y1, prime)
            point1 = Point(xx1, yy1, a, b)
            xx2 = FieldElement(x2, prime)
            yy2 = FieldElement(y2, prime)
            point2 = Point(xx2, yy2, a, b)
            xx3 = FieldElement(x3, prime)
            yy3 = FieldElement(y3, prime)
            point3 = Point(xx3, yy3, a, b)
            self.assertEqual(point1+point2, point3)

    def test_rmul(self):
        print("********** [타원곡선 상에 점이 rmul 인 경우 테스트] **********")
        # tests the following scalar multiplications
        # 2*(192,105)
        # 2*(143,98)
        # 2*(47,71)
        # 4*(47,71)
        # 8*(47,71)
        # 21*(47,71)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            # (coefficient, x1, y1, x2, y2)
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        # iterate over the multiplications
        for s, x1_raw, y1_raw, x2_raw, y2_raw in multiplications:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            # initialize the second point based on whether it's the point at infinity
            if x2_raw is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(x2_raw, prime)
                y2 = FieldElement(y2_raw, prime)
                p2 = Point(x2, y2, a, b)

            # check that the product is equal to the expected point
            self.assertEqual(s * p1, p2)

    def exercise1(self):
        # [연습문제 3.1]
        print(
            "********** [점들이 F223에서 정의된 타원곡선 y^2 = x^3 + 7 위에 있는지 확인하기] **********")
        points = ((192, 105), (17, 56), (200, 119), (1, 193), (42, 99))
        prime = 223
        a = FieldElement(num=0, prime=prime)
        b = FieldElement(num=7, prime=prime)
        for x_raw, y_raw in points:
            x = FieldElement(num=x_raw, prime=prime)
            y = FieldElement(num=y_raw, prime=prime)
            try:
                print(f'점 ({x.num}, {y.num}) 타원곡선 y^2 = x^3 + 7 위에 존재하나요?')
                Point(x, y, a, b)
                print(f'타원곡선 위에 존재합니다.')
            except:
                print(f'타원곡선 위에 존재하지 않습니다.')

    def exercise2(self):
        print("********** [유한체에서 점 덧셈] **********")
        # 유한체 클래스로 값들을 생성하고 Point(점) 클래스로 초기화하면 유한체에 정의된 연산 사용 가능
        prime = 223
        a = FieldElement(num=0, prime=prime)
        b = FieldElement(num=7, prime=prime)

        # (192, 105)
        x1 = FieldElement(num=192, prime=prime)
        y1 = FieldElement(num=105, prime=prime)
        # (17, 56)
        x2 = FieldElement(num=17, prime=prime)
        y2 = FieldElement(num=56, prime=prime)
        point1 = Point(x1, y1, a, b)
        point2 = Point(x2, y2, a, b)
        print("(192, 105) + (17, 56) = ", point1+point2)

    def exercise3(self):
        # [연습문제 3.2]
        print(
            "********** [유한체에서 점 덧셈 - F223 에서 정의된 곡선 y^2 = x^3 + 7 위의 점 덧셈] **********")
        # 유한체 클래스로 값들을 생성하고 Point(점) 클래스로 초기화하면 유한체에 정의된 연산 사용 가능
        prime = 223
        a = FieldElement(num=0, prime=prime)
        b = FieldElement(num=7, prime=prime)

        points = ((170, 142, 60, 139), (47, 71, 17, 56), (143, 98, 76, 66))
        for x1_raw, y1_raw, x2_raw, y2_raw in points:
            x1 = FieldElement(num=x1_raw, prime=prime)
            y1 = FieldElement(num=y1_raw, prime=prime)
            x2 = FieldElement(num=x2_raw, prime=prime)
            y2 = FieldElement(num=y2_raw, prime=prime)
            point1 = Point(x1, y1, a, b)
            point2 = Point(x2, y2, a, b)
            print(f"({x1_raw}, {y1_raw}) + ({x2_raw}, {y2_raw}) = ",
                  point1 + point2)

    def exercise4(self):
        # [연습문제 3.4]
        print("********** [유한체에서 점 덧셈 - F223 에서 정의된 곡선 y^2 = x^3 + 7 위의 스칼라 곱셈] **********")
        # 유한체 클래스로 값들을 생성하고 Point(점) 클래스로 초기화하면 유한체에 정의된 연산 사용 가능
        prime = 223
        a = FieldElement(num=0, prime=prime)
        b = FieldElement(num=7, prime=prime)

        # 스칼라 값 , x 좌표, y 좌표
        datas = ((2, 192, 105), (2, 143, 98), (2, 47, 71),
                 (4, 47, 71), (8, 47, 71), (21, 47, 71))
        # datas = ((2, 192, 105), (2, 143, 98))
        for k, x_raw, y_raw in datas:
            x = FieldElement(num=x_raw, prime=prime)
            y = FieldElement(num=y_raw, prime=prime)
            point = Point(x, y, a, b)
            result = point
            for i in range(1, k):
                result += point
            print(f"{k} * ({x}, {y}) = ", result)

    def exercise5(self):
        print("********** [F223 에서 정의된 곡선 y^2 = x^3 + 7 위의 스칼라 곱셈, k가 1 ~ 20] **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        point = Point(x, y, a, b)

        k = 3
        result = k * point
        for k in range(1, 21):
            result = k * point
            print(f'{k} * (47, 71) = ({result.x.num}, {result.y.num})')

    def exercise6(self):
        # [연습문제 3.5]
        print("********** [F223 에서 정의된 곡선 y^2 = x^3 + 7 위의 점 (15, 86) 으로 생성된 군의 위수 구하기] **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        point = Point(x, y, a, b)
        inf = Point(None, None, a, b)

        count = 1
        for k in range(1, 30):
            result = k * point
            if result == inf:
                break
            count += 1
        print("군의 위수: ", count)

    def exercise7(self):
        print("[bit 연산으로 곱셈 연산하기]")
        coef = 26
        result = 0
        current = 1
        while coef:
            #  비트 연산 수행됨
            if coef & 1:
                result += current

            current += current
            coef >>= 1

        print("result = ", result)




# ## 책 예제 테스트 코드 구현
# run(ECCTest("exercise1"))           # 점들이 타원곡선 위에 존재하는지 확인
# run(ECCTest("exercise2"))           # 유한체에서 점 덧셈
# run(ECCTest("exercise3"))           # y^2 = x^3 + 7 위의 점 덧셈
# run(ECCTest("exercise4"))           # y^2 = x^3 + 7 위의 스칼라값과 점 곱셈
# run(ECCTest("exercise5"))           # y^2 = x^3 + 7 위의 스칼라값과 점 곱셈 k가 1 ~ 20
# run(ECCTest("exercise6"))           # y^2 = x^3 + 7 위의 점(15, 86) 으로 생성된 군의 위수
# run(ECCTest("exercise7"))           # 비트연산으로 곱? 테스트 하기
#
#
# ## 타원곡선암호 클래스 기능 테스트
# run(ECCTest("test_on_curve"))     # 타원곡선 위에 존재하는지 확인
# run(ECCTest("test_add"))          # 점 덧셈 테스트
# run(ECCTest("test_rmul"))         # 서로 다른 타입의 곱 테스트

