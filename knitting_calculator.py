
import math

def prompt_for_int(question):
    while True:
        try:
            return int(input(question))
        except:
            print("Please enter an integer.")

def prompt_for_float(question):
    while True:
        try:
            return int(input(question))
        except:
            print("Please enter a number.")

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
    def __init__(self, st_dif, in_num = None):
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
            incdec_string = f'Work {rows_per_rep + 1} rows. Next row: work 1, increase 1, work to 1 st before end, increase 1, work 1. ' \
                   f'Repeat inc row every {rows_per_rep} rows {num_of_inc_rows - 1} times ({num_of_inc_rows} times ' \
                   f'total). Work {remainder} rows.'
        else:
            self.st_dif *= -1
            remainder = num_of_rows % self.st_dif
            num_of_dec_rows = int(self.st_dif / 2)
            rows_per_rep = int((num_of_rows - remainder) / num_of_dec_rows)
            incdec_string = f'Work {rows_per_rep + 1} rows. Next row: work 1, decrease 1, work to 1 st before end, decrease, work 1. ' \
                   f'Repeat dec row every {rows_per_rep} rows {num_of_dec_rows - 1} times ({num_of_dec_rows} times ' \
                   f'total). Work {remainder} rows.'
        return incdec_string

def inc_sts():
    while True:
        try:
            newans = input("Are you increasing \n(H) on a single row, ie. horizontally? \n"
                           "(V) over several rows, ie. vertically?")
            if newans.upper() == 'H':
                init_num = prompt_for_int("How many stitches do you have before increasing? ")
                diff_st = prompt_for_int("How many stitches do you want to increase? ")
                increases_hor = Spacing(diff_st, init_num)
                print(increases_hor.horizontal_spacing())
                break
            elif newans.upper() == 'V':
                rows = prompt_for_int("How many rows will you being increasing over? ")
                stitches = prompt_for_int("How many stitches do you want to increase? ")
                increase_ver = Spacing(st_dif = stitches)
                print(increase_ver.vertical_spacing(rows))
                break
            else:
                raise Exception
        except:
            print("Please choose either H or V.")
            continue

def dec_sts():
    while True:
        try:
            newans = input("Are you decreasing \n(H) on a single row, ie. horizontally? \n"
                           "(V) over several rows, ie. vertically?")
            if newans.upper() == 'H':
                init_num = prompt_for_int("How many stitches do you have before decreasing? ")
                diff_st = prompt_for_int("How many stitches do you want to decrease? ") * -1
                decreases_hor = Spacing(diff_st, init_num)
                print(decreases_hor.horizontal_spacing())
                break
            elif newans.upper() == 'V':
                rows = prompt_for_int("How many rows will you being decreasing over? ")
                stitches = prompt_for_int("How many stitches do you want to decrease? ") * -1
                decrease_ver = Spacing(st_dif = stitches)
                print(decrease_ver.vertical_spacing(rows))
                break
            else:
                raise Exception
        except:
            print("Please choose either H or V.")
            continue

def run_spacing():
    while True:
        try:
            answer = input("Do you want to increase stitches (I) or decrease stitches (D)?")
            if answer.upper() == 'I':
                inc_sts()
                break
            elif answer.upper() == 'D':
                dec_sts()
                break
            else:
                raise Exception
        except:
            print("Please choose either I or D.")
            continue


def new_yarn(yardage1, yardage2, num_of_skeins):
    """using the differing yardages, returns changed number of balls/skeins needed. 1 decimal.
    Works with any unit of measurement, but consistency is necessary"""
    return round((num_of_skeins * yardage1) / yardage2, 1)

def shoe_size():
    """Returns a tuple containing the length and width of the shoe size entered by user"""
    while True:
        size = int(input("This calculator accepts European shoe sizes between 18 and 51. Please enter your shoe size here: "))
        if size < 18 or size > 51:
            print("Sorry, that is not a valid size. Please use numbers to enter a European size between 18 and 51.")
            continue
        else:
            length = float((size - 2) / 1.5)
            circumf = float(length * 1.05)
            return (length, circumf)
    return

class Socks:
    def __init__(self, st_gauge, row_gauge, length, circumf,):
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
        return f'LEG: Cast on {self.st_in_leg} stitches and distribute evenly on 4 double pointed needles. \n' \
               f'Join stitches, being careful not to twist. \n' \
               f'*K1, P1* to end. Repeat rib row until work measures 1.5 centimetres. \n' \
               f'Change to stockinette (k all sts) and work until you have knitted {self.rows_in_leg} rows from rib, \n' \
               f'or until work has desired length for leg. \n' \
               f'HEEL: The short-row heel is worked over {self.half_leg} stitches. When the instructions state "knit to end", \n' \
               f'it is the end of these stitches. Ie. if you are working on 4 DPNs, knit to end of second needle. \n' \
               f'K to 1 st before end, W&T. P to 1 st before end, W&T. \n' \
               f'*K to 1 st before previously wrapped st, W&T. P to 1 st before previously wrapped st, W&T.* \n' \
               f'Repeat from * to * until you have {self.mid} unwrapped sts left in the middle. \n' \
               f'Work one round across all sts (including sts on hold), working wraps and wrapped sts together. \n' \
               f'K until end of previously unwrapped sts in middle of heel, W&T.\n' \
               f'P until end of previously unwrapped sts in middle of heel, W&T. \n' \
               f'*K to wrapped st, work st together with wrap, W&T. P to wrapped st, work st together with wrap, W&T* \n' \
               f'Repeat from * to * until all sts on heel have been worked and you have 1 wrapped st on either side of heel.\n' \
               f'Knit one round where wraps and wrapped sts are worked together.\n' \
               f'FOOT: Work in stockinette (k all sts) until you have worked {self.rows_in_leg} rows since last heel row,\n' \
               f'or until work from tip of heel measures {self.toe_length} centimetres less than desired length \n' \
               f'TOE: Row 1: *K1, K2tog, k {self.half_leg - 6}, ssk, k1*. Repeat from * to *. \n' \
               f'Row 2: K all sts. Repeat rows 1 & 2 until {self.mid * 2} sts are remaining. \n' \
               f'Graft remaining sts together using kitchener st.'

    def rib_socks(self):
        return f'LEG: Cast on {self.st_in_leg} stitches and distribute evenly on 4 double pointed needles. \n' \
               f'Join stitches, being careful not to twist. \n' \
               f'*K2, P2* to end. Repeat rib row until until you have knitted {self.rows_in_leg} rows, or ' \
               f'until work has desired length for leg.\n' \
               f'HEEL: The short-row heel is worked over {self.half_leg} stitches. When the instructions state "knit to end", \n' \
               f'it is the end of these stitches. Ie. if you are working on 4 DPNs, knit to end of second needle. \n' \
               f'K to 1 st before end, W&T. P to 1 st before end, W&T. \n' \
               f'*K to 1 st before previously wrapped st, W&T. P to 1 st before previously wrapped st, W&T.* \n' \
               f'Repeat from * to * until you have {self.mid} unwrapped sts left in the middle. \n' \
               f'Work one round across all sts, working wraps and wrapped sts together \n' \
               f'and working held sts in rib as established.\n' \
               f'K until end of previously unwrapped sts in middle of heel, W&T. \n' \
               f'P until end of previously unwrapped sts in middle of heel, W&T. \n' \
               f'*K to wrapped st, work st together with wrap, W&T. P to wrapped st, work st together with wrap, W&T* \n' \
               f'Repeat from * to * until all sts on heel have been worked and you have 1 wrapped st on either side of heel. \n' \
               f'Work one round where wraps and wrapped sts are worked together and held sts are worked in rib as established. \n' \
               f'FOOT: Work bottom of foot in stockinette (k all sts) and top of foot in rib \n' \
               f'until you have worked {self.rows_in_leg} rows since last heel row,\n' \
               f'or until work from tip of heel measures {self.toe_length} centimetres less than desired length \n' \
               f'TOE: Row 1: *K1, K2tog, k {self.half_leg - 6}, ssk, k1*. Repeat from * to *. \n' \
               f'Row 2: K all sts. Repeat rows 1 & 2 until {self.mid * 2} sts are remaining.\n' \
               f'Graft remaining sts together using kitchener st.'

class BustDarts:
    def __init__(self, b_s2u_b, f_s2u_b, centre_width, front_st, st_gauge, row_gauge):
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
        self.st_per_turn = int((self.st_per_dart - (self.st_per_dart % self.num_of_turns)) / self.num_of_turns)
        self.st_in_point = int(self.st_per_turn + (self.st_per_dart % self.num_of_turns))

    def __repr__(self):
        '''Returns a string with the input variables'''
        return f'BustDarts(b_s2u_b={self.b_s2u_b}, f_s2u_b={self.f_s2u_b}, row_gauge={self.row_gauge},' \
               f' st_gauge={self.st_gauge}, centre_width={self.centre_width}, front_st={self.front_st})'

    def top_down(self):
        '''To be used for sweaters worked from the top down.'''
        return f'Dart is worked over {self.rows_in_dart} rows: \n' \
               f'K to {self.st_per_dart} before end, W&T. P to {self.st_per_dart} before end, W&T.\n' \
               f'*K to wrapped st, work wrap together with st, k {self.st_per_turn - 1}, W&T.\n' \
               f'P to wrapped st, work wrap together with st, p {self.st_per_turn - 1}, W&T.*\n' \
               f'Repeat from * to * {self.num_of_turns - 3} times ({self.num_of_turns - 1} times total).\n' \
               f'K to wrapped st, work wrap together with st, k to 1 st before end, W&T.\n' \
               f'P to wrapped st, work wrap together with st, p to 1 st before end, W&T.\n' \
               f'On the first row after having completed all the dart rows, work all wraps together with wrapped st. \n'

    def bottom_up(self):
        '''To be used for sweaters worked from the bottom up.'''
        return f'Dart is worked over {self.rows_in_dart} rows: \n' \
               f'K to 1 st before end, W&T. P to 1 st before end, W%T.\n' \
               f'K to {self.st_in_point - 1} before last wrapped st, W&T. \n' \
               f'P to {self.st_in_point - 1} before last wrapped st, W&T\n' \
               f'*K to {self.st_per_turn - 1} before last wrapped st, W&T. \n' \
               f'P to {self.st_per_turn - 1} before last wrapped st, W&T*.\n' \
               f'Repeat from * to * {self.num_of_turns - 3} times ({self.num_of_turns - 2} times total).\n' \
               f'On the first row after having completed all the dart rows, work remaining wraps together with wrapped st. \n'


def dart_input():
    print("When taking your measurements, try to wear the bra you plan to wear with the finished garment, "
          "or at least one with a similar fit. \nIf that means no bra, that's cool too! ")
    back_sh2bu = prompt_for_float("The first measurement we need is the back shoulder to under bust.\n"
                       "On your back, measure from the top of your shoulder to right under your bust\n"
                       "– where the bottom of your bra band is or would be. How many centimeters is that? ")
    front_sh2bu = prompt_for_float("The next measurement we need is the front shoulder to under bust.\n"
                              "On your front, measure from the top of your shoulder to right under your bust "
                              "(your measuring tape should follow your boob curve) \n"
                              "– where the bottom of your bra band is or would be. How many centimeters is that? ")
    if front_sh2bu-back_sh2bu < 5:
        print("When the difference between the front and back shoulder to under bust measurement is less than 5 centimeters,\n"
              "bust darts aren't a great choice – consider adding extra stitches in the sides instead?")
        return
    cen_width = prompt_for_float("We'll also need a centre width. Please measure across your bust between the most prominent points "
                            "(that'll probably be your nipples). \nHow many centimeters is that? ")
    front_sts = prompt_for_int("How many stitches are on the front half of your sweater? ")

    return (back_sh2bu, front_sh2bu, cen_width, front_sts)


def run_bust_darts():
    while True:
        try:
            dart_answer = input("Bust darts are worked differently depending on the direction of your knitting.\n"
                                "Are you working from the top down (T) or from the bottom up (B)? ")
            if dart_answer.upper() == 'T':
                print(
                    "Cool! I love me some top-down knitting. It's so nice to be able to try things on as you go along.\n"
                    "We're going to need your measurements and a gauge swatch.")
                back_sh2bu, front_sh2bu, cen_width, front_sts = dart_input()
                stgauge = stitch_gauge()
                rgauge = row_gauge()
                darts = BustDarts(back_sh2bu, front_sh2bu, cen_width, front_sts, stgauge, rgauge)
                print(darts.top_down())
                break
            elif dart_answer.upper() == 'B':
                print("Awesome! Bottom-up knitting is a classic for a reason!\n"
                      "We're going to need your measurements and a gauge swatch.")
                back_sh2bu, front_sh2bu, cen_width, front_sts = dart_input()
                stgauge = stitch_gauge()
                rgauge = row_gauge()
                darts = BustDarts(back_sh2bu, front_sh2bu, cen_width, front_sts, stgauge, rgauge)
                print(darts.top_down())
                break
            else:
                raise Exception
        except:
            print("Please choose either T or B")
            continue



def run_socks():
    while True:
        try:
            sock_answer = input("Do you want to knit ribbed socks (R) or stockinette socks (S)? ")
            if sock_answer.upper() == 'R':
                print("We're going to need your gauge for that! "
                      "Please make a gauge swatch in your preferred yarn "
                      "if you have not already done so.")
                user_stitch_gauge = stitch_gauge()
                user_row_gauge = row_gauge()
                length, circum = shoe_size()
                socks = Socks(user_stitch_gauge, user_row_gauge, length, circum)
                print(socks.rib_socks())
                break
            elif sock_answer.upper() == 'S':
                print("We're going to need your gauge for that! "
                      "Please make a gauge swatch in your preferred yarn "
                      "if you have not already done so.")
                user_stitch_gauge = stitch_gauge()
                user_row_gauge = row_gauge()
                length, circum = shoe_size()
                socks = Socks(user_stitch_gauge, user_row_gauge, length, circum)
                print(socks.stock_socks())
                break
            else:
                raise Exception
        except:
            print('Please choose either R or S.')
            continue

def run_new_yardage():
        num_of_skeins = prompt_for_int("How many skeins/balls of the old yarn do you need? ")
        old_len = prompt_for_int("What is the yardage/meterage (yards or meters per ball/skein) "
                                "of the original yarn? ")
        new_len = prompt_for_int("What is the yardage/meterage (yards or meters per ball/skein) "
                                "of the new yarn? ")
        print(f"You'll need {new_yarn(old_len, new_len, num_of_skeins)} "
                  f"balls/skeins of your new yarn.")


while True:
    try:
        start_answer = input("What do you want to do?\n"
              "1) Calculate a sock pattern.\n"
              "2) Calculate bust darts.\n"
              "3) Calculate how much yarn you'll need when switching from the yarn in your pattern.\n"
              "4) Space increases or decreases evenly. ")

        if start_answer == '1':
            run_socks()
        elif start_answer == '2':
            run_bust_darts()
        elif start_answer == '3':
            run_new_yardage()
            break
        elif start_answer == '4':
            run_spacing()
        else:
            raise Exception
    except:
        print('Please choose a number between 1 and 4.')
        continue
    break