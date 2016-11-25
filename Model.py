from Data import ModelRunOptions
from Data import Generation
from enum import Enum
import random


class LifecycleStage(Enum):
    Juvenile = 0,
    Adult = 1,
    Senile = 2


class Population(object):

    def __init__(self, juveniles: int, adults: int, seniles: int):
        self.__juveniles = juveniles
        self.__adults = adults
        self.__seniles = seniles

    def create_generation_from_current_state(self, disease_rate: int):
        return Generation(self.__juveniles, self.__adults, self.__seniles, disease_rate)

    def get_count(self, stage: LifecycleStage):
        if stage == LifecycleStage.Juvenile.value:
            return self.__juveniles
        if stage == LifecycleStage.Adult.value:
            return self.__adults
        if stage == LifecycleStage.Senile.value:
            return self.__seniles

    def update_to_next_generation(self, options: ModelRunOptions, disease_rate: int):
        juveniles_born = self.calculate_born_juveniles(options.adult_birth_rate)
        surviving_juveniles = self.calculate_surviving_juveniles(options.juvenile_survival_rate, disease_rate)
        surviving_adults = self.calculate_surviving_adults(options.adult_survival_rate)
        surviving_seniles = self.calculate_surviving_seniles(options.senile_survival_rate, disease_rate)

        self.__seniles = surviving_seniles + surviving_adults
        self.__adults = surviving_juveniles
        self.__juveniles = juveniles_born

        return self.create_generation_from_current_state(disease_rate)

    def calculate_born_juveniles(self, adult_birth_rate: float):
        return int(self.__adults * adult_birth_rate)

    def calculate_surviving_juveniles(self, juvenile_survival_rate: float, disease_rate: float):
        return int(self.__juveniles * juvenile_survival_rate * (100 - disease_rate) / 100)

    def calculate_surviving_adults(self, adult_survival_rate: float):
        return int(self.__adults * adult_survival_rate)

    def calculate_surviving_seniles(self, senile_survival_rate: float, disease_rate: float):
        return int(self.__seniles * senile_survival_rate * (100 - disease_rate) / 100)

    def get_total_population(self):
        return self.__juveniles + self.__adults + self.__seniles


class PopulationModel(object):
    def __init__(self, options: ModelRunOptions):
        random.seed()
        self.__options = options
        self.__population = Population(options.starting_juveniles, options.starting_adults, options.starting_seniles)
        self.__generations = [self.__population.create_generation_from_current_state(0)]

    def get_generations_count(self):
        return len(self.__generations)

    def get_generation(self, index: int):
        return self.__generations[index]

    def get_generations(self):
        return self.__generations

    def run_all_generations(self):
        for generation in range(0, self.__options.generations):
            disease_rate = self.calculate_disease_rate()
            next_generation = self.__population.update_to_next_generation(self.__options, disease_rate)
            self.__generations.append(next_generation)

    def calculate_disease_rate(self):
        total_population = self.__population.get_total_population()
        if total_population >= self.__options.disease_trigger:
            return PopulationModel.random_disease_rate()
        return 0

    @classmethod
    def random_disease_rate(cls):
        return random.randrange(20, 50)
