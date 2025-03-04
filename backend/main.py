import json
from metrics import ValidatorSimple
from func_to_call import parse_all_data, parse_data_with_time

data_v2 = parse_data_with_time('united_data.json')

with open('parsed_dash.json', 'w', encoding='utf-8') as f:
    json.dump(data_v2, f, ensure_ascii=False)

print(1)
print(data_v2)