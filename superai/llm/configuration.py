import abc

from superai.config import settings


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

        self.openai_api_type = settings.get("llm").get("chatgpt").get("openai_api_type")
        self.openai_api_base = settings.get("llm").get("chatgpt").get("openai_api_base")
        self.openai_api_version = settings.get("llm").get("chatgpt").get("openai_api_version")
        self.open_ai_api_key = settings.get("llm").get("chatgpt").get("openai_api_key")
        self.smart_foundation_model_engine = settings.get("llm").get("chatgpt").get("smart_foundation_model_engine")
        self.fast_foundation_model_engine = settings.get("llm").get("chatgpt").get("fast_foundation_model_engine")
        self.embedding_model_engine = settings.get("llm").get("chatgpt").get("embedding_model_engine")
        self.pinecone_api_key = settings.get("llm").get("memory").get("pinecone_api_key")
        self.pinecone_region = settings.get("llm").get("memory").get("pinecone_region")
        self.embedding_dimension = settings.get("llm").get("memory").get("embedding_dimension")
        self.memory_index = settings.get("llm").get("memory").get("memory_index")
        self.memory_backend = settings.get("llm").get("memory").get("memory_backend")
        self.google_api_key = settings.get("llm").get("agents").get("google_api_key")
        self.google_cse_id = settings.get("llm").get("agents").get("google_cse_id")
        self.custom_search_engine_id = settings.get("llm").get("agents").get("custom_search_engine_id")
        self.serper_api_key = settings.get("llm").get("agents").get("serper_api_key")
        self.bing_subscription_key = settings.get("llm").get("agents").get("bing_subscription_key")
        self.bing_search_url = settings.get("llm").get("agents").get("bing_search_url")
        self.serp_api_key = settings.get("llm").get("agents").get("serp_api_key")
        self.wolfram_alpha_appid = settings.get("llm").get("agents").get("wolfram_alpha_appid")

        self.user_agent = settings.get("llm").get("agents").get("user_agent")

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
