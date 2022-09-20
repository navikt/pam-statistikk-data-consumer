from starlette.responses import JSONResponse
from fastapi import FastAPI
from starlette import status


class API:
    def __init__(self):
        self._app = FastAPI()
        self._is_alive = True
        self._is_ready = False
        self.add_endpoints()

    @property
    def app(self):
        return self._app

    def setReady(self, arg: bool):
        self._is_ready = arg

    def setAlive(self, arg: bool):
        self._is_ready = arg

    def healthiness(self):
        if self._is_alive:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"Unhealthy"},
            )

    def readiness(self):
        if self._is_ready:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"NotReady"},
            )

    def add_endpoints(self):

        self._app.add_api_route(path="/isalive", endpoint=self.healthiness)
        self._app.add_api_route(path="/isready", endpoint=self.readiness)

