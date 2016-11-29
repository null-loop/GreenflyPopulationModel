from Data import ModelRunOptions
from Data import Generation
from enum import Enum
import random


# this class is a simple definition of values - AKA - an Enumerator (shortened to Enum)
# notice how the class is inheriting from the Enum class in the enum model - the name in brackets
class LifecycleStage(Enum):
    # We're defining static values for each of our lifecycle stages - this just
    # makes it clearer later on when we're accessing some methods
    Juvenile = 0,
    Adult = 1,
    Senile = 2


class Population(object):

    def __init__(self, juveniles: int, adults: int, seniles: int):
        # Initialisation of the population - we take the starting populations and set them as field values
        self.__juveniles = juveniles
        self.__adults = adults
        self.__seniles = seniles

    def create_generation_from_current_state(self, disease_rate: int):
        # creates a new Data.Generation object from the current values of the population
        return Generation(self.__juveniles, self.__adults, self.__seniles, disease_rate)

    def get_count(self, stage: LifecycleStage):
        # gets one of the current counts of population - we take a LifecycleStage as a parameter
        # and then decide which field value to return
        if stage == LifecycleStage.Juvenile.value:
            return self.__juveniles
        if stage == LifecycleStage.Adult.value:
            return self.__adults
        if stage == LifecycleStage.Senile.value:
            return self.__seniles

    def update_to_next_generation(self, options: ModelRunOptions, disease_rate: int):
        # perform an update of the current population values based on our models options (contained in the
        # options parameter) - by passing it as a parameter we can control the inputs when performing testing

        # calculate the number of juveniles born
        juveniles_born = self.calculate_born_juveniles(options.adult_birth_rate)
        # calculate the number of juveniles surviving to become adults - passing the disease_rate
        surviving_juveniles = self.calculate_surviving_juveniles(options.juvenile_survival_rate, disease_rate)
        # calculate the number of adults surviving to become seniles
        surviving_adults = self.calculate_surviving_adults(options.adult_survival_rate)
        # calculate the number of seniles that are surviving as seniles - passing the disease_rate
        surviving_seniles = self.calculate_surviving_seniles(options.senile_survival_rate, disease_rate)

        # set the new senile population
        self.__seniles = surviving_seniles + surviving_adults
        # set the new adult population
        self.__adults = surviving_juveniles
        # set the new juveniles
        self.__juveniles = juveniles_born

        # create and return a new generation instance representing the current state
        return self.create_generation_from_current_state(disease_rate)

    def calculate_born_juveniles(self, adult_birth_rate: float):
        # calculate how many juveniles are born based on the number of adults and the adult birth rate
        return int(self.__adults * adult_birth_rate)

    def calculate_surviving_juveniles(self, juvenile_survival_rate: float, disease_rate: float):
        # calculate how many juveniles survive based on the number of juveniles, their survival rate
        # and the disease rate
        return int(self.__juveniles * juvenile_survival_rate * (100 - disease_rate) / 100)

    def calculate_surviving_adults(self, adult_survival_rate: float):
        # calculate how many adults survive based on the number of adults and their survival rate
        return int(self.__adults * adult_survival_rate)

    def calculate_surviving_seniles(self, senile_survival_rate: float, disease_rate: float):
        # calculate how many seniles survive based on the number of seniles, their survival rate
        # and the disease rate
        return int(self.__seniles * senile_survival_rate * (100 - disease_rate) / 100)

    def get_total_population(self):
        # helper method to get the total population (used in testing)
        return self.__juveniles + self.__adults + self.__seniles


class PopulationModel(object):
    def __init__(self, options: ModelRunOptions):
        # Initialising a new population model - all we need is an instance of the ModelRunOptions class
        # this contains all the information we need to run the model

        # the disease rate is calculated at random - using the pseudo random number generator
        # pseudo random number generators AREN'T really random - they're (like all things in a computer)
        # deterministic - which means they're predictable. That predictability is based on a "seed" value
        # Given the same seed value they will produce the same sequence of random numbers.
        # By calling random.seed() as we do below a seed value is calculated based on the current
        # date / time.
        random.seed()
        # stash away the options in a field
        self.__options = options
        # create a new population object using the starting populations on the options
        self.__population = Population(options.starting_juveniles, options.starting_adults, options.starting_seniles)
        # create list of generations populated with the first generation from the __population object.
        self.__generations = [self.__population.create_generation_from_current_state(0)]

    def get_generations_count(self):
        # simply gets the count of generations in the model.
        return len(self.__generations)

    def get_generation(self, index: int):
        # gets the generation object at the specified index
        return self.__generations[index]

    def get_generations(self):
        # gets all the generations
        return self.__generations

    def run_all_generations(self):
        # runs the model for number of generations specified in __options
        for generation in range(0, self.__options.generations):
            # calculate a disease rate to apply for the current generation
            disease_rate = self.calculate_disease_rate()
            # update the population to the next generation and get the result object
            next_generation = self.__population.update_to_next_generation(self.__options, disease_rate)
            # add the generation object we just got to the list of generations
            self.__generations.append(next_generation)

    def calculate_disease_rate(self):
        # using the total population determine if we've got disease - by comparing to the trigger
        # value in the options
        total_population = self.__population.get_total_population()
        if total_population >= self.__options.disease_trigger:
            return PopulationModel.random_disease_rate()
        return 0

    @classmethod
    def random_disease_rate(cls):
        return random.randrange(20, 50)


class ModelRunOptionsValidation(object):
    def __init__(self, min_generations: int, max_generations: int):
        # we're only taking two parameters here for our validation - these are the only
        # values that are configurable - we COULD hard code them - but good code inverts
        # control - there's no natural limits for the min / max generations so we're passing them
        # in as parameters
        self.min_generations = min_generations
        self.max_generations = max_generations

    # The code below should be self explanatory...

    def validate_starting_juveniles(self, value):
        if value < 0:
            return "Must be 0 or greater"
        return None

    def validate_starting_adults(self, value):
        if value < 0:
            return "Must be 0 or greater"
        return None

    def validate_starting_seniles(self, value):
        if value < 0:
            return "Must be 0 or greater"
        return None

    def validate_generations(self, value):
        if value < self.min_generations:
            return "Must be equal to or greater than {}".format(self.min_generations)
        if value > self.max_generations:
            return "Must be equal to or less than {}".format(self.max_generations)
        return None

    def validate_disease_trigger(self, value):
        if value <= 0:
            return "Must be greater than 0"
        return None

    def validate_adult_birth_rate(self, value):
        if value < 0:
            return "Must be 0 or greater"
        return None

    def validate_juvenile_survival_rate(self, value):
        if value < 0:
            return "Must be 0 or greater"
        if value > 1:
            return "Must be 1 or less"

    def validate_adult_survival_rate(self, value):
        if value < 0:
            return "Must be 0 or greater"
        if value > 1:
            return "Must be 1 or less"

    def validate_senile_survival_rate(self, value):
        if value < 0:
            return "Must be 0 or greater"
        if value > 1:
            return "Must be 1 or less"
