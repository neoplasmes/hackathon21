import json
from typing import List, Dict
import pandas as pd

from init_parser import parse_data_with_time, parse_contexts, extract_tags, clean_text

def _parse_united_data():
    '''
    Метод для генерации распарсенного документа из начального датасета.
    Использовать, когда нет файла 'parsed_data.json'
    '''
    data = parse_data_with_time('united_data.json')

    with open('parsed_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# для расчёта метрик всего сета (united_data) и подготовке к хранению в псевдо-БД
def prepare_row_for_metrics_calculation(row: Dict) -> Dict:
    parsed = {
        'selected_role': row['Выбранная роль'],
        'campus': row['Кампус'],
        'education_level': row['Уровень образования'],
        'question_category': row['Категория вопроса'],
        'question': clean_text(row['Вопрос пользователя']),
        'user_filters': row['user_filters'],
        'question_filters': row['question_filters'],
        'saiga_answer': clean_text(row['Saiga']),
        'giga_answer': clean_text(row['Giga']),
        'answer': clean_text(row['Ответ AI']), # ответ хсе бота
        'winner': row['Кто лучше?'],
        'comment': row['Комментарий'],
        # 'contexts': parse_contexts(row['Ресурсы для ответа']),
        'response_time': row['Время ответа модели (сек)'],
        'refined': row.get('Уточнённый ответ пользователя') != None,
        'refined_response_time': row.get('Время ответа модели на уточненный вопрос (сек)')
    }

    # keysToCopy =  ["selected_role", "campus", "education_level", "question_category"]

    # processedRow = {key: row.get(key, None) for key in keysToCopy}
    # parsed['question'] = parsed['user_question']
    # parsed['answer'] = parsed['hse_ai_answer']
    
    ground_truth = None
    if parsed['winner'] == 'Saiga':
        ground_truth = parsed['saiga_answer']
    else:
        ground_truth = parsed['giga_answer']
    parsed['ground_truth'] = ground_truth

    extended_contexts = parse_contexts(row['Ресурсы для ответа'])
    contexts = []
    for ctx in extended_contexts:
        contexts.append(ctx['text'])
    parsed['contexts'] = contexts

    return parsed

def prepare_data_for_metrics_calculation(path: str) -> pd.DataFrame:
    '''
    Метод для генерации dataframe для расчёта метрик
    '''
    with open(path, 'r', encoding='utf-8') as file:
        init_data = json.load(file)

        dataset_for_metrics = {
            'question': [],
            'answer': [],
            'ground_truth': [],
            'contexts': []
        }

        for item in init_data:
            dataset_for_metrics['question'].append(item['user_question'])
            dataset_for_metrics['answer'].append(item['hse_ai_answer'])
            
            ground_truth = None
            if item['winner'] == 'Saiga':
                ground_truth = item['saiga_answer']
            else:
                ground_truth = item['giga_answer']
            dataset_for_metrics['ground_truth'].append(ground_truth)

            contexts = []
            for ctx in item['contexts']:
                contexts.append(ctx['text'])
            dataset_for_metrics['contexts'].append(contexts)
        
        return pd.DataFrame(dataset_for_metrics)