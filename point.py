# 유한체 연산을 사용해야함
from fieldElement import FieldElement

class Point:
    """
    좌표상의 점 설계
    점 덧셈 정의
    점과 스칼라 곱 정의
    """

    def __init__(self, x, y, a, b):
        """
        점 데이터 초기화
        :param x: x 좌표
        :param y: y 좌표
        :param a: y^2 = x^3 + ax + b 에서의 a
        :param b: y^2 = x^3 + ax + b 에서의 b
        """
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        # x, y 가 None 값이면 무한원점 인 0 (항등원)
        if self.x is None and self.y is None:
            return

        # y**2 == x**3 + a*x + b
        # 주어진 값이 타원 곡선 상에 점이어야함
        if self.y**2 != self.x**3 + a * x + b:
            # if not, throw a ValueError
            raise ValueError('({}, {}) is not on the curve'.format(x, y))

    def __eq__(self, other):
        """
        점 끼리 같은지 비교
        :param other: 점 객체
        :return:
            boolean: 점끼리 같으면 True, 다르면 False
        """
        return self.x == other.x and self.y == other.y \
            and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        """
        점 끼리 다른지 비교
        :param other: 점 객체
        :return:
            boolean: 점끼리 다르면 True, 같으면 False
        """
        return not (self == other)

    def __repr__(self):
        """
        출력문 재정의
        :return:
            string: 조건에 따라 다른 문구 출력
        """
        if self.x is None:
            return 'Point(infinity)'
        elif isinstance(self.x, FieldElement):
            return 'Point({},{})_{}_{} FieldElement({})'.format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
        else:
            return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)

    def __add__(self, other):
        """
        점 덧셈 기능 구현
        점 덧셈의 경우 고려 사항이 4가지 존재
        1. 항등원끼리의 덧셈일 경우 다른 점 객체 반환
        2.

        :param other: 점 객체
        :return:
            object: 각 연산에 따른 점 객체
        """
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))

            ## 0. 자신과 항등원을 더하면 역원을 구할 수 있음.
            # Case 0.0: self is the point at infinity, return other
        if self.x is None:
            return other
            # Case 0.1: other is the point at infinity, return self
        if other.x is None:
            return self

            ## 1. 역원을 더하면 항등원을 반환
            # Case 1: self.x == other.x, self.y != other.y
            # Result is point at infinity
            # 무한원점 리턴 x 는 같고 y가 다른것 -> 무한원점
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

            ## 2. x 값이 다를 경우
            # Case 2: self.x ≠ other.x
            # Formula (x3,y3)==(x1,y1)+(x2,y2)
            # s=(y2-y1)/(x2-x1)
            # x3=s**2-x1-x2
            # y3=s*(x1-x3)-y1
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s ** 2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

            ## 3. 두 점이 같은 경우
            # Case 3: self == other
            # 같으면 기울기
            # Formula (x3,y3)=(x1,y1)+(x1,y1)
            # s=(3*x1**2+a)/(2*y1)
            # x3=s**2-2*x1
            # y3=s*(x1-x3)-y1
        if self == other:
            s = (3 * self.x ** 2 + self.a) / (2 * self.y)
            x = s ** 2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

            ## 일 직선이자, y=0 인 경우
            # Case 4: if we are tangent to the vertical line,
            # we return the point at infinity
            # note instead of figuring out what 0 is for each type
            # we just use 0 * self.x
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

    # coefficient 계수
    def __rmul__(self, coefficient):
        """
        스칼라 곱셈 정의?
        점 덧셈의 곱셈이지만, 다른 타입끼리의 곱셈일 경우 오른쪽 타입을 기준으로 수행
        :param coefficient: 스칼라 곱에서 스칼라 값
        :return:
        """
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b) # 무한원점으로 초기화, 점덧셈이므로 무한원점은 0
        while coef:
            if coef & 1: # 가장 오른쪽 비트가 1인지 조사해서 1이면 그 때의 current 값을 더함
                result += current
            current += current # 현재 점인 자신을 2배로 만듦
            coef >>= 1 # 최하위 비트 탈락 -> 다음 최하위 비트 사용 준비
        return result

