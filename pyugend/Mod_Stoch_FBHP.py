"""
Stochastic Model FBHP
---------------------





Notes:

04/30/2016 - this model is in development and not yet ready. The skeleton
still reflects the FSHP model. I have to add the banded structure to this.



"""



__author__ = 'krishnab'
__version__ = '0.1.0'


from operator import neg, truediv
import numpy as np
import pandas as pd
from numpy.random import binomial
from pyugend.Models import Base_model




class Mod_Stoch_FBHP(Base_model):

    def __init__(self, **kwds):
        Base_model.__init__(self, **kwds)
        self.name = "Stochastic Model(sim_orig)"
        self.label = "promote-hire"
    def run_model(self):

        ## initialize data structure

        self.res = np.zeros([self.duration, 12], dtype=np.float32)

        self.res[0, 0] = self.nf1
        self.res[0, 1] = self.nf2
        self.res[0, 2] = self.nf3
        self.res[0, 3] = self.nm1
        self.res[0, 4] = self.nm2
        self.res[0, 5] = self.nm3
        self.res[0, 6] = self.vac3
        self.res[0, 7] = self.vac2
        self.res[0, 8] = self.vac1
        self.res[0, 9] = self.female_promotion_probability_1
        self.res[0, 10] = self.female_promotion_probability_2
        self.res[0, 11] = np.float32(
            sum(list([self.nf1, self.nf2, self.nf3])) / sum(list([self.nf1,
                                                                  self.nf2,
                                                                  self.nf3,
                                                                  self.nm1,
                                                                  self.nm2,
                                                                  self.nm3])))

        hiring_rate_female_level_1 = self.bf1
        hiring_rate_female_level_2 = self.bf2
        hiring_rate_female_level_3 = self.bf3
        attrition_rate_female_level_1 = self.df1
        attrition_rate_female_level_2 = self.df2
        attrition_rate_female_level_3 = self.df3
        attrition_rate_male_level_1 = self.dm1
        attrition_rate_male_level_2 = self.dm2
        attrition_rate_male_level_3 = self.dm3
        probability_of_outside_hire_level_3 = self.phire3
        probability_of_outside_hire_level_2 = self.phire2
        male_promotion_probability_1_2 = self.male_promotion_probability_1
        male_promotion_probability_2_3 = self.male_promotion_probability_2
        department_size_upper_bound = self.upperbound
        department_size_lower_bound = self.lowerbound
        variation_range = self.variation_range
        unfilled_vacanies = 0
        change_to_level_1 = 0
        change_to_level_2 = 0
        change_to_level_3 = 0

        for i in range(1, self.duration):
            # initialize variables for this iteration



            prev_number_of_females_level_1 = self.res[i - 1, 0]
            prev_number_of_females_level_2 = self.res[i - 1, 1]
            prev_number_of_females_level_3 = self.res[i - 1, 2]
            prev_number_of_males_level_1 = self.res[i - 1, 3]
            prev_number_of_males_level_2 = self.res[i - 1, 4]
            prev_number_of_males_level_3 = self.res[i - 1, 5]
            prev_number_of_vacancies_level_3 = self.res[i - 1, 6]
            prev_number_of_vacancies_level_2 = self.res[i - 1, 7]
            prev_number_of_vacancies_level_1 = self.res[i - 1, 8]
            prev_promotion_rate_female_level_1 = self.female_promotion_probability_1
            prev_promotion_rate_female_level_2 = self.female_promotion_probability_2
            department_size = self.res[i - 1, 0:6].sum()


            # Process Model

            # Determine department size variation for this timestep


            # first both female and males leave the department according to binomial probability.

            female_attrition_level_3 = binomial(prev_number_of_females_level_3,
                                                attrition_rate_female_level_3)

            male_attrition_level_3 = binomial(prev_number_of_males_level_3,
                                              attrition_rate_male_level_3)

            # the departures create a set of vacancies. These vacancies are the basis for new hiring
            total_vacancies_3 = female_attrition_level_3 + \
                                male_attrition_level_3 + change_to_level_3

            # women are hired first and then men
            hiring_female_3 = binomial(max(0,total_vacancies_3),
                                       probability_of_outside_hire_level_3 * hiring_rate_female_level_3)
            hiring_male_3 = binomial(max(0, total_vacancies_3 - hiring_female_3),
                                     probability_of_outside_hire_level_3 * (
                                         1 - hiring_rate_female_level_3))

            total_hiring_3 = hiring_female_3 + hiring_male_3

            # level 3 vacancies that are not filled by new hires create opportunities
            # for promotion from level 2. Again women are promoted first and men second.
            # Also note the error trap that if we try to promote more professors from
            # level 2 than there exist at level 2, then we will prevent this from happening.

            vacancies_remaining_after_hiring_3 = total_vacancies_3 - total_hiring_3

            potential_promotions_after_hiring_3 = max(0,
                                                      vacancies_remaining_after_hiring_3)

            promotions_of_females_level_2_3 = binomial(min(
                potential_promotions_after_hiring_3,
                prev_number_of_females_level_2),
                prev_promotion_rate_female_level_2)

            promotions_of_males_level_2_3 = binomial(max(0,min(
                potential_promotions_after_hiring_3-promotions_of_females_level_2_3,
                prev_number_of_males_level_2)), male_promotion_probability_2_3)

            # attrition at level 2 - either people leave from attrition or promotion

            female_attrition_level_2 = binomial(
                max(0,
                    prev_number_of_females_level_2 - promotions_of_females_level_2_3),
                attrition_rate_female_level_2)

            male_attrition_level_2 = binomial(max(0,
                                                  prev_number_of_males_level_2 - promotions_of_males_level_2_3),
                                              attrition_rate_male_level_2)

            # the departures create a set of vacancies. These vacancies are the basis for new hiring
            total_vacancies_2 = sum(list([female_attrition_level_2,
                                          male_attrition_level_2,
                                          promotions_of_females_level_2_3,
                                          promotions_of_males_level_2_3,
                                          change_to_level_2]))

            hiring_female_2 = binomial(max(0,total_vacancies_2),
                                       probability_of_outside_hire_level_2 * hiring_rate_female_level_2)
            hiring_male_2 = binomial(max(0,total_vacancies_2-hiring_female_2),
                                     probability_of_outside_hire_level_2 * (1-hiring_rate_female_level_2))

            total_hiring_2 = hiring_female_2 + hiring_male_2

            vacancies_remaining_after_hiring_2 = total_vacancies_2 - total_hiring_2

            potential_promotions_after_hiring_2 = max(0,
                                                      vacancies_remaining_after_hiring_2)

            promotions_of_females_level_1_2 = binomial(max(0,
                min(potential_promotions_after_hiring_2, prev_number_of_females_level_1)),
                prev_promotion_rate_female_level_1)
            promotions_of_males_level_1_2 = binomial(max(0,min(
                potential_promotions_after_hiring_2 - promotions_of_females_level_1_2, prev_number_of_males_level_1)),
                male_promotion_probability_1_2)


            ## Level 1

            female_attrition_level_1 = binomial(max(0,prev_number_of_females_level_1-promotions_of_females_level_1_2),
                                                attrition_rate_female_level_1)

            male_attrition_level_1 = binomial(max(0,prev_number_of_males_level_1-promotions_of_males_level_1_2),
                                              attrition_rate_male_level_1)
            total_vacancies_1 = sum(list([female_attrition_level_1,
                                          male_attrition_level_1,
                                          promotions_of_females_level_1_2,
                                          promotions_of_males_level_1_2,
                                          change_to_level_1]))

            hiring_female_1 = binomial(max(0,total_vacancies_1),
                                       hiring_rate_female_level_1)
            hiring_male_1 = binomial(max(0,total_vacancies_1 - hiring_female_1),
                                     1 - hiring_rate_female_level_1)

            # Write state variables to array and move to next iteration

            self.res[i, 0] = number_of_females_level_1 = sum(
                list([prev_number_of_females_level_1,
                      neg(female_attrition_level_1),
                      neg(promotions_of_females_level_1_2),
                      hiring_female_1]))

            assert (number_of_females_level_1 >= 0), "negative number of females 1"


            self.res[i, 1] = number_of_females_level_2 = max(0, sum(
                list([prev_number_of_females_level_2,
                      neg(female_attrition_level_2),
                      neg(promotions_of_females_level_2_3),
                      promotions_of_females_level_1_2,
                      hiring_female_2])))
            self.res[i, 2] = number_of_females_level_3 = sum(list([
                prev_number_of_females_level_3,
                neg(female_attrition_level_3),
                promotions_of_females_level_2_3,
                hiring_female_3]))

            self.res[i, 3] = number_of_males_level_1 = sum(list([
                prev_number_of_males_level_1,
                neg(male_attrition_level_1),
                neg(promotions_of_males_level_1_2),
                hiring_male_1]))

            self.res[i, 4] = number_of_males_level_2 = sum(
                list([prev_number_of_males_level_2,
                      neg(male_attrition_level_2),
                      neg(promotions_of_males_level_2_3),
                      promotions_of_males_level_1_2,
                      hiring_male_2]))

            self.res[i, 5] = number_of_males_level_3 = sum(
                list([prev_number_of_males_level_3,
                      neg(male_attrition_level_3),
                      promotions_of_males_level_2_3,
                      hiring_male_3]))

            self.res[i, 6] = sum(list([
                male_attrition_level_3,
                female_attrition_level_3]))

            self.res[i, 7] = sum(list([
                male_attrition_level_2,
                female_attrition_level_2,
                promotions_of_females_level_2_3,
                promotions_of_males_level_2_3]))

            self.res[i, 8] = sum(list([
                male_attrition_level_1,
                female_attrition_level_1,
                promotions_of_males_level_1_2,
                promotions_of_females_level_1_2]))

            self.res[i, 9] = self.female_promotion_probability_1
            self.res[i, 10] = self.female_promotion_probability_2
            self.res[i, 11] = np.float32(
                truediv(sum(list([number_of_females_level_1,
                                  number_of_females_level_2,
                                  number_of_females_level_3])), sum(list([
                    number_of_females_level_1,
                    number_of_females_level_2,
                    number_of_females_level_3,
                    number_of_males_level_1,
                    number_of_males_level_2,
                    number_of_males_level_3]))))

            unfilled_vacanies = abs(department_size - self.res[i, 0:6].sum())

            # this produces an array of values. Then I need to assign the
            # values to levels. So if I have say a range of variation of 5. I
            #  will get something like [-1,0,1,-1,0] or something. I need to
            # turn this into something like [2,-1,0]. That means randomly
            # assigning the values in the array to levels.
            department_size = self.res[i, 0:6].sum()

            flag = False
            while flag == False:
                # changes = np.append(np.random.choice([-1, 0, 1],
                #                                      variation_range),
                #                     np.ones(department_size_upper_bound -
                #                             self.res[i,0:6].sum()))
                changes = np.ones(department_size_upper_bound -
                                  self.res[i, 0:6].sum())
                # random
                # growth/shrink

                levels = np.random.choice([1, 2, 3],
                                          department_size_upper_bound -
                                          self.res[i, 0:6].sum()
                                          )  #
                # random level
                # choice

                # need to test whether the candidate changes keep the
                # department size within bounds.
                # print(["old dept size:", department_size,
                #        "new dept size:", self.res[i, 0:6].sum(),
                #        "candidate:", department_size +
                #        changes.sum(),
                #        " added postions: ", changes.sum(),
                #        "unfilled ", unfilled_vacanies])
                if (department_size <=
                        department_size_upper_bound):
                    change_to_level_3 = np.int(changes[np.where(levels ==
                                                                3)[0]].sum())
                    change_to_level_2 = np.int(changes[np.where(levels ==
                                                                2)[0]].sum())
                    change_to_level_1 = np.int(changes[np.where(levels ==
                                                                1)[0]].sum())
                    flag = True

                if (department_size > department_size_upper_bound):
                    change_to_level_3 = 0
                    change_to_level_2 = 0
                    change_to_level_1 = 0

                    flag = True

            #print(i)
            # print(self.res[i,:])
            ## Print Data matrix

        df_ = pd.DataFrame(self.res)
        df_.columns = ['f1',
                       'f2',
                       'f3',
                       'm1',
                       'm2',
                       'm3',
                       't3',
                       't2',
                       't1',
                       'prom1',
                       'prom2',
                       'gendprop']
        # print(df_)
        recarray_results = df_.to_records(index=True)
        self.run = recarray_results
        return recarray_results
