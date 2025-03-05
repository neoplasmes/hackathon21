import json
from preprocessor import prepare_data_for_metrics_calculation, prepare_row_for_metrics_calculation
from metrics import ValidatorSimple

vs = ValidatorSimple(neural=True)
# result = vs.validate_rag_new(prepare_data_for_metrics_calculation('parsed_data.json').head(10))

with open('united_data.json', 'r', encoding='utf-8') as file:
    old_data = json.load(file)
    print(f'Total rows: {len(old_data)}')
    new_data = []

    i = 0

    for old_row in old_data:
        print('row will be calculated')
        new_row = prepare_row_for_metrics_calculation(old_row)
        new_row_metrics = vs.calc_new_metrics_for_row(new_row)

        keysToCopy =  ['selected_role', 'campus', 'education_level', 'question_category', 'response_time', 'refined', 'refined_response_time']
        normalized_new_row = {key: new_row.get(key, None) for key in keysToCopy}

        normalized_new_row = normalized_new_row | new_row_metrics
        new_data.append(normalized_new_row)  

        print(f'{i} row calculated')
        i = i + 15

        #если считать вообще все ряды, то это будет слишком долго     
        if i == 15 * 50:
            break

    with open('metrics_DB.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False)