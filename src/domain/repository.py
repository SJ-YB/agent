from abc import ABC, abstractmethod


class ModelRepository(ABC):
    @abstractmethod
    def download_model(
        self,
        model_id: str,
    ) -> None:
        raise NotImplementedError
