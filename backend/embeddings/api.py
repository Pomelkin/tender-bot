import litserve as ls
import torch
from embeddings.utils import LOGGER
from embeddings.schemas import EmbeddingsRequest, Embedding, EmbeddingsResponse
from embeddings.config import settings
from transformers import AutoTokenizer, AutoModel


class EmbeddingsAPI(ls.LitAPI):
    def setup(self, device: str):
        """
        Load the embedding model and tokenizer, also warm up the model.

        :param device: device to run the model on.
        """
        self.model = AutoModel.from_pretrained(settings.model_name).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
        self.device = device

        self.model.eval()

        LOGGER.info(f"Warmup the model {settings.model_name}")
        self.warm_up()
        LOGGER.info(f"Model {settings.model_name} is ready to serve")

    def warm_up(self) -> None:
        """
        Warm up the model by running a dummy input.
        """
        input_texts = [
            "Когда был спущен на воду первый миноносец «Спокойный»?",
            "Есть ли нефть в Удмуртии?",
            "Спокойный (эсминец)\nЗачислен в списки ВМФ СССР 19 августа 1952 года.",
            "Нефтепоисковые работы в Удмуртии были начаты сразу после Второй мировой войны в 1945 году и продолжаются по сей день. Добыча нефти началась в 1967 году.",
        ]
        encoded_input = self.tokenizer(
            input_texts, padding=True, truncation=True, return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            _ = model_output[0][:, 0]
        return

    def decode_request(self, request: EmbeddingsRequest, **kwargs) -> list:
        """
        Decode the request payload to the model input.

        :param request: request payload.
        :return: model input.
        """
        if isinstance(request.input, str):
            request.input = [request.input]
        return request.input

    def predict(self, x, **kwargs):
        """
        Run the model on the input and return the output.

        :param x: model input.
        :return: model output.
        """
        encoded_input = self.tokenizer(
            x, padding=True, truncation=True, return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        return model_output[0][:, 0]

    def encode_response(self, output, **kwargs) -> dict:
        """
        Encode embedding output.

        :param output: model output.
        :return: response payload.
        """
        embeddings = []
        for index, embedding in enumerate(output):
            embeddings.append(Embedding(index=index, embedding=embedding.tolist()))

        return EmbeddingsResponse(
            data=embeddings, model=settings.model_name
        ).model_dump()


if __name__ == "__main__":
    api = EmbeddingsAPI()
    server = ls.LitServer(
        api,
        api_path="/v1/embeddings",
        accelerator="gpu",
        devices=[settings.device_index],
    )
    server.run(
        port=settings.api.port,
    )
