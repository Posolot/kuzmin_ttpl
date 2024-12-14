import re
from typing import Any, Dict, List, Tuple


class InvalidConditionException(Exception):
    pass


class SpecialDict(dict):
    @property
    def iloc(self):
        class IlocPandas:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, index: int) -> Any:
                sorted_keys = sorted(self.parent.keys())
                return self.parent[sorted_keys[index]]

        return IlocPandas(self)

    @property
    def ploc(self):
        class PlocSearcher:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, condition: str) -> Dict[str, Any]:
                parsed_conditions = self._parse_condition(condition)
                result = {}
                for key, value in self.parent.items():
                    num_key = self._parse_key(key)
                    if num_key and self._match_approved_elements(num_key, parsed_conditions):
                        result[key] = value
                return result

            def _parse_key(self, key: str) -> List[float]:
                if re.search(r'[a-zA-Z]', key):
                    return []
                filtered_key = re.sub(r'[^\d.,-]', '',key)
                result = []
                for num in filtered_key.split(','):
                    if num:
                        try:
                            result.append(float(num))
                        except ValueError:
                            pass
                return result

            def _parse_condition(self, condition: str) -> List[Tuple[str, float]]:
                cond = condition.replace(" ", "")
                cond = cond.split(",")
                pars_cond = []

                for i in cond:
                    match = re.match(r"([<>]=?|==|<>)(-?\d+(\.\d+)?)", i)
                    if not match:
                        raise InvalidConditionException(f"Invalid condition: {i}")
                    operator, number = match.group(1), float(match.group(2))
                    pars_cond.append((operator, number))

                return pars_cond

            def _match_approved_elements(self, key_values: List[float], conditions: List[Tuple[str, float]]) -> bool:
                if len(key_values) != len(conditions):
                    return False
                for i in range(len(conditions)):
                    operator, limit_num = conditions[i]
                    key_value = key_values[i]
                    operators = {
                        ">": lambda x, y: x > y,
                        ">=": lambda x, y: x >= y,
                        "<": lambda x, y: x < y,
                        "<=": lambda x, y: x <= y,
                        "==": lambda x, y: x == y,
                        "<>": lambda x, y: x != y
                    }
                    if not operators[operator](key_value, limit_num):
                        return False
                return True

        return PlocSearcher(self)
