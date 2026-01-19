import os
from dotenv import load_dotenv

load_dotenv(override=True)


METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")
if __name__ == "__main__":
    print(os.getenv("METAPHOR_API_KEY"))