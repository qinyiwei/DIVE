from .vllm_model import VLLMModel
from .api_model import APIModel
from .hf_model import HuggingFaceModel

Models = {
    'vllm': VLLMModel,
    'api': APIModel,
    'hf': HuggingFaceModel,
}