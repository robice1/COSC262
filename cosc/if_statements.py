substance = input("What substance? ")
ph = float(input("Enter the measured pH: "))
if ph < 7:
    print(f"{substance} is acidic")
    print("Be careful with that!")
elif ph == 7:
    print(f"{substance} has radioactive properties, how he is still living is still unknown. He is a freak of nature. ")
else:
    print(f"{substance} is NOT acidic")
    print("But that doesn't mean it's safe")
