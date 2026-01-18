## input-->Rent,Food Order,Electricity,charge per unit,househelp,grocery,no.of person

Rent=int(input("Enter The Rent:"))
Food_order=int(input("Enter The amount of food order:"))
Electricity=int(input("ENter Total unit of enlectricity consumed:"))
charge_per_unit=int(input("Enter the per unit charge of electricity:"))
househelp=int(input("Enter the househelp salary:"))
Grocery=int(input("Enter Grocery Bill:"))
no_of_person=int(input("NUmber of roommate:"))

Total=Rent+Food_order+(Electricity*charge_per_unit)+househelp+Grocery

per_person=Total//no_of_person

print(f"Per person amount is {per_person}")