class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///DepartmentComputerNetworkProgramming.db"

    JWT_SECRET_KEY = "secret"
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = "leo20020529@gmail.com"
    MAIL_PASSWORD = "mxyp vfsm wpnw ydsu"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


