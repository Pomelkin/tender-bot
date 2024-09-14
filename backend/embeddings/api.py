import litserve as ls
import torch
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
        self.warm_up()

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
        """
        encoded_input = self.tokenizer(
            x, padding=True, truncation=True, return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        return model_output[0][:, 0].tolist()

    def encode_response(self, output, **kwargs) -> dict:
        """
        Encode embedding output.
        """
        embeddings = []
        for index, embedding in enumerate(output):
            embeddings.append(Embedding(index=index, embedding=embedding.tolist()))

        return EmbeddingsResponse(
            data=embeddings, model=settings.model_name
        ).model_dump()
