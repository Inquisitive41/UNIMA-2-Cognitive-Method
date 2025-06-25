import networkx as nx
import logging
from core.hypothesis_generator import HypothesisGenerator
from core.evaluator import HypothesisEvaluator
from core.adapter import HypothesisAdapter
from visual.graph_builder import GraphBuilder
from visual.explainer import Explainer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def predict(hypotheses, x):
    best = max(hypotheses, key=lambda h: h["score"], default=None)
    if best:
        try:
            return best["rule"].split("то ")[1].strip()
        except Exception as e:
            logging.error(f"Ошибка при предсказании: {e}")
            return "Неизвестно"
    return "Неизвестно"


if __name__ == "__main__":
    graph = nx.Graph()
    generator = HypothesisGenerator(graph)
    evaluator = HypothesisEvaluator()
    adapter = HypothesisAdapter()
    visualizer = GraphBuilder(graph)
    explainer = Explainer(graph)

    examples = [
        ({"color": "red", "shape": "circle"}, "A"),
        ({"color": "green", "shape": "square"}, "A"),
    ]
    hypotheses = generator.generate(examples)
    for hyp in hypotheses:
        evaluator.evaluate(hyp, examples)
    new_x = {"color": "green", "shape": "circle"}
    adapter.adapt(hypotheses, new_x, "A", 1, lambda x: predict(hypotheses, x))
    prediction = predict(hypotheses, new_x)
    print(prediction)
    print(explainer.explain(new_x, prediction, hypotheses))
    visualizer.visualize()
