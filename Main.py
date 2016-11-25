import Data
import IO
import Model

__menu = None
__model = None
__options = None
__validation = Data.ModelRunOptionsValidation(5, 25)


def main():
    global __menu

    IO.Console.init()

    __menu = IO.Menu("Greenfly Population Model Program", [
        IO.MenuOption("1", "Set starting options", configure_options),
        IO.MenuOption("2", "Display starting options", print_options),
        IO.MenuOption("3", "Run model", run_model),
        IO.MenuOption("4", "Export current model data", export_model),
        IO.MenuOption("0", "Exit", exit_main)
    ])
    __menu.run()

    IO.Console.exit()


def configure_options():
    global __options
    __options = IO.Console.collect_options(__validation)


def exit_main():
    __menu.exit()


def print_options():

    if assert_has_options():
        IO.Console.print_options(__options)


def run_model():
    global __model
    if assert_has_options():
        __model = Model.PopulationModel(__options)
        __model.run_all_generations()
        IO.Console.print_generations(__model)


def export_model():

    if assert_has_model():
        file_path = IO.Console.collect_file_path()
        IO.CsvGenerator.write_generations_file(__model, file_path)
        IO.Console.print_message("Generations data written to {}".format(file_path.absolute()))


def assert_has_options():
    if __options is None:
        IO.Console.print_error("No options have been configured")
        return False
    else:
        return True


def assert_has_model():
    if __model is None:
        IO.Console.print_error("No model has been created")
        return False
    else:
        return True


if __name__ == "__main__":
    main()
