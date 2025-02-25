import typing

class EventArray:

    def __init__(self, signal: typing.List[{str, int}]):
        self.e_data_array = list[{str, int}]

    def get(self):
        self.e_data_array._data = self.e_data_array.put()
        return self.e_data_array._data

    def set(self, new_value: dict[str, int]):
        if self.e_data_array._data.key == new_value.key and self.e_data_array._data.value != new_value.value:
            self.e_data_array.append(new_value)
        elif self.e_data_array._data.key != new_value.key and self.e_data_array._data.value != new_value.value:
            self.e_data_array.append(new_value)
        else:
            pass

