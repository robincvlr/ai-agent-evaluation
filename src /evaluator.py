import os
import json
from typing import Dict, Any, Type
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential


from azure.ai.evaluation import (
    IntentResolutionEvaluator,
    TaskAdherenceEvaluator,
    ToolCallAccuracyEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    CodeVulnerabilityEvaluator,
    ContentSafetyEvaluator,
    IndirectAttackEvaluator,
    FluencyEvaluator,
)

load_dotenv()


class AzureModelConfig:
    """Represents configuration for an Azure AI model deployment."""

    def __init__(self, deployment: str, api_key: str, endpoint: str, version: str):
        self.azure_deployment = deployment
        self.api_key = api_key
        self.azure_endpoint = endpoint
        self.api_version = version

    @classmethod
    def from_env(cls, deployment_env: str = "AZURE_DEPLOYMENT_NAME") -> "AzureModelConfig":
        """Create config from environment variables."""
        return cls(
            deployment=os.getenv(deployment_env),
            api_key=os.getenv("AZURE_API_KEY"),
            endpoint=os.getenv("AZURE_ENDPOINT"),
            version=os.getenv("AZURE_API_VERSION"),
        )

    def as_dict(self) -> Dict[str, Any]:
        """Return a dict representation of the model config."""
        return {
            "azure_deployment": self.azure_deployment,
            "api_key": self.api_key,
            "azure_endpoint": self.azure_endpoint,
            "api_version": self.api_version,
        }


class AzureEvaluatorPipeline:
    """
    Handles initialization and execution of multiple Azure AI evaluators.
    Designed for use in agentic and reasoning model workflows.
    """

    def __init__(self):
        self.model_config = AzureModelConfig.from_env()
        self.reasoning_model_config = AzureModelConfig(
            deployment="o3-mini",
            api_key=os.getenv("AZURE_API_KEY"),
            endpoint=os.getenv("AZURE_ENDPOINT"),
            version=os.getenv("AZURE_API_VERSION"),
        )
        self.azure_ai_project = os.getenv("AZURE_AI_PROJECT")

        self.quality_evaluators = self._init_quality_evaluators()
        self.safety_evaluators = self._init_safety_evaluators()
        self.all_evaluators = {**self.quality_evaluators, **self.safety_evaluators}

    def _init_quality_evaluators(self) -> Dict[str, Any]:
        """Initialize quality evaluators (reasoning + general)."""
        reasoning_evaluators = [
            IntentResolutionEvaluator,
            TaskAdherenceEvaluator,
            ToolCallAccuracyEvaluator,
        ]
        general_evaluators = [CoherenceEvaluator, FluencyEvaluator, RelevanceEvaluator]

        evaluators = {
            cls.__name__: cls(model_config=self.reasoning_model_config.as_dict(), is_reasoning_model=True)
            for cls in reasoning_evaluators
        }
        evaluators.update({
            cls.__name__: cls(model_config=self.model_config.as_dict())
            for cls in general_evaluators
        })
        return evaluators

    def _init_safety_evaluators(self) -> Dict[str, Any]:
        """Initialize safety evaluators."""
        safety_classes = [ContentSafetyEvaluator, IndirectAttackEvaluator, CodeVulnerabilityEvaluator]
        return {
            cls.__name__: cls(azure_ai_project=self.azure_ai_project, credential=DefaultAzureCredential())
            for cls in safety_classes
        }

    def evaluate(self, converted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all evaluators on the provided data.
        """
        results = {}
        for name, evaluator in self.all_evaluators.items():
            print(f"Running evaluator: {name}")
            result = evaluator(**converted_data)
            results[name] = result
            print(json.dumps(result, indent=4))
        return results
