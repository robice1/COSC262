def concat_list(strings):
    result = ''
    top_str = strings.pop()
    result += top_str
    result += concat_list(strings)
    return result