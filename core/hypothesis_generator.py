import logging
from typing import List, Dict, Any, Tuple
import networkx as nx


class HypothesisGenerator:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.hypotheses: List[Dict[str, Any]] = []

    def generate(
        self, examples: List[Tuple[Dict[str, Any], str]]
    ) -> List[Dict[str, Any]]:
        for x, y in examples:
            for k, v in x.items():
                self.graph.add_edge(f"{k}:{v}", y)
            rule = f"Если {', '.join(list(x.keys()))} присутствуют, то {y}"
            self.hypotheses.append({"rule": rule, "score": 0.0})
        logging.info(f"Сгенерировано гипотез: {len(self.hypotheses)}")
        return self.hypotheses
