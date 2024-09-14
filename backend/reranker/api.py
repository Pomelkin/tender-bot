import litserve as ls
import torch
from reranker.schemas import RerankerRequest
from reranker.config import settings
from reranker.utils import LOGGER
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class CrossEncoderAPI(ls.LitAPI):
    def setup(self, device: str):
        """
        Load the cross-encoder model, tokenizer, and warm up the model.

        :param device: device to run the model on.
        """
        self.model = AutoModelForSequenceClassification.from_pretrained(
            settings.model_name
        ).to(device)
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
        features = self.tokenizer(
            [
                "как часто нужно ходить к стоматологу?",
                "как часто нужно ходить к стоматологу?",
            ],
            [
                "Минимальный обязательный срок посещения зубного врача – раз в год, но специалисты рекомендуют делать это чаще – раз в полгода, а ещё лучше – раз в квартал. При таком сроке легко отследить любые начинающиеся проблемы и исправить их сразу же.",
                "Дядя Женя работает врачем стоматологом",
            ],
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(self.device)
        with torch.no_grad():
            _ = self.model(**features).logits

    def decode_request(self, request: RerankerRequest, **kwargs) -> dict:
        """
        Decode the request payload to the model input.

        :param request: request payload.
        :return: model input.
        """
        return request.model_dump()

    def predict(self, x, **kwargs) -> list[str]:
        """
        Run the model on the input and return the output.

        :param x: model input.
        :return: reranked documents.
        """
        features = self.tokenizer(
            x["query"] * len(x["documents"]),
            x["documents"],
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512,
        ).to(self.device)
        with torch.no_grad():
            scores = torch.sigmoid(self.model(**features).logits).squeeze().tolist()

        best_docs = []
        best_score = 0
        best_doc = ""

        # filter out documents with score below the threshold
        for score, doc in zip(scores, x["documents"]):
            if score >= settings.rerank_threshold:
                best_docs.append(doc)
            if score > best_score:
                best_doc = doc
                best_score = score
        # If no documents are above the threshold, return the best document
        if len(best_docs) == 0 and best_doc != "":
            best_docs.append(best_doc)

        return best_docs

    def encode_response(self, output, **kwargs):
        """
        Encode the reranked documents.

        :param output: model output.
        :return: response payload.
        """
        return {"documents": output}


if __name__ == "__main__":
    api = CrossEncoderAPI()
    server = ls.LitServer(
        api,
        api_path="/v1/reranker",
        accelerator="gpu",
        devices=[settings.device_index],
    )
    server.run(
        port=settings.api.port,
    )
