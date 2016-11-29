import _curses
import Data
import Model
from pathlib import Path

# note the imports above:
# we're bringing in access to all the classes defined in _curses (an external library responsible for
# console input output), all the classes defined in our own modules Data & Model, and finally a single
# class from pathlib (the Path class)


class Menu(object):
    # The menu class represents our top level menu, you can see we're passing three parameters on initialisation
    # The first - self - is a reference to the instance. YOU MUST HAVE THIS in all instance methods (that
    # is methods that are on an instance of a class) - it allows you to access values on the instance itself.
    # We also take a header (a string) and a list of menu options.
    # Each of these values is stored in a PRIVATE field - by convention in Python any field referenced with a
    # double underscore is private (that is NOT accessible by code outside of the class itself). This ISN'T a
    # hard boundary - you CAN access it from outside, it's just not visible when using an IDE - so consider
    # it inaccessible (it's good practice)
    def __init__(self, header, options: []):
        self.__header = header
        self.__options = options
        self.__exit = False

    # The render method is going to draw the menu to the console
    def __render(self):

        # Clear the console (the Console class is defined method - as what in some languages is called a static
        # class - that is to say we DON'T create instances of this class - just use methods on it - the class
        # is just there as an organisational structure to keep our code well structured)
        Console.clear()
        # define an initial line offset - where to start writing the menu from
        line_offset = 4
        # define the column we're starting from
        col = 4

        # write the header we passed in the initialiser
        Console.print_line_at(1, col, self.__header, _curses.COLOR_RED)
        # write a number of - characters equal to the length of the header
        Console.print_line_at(2, col, "-" * len(self.__header), _curses.COLOR_WHITE)
        # store a count of the number of options in our menu
        option_count = len(self.__options)
        # iterate over all the options
        for i in range(0, option_count):
            # set the current line by offsetting the loop index by our line_offset
            line = i + line_offset
            # the responsibility for rendering each option lies with the option itself - we don't care HOW it's rendered
            # just that it is.
            self.__options[i].render(line, col)

        # print a prompt to select an input
        Console.print_line_at(line_offset + option_count + 1, col, "Select Option", _curses.COLOR_WHITE)
        # push everything out to the console
        Console.refresh()

    def run(self):
        # runs the menu system
        # we're going to loop around this block until we've exited (which is performed by calling the exit() method on
        # the instance)
        while not self.__exit:
            # print the menu
            self.__render()
            # capture the option the user selected
            selected_option = self.__capture_option()
            # safety check that something WAS selected
            if selected_option is not None:
                # execute the action associated with the option
                selected_option.do()

    def __capture_option(self):
        # we're going to capture the user input and select the option that matches
        # each option stores the key character the user needs to press
        character = chr(Console.capture_character())
        for i in range(0, len(self.__options)):
            # so we loop over all the options
            # and if the character they pressed matches the option
            if self.__options[i].matches_input(character):
                # we return it.
                return self.__options[i]
        # if the key press doesn't match an option then return None
        return None

    def exit(self):
        # set the exit flag to true - which will cause the while loop in run to terminate
        self.__exit = True


class MenuOption(object):
    # we're initialising a menu option, for that we require the key that the user must press (option)
    # the text to display (text)
    # and the action to do when they've selected the option (action) - which is a "functor"
    # the code inside the menu option knows nothing at all about what action can be performed
    # or how - this is a key aspect of separation of concerns - we can make our menu do ANYTHING
    # without having to change the menu.
    def __init__(self, option, text, action):
        self.__option = option
        self.__text = text
        self.__action = action

    def do(self):
        # safety check - make sure we actually have an action before we do it.
        if self.__action is not None:
            # note how we're treating the __action field as a method
            # we were passed it to the initialisation method as parameter,
            # stored it in a field - and then invoked it as a method
            self.__action()

    def render(self, line, col):
        # renders the menu option at the specified line and col
        Console.print_line_at(line, col, "{} - {}".format(self.__option, self.__text), _curses.COLOR_WHITE)
        pass

    def matches_input(self, input_value):
        # checks whether the specified input_value matches the option this menu represents
        return input_value.lower() == self.__option.lower()


class CsvGenerator(object):
    # This class (like Console) - is composed entirely of non-instance methods - you'll notice there's no
    # initialisation method - you can't create instances of the CsvGenerator class.
    # You have to call methods here through the class identifier:
    # csv_lines = csv_generator.generate_csv_for_generations(generations)
    @classmethod
    def generate_csv_for_generations(cls, generations: []):
        # setup the first line (which contains the headers for the columns)
        lines = ["Generation,Juveniles,Adults,Seniles"]
        for index in range(0, len(generations)):
            # iterate over all the generations we got passed
            g = generations[index]
            # add a formatted line for each generation to our list o' lines
            lines.append(
                "{},{},{},{}".format(index, g.juveniles_in_thousands, g.adults_in_thousands, g.seniles_in_thousands))
        # return the list
        return lines

    @classmethod
    def write_generations_file(cls, model: Model.PopulationModel, file_path: Path):
        # get the CSV lines using the method above
        csv = CsvGenerator.generate_csv_for_generations(model.get_generations())
        # open the file for writing (note there's no error handling in here!)
        file = file_path.open('w')
        for i in range(0, len(csv)):
            # iterate over each line we got passed and write it the file we just opened
            file.write(csv[i] + "\n")
        # CLOSE the file (this is v. important - otherwise we're holding onto a file handle AFTER we've finished
        # which is very, very bad)
        file.close()


class Console(object):
    # Again the Console class is made up of non-instance methods accessed through the class name:
    # Console.init()
    # Console.exit()
    __screen = None

    @classmethod
    def init(cls):
        # sets up the initial state of the console - performs bootstrapping of the curses library
        # note this isn't an instance initialisation method (they're called __init__)
        cls.__screen = _curses.initscr()
        _curses.start_color()
        _curses.noecho()
        _curses.cbreak()
        _curses.curs_set(0)

    @classmethod
    def exit(cls):
        # resets everything we setup in the init method above
        _curses.curs_set(1)
        _curses.nocbreak()
        _curses.echo()

    @classmethod
    def refresh(cls):
        # forces a refresh of the console - which pushes all the output we've written
        # to the console
        cls.__screen.refresh()

    @classmethod
    def print_line_at(cls, row, col, text, colour: int):
        # writes a line of text at the specified row and column
        cls.__screen.addstr(row, col, text, _curses.color_pair(colour))

    @classmethod
    def capture_character(cls):
        # captures a single character from the keyboard
        return cls.__screen.getch()

    @classmethod
    def print_error(cls, text):
        # prints an error message in a common way - saves us from having to redo this everything
        # we encounter an error condition in our main code.
        Console.clear()
        Console.print_line_at(1, 4, "ERROR: " + text, _curses.COLOR_RED)
        Console.refresh()
        Console.capture_character()

    @classmethod
    def print_message(cls, text):
        # prints a normal message in a common way
        Console.clear()
        Console.print_line_at(1, 4, text, _curses.COLOR_GREEN)
        Console.refresh()
        Console.capture_character()

    @classmethod
    def clear(cls):
        # clears the console
        cls.__screen.clear()

    @classmethod
    def collect_options(cls, validation: Model.ModelRunOptionsValidation):
        # This method collects all the options from the user and performs validation using the
        # passed in validation parameter

        starting_juveniles = Console.collect_integer("Enter starting juvenile population (1000s)",
                                                     validation.validate_starting_juveniles) * 1000

        starting_adults = Console.collect_integer("Enter starting adult population (1000s)",
                                                  validation.validate_starting_adults) * 1000

        starting_seniles = Console.collect_integer("Enter starting senile population (1000s)",
                                                   validation.validate_starting_seniles) * 1000

        generations = Console.collect_integer("Enter number of generations",
                                              validation.validate_generations)

        disease_trigger = Console.collect_integer("Enter total population to trigger disease (1000s)",
                                                  validation.validate_disease_trigger) * 1000

        adult_birth_rate = Console.collect_float("Enter adult birth rate",
                                                 validation.validate_adult_birth_rate)

        juvenile_survival_rate = Console.collect_float("Enter juvenile survival rate",
                                                       validation.validate_juvenile_survival_rate)

        adult_survival_rate = Console.collect_float("Enter adult survival rate",
                                                    validation.validate_adult_survival_rate)

        senile_survival_rate = Console.collect_float("Enter senile survival rate",
                                                     validation.validate_senile_survival_rate)

        # once we've collected all the values we can return a new Data.ModelRunOptions object instance
        # with all the values we collected.
        # Note that since we imported the whole of the Data module (import Data) - we have to specify
        # the module name when reference the class (Data.ModelRunOptions)
        return Data.ModelRunOptions(starting_juveniles, starting_adults, starting_seniles, generations,
                                    juvenile_survival_rate, adult_survival_rate, senile_survival_rate,
                                    adult_birth_rate, disease_trigger)

    @classmethod
    def print_options(cls, options: Data.ModelRunOptions):
        # prints out all the options that have been configured on the specified options instance
        Console.clear()
        Console.print_option("Starting juvenile population", str(options.starting_juveniles), 1)
        Console.print_option("Starting adult population", str(options.starting_adults), 2)
        Console.print_option("Starting senile population", str(options.starting_seniles), 3)
        Console.print_option("No. of generations", str(options.generations), 4)
        Console.print_option("Disease population trigger", str(options.disease_trigger), 5)
        Console.print_option("Adult birth rate", str(options.adult_birth_rate), 6)
        Console.print_option("Juvenile survival rate", str(options.juvenile_survival_rate), 7)
        Console.print_option("Adult survival rate", str(options.adult_survival_rate), 8)
        Console.print_option("Senile survival rate", str(options.senile_survival_rate), 9)
        Console.capture_character()

    @classmethod
    def print_option(cls, label, value, line):
        # prints an option at the specified line composed of a line of text and a value
        Console.print_line_at(line, 4, label, _curses.COLOR_GREEN)
        Console.print_line_at(line, 40, value, _curses.COLOR_WHITE)

    @classmethod
    def collect_file_path(cls):
        # collects a valid file path to export the CSV file to from the keyboard
        valid_path = False
        label = "Enter file path to export to"
        while not valid_path:
            Console.clear()
            Console.print_line_at(1, 4, label + " : ", _curses.COLOR_GREEN)
            Console.refresh()
            input_characters = Console.collect_characters(1, 4 + len(label) + 3, None)
            if input_characters is None or len(input_characters) == 0:
                Console.print_error("Please enter a path")
            else:
                try:
                    file_path = Path(input_characters)
                except:
                    Console.print_error("Invalid path")
                    continue
                if file_path.exists():
                    overwrite = Console.collect_yes_no("File already exists at {}, overwrite (Y/N)"
                                                       .format(file_path.absolute())).lower() == "y"
                    if overwrite:
                        return file_path
                else:
                    return file_path

    @classmethod
    def collect_yes_no(cls, label):
        # collects a boolean value expressed as a Y/N option from the keyboard
        valid_boolean = False
        valid_characters = "YyNn"
        while not valid_boolean:
            Console.clear()
            Console.print_line_at(1, 4, label + " : ", _curses.COLOR_GREEN)
            Console.refresh()
            input_characters = Console.collect_characters(1, 4 + len(label) + 3, valid_characters)
            if input_characters is None or len(input_characters) == 0 or len(input_characters) > 1:
                Console.print_error("Please enter a Y or N")
            else:
                return input_characters

    @classmethod
    def collect_integer(cls, label, validation):
        # collects an integer from the keyboard - note it uses the collect_number method to do the majority
        # of the work. It passes a label, a validation method (using the functor technique),
        # a set of valid characters to enter, a parsing method (to turn the characters into a number)
        # and finally a string to identify what type of value we want
        return Console.collect_number(label, validation, "-1234567890", int, "integer")

    @classmethod
    def collect_float(cls, label, validation):
        # same as above - just with different valid set of characters, parse method and
        # type identifier
        return Console.collect_number(label, validation, "-1234567890.", float, "number")

    @classmethod
    def collect_number(cls, label, validation, valid_characters, parser, number_label):
        # collects a series of valid keypresses (expressed in valid_characters),
        # when enter is pressed it passes it through the parser method,
        # if a valid value (determined by NOT throwing an error),
        # we pass it to the validation method, if that passes we can return the number
        valid_number = False
        while not valid_number:
            Console.clear()
            Console.print_line_at(1, 4, label + " : ", _curses.COLOR_GREEN)
            Console.refresh()
            input_characters = Console.collect_characters(1, 4 + len(label) + 3, valid_characters)
            if input_characters is None or len(input_characters) == 0:
                Console.print_error("Please enter an {}".format(number_label))
            else:
                try:
                    input_value = parser(input_characters)
                except:
                    Console.print_error("Please enter a valid {}".format(number_label))
                    continue
                validation_error = validation(input_value)
                if validation_error is not None:
                    Console.print_error(validation_error)
                else:
                    return input_value

    @classmethod
    def collect_characters(cls, line, col, valid_characters):
        # collects a number of characters from the keyboard and returns them when enter is pressed
        current_col = col
        last_character_code = 0
        collected_characters = ""
        while last_character_code != 10:
            last_character_code = Console.capture_character()
            last_character = chr(last_character_code)
            if last_character_code == 8 and len(collected_characters) > 0:
                collected_characters = collected_characters[0:len(collected_characters) - 1]
                current_col -= 1
                Console.print_line_at(line, current_col, " ", _curses.COLOR_WHITE)
            else:
                if (valid_characters is None or last_character in valid_characters) and last_character_code != 10:
                    collected_characters += last_character
                    Console.print_line_at(line, current_col, last_character, _curses.COLOR_WHITE)
                    current_col += 1

        return collected_characters

    @classmethod
    def print_generations(cls, model):
        # prints all the generations from the model parameter
        col_offset = 3
        cols = 6
        col_width = 18

        Console.clear()

        Console.print_line_at(1, col_offset, "Results", _curses.COLOR_RED)
        Console.print_line_at(2, col_offset, "-------", _curses.COLOR_WHITE)

        Console.print_line_at(4, col_offset, "-" * ((cols * col_width) + 1), _curses.COLOR_WHITE)
        Console.print_line_at(5, col_offset, "| Generation", _curses.COLOR_WHITE)
        Console.print_line_at(5, col_width + col_offset, "| Juveniles", _curses.COLOR_WHITE)
        Console.print_line_at(5, (2 * col_width) + col_offset, "| Adults", _curses.COLOR_WHITE)
        Console.print_line_at(5, (3 * col_width) + col_offset, "| Seniles", _curses.COLOR_WHITE)
        Console.print_line_at(5, (4 * col_width) + col_offset, "| Total", _curses.COLOR_WHITE)
        Console.print_line_at(5, (5 * col_width) + col_offset, "| Disease", _curses.COLOR_WHITE)
        Console.print_line_at(5, (6 * col_width) + col_offset, "|", _curses.COLOR_WHITE)
        Console.print_line_at(6, col_offset, "-" * ((cols * col_width) + 1), _curses.COLOR_WHITE)

        start_line = 7
        for g in range(0, model.get_generations_count()):
            gen = model.get_generation(g)
            line = start_line + g
            Console.print_line_at(line, col_offset, "| {}".format(g), _curses.COLOR_WHITE)
            Console.print_line_at(line, col_width + col_offset, "| {}".format(gen.juveniles_in_thousands), _curses.COLOR_WHITE)
            Console.print_line_at(line, (2 * col_width) + col_offset, "| {}".format(gen.adults_in_thousands), _curses.COLOR_WHITE)
            Console.print_line_at(line, (3 * col_width) + col_offset, "| {}".format(gen.seniles_in_thousands), _curses.COLOR_WHITE)
            Console.print_line_at(line, (4 * col_width) + col_offset,
                                  "| {}".format(gen.total_population_in_thousands), _curses.COLOR_WHITE)
            Console.print_line_at(line, (5 * col_width) + col_offset, "| {}".format(gen.disease_rate), _curses.COLOR_WHITE)
            Console.print_line_at(line, (6 * col_width) + col_offset, "|", _curses.COLOR_WHITE)

        Console.print_line_at(start_line + model.get_generations_count(),
                              col_offset, "-" * ((cols * col_width) + 1), _curses.COLOR_WHITE)
        Console.refresh()
        Console.capture_character()
