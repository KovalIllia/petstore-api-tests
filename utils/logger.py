import os
import datetime


class LogLevel:
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Logger:

    LOG_DIR = "./output/logs"

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    file_name = (
        f"{LOG_DIR}/log_"
        + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        + ".log"
    )

    @classmethod
    def write_log_to_file(cls, data: str, level: str = LogLevel.INFO):
        if "test_result" in cls.file_name:
            raise ValueError(
                "Logger is trying to write to test_result. Check configuration!"
            )
        with open(cls.file_name, "a", encoding="utf-8") as logger_file:
            log_line = f"[{level}] {datetime.datetime.now()} - {data}\n"
            logger_file.write(log_line)

    @classmethod
    def info(cls, message: str):
        cls.write_log_to_file(message, level=LogLevel.INFO)

    @classmethod
    def debug(cls, message: str):
        cls.write_log_to_file(message, level=LogLevel.DEBUG)

    @classmethod
    def warning(cls, message: str):
        cls.write_log_to_file(message, level=LogLevel.WARNING)

    @classmethod
    def error(cls, message: str):
        cls.write_log_to_file(message, level=LogLevel.ERROR)

    @classmethod
    def add_request(cls, url: str, method: str, body: None, files_meta=None):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = f"\n-----\n"
        data_to_add += f"Test:  {test_name}\n"
        data_to_add += f"Time:  {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method:  {method}\n"
        data_to_add += f"Request URL:  {url}\n"
        data_to_add += "\n"
        if body is not None:
            data_to_add += f"Request body: {body}\n"

        data_to_add += "\n"
        cls.debug(data_to_add)

    @classmethod
    def add_response(
        cls, response, body=None, endpoint_name: str = None, files_meta=None
    ):
        data_to_add = ""
        if endpoint_name:
            data_to_add += f"Endpoint: {endpoint_name}\n"
        data_to_add += f"Response status: {response.status_code}\n"
        data_to_add += f"Response body: {response.text}\n"

        if body is not None:
            data_to_add += f"Request body: {body}\n"

        data_to_add += "-----\n"

        if response.status_code >= 400:
            cls.error(data_to_add)  # 👈 ERROR for fails
        else:
            cls.info(data_to_add)
