from unittest import TestCase
from Data import ModelRunOptions
from Data import ModelRunOptionsValidation
from Model import PopulationModel, ModelRunOptionsValidation
from Model import Population
from Model import LifecycleStage
from Model import Generation
from IO import CsvGenerator


class CsvGeneratorTests(TestCase):
    def test_generate_csv_for_generations(self):
        generations = [Generation(1, 2, 3, 4), Generation(2, 3, 4, 5), Generation(3, 4, 5, 6)]
        lines = CsvGenerator.generate_csv_for_generations(generations)
        self.assertEqual(lines[0], "Generation,Juveniles,Adults,Seniles")
        self.assertEqual(lines[1], "0,0.001,0.002,0.003")
        self.assertEqual(lines[2], "1,0.002,0.003,0.004")
        self.assertEqual(lines[3], "2,0.003,0.004,0.005")


class GenerationTests(TestCase):
    def test_initialisation_values(self):
        generation = Generation(1, 2, 3, 4)
        self.assertEqual(generation.juveniles, 1)
        self.assertEqual(generation.adults, 2)
        self.assertEqual(generation.seniles, 3)
        self.assertEqual(generation.disease_rate, 4)
        self.assertEqual(generation.juveniles_in_thousands, 0.001)
        self.assertEqual(generation.adults_in_thousands, 0.002)
        self.assertEqual(generation.seniles_in_thousands, 0.003)


class ModelRunOptionsTests(TestCase):
    def test_initialisation_values(self):
        options = ModelRunOptions(1, 2, 3, 100, 0.5, 1.5, 2.5, 3.5, 1000)
        self.assertEqual(options.starting_juveniles, 1)
        self.assertEqual(options.starting_adults, 2)
        self.assertEqual(options.starting_seniles, 3)
        self.assertEqual(options.generations, 100)
        self.assertEqual(options.juvenile_survival_rate, 0.5)
        self.assertEqual(options.adult_survival_rate, 1.5)
        self.assertEqual(options.senile_survival_rate, 2.5)
        self.assertEqual(options.adult_birth_rate, 3.5)
        self.assertEqual(options.disease_trigger, 1000)


class ModelRunOptionsValidationTests(TestCase):
    def test_initialisation_values(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(1, validation.min_generations)
        self.assertEqual(100, validation.max_generations)

    def test_validate_starting_juveniles_must_be_0_or_greater_with_value_of_minus_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_starting_juveniles(-1))

    def test_validate_starting_juveniles_must_be_0_or_greater_with_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_starting_juveniles(0))

    def test_validate_starting_juveniles_must_be_0_or_greater_with_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_starting_juveniles(1))

    def test_validate_starting_adults_must_be_0_or_greater_with_value_of_minus_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_starting_adults(-1))

    def test_validate_starting_adults_must_be_0_or_greater_with_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_starting_adults(0))

    def test_validate_starting_adults_must_be_0_or_greater_with_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_starting_adults(1))

    def test_validate_starting_seniles_must_be_0_or_greater_with_value_of_minus_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_starting_seniles(-1))

    def test_validate_starting_seniles_must_be_0_or_greater_with_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_starting_seniles(0))

    def test_validate_starting_seniles_must_be_0_or_greater_with_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_starting_seniles(1))

    def test_validate_generations_cannot_be_less_than_min_for_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be equal to or greater than 1", validation.validate_generations(0))

    def test_validate_generations_cannot_be_less_than_min_for_value_of_minus_one(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be equal to or greater than 1", validation.validate_generations(-1))

    def test_validate_generations_ok_for_value_of_one(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_generations(1))

    def test_validate_generations_cannot_be_more_than_max_for_value_of_101(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be equal to or less than 100", validation.validate_generations(101))

    def test_validate_generations_ok_for_value_of_100(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_generations(100))

    def test_validate_disease_trigger_must_be_greater_than_0_with_value_of_minus_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be greater than 0", validation.validate_disease_trigger(-1))

    def test_validate_disease_trigger_must_be_greater_than_0_with_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be greater than 0", validation.validate_disease_trigger(0))

    def test_validate_disease_trigger_must_be_greater_than_0_with_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_disease_trigger(1))

    def test_validate_adult_birth_rate_must_be_0_or_greater_for_value_of_minus_one(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_adult_birth_rate(-1))

    def test_validate_adult_birth_rate_must_be_0_or_greater_for_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_adult_birth_rate(0))

    def test_validate_adult_birth_rate_must_be_0_or_greater_for_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_adult_birth_rate(1))

    def test_validate_juvenile_survival_rate_must_be_0_or_greater_for_value_of_minus_one(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_juvenile_survival_rate(-1))

    def test_validate_juvenile_survival_rate_must_be_0_or_greater_for_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_juvenile_survival_rate(0))

    def test_validate_juvenile_survival_rate_must_be_0_or_greater_for_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_juvenile_survival_rate(1))
        
    def test_validate_juvenile_survival_rate_must_be_1_or_less_for_value_of_2(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 1 or less", validation.validate_juvenile_survival_rate(2))

    def test_validate_adult_survival_rate_must_be_0_or_greater_for_value_of_minus_one(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_adult_survival_rate(-1))

    def test_validate_adult_survival_rate_must_be_0_or_greater_for_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_adult_survival_rate(0))

    def test_validate_adult_survival_rate_must_be_0_or_greater_for_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_adult_survival_rate(1))

    def test_validate_adult_survival_rate_must_be_1_or_less_for_value_of_2(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 1 or less", validation.validate_adult_survival_rate(2))

    def test_validate_senile_survival_rate_must_be_0_or_greater_for_value_of_minus_one(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 0 or greater", validation.validate_senile_survival_rate(-1))

    def test_validate_senile_survival_rate_must_be_0_or_greater_for_value_of_0(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_senile_survival_rate(0))

    def test_validate_senile_survival_rate_must_be_0_or_greater_for_value_of_1(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual(None, validation.validate_senile_survival_rate(1))

    def test_validate_senile_survival_rate_must_be_1_or_less_for_value_of_2(self):
        validation = ModelRunOptionsValidation(1, 100)
        self.assertEqual("Must be 1 or less", validation.validate_senile_survival_rate(2))


class PopulationModelTests(TestCase):
    def test_new_model_has_one_generation(self):
        model = PopulationModel(ModelRunOptions(1, 2, 3, 100, 0, 0, 0, 0, 0))
        self.assertEqual(model.get_generations_count(), 1)

    def test_new_model_has_correct_first_generation(self):
        model = PopulationModel(ModelRunOptions(1, 2, 3, 100, 0, 0, 0, 0, 0))
        first_generation = model.get_generation(0)
        self.assertEqual(first_generation.juveniles, 1)
        self.assertEqual(first_generation.adults, 2)
        self.assertEqual(first_generation.seniles, 3)
        self.assertEqual(first_generation.disease_rate, 0)

    def test_model_runs_to_second_generation_with_survival_rate_of_point_five_birth_rate_of_two_no_disease(self):
        model = PopulationModel(ModelRunOptions(10, 10, 10, 1, 0.5, 0.5, 0.5, 2, 1000))
        model.run_all_generations()
        self.assertEqual(model.get_generations_count(), 2)
        second_generation = model.get_generation(1)
        self.assertEqual(second_generation.juveniles, 20)
        self.assertEqual(second_generation.adults, 5)
        self.assertEqual(second_generation.seniles, 10)

    def test_model_runs_to_second_generation_with_disease(self):
        model = PopulationModel(ModelRunOptions(10, 10, 10, 1, 0.5, 0.5, 0.5, 2, 1))
        model.run_all_generations()
        self.assertEqual(model.get_generations_count(), 2)
        second_generation = model.get_generation(1)
        self.assertGreater(second_generation.disease_rate, 19)
        self.assertLess(second_generation.disease_rate, 51)

    def test_specification_example(self):
        model = PopulationModel(ModelRunOptions(10, 10, 10, 5, 1, 1, 0, 2, 10000))
        model.run_all_generations()
        self.assert_generation(model.get_generation(0), 10, 10, 10, 0)
        self.assert_generation(model.get_generation(1), 20, 10, 10, 0)
        self.assert_generation(model.get_generation(2), 20, 20, 10, 0)
        self.assert_generation(model.get_generation(3), 40, 20, 20, 0)
        self.assert_generation(model.get_generation(4), 40, 40, 20, 0)
        self.assert_generation(model.get_generation(5), 80, 40, 40, 0)

    def assert_generation(self, generation, juvenile, adult, senile, disease_rate):
        self.assertEqual(generation.juveniles, juvenile)
        self.assertEqual(generation.adults, adult)
        self.assertEqual(generation.seniles, senile)
        self.assertEqual(generation.disease_rate, disease_rate)


class PopulationTests(TestCase):

    def test_initialisation_values(self):
        population = Population(1, 2, 3)
        self.assertEqual(population.get_count(LifecycleStage.Juvenile.value), 1)
        self.assertEqual(population.get_count(LifecycleStage.Adult.value), 2)
        self.assertEqual(population.get_count(LifecycleStage.Senile.value), 3)

    def test_total_population(self):
        population = Population(1, 2, 3)
        self.assertEqual(6, population.get_total_population())

    def test_random_disease_rate(self):
        for r in range(0, 100000):
            disease_rate = PopulationModel.random_disease_rate()
            self.assertLess(disease_rate, 51)
            self.assertGreater(disease_rate, 19)

    def test_create_generation_records_current_state(self):
        population = Population(1, 2, 3)
        generation = population.create_generation_from_current_state(0)
        self.assertEqual(generation.juveniles, 1)
        self.assertEqual(generation.adults, 2)
        self.assertEqual(generation.seniles, 3)
        self.assertEqual(generation.disease_rate, 0)

    def test_calculate_born_juveniles_birth_rate_of_one(self):
        self.calculate_born_juveniles(10, 1, 10)

    def test_calculate_born_juveniles_birth_rate_of_two(self):
        self.calculate_born_juveniles(10, 2, 20)

    def test_calculate_born_juveniles_birth_rate_of_one_point_five(self):
        self.calculate_born_juveniles(10, 1.5, 15)

    def test_calculate_born_juveniles_birth_rate_of_one_point_two_six(self):
        self.calculate_born_juveniles(10, 1.26, 12)

    def test_calculate_surviving_juveniles_survival_rate_of_one_disease_rate_of_zero(self):
        self.calculate_surviving_juveniles(10, 1, 0, 10)

    def test_calculate_surviving_juveniles_survival_rate_of_point_five_disease_rate_of_zero(self):
        self.calculate_surviving_juveniles(10, 0.5, 0, 5)

    def test_calculate_surviving_juveniles_survival_rate_of_point_two_six_disease_rate_of_zero(self):
        self.calculate_surviving_juveniles(10, 0.26, 0, 2)

    def test_calculate_surviving_juveniles_survival_rate_of_1_disease_rate_of_fifty(self):
        self.calculate_surviving_juveniles(10, 1, 50, 5)

    def test_calculate_surviving_juveniles_survival_rate_of_point_5_disease_rate_of_fifty(self):
        self.calculate_surviving_juveniles(10, 0.5, 50, 2)

    def test_calculate_surviving_adults_survival_rate_of_1(self):
        self.calculate_surviving_adults(10, 1, 10)

    def test_calculate_surviving_adults_survival_rate_of_point_five(self):
        self.calculate_surviving_adults(10, 0.5, 5)

    def test_calculate_surviving_adults_survival_rate_of_point_two_six(self):
        self.calculate_surviving_adults(10, 0.26, 2)

    def test_calculate_surviving_seniles_survival_rate_of_one_disease_rate_of_zero(self):
        self.calculate_surviving_seniles(10, 1, 0, 10)

    def test_calculate_surviving_seniles_survival_rate_of_point_five_disease_rate_of_zero(self):
        self.calculate_surviving_seniles(10, 0.5, 0, 5)

    def test_calculate_surviving_seniles_survival_rate_of_point_two_six_disease_rate_of_zero(self):
        self.calculate_surviving_seniles(10, 0.26, 0, 2)

    def test_calculate_surviving_seniles_survival_rate_of_1_disease_rate_of_fifty(self):
        self.calculate_surviving_seniles(10, 1, 50, 5)

    def test_calculate_surviving_seniles_survival_rate_of_point_5_disease_rate_of_fifty(self):
        self.calculate_surviving_seniles(10, 0.5, 50, 2)

    def test_calculate_surviving_seniles_survival_rate_of_one_disease_rate_of_20(self):
        self.calculate_surviving_seniles(10, 1, 20, 8)

    def test_update_to_next_generation_survival_rate_of_point_five_disease_rate_of_zero_birth_rate_of_two(self):
        population = Population(10, 10, 10)
        options = ModelRunOptions(10, 10, 10, 100, 0.5, 0.5, 0.5, 2, 1000)
        next_generation = population.update_to_next_generation(options, 0)
        self.assertEqual(next_generation.juveniles, 20)
        self.assertEqual(next_generation.adults, 5)
        self.assertEqual(next_generation.seniles, 10)
        self.assertEqual(next_generation.disease_rate, 0)

    def test_update_to_next_generation_survival_rate_of_point_five_disease_rate_of_fifty_birth_rate_of_two(self):
        population = Population(10, 10, 10)
        options = ModelRunOptions(10, 10, 10, 100, 0.5, 0.5, 0.5, 2, 1000)
        next_generation = population.update_to_next_generation(options, 50)
        self.assertEqual(next_generation.juveniles, 20)
        self.assertEqual(next_generation.adults, 2)
        self.assertEqual(next_generation.seniles, 7)
        self.assertEqual(next_generation.disease_rate, 50)

    def calculate_born_juveniles(self, adults: int, birth_rate: float, expected_juveniles):
        population = Population(0, adults, 0)
        born_juveniles = population.calculate_born_juveniles(birth_rate)
        self.assertEqual(expected_juveniles, born_juveniles)

    def calculate_surviving_juveniles(self, juveniles, survival_rate, disease_rate, expected_juveniles):
        population = Population(juveniles, 0, 0)
        surviving_juveniles = population.calculate_surviving_juveniles(survival_rate, disease_rate)
        self.assertEqual(surviving_juveniles, expected_juveniles)

    def calculate_surviving_adults(self, adults, survival_rate, expected_adults):
        population = Population(0, adults, 0)
        surviving_adults = population.calculate_surviving_adults(survival_rate)
        self.assertEqual(surviving_adults, expected_adults)

    def calculate_surviving_seniles(self, seniles, survival_rate, disease_rate, expected_seniles):
        population = Population(0, 0, seniles)
        surviving_seniles = population.calculate_surviving_seniles(survival_rate, disease_rate)
        self.assertEqual(surviving_seniles, expected_seniles)
