import networkx as nx
import matplotlib.pyplot as plt
import logging


class GraphBuilder:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def visualize(self, title: str = "Граф гипотез UNIMA-2") -> None:
        try:
            pos = nx.spring_layout(self.graph)
            nx.draw(
                self.graph,
                pos,
                with_labels=True,
                node_color="lightgreen",
                node_size=700,
                font_size=12,
            )
            plt.title(title)
            plt.show()
        except Exception as e:
            logging.error(f"Ошибка визуализации: {e}")
