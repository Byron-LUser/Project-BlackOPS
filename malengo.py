import math

#In this program we shall print a list of countries in europe asia and Africa or America
#we shall then let the user type a country they want to work in
#then calculate how much they will contribute

def this_import_another():
    countries = {
        "Germany": {
            "capital": "Berlin",
            "currency": "EUR",
            "monthly_living_cost": 1200,
            "flight_cost": 700,
            "average_salary": 3200,
            "malengo_percentage": 12
        },

        "Canada": {
            "capital": "Ottawa",
            "currency": "CAD",
            "monthly_living_cost": 1800,
            "flight_cost": 900,
            "average_salary": 4000,
            "malengo_percentage": 10
        },

        "Japan": {
            "capital": "Tokyo",
            "currency": "JPY",
            "monthly_living_cost": 2000,
            "flight_cost": 1100,
            "average_salary": 3500,
            "malengo_percentage": 14
        },

        "Kenya": {
            "capital": "Nairobi",
            "currency": "KES",
            "monthly_living_cost": 700,
            "flight_cost": 250,
            "average_salary": 1200,
            "malengo_percentage": 8
        },

        "Brazil": {
            "capital": "Brasilia",
            "currency": "BRL",
            "monthly_living_cost": 900,
            "flight_cost": 850,
            "average_salary": 1500,
            "malengo_percentage": 9
        },

        "Australia": {
            "capital": "Canberra",
            "currency": "AUD",
            "monthly_living_cost": 2500,
            "flight_cost": 1300,
            "average_salary": 5000,
            "malengo_percentage": 15
        },

        "France": {
            "capital": "Paris",
            "currency": "EUR",
            "monthly_living_cost": 1600,
            "flight_cost": 750,
            "average_salary": 3100,
            "malengo_percentage": 11
        },

        "India": {
            "capital": "New Delhi",
            "currency": "INR",
            "monthly_living_cost": 500,
            "flight_cost": 400,
            "average_salary": 900,
            "malengo_percentage": 7
        },

        "South Africa": {
            "capital": "Pretoria",
            "currency": "ZAR",
            "monthly_living_cost": 800,
            "flight_cost": 300,
            "average_salary": 1400,
            "malengo_percentage": 8
        },

        "United States": {
            "capital": "Washington D.C.",
            "currency": "USD",
            "monthly_living_cost": 2800,
            "flight_cost": 1200,
            "average_salary": 5500,
            "malengo_percentage": 15
        }
    }

    # --------------------------------------------
    # FUNCTIONS
    # --------------------------------------------

    def display_countries():
        print("\nAVAILABLE COUNTRIES:\n")

        for index, country in enumerate(countries.keys(), start=1):
            print(f"{index}. {country}")

        print()


    def get_country_by_number(choice):
        country_list = list(countries.keys())

        if 1 <= choice <= len(country_list):
            return country_list[choice - 1]

        return None


    def calculate_travel_cost(country_name, months):
        country = countries[country_name]

        flight = country["flight_cost"]
        living = country["monthly_living_cost"] * months

        # extra estimated expenses
        food = 250 * months
        transport = 100 * months

        total = flight + living + food + transport

        return {
            "flight": flight,
            "living": living,
            "food": food,
            "transport": transport,
            "total": total
        }


    def recommend_affordable_country(budget, months):
        affordable = []

        for country_name in countries:
            costs = calculate_travel_cost(country_name, months)

            if costs["total"] <= budget:
                affordable.append((country_name, costs["total"]))

        if affordable:
            affordable.sort(key=lambda x: x[1])
            return affordable[0]

        return None


    def explore_option():
        print("\n===== EXPLORE COUNTRIES =====")

        try:
            budget = float(input("Enter your budget in USD: "))
            months = int(input("How many months will you stay? "))

            display_countries()

            choice = int(input("Choose a country number: "))

            selected_country = get_country_by_number(choice)

            if not selected_country:
                print("Invalid country choice.")
                return

            costs = calculate_travel_cost(selected_country, months)

            print("\n========== TRAVEL REPORT ==========")
            print(f"Country: {selected_country}")
            print(f"Capital City: {countries[selected_country]['capital']}")
            print(f"Currency: {countries[selected_country]['currency']}")

            print("\n------ COST BREAKDOWN ------")
            print(f"Flight Cost: ${costs['flight']}")
            print(f"Living Cost: ${costs['living']}")
            print(f"Food Cost: ${costs['food']}")
            print(f"Transport Cost: ${costs['transport']}")

            print("\n-----------------------------------")
            print(f"TOTAL COST: ${costs['total']}")

            remaining = budget - costs["total"]

            if remaining >= 0:
                print(f"Remaining Balance: ${remaining}")
                print("Good news! Your budget is enough.")
            else:
                print(f"You are short by: ${abs(remaining)}")

                recommendation = recommend_affordable_country(
                    budget,
                    months
                )

                if recommendation:
                    print("\nSuggested Affordable Destination:")
                    print(f"{recommendation[0]} "
                          f"(Estimated Cost: ${recommendation[1]})")
                else:
                    print("No destination matches your current budget.")

        except ValueError:
            print("Please enter valid numbers.")


    def work_option():
        print("\n===== WORK ABROAD =====")

        try:
            budget = float(input("Enter your current savings in USD: "))

            display_countries()

            choice = int(input("Choose a country number: "))

            selected_country = get_country_by_number(choice)

            if not selected_country:
                print("Invalid country choice.")
                return

            country = countries[selected_country]

            support_amount = 10000

            salary = country["average_salary"]

            percentage = country["malengo_percentage"]

            monthly_repayment = salary * (percentage / 100)

            repayment_months = math.ceil(
                support_amount / monthly_repayment
            )

            print("\n========== WORK ABROAD REPORT ==========")

            print(f"Destination Country: {selected_country}")
            print(f"Capital City: {country['capital']}")
            print(f"Average Monthly Salary: ${salary}")

            print("\n------ MALE NGO ISA PROGRAM ------")
            print(f"Training/Support Given: ${support_amount}")
            print(f"ISA Repayment Percentage: {percentage}%")

            print(f"\nEstimated Monthly Repayment: "
                  f"${monthly_repayment:.2f}")

            print(f"Estimated Repayment Duration: "
                  f"{repayment_months} months")

            if budget < country["flight_cost"]:
                print("\nWARNING:")
                print("Your savings may not cover flight expenses.")

            else:
                print("\nYour savings can cover initial travel expenses.")

        except ValueError:
            print("Please enter valid numbers.")


    # --------------------------------------------
    # MAIN PROGRAM
    # --------------------------------------------

    while True:

        print("\n====================================")
        print(" GLOBAL TRAVEL & WORK ADVISOR ")
        print("====================================")

        print("1. Explore Countries")
        print("2. Work Abroad")
        print("3. Exit")

        option = input("\nChoose an option: ")

        if option == "1":
            explore_option()

        elif option == "2":
            work_option()

        elif option == "3":
            print("\nThank you for using the system.")
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")