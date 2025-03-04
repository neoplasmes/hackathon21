import json
import pandas as pd

from init_parser import parse_data_with_time

def _parse_united_data():
    '''
    Метод для генерации распарсенного документа из начального датасета.
    Использовать, когда нет файла 'parsed_data.json'
    '''
    data = parse_data_with_time('united_data.json')

    with open('parsed_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


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