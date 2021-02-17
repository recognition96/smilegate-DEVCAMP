import logging.handlers


class Log:
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] > %(message)s")

    # INFO 레벨 이상의 로그를 콘솔에 출력하는 Handler
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    # DEBUG 레벨 이상의 로그를 디버깅파일에 출력하는 Handler
    file_debug_handler = logging.FileHandler("logs/debug.log")
    file_debug_handler.setLevel(logging.DEBUG)
    file_debug_handler.setFormatter(formatter)
    logger.addHandler(file_debug_handler)

    # ERROR 레벨 이상의 로그를 에러파일에 출력하는 Handler
    file_error_handler = logging.FileHandler("logs/error.log")
    file_error_handler.setLevel(logging.ERROR)
    file_error_handler.setFormatter(formatter)
    logger.addHandler(file_error_handler)

    # classmethod 로 선언하여 객체 생성없이 사용가능

    @classmethod
    def d(cls, message):
        cls.logger.debug(message)

    @classmethod
    def i(cls, message):
        cls.logger.info(message)

    @classmethod
    def w(cls, message):
        cls.logger.warning(message)

    @classmethod
    def e(cls, message):
        cls.logger.error(message)

    @classmethod
    def c(cls, message):
        cls.logger.critical(message)
