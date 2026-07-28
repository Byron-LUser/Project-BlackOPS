#this will clone the Malengo ISA
#list of countries and then their base salary in dollars
#after choosing they are shown the rates for the country
#then they enter their annual salary, and they are told how much they are paying in dollars

my_choice = None
new_choice = None
user_choice = None

developed_country = "14%"
developing_country = "12%"

#Dictionary: List of countries
countries = {
    # "Europe": {
        "Germany": 100000,
        "France": 97000,
        "Italy": 59800,
        "Uganda": 28000,
        "Spain": 200000,
        "Sweden": 78000,
        "Switzerland": 90000,
        "Poland": 57000,
        "Portugal": 60000,
        "United Kingdom": 90000,
        "Kenya": 30000,
        "Austria": 97000,
       # },

    #Asian countries
       # "Asia": {
        "China": 70000,
        "Russia": 97000,
        "India": 59800,
        "Japan": 300000,
        "South Korea": 28000,
        "North Korea": 160000,
        "Iran": 78000,
        "Israel": 90000,
        "Palestine": 57000,
        "Indonesia": 69000,
        "Malaysia": 90000,
        "Lebanon": 80000,
        "Iraq": 56000,
        "Vietnam": 65000,
        "Saudi Arabia": 90000,
       # }
    }

    #New function
def country_or_continent():
        pass

    #New function
def country_choice():

    print("\n========== Welcome to the Income Share Agreement! ==========")
    print("We believe you have read and understood the (TERMS and CONDITIONS) of the Program. ")
    print("\n\tWhich country from the list are you working in currently?")
    print("\n====================================")
    print(" \t\t\tCOUNTRIES")
    print("====================================")

    for my_index, key in enumerate(countries.keys(),  start=1):
        print(f"\t{my_index}.{key}")

    # Ask to choose their destination
    # Tell them the percentage

    tries = 3
    for try_count in range(tries):
        global my_choice
        my_choice = input("\nCountry Name: ")

        #validating the choice of continent
        if my_choice in countries.keys():
            return my_choice
        else:
            print("Please enter a valid choice")
        continue
    return None

    #New function
def income_return():
    for num_tries in range(3):
        try:
            salary = int(input("\nPlease enter your annual salary in dollars: "))
        except ValueError:
            print("Please enter a valid salary")
            continue
        if salary <= 27000:
            print("Your salary is too low to participate. you will be considered in the next round ")
            break
        else:
            print("You qualify to be part of the Income Share Agreement. Please proceed to HR ")
            break

        #Here we'll calculate the amount of money to be given back
    under = 14/100


    #New function
def find_employment():
    # print(""what is your area of specialty? ")
    # profession = input("Field: ")
   pass


#========================================================================
    #This function calls all the other functions
#========================================================================
def to_manage_function():
    #checking Work Status
    print("\n====================================")
    print(" \t\t\tEMPLOYMENT STATUS")
    print("====================================")

#checking employment status
#----------------------------------------------
    print("\n\tWelcome Proud Malengo Scholar.")
    employment_status = input("Are you currently employed? Please type (Yes or No): ").upper()
    if employment_status == "YES":
        country_choice()
        income_return()

        #Processing the "NO" Response
    elif employment_status == "NO":
        #Ask scholar if they would like to get a job
        get_job = input("\nWould you like to find a job? Please type (Yes or No):  ").upper()

        if get_job == "YES":
            print("Hold on, we'll refer you to Human Resource for further assistance. ")
        elif get_job == "NO":
            print("Alright. Thank you for working with us. ")
        else:
            print("Please enter a valid choice")

    else:
        print("Please enter a valid choice. ")

def main_function():
    # This function is the main function, no function gets called unless through this mother function
    to_manage_function()

main_function()




