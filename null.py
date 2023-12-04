data = [{'role': 'user', 'content': 'afaffffaf'},
        {'role': 'assistant', 'content': 'asafhaha'},
        {'role': 'user', 'content': 'agahrhr'}]
string_to_be_short=''
for entry in data:
    if entry['role'] == 'user':
        string_to_be_short = string_to_be_short + (f"Клиент: {entry['content']} ")
    elif entry['role'] == 'assistant':
        string_to_be_short = string_to_be_short + (f"Ты: {entry['content']} ")