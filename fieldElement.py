class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = 'Num {} not in field range 0 to {}'.format(
                num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        # this should be the inverse of the == operator
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num + other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different Fields')
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num - other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num * other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        # use fermat's little theorem:
        # self.num**(p-1) % p == 1
        # this means:
        # 1/n == pow(n, p-2, p)
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)

# class FieldElement:
#     """
#     유한체 설계
#     """
#     def __init__(self, num, prime):
#         """
#         유한체 초기화 함수로 유한체 값, 소수를 받음
#         유한체 값이 소수보다 크거나 0 보다 작으면 에러 발생
#         :param num: 유한체 상에 값
#         :param prime: 위수 P
#         """
#         if num >= prime or num < 0:
#             error = 'Num {} not in field range 0 to {}'.format(
#                 num, prime - 1)
#             raise ValueError(error)
#         self.num = num
#         self.prime = prime
#
#     def __repr__(self):
#         """
#         출력을 재정의
#         :return:
#             string: 유한체의 형태 출력문을 반환함
#         """
#         return 'FieldElement_{}({})'.format(self.prime, self.num)
#
#     def __eq__(self, other):
#         """
#         유한체끼리 같은지 비교
#         :param
#             other: 유한체 객체
#         :return:
#             boolean: 같으면 True, 다르면 False
#         """
#         if other is None:
#             return False
#         return self.num == other.num and self.prime == other.prime
#
#     def __ne__(self, other):
#         """
#         유한체끼리 다른지 비교
#         :param other: 유한체 객체
#         :return:
#             boolean: 유한체끼리 같으면 False, 다르면 True
#         """
#         # this should be the inverse of the == operator
#         return not (self == other)
#
#     def __add__(self, other):
#         """
#         유한체 덧셈 기능 정의
#         :param other: 유한체 객체
#         :return:
#             Object: 유한체끼리의 덧셈 값을 가진 유한체 객체
#         """
#         if self.prime != other.prime:
#             raise TypeError('Cannot add two numbers in different Fields')
#         # self.num and other.num are the actual values
#         # self.prime is what we need to mod against
#         num = (self.num + other.num) % self.prime
#         # We return an element of the same class
#         return self.__class__(num, self.prime)
#
#     def __sub__(self, other):
#         """
#         유한체 뺄셈 기능 정의
#         :param other: 유한체 객체
#         :return:
#             Object: 유한체끼리의 뺄셈 값을 가진 유한체 객체
#         """
#         if self.prime != other.prime:
#             raise TypeError('Cannot subtract two numbers in different Fields')
#         # self.num and other.num are the actual values
#         # self.prime is what we need to mod against
#         num = (self.num - other.num) % self.prime
#         # We return an element of the same class
#         return self.__class__(num, self.prime)
#
#     def __mul__(self, other):
#         """
#         유한체 곱셈 기능 정의
#         :param other: 유한체 객체
#         :return:
#             Object: 유한체끼리의 뺄셈 값을 가진 유한체 객체
#         """
#         if self.prime != other.prime:
#             raise TypeError('Cannot multiply two numbers in different Fields')
#         # self.num and other.num are the actual values
#         # self.prime is what we need to mod against
#         num = (self.num * other.num) % self.prime
#         # We return an element of the same class
#         return self.__class__(num, self.prime)
#
#     def __pow__(self, exponent):
#         """
#         유한체 제곱 기능 정의
#         :param exponent: 지수 값
#         :return:
#             Object: 유한체끼리의 제곱 값을 가진 유한체 객체
#         """
#         n = exponent % (self.prime - 1)
#         num = pow(self.num, n, self.prime)
#         return self.__class__(num, self.prime)
#
#     def __truediv__(self, other):
#         """
#         유한체 나눗셈 기능 정의
#         :param other: 유한체 객체
#         :return:
#             Object: 유한체끼리의 제곱 값을 가진 유한체 객체
#         """
#         if self.prime != other.prime:
#             raise TypeError('Cannot divide two numbers in different Fields')
#         # self.num and other.num are the actual values
#         # self.prime is what we need to mod against
#         # use fermat's little theorem:
#         # self.num**(p-1) % p == 1
#         # this means:
#         # 1/n == pow(n, p-2, p)
#         num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
#         # We return an element of the same class
#         return self.__class__(num, self.prime)