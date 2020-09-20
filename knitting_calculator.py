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

def stitch_gauge():
    '''returns stitch gauge'''
    while True:
        try:
            stitch_gauge = float(input('Measuring over 10 cm / 4", how many stitches do you have? ')) / 10
            return stitch_gauge
        except:
            print('Please write a number for your answer.')
            continue

def row_gauge():
    '''returns row gauge'''
    while True:
        try:
            row_gauge = float(input('Measuring over 10 cm / 4", how many rows do you have? ')) / 10
            return row_gauge
        except:
            print('Please write a number for your answer.')
            continue

class Spacing:
    """Uses inital number and goal number to return instructions to distribute sts evenly"""
    def __init__(self, in_num, st_dif):
        self.in_num = in_num
        self.st_dif = st_dif
        self.st_quotient = self.in_num / self.st_dif

    def __repr__(self):
        return f'Spacing({self.in_num, self.st_dif})'

    def odd_even(self):
        """If increasing, use this unless your initial number and your stitch difference both are even and (in_num / st_dif) is uneven.
            If decreasing, use this unless (in_num - st_dif) and st_dif are both even and and ((in_num - st_dif)/ st_dif) is uneven"""

        num_of_mid = self.st_dif - 1 # the number of repeats between sts_start and sts_end
        sts_mid_rep = int(((self.in_num - (self.in_num % self.st_dif)) / self.st_dif)) # the number of sts pr. repeat
        mid_reps_total = num_of_mid * sts_mid_rep # the total number of sts used in middle repeats
        remainder = self.in_num - mid_reps_total # the number of sts left for sts_start and sts_end when completing mid_reps
        sts_start = math.ceil(remainder / 2)  # the number of sts to be knitted before mid_reps
        sts_end = math.floor(remainder / 2)  # the number of sts to be knitted after mid_reps
        spacing_dict = {"sts_start": sts_start, "sts_mid_rep": sts_mid_rep, "num_of_mid": num_of_mid, "sts_end": sts_end}

        return spacing_dict

    def odd_quotient(self):
        """If increasing, use this unless your initial number and your stitch difference both are even and (in_num / st_dif) is uneven.
            If decreasing, use this unless (in_num - st_dif) and st_dif are both even and and ((in_num - st_dif)/ st_dif) is uneven"""
        # the number of sts in middle of work
        num_mid = math.floor(self.st_quotient / 2) * 2
        # the number of repeats between middle and either side
        sts_side_rep = int((self.st_dif - 2) / 2)
        # the number of sts in side repeats
        sts_in_rep = int(self.st_quotient)
        sts_start_end = math.ceil(self.st_quotient / 2)
        spacing_dict = {"sts_start_end": sts_start_end, "sts_side_rep": sts_side_rep,
                        "num_mid": num_mid, "sts_in_rep": sts_in_rep}
        return spacing_dict

    def horizontal_spacing(self):
        if self.st_dif > 0:
            in_num_mod = self.in_num % 2
            st_dif_mod = self.st_dif % 2
            if in_num_mod == st_dif_mod == 0 and self.st_quotient % 2 != 0:
                spacing_dict = self.odd_quotient()
                spacing_string = f'k{spacing_dict["sts_start_end"]}, m1, *k{spacing_dict["sts_in_rep"]}, m1* ' \
                       f'{spacing_dict["sts_side_rep"]} times, k{spacing_dict["num_mid"]}, m1, *k{spacing_dict["sts_in_rep"]}, m1* ' \
                       f'k{spacing_dict["sts_side_rep"]} times, k{spacing_dict["sts_start_end"]}'
            else:
                spacing_dict = self.odd_even()
                spacing_string = f'k{spacing_dict["sts_start"]}, m1, *k{spacing_dict["sts_mid_rep"]}, m1* {spacing_dict["num_of_mid"]} times, ' \
                       f'k{spacing_dict["sts_end"]}'
        else: # if st_dif is negative, ie. when decreasing sts.
            self.in_num += self.st_dif
            self.st_dif *= -1
            self.st_quotient = self.in_num / self.st_dif
            in_num_mod = self.in_num % 2
            st_dif_mod = self.st_dif % 2
            if in_num_mod == st_dif_mod == 0 and self.st_quotient % 2 != 0:
                spacing_dict = self.odd_quotient()
                spacing_dict["sts_in_rep"] -= 1
                spacing_dict["num_mid"] -= 2
                spacing_string = f'k{spacing_dict["sts_start_end"]}, dec 1, *k{spacing_dict["sts_in_rep"]}, dec 1* ' \
                       f'{spacing_dict["sts_side_rep"]} times, k{spacing_dict["num_mid"]}, dec 1, *k{spacing_dict["sts_in_rep"]}, dec 1* ' \
                       f'k{spacing_dict["sts_side_rep"]} times, k{spacing_dict["sts_start_end"]}'
            else:
                spacing_dict = self.odd_even()
                spacing_dict["sts_start"] -= 1
                spacing_dict["sts_end"] -=1
                spacing_dict["sts_mid_rep"] -= 1
                spacing_string =  f'k{spacing_dict["sts_start"]}, dec 1, *k{spacing_dict["sts_mid_rep"]}, dec 1* {spacing_dict["num_of_mid"]} times, ' \
                       f'k{spacing_dict["sts_end"]}'
        return spacing_string

    def vertical_spacing(self, num_of_rows):
        if self.st_dif > 0:
            remainder = num_of_rows % self.st_dif
            num_of_inc_rows = int(self.st_dif / 2)
            rows_per_rep = int((num_of_rows - remainder) / num_of_inc_rows)
            dec_string = f'Work {rows_per_rep + 1} rows. Next row: work 1, increase 1, work to 1 st before end, increase 1, work 1. ' \
                   f'Repeat inc row every {rows_per_rep} rows {num_of_inc_rows - 1} times ({num_of_inc_rows} times ' \
                   f'total). Work {remainder} rows.'
        else:
            self.st_dif *= -1
            remainder = num_of_rows % self.st_dif
            num_of_dec_rows = int(self.st_dif / 2)
            rows_per_rep = int((num_of_rows - remainder) / num_of_dec_rows)
            dec_string = f'Work {rows_per_rep + 1} rows. Next row: work 1, decrease 1, work to 1 st before end, decrease, work 1. ' \
                   f'Repeat dec row every {rows_per_rep} rows {num_of_dec_rows - 1} times ({num_of_dec_rows} times ' \
                   f'total). Work {remainder} rows.'
        return dec_string

def new_yarn(yardage1, yardage2, num_of_skeins):
    """using the differing yardages, returns changed number of balls/skeins needed. 1 decimal.
    Works with any unit of measurement, but consistency is necessary"""
    return round((num_of_skeins * yardage1) / yardage2, 1)

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
            circumf = float(length * 1.05)
            return (length, circumf)
    return

class Socks:
    def __init__(self, length, circumf, row_gauge, st_gauge):
        self.length = length
        self.circumf = circumf
        self.row_gauge = row_gauge
        self.st_gauge = st_gauge
        prelim_leg = self.circumf * self.st_gauge
        self.st_in_leg = int(prelim_leg - (prelim_leg % 4))
        self.half_leg = int(self.st_in_leg / 2)
        self.mid = int(self.st_in_leg * 0.14 - ((self.st_in_leg * 0.14) % 2))
        self.toe_length = int(self.length * 0.2)
        self.rows_in_leg = int((self.length - self.toe_length) * row_gauge)

    def __repr__(self):
        return f'Socks({self.length}, {self.circumf}, {self.row_gauge}, {self.st_gauge})'

    def stock_socks(self):
        return f'LEG: Cast on {self.st_in_leg} stitches and distribute evenly on 4 double pointed needles. ' \
               f'Join stitches, being careful not to twist. ' \
               f'*K1, P1* to end. Repeat rib row until work measures 1.5 centimetres. ' \
               f'Change to stockinette (k all sts) and work until you have knitted {self.rows_in_leg} rows from rib, or ' \
               f'until work has desired length for leg. ' \
               f'HEEL: The short-row heel is worked over {self.half_leg} stitches. When the instructions state "knit to end", ' \
               f'it is the end of these stitches. Ie. if you are working on 4 DPNs, knit to end of second needle. ' \
               f'K to 1 st before end, W&T. P to 1 st before end, W&T. ' \
               f'*K to 1 st before previously wrapped st, W&T. P to 1 st before previously wrapped st, W&T.* ' \
               f'Repeat from * to * until you have {self.mid} unwrapped sts left in the middle. ' \
               f'Work one round across all sts (including sts on hold), working wraps and wrapped sts together. ' \
               f'K until end of previously unwrapped sts in middle of heel, W&T. ' \
               f'P until end of previously unwrapped sts in middle of heel, W&T. ' \
               f'*K to wrapped st, work st together with wrap, W&T. P to wrapped st, work st together with wrap, W&T* ' \
               f'Repeat from * to * until all sts on heel have been worked and you have 1 wrapped st on either side of heel. ' \
               f'Knit one round where wraps and wrapped sts are worked together. ' \
               f'FOOT: Work in stockinette (k all sts) until you have worked {self.rows_in_leg} rows since last heel row, ' \
               f'or until work from tip of heel measures {self.toe_length} centimetres less than desired length ' \
               f'TOE: Row 1: *K1, K2tog, k {self.half_leg - 6}, ssk, k1*. Repeat from * to *. ' \
               f'Row 2: K all sts. Repeat rows 1 & 2 until {self.mid * 2} sts are remaining. ' \
               f'Graft remaining sts together using kitchener st.'

    def rib_socks(self):
        return f'LEG: Cast on {self.st_in_leg} stitches and distribute evenly on 4 double pointed needles. ' \
               f'Join stitches, being careful not to twist. ' \
               f'*K2, P2* to end. Repeat rib row until until you have knitted {self.rows_in_leg}, or ' \
               f'until work has desired length for leg. ' \
               f'HEEL: The short-row heel is worked over {self.half_leg} stitches. When the instructions state "knit to end", ' \
               f'it is the end of these stitches. Ie. if you are working on 4 DPNs, knit to end of second needle. ' \
               f'K to 1 st before end, W&T. P to 1 st before end, W&T. ' \
               f'*K to 1 st before previously wrapped st, W&T. P to 1 st before previously wrapped st, W&T.* ' \
               f'Repeat from * to * until you have {self.mid} unwrapped sts left in the middle. ' \
               f'Work one round across all sts, working wraps and wrapped sts together ' \
               f'and working held sts in rib as established.' \
               f'K until end of previously unwrapped sts in middle of heel, W&T. ' \
               f'P until end of previously unwrapped sts in middle of heel, W&T. ' \
               f'*K to wrapped st, work st together with wrap, W&T. P to wrapped st, work st together with wrap, W&T* ' \
               f'Repeat from * to * until all sts on heel have been worked and you have 1 wrapped st on either side of heel. ' \
               f'Work one round where wraps and wrapped sts are worked together and held sts are worked in rib as established. ' \
               f'FOOT: Work bottom of foot in stockinette (k all sts) and top of foot in rib ' \
               f'until you have worked {self.rows_in_leg} rows since last heel row, ' \
               f'or until work from tip of heel measures {self.toe_length} centimetres less than desired length ' \
               f'TOE: Row 1: *K1, K2tog, k {self.half_leg - 6}, ssk, k1*. Repeat from * to *. ' \
               f'Row 2: K all sts. Repeat rows 1 & 2 until {self.mid * 2} sts are remaining. ' \
               f'Graft remaining sts together using kitchener st.'


class BustDarts:
    def __init__(self, b_s2u_b, f_s2u_b, row_gauge, st_gauge, centre_width, front_st):
        """returns instructions for knitting bust darts using Ysolda's method. Works only with centimetres"""
        #b_s2u_b = the back measurement from top of shoulder to the horizontal line directly under the bust
        #f_s2u_b = the front measurement from top of shoulder to the horizontal line directly under the bust, i.e including bust
        self.b_s2u_b = b_s2u_b
        self.f_s2u_b = f_s2u_b
        self.row_gauge = row_gauge
        self.st_gauge = st_gauge
        self.centre_width = centre_width
        self.front_st = front_st
        self.dart_depth = self.f_s2u_b - self.b_s2u_b
        #dart depths shorter than 5 centimetres are not recommended
        if self.dart_depth < 5:
            raise ValueError
        elif self.dart_depth >= 5 and self.dart_depth < 7.5:
            prelim_rows_in_dart = 2.5 * self.row_gauge
        else:
            prelim_rows_in_dart = self.dart_depth * self.row_gauge - 5
        if prelim_rows_in_dart % 2 <= 1:
            self.rows_in_dart = int(prelim_rows_in_dart - prelim_rows_in_dart % 2)
        else:
            self.rows_in_dart = int(prelim_rows_in_dart + (1 - (prelim_rows_in_dart % 2 % 1)))
        self.num_of_turns = int(self.rows_in_dart / 2)
        self.st_per_dart = int((self.front_st - ((self.centre_width + 5) * self.st_gauge)) / 2)
        self.st_per_turn = int(self.st_per_dart / self.num_of_turns)

    def top_down(self):
        '''To be used for sweaters worked from the top down.'''
        return f'Dart is worked over {self.rows_in_dart} rows: \n' \
               f'K to {self.st_per_dart} before end, W&T. P to {self.st_per_dart} before end, W&T.\n' \
               f'*K to wrapped st, work wrap together with st, k {self.st_per_turn - 1}, W&T.\n' \
               f'P to wrapped st, work wrap together with st, k {self.st_per_turn - 1}, W&T.*\n' \
               f'Repeat from * to * {self.num_of_turns - 2} times ({self.num_of_turns - 1} times total).\n' \
               f'On the first row after having completed all the dart rows, work all wraps together with wrapped st. \n'

    def bottom_up(self):
        '''To be used for sweaters worked from the bottom up.'''
        return f'Dart is worked over {self.rows_in_dart} rows: \n' \
               f'K to 1 st before end, W&T. P to 1 st before end, W%T.\n' \
               f'*K to {self.st_per_turn - 1} before last wrapped st, W&T. \n' \
               f'P to {self.st_per_turn - 1} before last wrapped st, W&T*.\n' \
               f'Repeat from * to * {self.num_of_turns - 2} times ({self.num_of_turns - 1} times total).\n' \
               f'On the first row after having completed all the dart rows, work remaining wraps together with wrapped st. \n'

bust_darts = BustDarts(20, 25, 4, 2.8, 15, 100)
print(bust_darts.top_down())
