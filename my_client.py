

print("Lamda function")
print("\nyoun have only five tries")

count = 0
while True:
    count += 1
    if count == 6:
        break
    if range == 2:
        print("Those are two tries, one remaning.")
    elif range == 3:
        print("Those are three tries. You had your chances.")

    #my_addition = lambda x: x + 1
#OR
    def my_addition(x):
        result = x+1
        return result
    
    try:
        result = my_addition(int(input("number: ")))
        print(result)
    except ValueError:
        print("please enter a number: ")

    print(count, "Tries now")
    


    # print("Do you want to go again? y/n")
    # go_again = input("REsponse: ")
    # if go_again.upper() == "Y":
    #     continue
    # elif go_again.upper() == "N":
    #     print("See you next time. ")
    #     break
    # else:
    #     print("Invalid response. Bye")
    #     break



    