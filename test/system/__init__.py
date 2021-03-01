import base64


TIME_OUT = 10

TEST_USER = "test1"
TEST_USER_PASSWORD = "1tset"
AUTH_STRING = (
    (base64.encodebytes(f"{TEST_USER}:{TEST_USER_PASSWORD}".encode()))
    .rstrip()
    .decode("utf-8")
)

HOST = "http://127.0.0.1:8000"

DOI = "10.5286/TEST.24014237"

DATA_DIR = "../data"
