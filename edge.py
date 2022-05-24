class Edge:
    def __init__(self, vertice1, vertice2, weight=1) -> None:
        self.vertice1 = vertice1
        self.vertice2 = vertice2
        self.weight = weight

    def __eq__(self, other: object) -> bool:
        return (
            self.vertice1 == other.vertice1 and self.vertice2 == other.vertice2
        ) or (self.vertice2 == other.vertice1 and self.vertice1 == other.vertice2)

    def __hash__(self) -> int:
        return hash(self.vertice1) ^ hash(self.vertice2) ^ hash(self.weight)

    def __str__(self) -> str:
        return str(tuple(self.vertice1, self.vertice2, self.weight))
