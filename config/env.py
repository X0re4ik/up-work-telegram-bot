from dotenv import load_dotenv, dotenv_values

load_dotenv()
ENV = dotenv_values()
print(ENV)