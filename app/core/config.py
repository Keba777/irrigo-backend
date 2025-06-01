import os
from dotenv import load_dotenv

load_dotenv()

raw_url = os.getenv("DATABASE_URL", "")
# Replace every literal "\x3a" with ":" so SQLAlchemy can parse it
fixed_url = raw_url.replace("\\x3a", ":")
# If you also see uppercase X like "\X3A", you could do:
# fixed_url = re.sub(r"\\[xX]3[Aa]", ":", raw_url)


class Settings:
    PROJECT_NAME: str = "Irrigo"
    # Use the fixed, un-escaped version
    SQLALCHEMY_DATABASE_URI: str = fixed_url


settings = Settings()
print("Database URL:", repr(settings.SQLALCHEMY_DATABASE_URI))

# … pass settings.SQLALCHEMY_DATABASE_URI into create_engine(…) or FastAPI’s
# database setup as usual.
