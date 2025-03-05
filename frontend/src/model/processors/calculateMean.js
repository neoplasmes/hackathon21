// дата как в metrics_DB
export const calculateMean = (data) => {
    const meanMetrics = {
        "response_time": 0,
        "context_recall": 0,
        "context_precision": 0,
        "context_relevance": 0,
        "answer_correctness_literal": 0,
        "answer_correctness_neural": 0,
        "document_fidelity": 0,
        "logical_consistency": 0,
        "Deception Probability": 0,
    }

    data.forEach(element => {
        for (const key in meanMetrics) {
            meanMetrics[key] = meanMetrics[key] + element[key];
        }
    });

    for (const key in meanMetrics) {
        meanMetrics[key] = meanMetrics[key] / data.length;
    }

    return meanMetrics;
}