import logging
import json
import re
from typing import Any, Dict, List, Union

class SensitiveDataFilter(logging.Filter):
    sensitive_keys = [
        'password', 'email', 'token', 'password_confirm', 'new_password', 'confirm_password',
        'credit_card', 'cvv', 'card_number', 'api_key', 'secret', 'access_token', 'refresh_token'
    ]

    def __init__(self, name: str = '') -> None:
        super().__init__(name)
        self.json_pattern = re.compile(r'\{(?:[^{}]|\{[^{}]*\})*\}')

    def _filter_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        filtered_data = {}
        for key, value in data.items():
            if key.lower() in [k.lower() for k in self.sensitive_keys]:
                filtered_data[key] = '[FILTERED]'
            elif isinstance(value, dict):
                filtered_data[key] = self._filter_dict(value)
            elif isinstance(value, list):
                filtered_data[key] = [self._filter_item(item) for item in value]
            else:
                filtered_data[key] = value
        return filtered_data

    def _filter_item(self, item: Any) -> Any:
        if isinstance(item, dict):
            return self._filter_dict(item)
        elif isinstance(item, list):
            return [self._filter_item(sub_item) for sub_item in item]
        return item

    def _replace_sensitive_in_json(self, msg: str) -> str:
        def replace_json(match: re.Match) -> str:
            json_str = match.group(0)
            try:
                json_data = json.loads(json_str)
                if isinstance(json_data, dict):
                    filtered_data = self._filter_dict(json_data)
                    return json.dumps(filtered_data, ensure_ascii=False)
                return json_str
            except json.JSONDecodeError:
                return json_str
        return self.json_pattern.sub(replace_json, msg)

    def _replace_sensitive_in_text(self, msg: str) -> str:
        for key in self.sensitive_keys:
            pattern = rf'\b{re.escape(key)}\b(?!\s*":)'
            msg = re.sub(pattern, '[FILTERED]', msg, flags=re.IGNORECASE)
        return msg

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        if not msg:
            return True

        # Обробляємо JSON-рядки
        msg = self._replace_sensitive_in_json(msg)
        # Обробляємо текст
        msg = self._replace_sensitive_in_text(msg)
        record.msg = msg

        # Фільтруємо аргументи лише якщо вони є словником або списком
        if record.args and isinstance(record.args, (dict, list, tuple)):
            if isinstance(record.args, dict):
                record.args = self._filter_dict(record.args)
            elif isinstance(record.args, tuple):
                record.args = tuple(self._filter_item(arg) if isinstance(arg, (dict, list)) else arg for arg in record.args)
            elif isinstance(record.args, list):
                record.args = [self._filter_item(arg) if isinstance(arg, (dict, list)) else arg for arg in record.args]

        return True