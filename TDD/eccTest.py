from unittest import TestCase
import os
import sys
sys.path.append(os.path.abspath("/Users/SG/PycharmProjects/bitcoin/"))
from point import Point
from fieldElement import FieldElement
from lib.helper import run

class ECCTest(TestCase):
    def test_on_curve(self):
        # tests the following points whether they are on the curve or not
        # on curve y^2=x^3-7 over F_223:
        # (192,105) (17,56) (200,119) (1,193) (42,99)
        # the ones that aren't should raise a ValueError
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))

        # iterate over valid points
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            # Creating the point should not result in an error
            Point(x, y, a, b)

        # iterate over invalid points
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)
    def test_add(self):
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
        # iterate over the additions
        for x1_raw, y1_raw, x2_raw, y2_raw, x3_raw, y3_raw in additions:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            x2 = FieldElement(x2_raw, prime)
            y2 = FieldElement(y2_raw, prime)
            p2 = Point(x2, y2, a, b)
            x3 = FieldElement(x3_raw, prime)
            y3 = FieldElement(y3_raw, prime)
            p3 = Point(x3, y3, a, b)
            # check that p1 + p2 == p3
            self.assertEqual(p1 + p2, p3)
    def test_rmul(self):
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
    def ex_1(self):
        print("타원곡선 y^2=x^3+7 상의 점인지 확인")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        # (192,105)
        x1 = FieldElement(192, prime)
        y1 = FieldElement(105, prime)
        print("(192, 105):", pow(y1, 2) == pow(x1, 3) + b)

        # (17,56)
        x1 = FieldElement(17, prime)
        y1 = FieldElement(56, prime)
        print("(17, 56):", pow(y1, 2) == pow(x1, 3) + b)

        # (200,119) false
        x1 = FieldElement(200, prime)
        y1 = FieldElement(119, prime)
        print("(200, 119):", pow(y1, 2) == pow(x1, 3) + b)

        # (1,193)
        x1 = FieldElement(1, prime)
        y1 = FieldElement(193, prime)
        print("(1, 193):", pow(y1, 2) == pow(x1, 3) + b)

        # (42,99) false
        x1 = FieldElement(42, prime)
        y1 = FieldElement(99, prime)
        print("(42, 99):", pow(y1, 2) == pow(x1, 3) + b)
    def ex_2(self):
        print("타원 곡선 상에서 덧셈 연산")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        point1 = Point(FieldElement(170, prime), FieldElement(142, prime), a, b)
        point2 = Point(FieldElement(60, prime), FieldElement(139, prime), a, b)
        print("(170,142) + (60,139):",point1 + point2)

        point1 = Point(FieldElement(47, prime), FieldElement(71, prime), a, b)
        point2 = Point(FieldElement(17, prime), FieldElement(56, prime), a, b)
        print("(47, 71) + (17, 56):", point1 + point2)

        # (143,98) + (76,66)
        point1 = Point(FieldElement(143, prime), FieldElement(98, prime), a, b)
        point2 = Point(FieldElement(76, prime), FieldElement(66, prime), a, b)
        print("(143, 98) + (76, 66):", point1 + point2)

    def ex_3(self):
        print("타원 곡선 상에서 스칼라 곱셈 연산")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        # 2*(192, 105)
        x = FieldElement(num=192, prime=prime)
        y = FieldElement(num=105, prime=prime)
        point = Point(x, y, a, b)
        print("2*(192, 105) = ", point + point)

        # 2*(143, 98)
        x = FieldElement(143, prime)
        y = FieldElement(98, prime)
        point = Point(x, y, a, b)
        print("2*(143, 98) = ",point+point)

        # 2*(47, 71)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        point = Point(x, y, a, b)
        print("2*(47, 71) = ",point+point)
        # print(2*point)

        # 4*(47, 71)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        point = Point(x, y, a, b)
        print("4*(47, 71) = ",point+point+point+point)
        # print(4*point)

        # 8*(47, 71)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        point = Point(x, y, a, b)
        print("8*(47, 71) = ",point+point+point+point+point+point+point+point)

        # 21*(47, 71)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        point = Point(x, y, a, b)
        print("21*(47, 71) = ",21 * point)

    def ex_4(self):
        # 대칭이 있음.!!
        # 무한원점이 안보임 -> 수를 늘리니깐 에러 발생
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        p = Point(x, y, a, b)  # G
        for s in range(1, 21):
            result = s * p  # 스칼라 곱!
            print('{}*(47,71)=({},{})'.format(s, result.x.num, result.y.num))

    def ex_5(self):
        print("F223 에서 곡선 y^2 = x^3 + 7 위의 점 (15, 86) 으로 생성된 군의 위수 구하기")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        inf = Point(None, None, a, b)
        count = 1
        product = p
        while product != inf:
            product += p
            count += 1
        print("군의 위수:", count)

    def ex_6(self):
        print("F223 에서 곡선 y^2 = x^3 + 7 위의 점 (15, 86) 으로 생성된 군의 위수 구하기 2 - 하드코딩으로 확인해보기")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        print(0 * p)
        print(1 * p)
        print(2 * p)
        print(3 * p)
        print(4 * p)
        print(5 * p)
        print(6 * p)
        print(7 * p)
        print(8 * p)

    def ex_7(self):
        print("생성점 G 의 x, y 좌표가 타원곡선 y^2 = x^3 + 7 위의 점인가")
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        prime = pow(2, 256) - pow(2, 32) - 977

        print(pow(gy, 2,) % prime == (pow(gx,3) + 7) % prime)

    def ex_8(self):
        print("생성점 G 로 생성한 군의 위수 N 인지 확인")
        GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        prime = pow(2, 256) - pow(2, 32) - 977
        N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

        x = FieldElement(GX, prime)
        y = FieldElement(GY, prime)
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        G = Point(x, y, a, b)
        # print("G", G)
        print(N*G)

# run(ECCTest('test_on_curve'))
# run(ECCTest('test_add'))
# run(ECCTest('test_rmul'))

# run(ECCTest("ex_1"))
# run(ECCTest("ex_2"))
# run(ECCTest("ex_3"))
# run(ECCTest("ex_4"))
# run(ECCTest("ex_5"))
# run(ECCTest("ex_6"))
# run(ECCTest("ex_7"))
run(ECCTest("ex_8"))
