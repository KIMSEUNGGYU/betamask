class FiniteFieldElement:
    """
    유한체 클래스 정의
    1. 생성자 (__init__)
    2. 출력문 재정의 (__repr__)
    """

    def __init__(self, value, prime):
        """
        유한체 생성자
        - 유한체 객체 생성시 유한체 값, 위수 초기

        Arguments:
            value (int): 유한체의 값
            prime (int): 유한체 위수

        Raise:
            ValueError: `prime` 위수가 0보다 작거나 유한체 상의 값이 아닐 경우 (prime-1 보다 큰 값일 경우)
        """
        if value >= prime or value < 0:
            error = f'유한체 {value} 는 0 보다 커야하고 {prime-1} 보다 작아야 합니다'
            raise ValueError(error)

        self.value = value
        self.prime = prime



