from fieldElement import FieldElement

## 비트코인에서 사용하는 secp256k1 에서 정의한 값
## 하지만 여기서는 P 값만 사용
# A = 0
# B = 7
P = pow(2, 256) - pow(2, 32) - 977
# N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

class S256Field(FieldElement):
    """
    비트코인에서 사용하는 secp256k1 에 맞춘 유한체 정의
    secp256k1 에서의 유한체 정의
    """
    def __init__(self, num, prime=None):
        """
        비트코인에서 사용하는 S256 형식을 맞추고 상속받은 유한체에 전달
        :param num:
        :param prime:
        """
        super().__init__(num=num, prime=P)

    def __repr__(self):
        """
        출력 재정의
        :return:
            string: 유한체를 수를 16진수로 표현, 256비트 수는 64자리 16진수로 표현, 빈 자리를 ‘0’으로 채움
        """
        # return 'FieldElement_{}({})'.format(self.prime, self.num)
        return '{}'.format(self.num).zfill(64)
