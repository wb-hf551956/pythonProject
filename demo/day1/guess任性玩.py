# Author:hufei

age_of_oldboy = 56
count = 0
while count < 3:
    guess_age = int(input("guess age:"))
    if guess_age == age_of_oldboy:
        print("you got it")
        break
    elif guess_age > age_of_oldboy:
        print("think smaller...")
    else:
        print("think bigger!")
    count +=1
    if count == 3:
        continue_confirm = input("do you want to keep guessing..?")
        if continue_confirm !='n':
            count = 0


