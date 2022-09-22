import uvicorn
from logger import init_app_logging, get_logger

init_app_logging()
logger = get_logger(__name__)

logger.info("running uvicorn")
uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, debug=True, workers=3)