import jsonpickle


class Schema:
    """Mocked class for all schema related functionalities."""

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.params = None

    def parameters(self, **kwargs) -> "SchemaParameters":
        self.params = SchemaParameters(**kwargs)
        return self.params

    @property
    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, input):
        return jsonpickle.decode(input)

    def __eq__(self, other):
        return self.to_json == other.to_json


class Image(Schema):
    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)


class SingleChoice(Schema):
    def __init__(self, **kwargs):
        super(SingleChoice, self).__init__(**kwargs)


class SchemaParameters:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, input):
        return jsonpickle.decode(input)
