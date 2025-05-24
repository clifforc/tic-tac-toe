from tic_tac_toe.di.config import Settings
from tic_tac_toe.di.container import injector
from tic_tac_toe.web.module.app_module import create_app


def main():
    settings = injector.get(Settings)

    app = create_app(injector)
    app.run(debug=settings.debug, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
