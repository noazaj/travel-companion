from openai import OpenAI
# import dotenv
# dotenv.dotenv_values('../../.ENV').get('API_KEY')


class Client():

    def __init__(self) -> None:
        # print(os.getenv('API_KEY'))
        self.client = OpenAI(
            api_key='',
            organization=None,
            project=None,
            base_url=None,
            timeout=None,
            max_retries=0,
            default_headers=None,
            default_query=None,
            http_client=None,
        )

    def getClient(self) -> OpenAI:
        return self.client
