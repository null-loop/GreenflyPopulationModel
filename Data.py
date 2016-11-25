class Generation(object):
    def __init__(self, juveniles: int, adults: int, seniles: int, disease_rate: int):
        self.juveniles = juveniles
        self.adults = adults
        self.seniles = seniles
        self.disease_rate = disease_rate
        self.juveniles_in_thousands = Generation.format_in_thousands(juveniles)
        self.adults_in_thousands = Generation.format_in_thousands(adults)
        self.seniles_in_thousands = Generation.format_in_thousands(seniles)

    @classmethod
    def format_in_thousands(cls, value):
        return value / 1000


class ModelRunOptions(object):

    def __init__(self, starting_juveniles: int, starting_adults: int, starting_seniles: int,
                 generations: int, juvenile_survival_rate: float, adult_survival_rate: float,
                 senile_survival_rate: float, adult_birth_rate: float, disease_trigger: int):
        self.starting_juveniles = starting_juveniles
        self.starting_adults = starting_adults
        self.starting_seniles = starting_seniles
        self.generations = generations
        self.juvenile_survival_rate = juvenile_survival_rate
        self.adult_survival_rate = adult_survival_rate
        self.senile_survival_rate = senile_survival_rate
        self.adult_birth_rate = adult_birth_rate
        self.disease_trigger = disease_trigger


class ModelRunOptionsValidation(object):
    def __init__(self, min_generations: int, max_generations: int):
        self.min_generations = min_generations
        self.max_generations = max_generations

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
