from huggingface_hub import HfApi
from loguru import logger

from src.domain.repository import ModelRepository


class HuggingfaceModelRepository(ModelRepository):
    def __init__(
        self,
        huggingface_hub_client: HfApi,
    ) -> None:
        self.huggingface_hub_client = huggingface_hub_client

    def download_model(
        self,
        model_id: str,
    ) -> None:
        path = self.huggingface_hub_client.snapshot_download(
            repo_id=model_id,
        )
        logger.info(path)
