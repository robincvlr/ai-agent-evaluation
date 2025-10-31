from src.evaluator import AzureEvaluatorPipeline


def test_evaluator_from_sample():
    sample_data = {
        "input": "The assistant should summarize this text.",
        "output": "Here is a short summary of your content.",
    }
    pipeline = AzureEvaluatorPipeline()
    evaluation_results = pipeline.evaluate(sample_data)
