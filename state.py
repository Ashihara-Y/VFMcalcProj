from typing import TypeVar, Generic, Union, Callable

T = TypeVar('T')

class State(Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._observers: list[Callable] = []
    
    def get(self):
        return self._value

    def set(self, new_value: T):
        if self._value != new_value:
            self._value = new_value
            for observer in self._observers:
                observer()

    def bind(self, observer):
        self._observers.append(observer)

class ReactiveState(Generic[T]):
    def __init__(self, formula: Callable[[], T], reliance_states: list[State]):
        self._value = State(formula())
        self._formula = formula
        self._observers: list[Callable] = []

        for state in reliance_states:
            state.bind(lambda : self.update())

    def get(self):
        return self._value.get()
    
    def update(self):
        old_value = self._value.get()
        self._value.set(self._formula())
        if old_value != self._value.get():
            for observer in self._observers:
                observer()

    def bind(self, observer):
        self._observers.append(observer)
    
# なぜ、ここでグローバルな定義や関数が入るのか？インスタンス属性・メソッドではなく、クラス属性・メソッドか？
# そうはいっても、このモジュールにはクラスが２つ定義されている。いずれのクラスにも反映される属性・メソッドなのか？
# 以下の属性と関数は、Reactive_textでインポートされて使われている。ここに実装するのはなぜか？
StateProperty = Union[T, State[T], ReactiveState[T]]

def bind_props(props: list[StateProperty], bind_func: Callable[[], None]):
    for prop in props:
        if isinstance(prop, State) or isinstance(prop, ReactiveState):
            prop.bind(lambda: bind_func())

def get_prop_value(prop: StateProperty):
    if isinstance(prop, State):
        return prop.get()
    elif isinstance(prop, ReactiveState):
        return prop.get()
    else:
        return prop
