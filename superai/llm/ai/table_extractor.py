from superai.llm.ai import LLM


class TableExtractor(LLM):
    def train(
        self,
        data,
        prompt=None,
        max_prompt_size=None,
        reduce_prompt_size=False,
        improve_prompt=False,
        parallelize=True,
        n_models=3,
        max_iterations=10,
        cross_validation=False,
    ):
        # add prompt trainer
        pass

    def train(self):
        raise NotImplementedError

    def fine_tune(self, data):
        raise NotImplementedError

    def score(self, data):
        # Score the AI foundation_model on the test data
        pass
