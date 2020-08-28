# Det jeg gerne vil, er at lave en strikkeregnemaskine, der kan
# 1. Udregne fordeling af udtagning/indtagning på én pind. **
# 2. Udregne fordeling af udtagning/indtagning over flere pinde. **
# 3. Udregne brystindsnit baseret på Ysoldas metode. **
# 4. Udregne nyt antal nøgler, hvis man ønsker at skifte garn ** – måske med Ravelrys API? *
# 5. Give en strømpeopskrift enten i glatstrik eller med ribbet top,
#    baseret på skostørrelse og strikkefasthed *
# ** er mest væsentligt, * er mere nice to have.
# Scriptet skal byde velkommen og så spørge, hvad man ønsker at gøre.
# Svaret skal tages som input og så lede over i et af fem subscripts.
# De tre sidste subscripts kræver en strikkefasthed,
# og det kan derfor måske være en god idé at lave en klasse med dette?
# Skostørrelse kan bruges til en dictionary med længde i cm.
# Alle fem subscripts skal give mulighed for at lave en .pdf-fil, så de kan printes.
# Subscript 1 skal tage input: Strikker du rundt eller fladt?
# Hvor mange masker har du? Hvor mange masker skal du ende med?
# Hvis slutantallet er større -> tillægsfunktion
# Hvis slutantallet er mindre -> fratrækningsfunktion
# Og så give instruktioner til, hvordan dette skal gøres og tilbyde, om det skal laves til en .pdf-fil.
# Hvis ja, lægges filen på skrivebordet eller der spørges, hvor den skal gemmes.
# Subscript 2 gør det samme, men over flere pinde. Udregningen kan være den samme,
# men outputtet skal være anderledes.
# skal tage input. Hvad er din strikkefasthed?
# Vil du tillægge eller fjerne vidde? Hvor mange cm starter du med?
# Hvor mange cm vil du lægge til / trække fra? Over hvor mange cm skal det gøres?
# Og så give instruktioner til, hvordan dette skal gøres og tilbyde, om det skal laves til en .pdf-fil.
# Subscript 4 skal spørge enten, hvor mange nøgler, der skal bruges af det oprindelige garn
# og hvor mange meter, der er pr. nøgle (eller find denne information med Ravelrys API) og så spørge,
# hvor mange meter, der er pr. nøgle på det garn, man erstatter med (eller find denne information med
# Ravelrys API). Så skal output være antallet af nøgler, der skal bruges af det nye garn.
# Subscript 5 skal tage input. Hvad er din strikkefasthed?
# Vil du lave glatstrikkede strømper eller sokker med ribstrik på toppen?
# Hvilken størrelse vil du lave? Hvor langt skal skaftet være?
# Til sidst printes instruktioner og .pdf-fil tilbydes.
# Til sidst spørges, om man ønsker at gøre mere. Hvis ja, køres programmet igen, hvis nej, tak for i dag.

import math

def shoe_size():
    """Returns a tuple containing the length and width of the shoe size entered by user"""
    while True:
        size = int(input("This calculator accepts European shoe sizes between 18 and 51. Please enter your size here: "))
        if size < 18 or size > 51:
            print(size)
            print("Sorry, that is not a valid size. Please use numbers to enter a European size between 18 and 51.")
            continue
        else:
            length = float((size - 2) / 1.5)
            width = float(length * 1.05)
            return (length, width)

def gauge():
    """Returns a tuple containing the stitch gauge and row gauge pr. cm based on input from the user"""
    while True:
        try:
            stitch_gauge = float(input('Measuring over 10 cm / 4", how many stitches do you have? ')) / 10
        except:
            print('Please write a number for your answer.')
            continue
        try:
            row_gauge = float(input('Measuring over 10 cm / 4", how many rows do you have? ')) / 10
            return (stitch_gauge, row_gauge)
        except:
            print('Please write a number for your answer.')
            continue

class Spacing:
    """Uses inital number and goal number to return a dictionary with values to distribute the difference evenly."""
    def __init__(self, in_num, st_dif):
        self.in_num = in_num
        self.st_dif = st_dif

    def odd_even_divisor(self):
        """If increasing, use this unless your initial number and your stitch difference both are even and (in_num / st_dif) is uneven.
            If decreasing, use this unless (in_num - st_dif) and st_dif are both even and and ((in_num - st_dif)/ st_dif) is uneven"""

        num_of_mid = self.st_dif - 1 # the number of repeats between sts_start and sts_end
        sts_mid_rep = int(((self.in_num - (self.in_num % self.st_dif)) / self.st_dif)) # the number of sts pr. repeat
        mid_reps_total = num_of_mid * sts_mid_rep # the total number of sts used in middle repeats
        remainder = self.in_num - mid_reps_total # the number of sts left for sts_start and sts_end when completing mid_reps
        sts_start = math.ceil(remainder / 2)  # the number of sts to be knitted before mid_reps
        sts_end = math.ceil(remainder / 2)  # the number of sts to be knitted after mid_reps
        spacing_dict = {"sts_start": sts_start, "sts_mid_rep": sts_mid_rep, "num_of_mid": num_of_mid, "sts_end": sts_end}
        # f'k{spacing_dict["sts_start"]}, m1, *k{spacing_dict["sts_mid_rep"]}, m1* {spacing_dict[num_of_mid]} times, k{spacing_dict["sts_end"]}')
        return spacing_dict

    def even_divisor(self):
        """If increasing, use this unless your initial number and your stitch difference both are even and (in_num / st_dif) is uneven.
            If decreasing, use this unless (in_num - st_dif) and st_dif are both even and and ((in_num - st_dif)/ st_dif) is uneven"""
        num_mid = math.floor((self.in_num/self.st_dif) / 2) * 2 # the number of sts in middle of work
        sts_side_rep = int((self.st_dif - 2) / 2) # the number of repeats between middle and either side
        sts_in_rep = int(self.in_num/self.st_dif) # the number of sts in side repeats
        sts_start = math.ceil((self.in_num/self.st_dif) / 2)
        sts_end = math.ceil((self.in_num/self.st_dif) / 2)
        spacing_dict = {"sts_start": sts_start, "sts_side_rep": sts_side_rep, "num_mid": num_mid, "sts_in_rep": sts_in_rep, "sts_end": sts_end}
        return spacing_dict

    #def get_spacing(self):


test = Spacing(20,4)
spacing_dict = test.even_divisor()
#print(spacing_dict["num_of_mid"])
print(f'k{spacing_dict["sts_start"]}, m1, *k{spacing_dict["sts_in_rep"]}, m1* {spacing_dict["sts_side_rep"]} times, '
      f'k{spacing_dict["num_mid"]}, m1, *k{spacing_dict["sts_in_rep"]}, m1* {spacing_dict["sts_side_rep"]} times, k{spacing_dict["sts_end"]}')
#print(f'k{spacing_dict["sts_start"]}, m1, *k{spacing_dict["sts_mid_rep"]}, m1* {spacing_dict["num_of_mid"]} times, k{spacing_dict["sts_end"]}')
