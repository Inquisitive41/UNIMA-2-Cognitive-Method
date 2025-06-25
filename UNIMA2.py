import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class UNIMA2:
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.hypotheses: List[Dict[str, Any]] = []
        self.weights = defaultdict(float)

    def generate_hypotheses(self, examples: List[Tuple[Dict[str, Any], str]]) -> None:
        for x, y in examples:
            for k, v in x.items():
                self.graph.add_edge(f"{k}:{v}", y)
            rule = f"Если {', '.join(list(x.keys()))} присутствуют, то {y}"
            self.hypotheses.append({"rule": rule, "score": 0.0})
        logging.info(f"Сгенерировано гипотез: {len(self.hypotheses)}")

    def evaluate_hypotheses(
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

    def _count_features(self, rule_text: str) -> int:
        # "Если color, shape присутствуют, то A" -> [color, shape]
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

    def adapt(self, x: Dict[str, Any], y: str, feedback: int) -> None:
        pred = self.predict(x)
        reward = 1.0 if pred == y else -1.0
        for hyp in self.hypotheses:
            if feedback < 0:
                hyp["score"] = max(0, hyp["score"] + reward * 0.01)
        logging.info(f"Адаптация завершена. Feedback: {feedback}, Reward: {reward}")

    def predict(self, x: Dict[str, Any]) -> str:
        best = max(self.hypotheses, key=lambda h: h["score"], default=None)
        if best:
            try:
                return best["rule"].split("то ")[1].strip()
            except Exception as e:
                logging.error(f"Ошибка при предсказании: {e}")
                return "Неизвестно"
        return "Неизвестно"

    def explain(self, x: Dict[str, Any]) -> str:
        prediction = self.predict(x)
        return f"Предсказание: {prediction}. Граф: {nx.to_dict_of_lists(self.graph)}"

    def visualize(self) -> None:
        try:
            pos = nx.spring_layout(self.graph)
            nx.draw(
                self.graph,
                pos,
                with_labels=True,
                node_color="lightgreen",
                node_size=700,
            )
            plt.title("Граф гипотез UNIMA-2")
            plt.show()
        except Exception as e:
            logging.error(f"Ошибка визуализации: {e}")


# Пример использования
if __name__ == "__main__":
    unima2 = UNIMA2()
    examples = [
        ({"color": "red", "shape": "circle"}, "A"),
        ({"color": "green", "shape": "square"}, "A"),
    ]
    unima2.generate_hypotheses(examples)
    for hyp in unima2.hypotheses:
        unima2.evaluate_hypotheses(hyp, examples)
    new_input = {"color": "green", "shape": "circle"}
    unima2.adapt(new_input, "A", 1)
    print(unima2.predict(new_input))
    print(unima2.explain(new_input))
    unima2.visualize()
