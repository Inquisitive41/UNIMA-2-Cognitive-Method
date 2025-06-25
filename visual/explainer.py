import networkx as nx
import logging
from typing import Dict, Any, List


class Explainer:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def explain(
        self, x: Dict[str, Any], prediction: str, hypotheses: List[Dict[str, Any]]
    ) -> str:
        try:
            return f"Предсказание: {prediction}. Граф: {nx.to_dict_of_lists(self.graph)}. Гипотезы: {[h['rule'] for h in hypotheses]}"
        except Exception as e:
            logging.error(f"Ошибка объяснения: {e}")
            return "Ошибка объяснения"
