import logging
from typing import List, Dict, Any, Tuple


class HypothesisEvaluator:
    def _count_features(self, rule_text: str) -> int:
        try:
            features = (
                rule_text.split("Если")[1].split("присутствуют")[0].strip().split(",")
            )
            return len([f for f in features if f.strip()])
        except Exception as e:
            logging.error(f"Ошибка при подсчёте признаков: {e}")
            return 1

    def _matches(self, x: Dict[str, Any], rule_text: str) -> bool:
        try:
            features = (
                rule_text.split("Если")[1].split("присутствуют")[0].strip().split(",")
            )
            return all(f.strip() in x for f in features if f.strip())
        except Exception as e:
            logging.error(f"Ошибка при сопоставлении: {e}")
            return False

    def evaluate(
        self, hypothesis: Dict[str, Any], examples: List[Tuple[Dict[str, Any], str]]
    ) -> None:
        coverage = sum(1 for x, y in examples if self._matches(x, hypothesis["rule"]))
        complexity = self._count_features(hypothesis["rule"])
        energy = complexity * 5 if complexity > 0 else 1
        generality = 0.9
        hypothesis["score"] = (
            (coverage * generality) / (complexity * energy) if complexity > 0 else 0.0
        )
        logging.info(
            f"Оценена гипотеза: {hypothesis['rule']} | Score: {hypothesis['score']:.4f}"
        )
