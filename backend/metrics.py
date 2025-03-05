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

    print('calculated ctx recall')
    return np.mean(rs)


def context_precision(ground_truth: str, contexts: List[str])->float:
    """
    Calc blue btw contexts and ground truth.
    Interpretation: ngram match (precision) btw contexts and desired answer.

    BLEU - https://aclanthology.org/P02-1040.pdf
    max_order - max n-grams to count

    return: average bleu (precision2, w/o brevity penalty) for all contexts.
    Чисто совпадение слов
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

    print('calculated ctx prec')
    return np.mean(bs)

def context_relevance(ground_truth: str, contexts: List[str]) -> float:
    """
    Оценка релевантности извлеченного контекста к правильному ответу с помощью BERTScore.
    
    - BERTScore: оценивает семантическую схожесть на уровне эмбеддингов.
    Совпадение по смыслу
    """
    bert_scores = []
    
    for context in contexts:
        score = bertscore.compute(
            predictions=[context],
            references=[ground_truth],
            model_type="bert-base-uncased"  # Можно выбрать другую предобученную модель
        )["f1"][0]  # Берем F1-оценку из результата
        bert_scores.append(score)

    print('calculated ctx relev')

    return np.mean(bert_scores)


def answer_correctness_literal(
    ground_truth: str,
    answer: str,
    char_order: int = 6,
    word_order: int = 2,
    beta: float = 1,
):
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

    print('calculated acl')

    return score/100


def answer_correctness_neural(
    ground_truth: str,
    answer: str,
    model_type: str = "cointegrated/rut5-base",
):
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
    )["f1"][0]

    print('calculated acn')

    return score

def logical_consistency_using_bertscore(
    context: str,
    answer: str,
    model_type: str = "distilbert-base-uncased",
):
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
    )["f1"][0]

    print('calculated log cons')

    return score

def document_fidelity(answer: str, contexts: List[str]):
    fidelity_scores = []
    
    for context in contexts:
        # Вычисляем ROUGE-1 между ответом и каждым документом
        score = rouge.compute(
            predictions=[answer],
            references=[context],
        )["rouge1"]  # Используем ROUGE-1 вместо ROUGE-2
        fidelity_scores.append(score)

    print('Calculated Document Fidelity (ROUGE-1)')
    
    # Возвращаем среднее значение ROUGE-1
    return np.mean(fidelity_scores) if fidelity_scores else 0.0

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

        scores["context_relevance"]=[
            context_relevance(
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

        scores["document_fidelity"]=[
            document_fidelity(
                answer,
                context,
            )
        ]

        scores["logical_consistency"]=[
            logical_consistency_using_bertscore(
                context,
                answer,
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
    
    def validate_rag_new(self, test_set: pd.DataFrame, weigths: Dict = {}):
        CR_weigth = weigths.get('CR', 0.4)
        DF_weigth = weigths.get('DF', 0.2)
        LAC_weigth = weigths.get('LAC', 0.4)

        res = []
        for _, row in tqdm(test_set.iterrows(), "score_sample"):
            ground_truth = row.ground_truth
            answer = row.answer
            context = row.contexts

            score = self.score_sample(answer, ground_truth, context)
            score['Deception Probability'] = (CR_weigth * score['context_relevance'] + DF_weigth * score['document_fidelity'] + 
                                              LAC_weigth * score['answer_correctness_literal']) / (CR_weigth + DF_weigth + LAC_weigth) * (score['answer_correctness_neural'] * score['logical_consistency'])

            res.append(score)

        return res
    
    # для расчёта метрик всего сета
    def calc_new_metrics_for_row(self, row: Dict, weights: Dict = {}) -> Dict:
        CR_weigth = weights.get('CR', 0.4)
        DF_weigth = weights.get('DF', 0.3)
        LAC_weigth = weights.get('LAC', 0.3)

        ground_truth = row['ground_truth']
        answer = row['answer']
        context = row['contexts']

        bad_score = self.score_sample(answer, ground_truth, context)

        score = {key: float(value[0]) for key, value in bad_score.items()}

        score['Deception Probability'] = 1 - ((CR_weigth * score['context_relevance'] + DF_weigth * score['document_fidelity'] + 
                                            LAC_weigth * score['answer_correctness_literal']) / (CR_weigth + DF_weigth + LAC_weigth) * (score['answer_correctness_neural'] * score['logical_consistency']))
        
        return score