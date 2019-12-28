import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
sys.path.append(os.path.abspath(path))

from unittest import TestCase

from lib.helper import run
from src.fieldElement import FieldElement

class FieldElementTest(TestCase):
    def exercise1(self):
        # [연습 문제 1.1]
        print("********** [같은 유한체인지 확인] **********")
        a = FieldElement(7, 13)
        b = FieldElement(6, 13)
        print("a == b ? ", a == b)
        print("a == a ? ", a == a)

    def exercise2(self):
        # [연습 문제 1.2]
        print("********** [유한체 F57 에서 덧셈, 뺄셈 연산하기] **********")
        a = FieldElement(44, 57)
        b = FieldElement(33, 57)
        print("44 +f 33 = ", a + b)
        a = FieldElement(9, 57)
        b = FieldElement(29, 57)
        print("9 -f 29 = ", a - b)
        a = FieldElement(17, 57)
        b = FieldElement(42, 57)
        c = FieldElement(49, 57)
        print("17 +f 42 +f 49 = ", a + b + c)
        a = FieldElement(52, 57)
        b = FieldElement(30, 57)
        c = FieldElement(38, 57)
        print("52 -f 30 -f 38 = ", a - b - c)

    def exercise3(self):
        # [연습 문제 1.4]
        print("********** [유한체 F97 에서 곱셈과 거듭제곱 연산하기] **********")
        a = FieldElement(95, 97)
        b = FieldElement(45, 97)
        c = FieldElement(31, 97)
        print("95 *f 45 * 31 = ", a * b * c)
        a = FieldElement(17, 97)
        b = FieldElement(13, 97)
        c = FieldElement(19, 97)
        d = FieldElement(44, 97)
        print("17 *f 13 * 19 * 44 = ", a * b * c * d)
        a = FieldElement(12, 97)
        b = FieldElement(77, 97)
        exponent_a = 7
        exponent_b = 49
        print("(12**7) *f (77 f** 49) = ", (a ** exponent_a) * (b ** exponent_b))

    def exercise4(self):
        # [연습 문제 1.5]
        print("********** [k가 각각 1, 3, 7, 13, 18 인 경우 유한체 f19 에서 집합 구하기] **********")
        print("********** [집합 {k *f 0, k *f 1, k *f 2, ... k *f 18}] **********")
        prime = 19
        for k in (1, 3, 7, 13, 18):
            print([k * i % prime for i in range(prime)])
            # print(sorted([k * i % prime for i in range(prime)]))

    def exercise5(self):
        # [연습 문제 1.7]
        print("********** [7, 11, 17, 31 인 p 값에 대해 유한체 Fp 에서 집합을 구하기] **********")
        print("********** [{1^(p-1), 2^(p-1), 3^(p-1), 4^(p-1), (p-1)^(p-1)}] **********")
        for prime in (7, 11, 17, 31):
            print([pow(i, prime-1, prime) for i in range(1, prime)])

    def exercise6(self):
        # [연습 문제 1.8]
        print("********** [유한체 31, F31 에서 나눗셈, 역수 계산하기] **********")
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        print("3 /f 24", a / b)
        a = FieldElement(17, 31)
        exponent = -3
        print("17^-3", a ** exponent)
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        exponent = -4
        print("4^-4 *f 11", a ** exponent * b)


    def test_ne(self):
        print("********** [유한체가 다른지 확인] **********")
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        print("********** [유한체 덧셈] **********")
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        self.assertEqual(a + b, FieldElement(17, 31))
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        self.assertEqual(a + b, FieldElement(7, 31))

    def test_sub(self):
        print("********** [유한체 뺄셈] **********")
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        self.assertEqual(a - b, FieldElement(25, 31))
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        self.assertEqual(a - b, FieldElement(16, 31))

    def test_mul(self):
        print("********** [유한체 곱셈] **********")
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        self.assertEqual(a * b, FieldElement(22, 31))

    def test_pow(self):
        print("********** [유한체 거듭 제곱] **********")
        a = FieldElement(17, 31)
        self.assertEqual(a**3, FieldElement(15, 31))
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        self.assertEqual(a**5 * b, FieldElement(16, 31))

    def test_div(self):
        print("********** [유한체 나눗셈] **********")
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        self.assertEqual(a / b, FieldElement(4, 31))
        a = FieldElement(17, 31)
        self.assertEqual(a**-3, FieldElement(29, 31))
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        self.assertEqual(a**-4 * b, FieldElement(13, 31))


## 책 예제 테스트 코드 구현
# run(FieldElementTest("exercise1"))
# run(FieldElementTest("exercise2"))
# run(FieldElementTest("exercise3"))
# run(FieldElementTest("exercise4"))
# run(FieldElementTest("exercise5"))
# run(FieldElementTest("exercise6"))

## 유한체 클래스 기능 테스트셈
run(FieldElementTest("test_ne"))
run(FieldElementTest("test_add"))
run(FieldElementTest("test_sub"))
run(FieldElementTest("test_mul"))
run(FieldElementTest("test_pow"))
run(FieldElementTest("test_div"))

