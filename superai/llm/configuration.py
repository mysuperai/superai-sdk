import abc
import os

from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)


class Singleton(abc.ABCMeta, type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):
    def __init__(self, autonomous=False, autonomous_limit=10, debug=False) -> None:
        self.autonomous = autonomous
        self.autonomous_limit = autonomous_limit
        self.debug = debug

        self.open_ai_api_key = os.getenv("OPENAI_API_KEY")
        self.smart_foundation_model_engine = os.getenv("SMART_FOUNDATION_MODEL", "gpt-4")
        self.fast_foundation_model_engine = os.getenv("FAST_FOUNDATION_MODEL", "gpt-3.5-turbo")
        self.embedding_model_engine = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_region = os.getenv("PINECONE_ENV")
        self.embedding_dimension = os.getenv("EMBEDDING_DIMENSION", 1536)
        self.memory_index = os.getenv("MEMORY_INDEX", "super_llm")
        self.memory_backend = os.getenv("MEMORY_BACKEND", "local")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID")
        self.custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.bing_subscription_key = os.getenv("BING_SUBSCRIPTION_KEY")
        self.bing_search_url = os.getenv("BING_SEARCH_URL")
        self.serp_api_key = os.getenv("SERP_API_KEY")
        self.wolfram_alpha_appid = os.getenv("WOLFRAM_ALPHA_APPID")

        self.user_agent = os.getenv(
            "USER_AGENT",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        )

    def set_autonomous(self, autonomous: bool) -> None:
        self.autonomous = autonomous

    def set_autonous_limit(self, autonomous_limit: int) -> None:
        self.autonomous_limit = autonomous_limit

    def set_open_ai_api_key(self, open_ai_api_key: str) -> None:
        self.open_ai_api_key = open_ai_api_key

    def set_debug(self, debug: bool) -> None:
        self.debug = debug


def check_api_keys() -> None:
    config = Configuration()
    if config.open_ai_api_key:
        config.smart_foundation_model.check_api_key(config.open_ai_api_key)
        config.fast_foundation_model.check_api_key(config.open_ai_api_key)
    else:
        raise Exception("OpenAI API Key is not set")

    if config.pinecone_api_key or config.pinecone_region:
        if config.pinecone_region:
            if config.pinecone_api_key:
                import pinecone

                pinecone.init(api_key=config.pinecone_api_key, environment=config.pinecone_region)
            else:
                raise Exception("Pinecone API Key is not set")
        else:
            raise Exception("Pinecone region is not set")

    if config.google_api_key or config.google_cse_id:
        if config.google_api_key and config.google_cse_id:
            try:
                from googleapiclient.discovery import build

                service = build("customsearch", "v1", developerKey=config.google_api_key)

            except ImportError:
                raise ImportError(
                    "google-api-python-client is not installed. "
                    "Please install it with `pip install google-api-python-client`"
                )
        else:
            raise Exception("Google API Key or Google CSE ID is not set")


def create_configuration() -> None:
    pass
