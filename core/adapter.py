import logging
from typing import List, Dict, Any


class HypothesisAdapter:
    def adapt(
        self,
        hypotheses: List[Dict[str, Any]],
        x: Dict[str, Any],
        y: str,
        feedback: int,
        predict_func,
    ) -> None:
        pred = predict_func(x)
        reward = 1.0 if pred == y else -1.0
        for hyp in hypotheses:
            if feedback < 0:
                hyp["score"] = max(0, hyp["score"] + reward * 0.01)
        logging.info(f"Адаптация завершена. Feedback: {feedback}, Reward: {reward}")
