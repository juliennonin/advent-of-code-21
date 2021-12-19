# %%
from numpy import prod

# %%
def hex2bin(shex):
    n = len(shex)
    return bin(int(shex, 16))[2:].zfill(n * 4)

class Stream():
    def __init__(self, stream):
        self.stream = stream
        self._pointer = 0
    
    def move(self, n):
        assert self._pointer + n <= self.__len__()
        self._pointer += n

    def pop(self, n):
        s = self.__getitem__(slice(0, n))
        self.move(n)
        return s

    @property
    def pointer(self):
        return self._pointer

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = (index.start or 0) + self._pointer
            index = slice(start, index.stop + self._pointer, index.step)
        elif isinstance(index, int):
            index = index + self._pointer
        else:
            raise IndexError("Must be either int or slice.")
        return self.stream[index]
            
    def __len__(self):
        return len(self.stream)
    
    def parse(self):
        version = int(self.pop(3), 2)
        ttype = int(self.pop(3), 2)
        if ttype == 4:
            value = self._pop_literal()
            return Literal(version, value)
        
        match int(self.pop(1), 2):  # length_type_id
            case 0: content = self._parse_with_length_in_bits()
            case 1: content = self._parse_with_number_of_packets()
            case _: raise IndexError
        
        match ttype:
            case 0: return Sum(version, content)
            case 1: return Prod(version, content)
            case 2: return Min(version, content)
            case 3: return Max(version, content)
            case 5: return Sup(version, content)
            case 6: return Inf(version, content)
            case 7: return Eq(version, content)
            case _: raise ValueError

    def _parse_with_length_in_bits(self):
        total_length_in_bits = int(self.pop(15), 2)
        pos_beg = pos_end = self._pointer
        content = []
        while pos_end - pos_beg < total_length_in_bits:
            content.append(self.parse())
            pos_end = self._pointer
        return content

    def _parse_with_number_of_packets(self):
        number_of_subpackets = int(self.pop(11), 2)
        content = []
        for _ in range(number_of_subpackets):
            content.append(self.parse())
        return content

    def _pop_literal(self):
        content = []
        once_more = True
        while once_more:
            if self.pop(1) != '1':
                once_more = False
            content.append(self.pop(4))
        return int(''.join(content), 2)

# %%
class Literal:
    TYPE = 4
    def __init__(self, version, number):
        self.version = version
        self.number = number

    def __repr__(self):
        return f"{self.number}"

    def total_version(self):
        return self.version
    
    def evaluate(self):
        return self.number

class Operator:
    SYMBOL = '?'
    def __init__(self, version, content):
        self.version = version
        self.content = content
    
    def total_version(self):
        version = self.version
        for op in self.content:
            version += op.total_version()
        return version
    
    def _children_evaluation(self):
        return (op.evaluate() for op in self.content)

    def evaluate(self):
        raise NotImplementedError

    def __repr__(self):
        symb = f" {self.SYMBOL} "
        return f"({symb.join([str(s) for s in self.content])})"   

class BinaryOperator(Operator):
    def __init__(self, version, content):
        assert len(content) == 2
        self.left, self.right = content
        super().__init__(version, content)

    def __repr__(self):
        return f"{{{self.left} {self.SYMBOL} {self.right}}}"

class Sum(Operator):
    SYMBOL = "+"
    TYPE = 0

    def evaluate(self):
        return sum(self._children_evaluation())

class Prod(Operator):
    SYMBOL = "×"
    TYPE = 1

    def evaluate(self):
        return prod(list(self._children_evaluation()))

class Min(Operator):
    SYMBOL = "min"
    TYPE = 2

    def evaluate(self):
        return min(self._children_evaluation())

    def __repr__(self):
        return f"{self.SYMBOL}({', '.join([str(s) for s in self.content])})"

class Max(Operator):
    SYMBOL = "max"
    TYPE = 3

    def evaluate(self):
        return max(self._children_evaluation())
    
    def __repr__(self):
        return f"{self.SYMBOL}({', '.join([str(s) for s in self.content])})"

class Sup(BinaryOperator):
    SYMBOL = '>'
    TYPE = 5

    def evaluate(self):
        left, right = self._children_evaluation()
        return int(left > right)

class Inf(BinaryOperator):
    SYMBOL = '<'
    TYPE = 6

    def evaluate(self):
        left, right = self._children_evaluation()
        return int(left < right)

class Eq(BinaryOperator):
    SYMBOL = '='
    TYPE = 7

    def evaluate(self):
        left, right = self._children_evaluation()
        return int(left == right)

# %%
if __name__ == "__main__":
    with open("../data/day16.txt", "r") as f:
        shex = f.read()
        stream = Stream(hex2bin(shex))

    operation = stream.parse()
    part1 = operation.total_version()
    part2 = operation.evaluate()

    print("Part 1 —", part1)
    print("Part 2 —", part2)

