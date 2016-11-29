# Contains classes used as data objects. That is they represent sets of discrete data in the system
# These classes do not depend onto any other classes in the system


class Generation(object):
    # __init__ methods are used to initialise instance of classes, here we can see that a generation requires
    # a count of juveniles, adults, seniles as well as the disease rate that applied for the generation
    # once a model has been run it will contain multiple instances of the generation class.
    # during initialisation we pass each parameter to a field of the class.
    # so we can do:
    # g = Generation(1, 2, 3, 4)
    # and then access each value as:
    # juveniles = g.juveniles
    # juveniles_in_thousands = g.juveniles_in_thousands
    def __init__(self, juveniles: int, adults: int, seniles: int, disease_rate: int):
        self.juveniles = juveniles
        self.adults = adults
        self.seniles = seniles
        self.disease_rate = disease_rate
        self.juveniles_in_thousands = Generation.format_in_thousands(juveniles)
        self.adults_in_thousands = Generation.format_in_thousands(adults)
        self.seniles_in_thousands = Generation.format_in_thousands(seniles)
        self.total_population_in_thousands = Generation.format_in_thousands(juveniles + adults + seniles)

    # this method doesn't require any of the state of an instance of the class - so it's defined as a class method
    # we access this method through the class name - so if we wanted to use it in code external to this class, we
    # would call as:
    # f = Generation.format_in_thousands(1000)
    # and f would now contain 1.
    @classmethod
    def format_in_thousands(cls, value):
        return value / 1000


class ModelRunOptions(object):

    # this class is holding the configuration information that we use to run the model
    # you'll notice these classes have no particular behaviour associated with them. Sometimes we require to have simple
    # data objects - these are (typically) called DTOs (Data Transportation Objects) or (dependent on language):
    # POPOs (Plain Old Python Objects) / POCO (Plain Old CLR Objects) / POJO (Plain Old Java Object). That is something
    # with no particular behaviour.
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


