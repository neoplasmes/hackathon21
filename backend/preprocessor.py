import json
import pandas as pd

with open('parsed_dash.json', 'r', encoding='utf-8') as file:
    init_data = json.load(file)

    dataset_for_metrics = {
        "question": [],
        "answer": [],
        "ground_truth": [],
        "contexts": []
    }

    for item in init_data:
        
