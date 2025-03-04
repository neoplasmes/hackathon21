from preprocessor import prepare_data_for_metrics_calculation
from metrics import ValidatorSimple

vs = ValidatorSimple(neural=True)
result = vs.validate_rag_new(prepare_data_for_metrics_calculation('parsed_data.json').head(10))

print(result)