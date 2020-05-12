

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        return None

    def __setitem__(self, i, value):
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value

    def __str__(self):
        return "[ " + str(self[0]) + " " + str(self[1]) + " ]"
    def __mul__(self, other):
        return Vector(self[0] * other[0], self[1] * other[1])



class Matrix(Vector):

    def __init__(self, v1, v2, isvector=False):
        Vector.__init__(self, v1, v2)
        self.isvector = isvector

    def __add__(self, other):
        return Matrix(
            Vector(self[0][0] + other[0][0], self[0][1] + other[0][1]),
            Vector(self[1][0] + other[1][0], self[1][1] + other[1][1]),
            isvector=self.isvector + other.isvector
        )

    def __sub__(self, other):
        return Matrix(
            Vector(self[0][0] - other[0][0], self[0][1] - other[0][1]),
            Vector(self[1][0] - other[1][0], self[1][1] - other[1][1]),
            isvector=self.isvector + other.isvector
        )

    def __mul__(self, other):
        mtx = Matrix(Vector(0,0), Vector(0,0), isvector=self.isvector + other.isvector)
        for i in range(2):  # dla każdego wiersza w A:
            for j in range(2):  # dla każdej kolumny w B:
                for k in range(2):  # dla każdego wyrazu:
                    mtx[i][j]  += self[k][j] * other[i][k]
        return mtx

    def __truediv__(self, n):
        return Matrix(
            Vector(self[0][0] / n, self[0][1] / n),
            Vector(self[1][0] / n, self[1][1] / n),
            isvector=self.isvector
        )


class Lin:

    def __init__(self, k, side):
        self.start = []
        k = (2 * k - 1)
        d = side / (k + 1)
        val = side / 2

        for i in range((k + 1) // 2):
            v1 = Vector(d * i, val)
            v2 = Vector(d * i, -val)
            self.start += [Matrix(v1, v2)]

            v1 = Vector(d * -i, val)
            v2 = Vector(d * -i, -val)
            self.start += [Matrix(v1, v2)]

            v1 = Vector(val, d * i)
            v2 = Vector(-val, d * i)
            self.start += [Matrix(v1, v2)]

            v1 = Vector(val, d * -i)
            v2 = Vector(-val, d * -i)
            self.start += [Matrix(v1, v2)]

        self.frame = self.start
        self.diff = [Matrix(Vector(0,0), Vector(0,0)) for _ in range(len(self))]

    def __len__(self):
        return len(self.frame)

    def __getitem__(self, i):
        return self.frame[i]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self):
            result = self[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def transform(self, F):
        self.frame = [F * M for M in self]
        self.diff = [(self.frame[i] - self.start[i]) / 100 for i in range(len(self))]
        self.frame, self.start = self.start, self.frame

    def nextFrame(self):
        self.frame = [(self.frame[i] + self.diff[i]) for i in range(len(self))]

    def add(self, v):
        mtx = Matrix(Vector(0, 0), v)
        mtx.isvector = True
        self.start += [mtx]