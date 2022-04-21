import pandas as pd
from pathlib import Path

iPath = Path("learning-python/boilerplate-demographic-data-analyzer")

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(iPath / "adult.data.csv")
    #df = pd.read_csv("adult.data.csv")
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts()

    # What is the average age of men?
    aveMen = df[(df["sex"] == "Male")]
    average_age_men = round(aveMen["age"].sum() / len(aveMen["age"]), 1)

    # What is the percentage of people who have a Bachelor's degree?
    dff = df["education"].value_counts("Bachelors")
    percentage_bachelors = round(dff.loc["Bachelors"] * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    df50k = df[(df["salary"] != "<=50K")]
    count50k = len(df50k)
    countB50k = len(df50k[(df50k["education"] == "Bachelors")])
    countM50k = len(df50k[(df50k["education"] == "Masters")])
    countD50k = len(df50k[(df50k["education"] == "Doctorate")])
    countBT50k = len(df[(df["education"] == "Bachelors")])
    countMT50k = len(df[(df["education"] == "Masters")])
    countDT50k = len(df[(df["education"] == "Doctorate")])
    countTotalHigh = countBT50k + countMT50k + countDT50k
    countTotalLow = len(df) - countTotalHigh

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    # percentage with salary >50K
    higher_education_rich = round(((countB50k + countM50k + countD50k) / countTotalHigh) * 100, 1)
    lower_education_rich = round(((count50k - (countB50k + countM50k + countD50k)) / countTotalLow) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()
    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[(df["hours-per-week"] == min_work_hours)].count()
    num_min_workers = num_min_workers["hours-per-week"]

    rich_percentage = df[(df["hours-per-week"] == min_work_hours) & (df["salary"] == ">50K")].count()
    rich_percentage = rich_percentage["salary"]
    rich_percentage /= num_min_workers
    rich_percentage = round(rich_percentage * 100, 1)

    countriesDict = dict ()
    # What country has the highest percentage of people that earn >50K?
    
    country_salary = df[(df["salary"] == ">50K")]
    country_salary = country_salary[["native-country", "salary"]]
    country_salary = country_salary.rename(columns = {"native-country": "native-country-rich"})
    country_salary = country_salary["native-country-rich"].value_counts()
    country_salary2 = df["native-country"].value_counts()
    country_salary = dict(country_salary)
    country_salary2 = dict(country_salary2)
    for v in country_salary:
        aux = round((country_salary.get(v) / country_salary2.get(v))*100, 1)
        countriesDict[v] = aux
    countriesList = list(countriesDict.items())
    countriesList.sort(key = lambda x : x[1], reverse = True)

    highest_earning_country = countriesList[0][0]
    highest_earning_country_percentage = countriesList[0][1]


    # Identify the most popular occupation for those who earn >50K in India.
    teste = df[(df["salary"] == ">50K") & (df["native-country"] == "India")]
    teste = dict(teste["occupation"].value_counts())
    teste = list(teste.items())
    top_IN_occupation = teste[0][0]
    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
