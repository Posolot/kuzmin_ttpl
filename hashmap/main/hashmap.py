import re
from typing import Any, Dict, List, Tuple


class InvalidConditionException(Exception):
    pass


class SpecialDict(dict):
    def iloc(self):
        class IlocAccessor:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, index: int) -> Any:
                sorted_keys = sorted(self.parent.keys())
                return self.parent[sorted_keys[index]]

        return IlocAccessor(self)

    def ploc(self):
        class PlocAccessor:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, condition: str) -> Dict[str, Any]:
                parsed_conditions = self._parse_condition(condition)
                result = {}
                for key, value in self.parent.items():
                    numeric_key = self._parse_key(key)
                    if numeric_key and self._match_condition(numeric_key, parsed_conditions):
                        result[key] = value
                return result

            def _parse_key(self, key: str) -> List[float]:
                if re.search(r'[a-zA-Z]', key):
                    return []
                filtered_key = re.sub(r'[^\d.,-]', '', key)
                try:
                    return [float(num) for num in filtered_key.split(',') if num]
                except ValueError:
                    return []

            def _parse_condition(self, condition: str) -> List[Tuple[str, float]]:
                condition = condition.replace(" ", "")
                conditions = condition.split(",")
                parsed_conditions = []

                for cond in conditions:
                    match = re.match(r"([<>]=?|==|<>)(-?\d+(\.\d+)?)", cond)
                    if not match:
                        raise InvalidConditionException(f"Invalid condition: {cond}")
                    operator, number = match.group(1), float(match.group(2))
                    parsed_conditions.append((operator, number))

                return parsed_conditions

            def _match_condition(self, key_values: List[float], conditions: List[Tuple[str, float]]) -> bool:
                if len(key_values) != len(conditions):
                    return False
                for i in range(len(conditions)):
                    operator, threshold = conditions[i]
                    key_value = key_values[i]
                    if operator == ">" and not key_value > threshold:
                        return False
                    elif operator == ">=" and not key_value >= threshold:
                        return False
                    elif operator == "<" and not key_value < threshold:
                        return False
                    elif operator == "<=" and not key_value <= threshold:
                        return False
                    elif operator == "==" and not key_value == threshold:
                        return False
                    elif operator == "<>" and not key_value != threshold:
                        return False
                return True

        return PlocAccessor(self)

