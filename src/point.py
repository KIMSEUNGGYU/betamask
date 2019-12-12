class Point:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        if self.x is None and self.y is None: # 항등원 부분 처리
            return

        if pow(self.y, 2) != pow(self.x, 3) + a * x + b:
            raise ValueError(f'({x}, {y}) 는 타원 곡선상에 존재하지 않습니다.')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        if self.x is None:
            return f'Point(항등원[무한원점])'
        else:
            return f'Point({self.x}, {self.y})_{self.a}_{self.b}'

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(f'점 {self} {other} 는 같은 타원곡선 위에 존재하지 않습니다')

        # 점 덧셈 성질 1. 항등원끼리의 덧셈인 경우 다른 객체를 반환 (역원)
        if self.x is None:
            return other
        if other.x is None:
            return self

        # 점 덧셈 성질 2. 한 점 + 역원 = 항등원
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # 점 덧셈 성질 3. 서로 다른 두 점(x1 != x2) 상에서의 덧셈
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = pow(s, 2) - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        # 점 덧셈 성질 4. 같은 두 점(P1 == P2) 상에서의 덧셈
        # if self == other: # 이렇게 안하는 이유가 점 덧셈 5 의 성질 때문에
        if self.x == other.x and self.y == other.y:
            s = (3 * pow(self.x, 2) + self.a) / (2 * self.y)
            x3 = pow(s, 2) - (2 * self.x)
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        # 점 덧셈 성질 5. 두 점이 같고, y 가 0 인 경우
        # 두 점이 같고 y 좌표가 0이면 무한원점을 반환
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)