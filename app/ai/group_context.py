from collections import defaultdict
from typing import Dict, List

_group_context: Dict[int, List[dict]] = defaultdict(list)

MAX_GROUP_HISTORY = 20


def add_group_user_message(chat_id: int, text: str):
    _group_context[chat_id].append({"role": "user", "content": text})
    _group_context[chat_id] = _group_context[chat_id][-MAX_GROUP_HISTORY:]


def add_group_assistant_message(chat_id: int, text: str):
    _group_context[chat_id].append({"role": "assistant", "content": text})
    _group_context[chat_id] = _group_context[chat_id][-MAX_GROUP_HISTORY:]


def get_group_context(chat_id: int):
    return list(_group_context[chat_id])


def clear_group_context(chat_id: int):
    _group_context[chat_id].clear()
