from starlette.responses import JSONResponse
from fastapi import FastAPI
from starlette import status

from logger import init_app_logging, get_logger

init_app_logging()
logger = get_logger(__name__)


class API:
    def __init__(self):
        self._is_alive = True
        self._is_ready = True
        self._app = FastAPI()
        self.add_endpoints()

    @property
    def app(self):
        return self._app

    def set_ready(self, arg: bool):
        logger.info(f"API ready endpoint set to {arg}")
        self._is_ready = arg

    def set_alive(self, arg: bool):
        logger.info(f"API alive endpoint set to {arg}")
        self._is_ready = arg

    async def healthiness(self):
        if self._is_alive:
            logger.debug(f"API: returned status 200 on isalive")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            logger.debug(f"API: returned status 500 on isalive")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"Unhealthy"},
            )

    async def readiness(self):
        if self._is_ready:
            logger.debug(f"API: returned status 200 on isready")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            logger.debug(f"API: returned status 500 on isready")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"NotReady"},
            )

    def add_endpoints(self):
        self._app.add_api_route(path="/isalive", endpoint=self.healthiness)
        self._app.add_api_route(path="/isready", endpoint=self.readiness)
