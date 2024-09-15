import logging
import functools
import torch
from embeddings.config import settings


def configure_logging(level=logging.INFO):
    """Configure logging
    :param level: Logging level
    """
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s: %(levelname)-7s - %(message)s",
    )
    return


LOGGER = logging.getLogger()
configure_logging()


@functools.lru_cache(maxsize=1)
def get_total_vram(device_index=0):
    """
    Get the total VRAM of the GPU.

    :param device_index: Index of the GPU device (default is 0)
    :return: Total VRAM in MB
    """
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available")

    device_properties = torch.cuda.get_device_properties(device_index)
    total_vram = device_properties.total_memory / 1024**2  # Convert bytes to MB
    return total_vram


def cuda_cache_manager():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if (
                torch.cuda.memory_reserved(settings.device_index)
                / 1024**2
                * get_total_vram(settings.device_index)
                > 0.4
            ):
                logging.info(
                    f"Starting cache clear: current memory usage: {torch.cuda.memory_reserved(settings.device) / 1024**2} MB"
                )
                torch.cuda.empty_cache()
                LOGGER.info("Cache cleared")
            return result

        return wrapper

    return decorator
