import json

def extract_valid_json(text):
    start_index = text.find('{')
    if start_index == -1:
        return None  # 没有找到起始大括号

    brace_count = 0
    for i, char in enumerate(text[start_index:], start=start_index):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                json_text = text[start_index:i+1]
                try:
                    json_obj = json.loads(json_text)
                    return json_obj  # 返回解析后的 JSON 对象
                except json.JSONDecodeError:
                    return None  # 提取的字符串不是有效的 JSON
    return None  # 没有找到有效的闭合大括号

