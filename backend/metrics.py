from typing import List, Dict

import evaluate
import numpy as np
import pandas as pd
from tqdm import tqdm

rouge = evaluate.load("rouge")
bleu = evaluate.load("bleu")
chrf = evaluate.load("chrf")
bertscore = evaluate.load("bertscore")

def context_recall(ground_truth: str, contexts: List[str])->float:
    """
    Calc rouge btw contexts and ground truth.
    Interpretation: ngram match (recall) btw contexts and desired answer.

    ROUGE - https://huggingface.co/spaces/evaluate-metric/rouge

    return: average rouge for all contexts.
    """
    rs = []
    for c in contexts:
        rs.append(
            rouge.compute(
                predictions=[str(c)],
                references=[str(ground_truth)],
            )["rouge2"]
        )

    return np.mean(rs)


def context_precision(ground_truth: str, contexts: List[str])->float:
    """
    Calc blue btw contexts and ground truth.
    Interpretation: ngram match (precision) btw contexts and desired answer.

    BLEU - https://aclanthology.org/P02-1040.pdf
    max_order - max n-grams to count

    return: average bleu (precision2, w/o brevity penalty) for all contexts.
    """
    bs = []
    for c in contexts:

        try:
            bs.append(
                bleu.compute(
                    predictions=[str(c)],
                    references=[str(ground_truth)],
                    max_order=2,
                )["precisions"][1]
            )
        except ZeroDivisionError:
            bs.append(0)

    return np.mean(bs)


def answer_correctness_literal(
    ground_truth: str,
    answer: str,
    char_order: int = 6,
    word_order: int = 2,
    beta: float = 1,
)->float:
    """
    Calc chrF btw answer and ground truth.
    Interpretation: lingustic match btw answer and desired answer.

    chrF - https://aclanthology.org/W15-3049.pdf
    char_order - n-gram length for chars, default is 6 (from the article)
    word_order - n-gram length for words (chrF++), default is 2 (as it outperforms simple chrF)
    beta - recall weight, beta=1 - simple F1-score

    return: chrF for answ and gt.
    """

    score = chrf.compute(
        predictions=[str(answer)],
        references=[str(ground_truth)],
        word_order=word_order,
        char_order=char_order,
        beta=beta,
    )["score"]

    return score


def answer_correctness_neural(
    ground_truth: str,
    answer: str,
    model_type: str = "cointegrated/rut5-base",
) -> float:
    """
    Calc bertscore btw answer and ground truth.
    Interpretation: semantic cimilarity btw answer and desired answer.

    BertScore - https://arxiv.org/pdf/1904.09675.pdf
    model_type - embeds model  (default t5 as the best from my own research and experience)

    return: bertscore-f1 for answ and gt.
    """

    score = bertscore.compute(
        predictions=[str(answer)],
        references=[str(ground_truth)],
        batch_size=1,
        model_type=model_type,
        num_layers=11,
    )["f1"]

    return score


def contextual_relevance(ground_truth: str, contexts: List[str])->float:
    """
    Оценка релевантности извлеченного контекста к правильному ответу.
    
    - ROUGE-2: n-граммное совпадение (важно для точных фраз)
    - BLEU-2: precision-похожесть (оценивает точные совпадения)
    - chrF: n-граммы символов (устойчив к небольшим вариациям)
    - BERTScore: семантическая схожесть (учитывает смысл)
    """

    
    bleu_scores = []

    for context in contexts:
        # BLEU-2 (Precision-based)
        bleu_score = bleu.compute(predictions=[context], references=[ground_truth], max_order=2)["bleu"]
        bleu_scores.append(bleu_score)


    # Усредняем значения по всем retrieved contexts
    return {
        "BLEU-2": np.mean(bleu_scores)
    }

def logical_consistency_using_bertscore(
    context: str,
    answer: str,
    model_type: str = "bert-base-uncased",
) -> float:
    """
    Оценка логической согласованности ответа с контекстом через BertScore.
    Предполагается, что высокая схожесть (близость эмбеддингов) указывает на логическую согласованность.

    Параметры:
    context (str): Контекст или вопрос.
    answer (str): Ответ.
    model_type (str): Модель для эмбеддингов (по умолчанию 'bert-base-uncased').

    Возвращает:
    float: Оценка логической согласованности.
    """
    score = bertscore.compute(
        predictions=[str(answer)],
        references=[str(context)],
        model_type=model_type,
    )["f1"]

    return score[0]  # Возвращаем первый элемент из списка (поскольку у нас только одна пара)

def evaluate_consistency(
    df: pd.DataFrame,
    model_type: str = "bert-base-uncased",
) -> pd.DataFrame:
    """
    Оценка логической согласованности для всего датасета.

    Параметры:
    df (pd.DataFrame): Датасет с колонками 'context' и 'answer'.
    model_type (str): Модель для BertScore.

    Возвращает:
    pd.DataFrame: Датасет с логической согласованностью для каждой строки.
    """
    consistency_scores = []

    # Проход по всем строкам датасета
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Evaluating logical consistency"):
        context = row['context']
        answer = row['answer']
        score = logical_consistency_using_bertscore(context, answer, model_type)
        consistency_scores.append(score)
    
    df['logical_consistency'] = consistency_scores
    return df

# Пример использования с датасетом
data = {
    'context': [
        "The sun rises in the east.",
        "The Earth is the third planet from the sun.",
        "Water boils at 100 degrees Celsius at sea level."
    ],
    'answer': [
        "The sun rises in the west.",
        "Earth is the third planet from the sun.",
        "Water boils at 80 degrees Celsius."
    ]
}

df = pd.DataFrame(data)
result_df = evaluate_consistency(df)

# Выводим результат
print(result_df[['context', 'answer', 'logical_consistency']])


class ValidatorSimple:
    """
    Расчет простых метрик качества для заданного датасета.
    """
    def __init__(
        self,
        neural: bool = False,
    ):
        """
        param neural: есть гпу или нет. По дефолту ее нет(
        """
        self.neural = neural

    def score_sample(
        self,
        answer: str,
        ground_truth: str,
        context: List[str],
    ):
        """
        Расчет для конкретного сэмпла в тестовом датасете.
        """
        scores = {}
        scores["context_recall"] = [
            context_recall(
                ground_truth,
                context,
            )
        ]
        scores["context_precision"] = [
            context_precision(
                ground_truth,
                context,
            )
        ]
        scores["answer_correctness_literal"] = [
            answer_correctness_literal(
                ground_truth=ground_truth,
                answer=answer,
            )
        ]
        if self.neural:
            scores["answer_correctness_neural"] = [
                answer_correctness_neural(
                    ground_truth=ground_truth,
                    answer=answer,
                )
            ]
        return scores

    def validate_rag(
        self,
        test_set: pd.DataFrame,
    ):
        """
        param test_set: пандас датасет с нужными полями: answer, ground_truth, context, question
        """

        res = {}
        for _, row in tqdm(test_set.iterrows(), "score_sample"):
            gt = row.ground_truth
            answer = row.answer
            context = row.contexts

            scores = self.score_sample(answer, gt, context)

            if not res:
                res = scores
            else:
                for k, v in scores.items():
                    res[k].extend(v)
        for k, v in res.items():
            res[k] = np.mean(res[k])
        return res
    
    def validate_rag_new(self, test_set: pd.DataFrame):
        res = []
        for _, row in tqdm(test_set.iterrows(), "score_sample"):
            gt = row.ground_truth
            answer = row.answer
            context = row.contexts

            res.append(self.score_sample(answer, gt, context))

        return res