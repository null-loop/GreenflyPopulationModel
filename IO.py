import _curses
import Data
import Model
from pathlib import Path


class Menu(object):
    def __init__(self, header, options: []):
        self.__header = header
        self.__options = options
        self.__exit = False

    def __render(self):

        Console.clear()
        line_offset = 4
        col = 4

        Console.print_line_at(1, col, self.__header, _curses.COLOR_RED)
        Console.print_line_at(2, col, "-" * len(self.__header), _curses.COLOR_WHITE)

        option_count = len(self.__options)

        for i in range(0, option_count):
            line = i + line_offset
            self.__options[i].render(line, col)

        Console.print_line_at(line_offset + option_count + 1, col, "Select Option", _curses.COLOR_WHITE)
        Console.refresh()

    def run(self):
        while not self.__exit:
            self.__render()
            selected_option = self.__capture_option()
            if selected_option is not None:
                selected_option.do()

    def __capture_option(self):
        character = chr(Console.capture_character())
        for i in range(0, len(self.__options)):
            if self.__options[i].matches_input(character):
                return self.__options[i]
        return None

    def exit(self):
        self.__exit = True


class MenuOption(object):
    def __init__(self, option, text, action):
        self.__option = option
        self.__text = text
        self.__action = action

    def do(self):
        if self.__action is not None:
            self.__action()

    def render(self, line, col):
        Console.print_line_at(line, col, "{} - {}".format(self.__option, self.__text), _curses.COLOR_WHITE)
        pass

    def matches_input(self, input_value):
        return input_value.lower() == self.__option.lower()


class CsvGenerator(object):
    @classmethod
    def generate_csv_for_generations(cls, generations: []):
        lines = ["Generation,Juveniles,Adults,Seniles"]
        for index in range(0, len(generations)):
            g = generations[index]
            lines.append(
                "{},{},{},{}".format(index, g.juveniles_in_thousands, g.adults_in_thousands, g.seniles_in_thousands))
        return lines

    @classmethod
    def write_generations_file(cls, model: Model.PopulationModel, file_path: Path):
        csv = CsvGenerator.generate_csv_for_generations(model.get_generations())
        file = file_path.open('w')
        for i in range(0, len(csv)):
            file.write(csv[i] + "\n")
        file.close()


class Console(object):
    __screen = None

    @classmethod
    def init(cls):
        cls.__screen = _curses.initscr()
        _curses.start_color()
        _curses.noecho()
        _curses.cbreak()
        _curses.curs_set(0)

    @classmethod
    def exit(cls):
        _curses.curs_set(1)
        _curses.nocbreak()
        _curses.echo()

    @classmethod
    def refresh(cls):
        cls.__screen.refresh()

    @classmethod
    def print_line_at(cls, row, col, text, colour: int):
        cls.__screen.addstr(row, col, text, _curses.color_pair(colour))

    @classmethod
    def capture_character(cls):
        return cls.__screen.getch()

    @classmethod
    def print_error(cls, text):
        Console.clear()
        Console.print_line_at(1, 4, "ERROR: " + text, _curses.COLOR_RED)
        Console.refresh()
        Console.capture_character()

    @classmethod
    def print_message(cls, text):
        Console.clear()
        Console.print_line_at(1, 4, text, _curses.COLOR_GREEN)
        Console.refresh()
        Console.capture_character()

    @classmethod
    def clear(cls):
        cls.__screen.clear()

    @classmethod
    def collect_options(cls, validation: Data.ModelRunOptionsValidation):
        starting_juveniles = Console.collect_integer("Enter starting juvenile population",
                                                     validation.validate_starting_juveniles)

        starting_adults = Console.collect_integer("Enter starting adult population",
                                                  validation.validate_starting_adults)

        starting_seniles = Console.collect_integer("Enter starting senile population",
                                                   validation.validate_starting_seniles)

        generations = Console.collect_integer("Enter number of generations",
                                              validation.validate_generations)

        disease_trigger = Console.collect_integer("Enter total population to trigger disease",
                                                  validation.validate_disease_trigger)

        adult_birth_rate = Console.collect_float("Enter adult birth rate",
                                                 validation.validate_adult_birth_rate)

        juvenile_survival_rate = Console.collect_float("Enter juvenile survival rate",
                                                       validation.validate_juvenile_survival_rate)

        adult_survival_rate = Console.collect_float("Enter adult survival rate",
                                                    validation.validate_adult_survival_rate)

        senile_survival_rate = Console.collect_float("Enter senile survival rate",
                                                     validation.validate_senile_survival_rate)

        return Data.ModelRunOptions(starting_juveniles, starting_adults, starting_seniles, generations,
                                    juvenile_survival_rate, adult_survival_rate, senile_survival_rate,
                                    adult_birth_rate, disease_trigger)

    @classmethod
    def print_options(cls, options: Data.ModelRunOptions):
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
        Console.print_line_at(line, 4, label, _curses.COLOR_GREEN)
        Console.print_line_at(line, 40, value, _curses.COLOR_WHITE)

    @classmethod
    def collect_file_path(cls):
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
        return Console.collect_number(label, validation, "-1234567890", int, "integer")

    @classmethod
    def collect_float(cls, label, validation):
        return Console.collect_number(label, validation, "-1234567890.", float, "number")

    @classmethod
    def collect_number(cls, label, validation, valid_characters, parser, number_label):
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

        col_offset = 3
        cols = 5
        col_width = 20

        Console.clear()

        Console.print_line_at(1, col_offset, "Results", _curses.COLOR_RED)
        Console.print_line_at(2, col_offset, "-------", _curses.COLOR_WHITE)

        Console.print_line_at(4, col_offset, "-" * ((cols * col_width) + 1), _curses.COLOR_WHITE)
        Console.print_line_at(5, col_offset, "| Generation", _curses.COLOR_WHITE)
        Console.print_line_at(5, col_width + col_offset, "| Juveniles", _curses.COLOR_WHITE)
        Console.print_line_at(5, (2 * col_width) + col_offset, "| Adults", _curses.COLOR_WHITE)
        Console.print_line_at(5, (3 * col_width) + col_offset, "| Seniles", _curses.COLOR_WHITE)
        Console.print_line_at(5, (4 * col_width) + col_offset, "| Total", _curses.COLOR_WHITE)
        Console.print_line_at(5, (5 * col_width) + col_offset, "|", _curses.COLOR_WHITE)
        Console.print_line_at(6, col_offset, "-" * ((cols * col_width) + 1), _curses.COLOR_WHITE)

        start_line = 7
        for g in range(0, model.get_generations_count()):
            gen = model.get_generation(g)
            line = start_line + g
            Console.print_line_at(line, col_offset, "| {}".format(g), _curses.COLOR_WHITE)
            Console.print_line_at(line, col_width + col_offset, "| {}".format(gen.juveniles), _curses.COLOR_WHITE)
            Console.print_line_at(line, (2 * col_width) + col_offset, "| {}".format(gen.adults), _curses.COLOR_WHITE)
            Console.print_line_at(line, (3 * col_width) + col_offset, "| {}".format(gen.seniles), _curses.COLOR_WHITE)
            Console.print_line_at(line, (4 * col_width) + col_offset,
                                  "| {}".format(gen.juveniles + gen.adults + gen.seniles), _curses.COLOR_WHITE)
            Console.print_line_at(line, (5 * col_width) + col_offset, "|", _curses.COLOR_WHITE)

        Console.print_line_at(start_line + model.get_generations_count(),
                              col_offset, "-" * ((cols * col_width) + 1), _curses.COLOR_WHITE)
        Console.refresh()
        Console.capture_character()
