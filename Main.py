import IO
import Model

# Our global state is below:
# __menu contains our menu
# __model contains our model
# __options contains our options
# __validation contains the validation configuration for the options

__menu = None
__model = None
__options = None
# note we can initialise this here since the values don't change
__validation = Model.ModelRunOptionsValidation(5, 25)


def main():
    # The main loop of the program - we create a menu and then run it.
    # we have to have the global __menu line below because we're assigning to our menu.
    # we DON'T need this to be able to read from the menu / access methods on it (see the exit_main method)
    global __menu

    IO.Console.init()

    # notice how when we're creating the MenuOptions below we reference the methods
    # each option will invoke when selected. We don't reference them directly as invocations:
    # i.e. NOT configure_options()
    # But rather by just referencing their names
    # Invocation of the method is performed by the option when it's selected.
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
    # Uses the Console class in IO to collect all the options from the user
    # Note that we pass the __validation object we created earlier to validate the input
    global __options
    __options = IO.Console.collect_options(__validation)


def exit_main():
    # poke the menu and tell it we want to exit
    # note that we don't need a global __menu to do this.
    __menu.exit()


def print_options():
    # check that we have options - and if we do print them out
    if assert_has_options():
        IO.Console.print_options(__options)


def run_model():
    # we've got a global __model here as we're going to create a model if the user
    # has provided options
    global __model
    if assert_has_options():
        # create the model instance
        __model = Model.PopulationModel(__options)
        # run it
        __model.run_all_generations()
        # print the results
        IO.Console.print_generations(__model)


def export_model():

    # check we've run a model
    if assert_has_model():
        # collect the output path
        file_path = IO.Console.collect_file_path()
        # generate the file
        IO.CsvGenerator.write_generations_file(__model, file_path)
        # write confirmation
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

# points the interpreter at our entry point main()
if __name__ == "__main__":
    main()
