import logging
import sys
import time
from pathlib import Path

from config.prompts_objects import ID_PROMPT_PROOFREAD_BASE, PROMPT_PARAM_USER_TEXT
from context import create_context, AppContext
from core.models.data_types import ProcessingContext, TaskResult, TaskInput
from core.models.enums.settings import LlmProviderType


def configure_logger(log_level: int = logging.INFO) -> None:
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)-8s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    root_logger.propagate = False
    logging.info("Logger configured successfully")
    logging.debug("Debug logging is enabled")


logger = logging.getLogger(__name__)

APP_ROOT_PATH = Path(__file__).resolve().parents[2]


def on_task_finished(task_res: TaskResult):
    logger.debug(f"Task {task_res.id} finished with result {task_res}")


def test_request(app_context: AppContext):
    logger.debug(f"Will be tested proofread")
    req = ProcessingContext(user_prompt_id=ID_PROMPT_PROOFREAD_BASE,
                            prompt_parameters={PROMPT_PARAM_USER_TEXT: 'Helllo,, wword!'})
    logger.debug(f"Request: {req}")
    # res = app_context.text_processing_service.process(req)
    # logger.debug(f"Result: {res}")
    input = TaskInput(
        id='new_task_id',
        task_func=lambda: app_context.text_processing_service.process(req),
        on_task_finished=on_task_finished
    )
    app_context.task_service.submit_task(input)
    time.sleep(120)


def global_task_listener(task_res: TaskResult):
    logger.debug(f"Global Task {task_res.id} status changed to {task_res}")


def global_busy_listener(is_busy: bool):
    logger.debug(f"Global is_busy changed to {is_busy}")


def testing(app_context: AppContext):
    app_context.task_service.subscribe_global_task_finished(global_task_listener)
    app_context.task_service.subscribe_global_busy_state_changed(global_busy_listener)
    # Testing code:
    test_request(app_context)

    app_context.settings_service.set_llm_model_name('Qwen3-14B (Reasoning)')
    logger.debug(f"Changed model {app_context.settings_service.get_llm_model()}")

    test_request(app_context)

    app_context.settings_service.set_llm_model_name('Qwen3-14B (Non-Reasoning)')
    logger.debug(f"Changed model {app_context.settings_service.get_llm_model()}")

    test_request(app_context)

    logger.debug(f"Providers {app_context.settings_service.get_llm_provider_list()}")
    logger.debug(f"Models {app_context.settings_service.get_llm_models_for_selected_provider()}")

    app_context.settings_service.set_llm_provider(LlmProviderType.OLLAMA)

    logger.debug(f"Changed provider {app_context.settings_service.get_llm_provider()}")
    logger.debug(f"Models {app_context.settings_service.get_llm_models_for_selected_provider()}")

    app_context.settings_service.set_llm_model_name('llama3.1:8b-instruct-q4_K_M')
    logger.debug(f"Changed model")

    test_request(app_context)


def start_application():
    configure_logger(log_level=logging.DEBUG)
    logger.info("Starting application")
    logger.debug(f"Application root path: {APP_ROOT_PATH}")
    ctx = create_context(APP_ROOT_PATH)
    # testing(ctx)
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())


if __name__ == '__main__':
    start_application()
