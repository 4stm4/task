import re
from typing import Dict, Any
from . import interfaces

class PostProcessor:

    normalizer: interfaces.Normalizer

    def __init__(self, normalizer):
        self.normalizer = normalizer

    def find_lists(self, node: Dict[str, Any]):
        repeat_dict = {}
        keys_for_del = []
        for index, value in node.items():
            if len(index) < 4:
                continue
            pos = re.search(r'\w{0,}[\d]', str(index))
            if pos:
                word = index[:str(index).find('[')]
                if word in repeat_dict:
                    repeat_dict[word].append(value)
                else:
                    repeat_dict[word] = [value]
                keys_for_del.append(index)
        for key in keys_for_del:
            if key in node:
                del node[key]
        node.update(repeat_dict)
        return node

    def process_node(self, node: Dict[str, Any], path: str ='')-> Dict[str, Any]:
        result_dict = {}
        for index, value in node.items():
            new_path = f"{path}/{index}" if path else index
            if isinstance(value, dict):
                result_dict.update(
                    self.process_node(value, path=new_path),
                )
            else:
                if "дата" in new_path.lower():
                    value = self.normalizer.date(value)
                elif 'срок' in new_path.lower():
                    value = self.normalizer.period(value)
                result_dict[new_path] = value
        return result_dict
