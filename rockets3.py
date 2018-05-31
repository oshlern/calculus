import math, time, sys
import matplotlib.pyplot as plot

VEL_TARG = 42 # velocity to escape the sun, in Km/s
PAYLOAD = 1000 # payload mass, in Kg
eng_dict_print = { # dictionary of types of engines and exhaust velocity in Km/s, formatted for print
    'Solid' : 2.5,
    'NK-33' : 3.25,
    'Liquid' : 4.4,
    'SSME' : 4.44,
    'Ramjet' : 7.8,
    'J-58' : 19,
    'EJ200 reheat minimum' : 20.4,
    'EJ200 reheat maximum' : 21.3,
    'Ion' : 29,
    'Jet' : 29,
    'RR/SO 593' : 29.5,
    'VASIMR minimum' : 30,
    'EJ200 dry minimum' : 44,
    'EJ200 dry maximum' : 48,
    'Boeing CF6' : 58.4,
    'GE CF6' : 115,
    'VASIMR maximum' : 120,
    'Magnetoplasmic' : 160,
    'Electrostatic Ion' : 210,
}
eng_dict = { # dictionary of types of engines and exhaust velocity in Km/s, including leeway for input
    'Solid' : 2.5, 'solid' : 2.5,
    'NK-33' : 3.25, 'NK33' : 3.25, 'NK 33' : 3.25, 'nk-33' : 3.25, 'nk 33' : 3.25, 'nk33' : 3.25,
    'Liquid' : 4.4 , 'liquid' : 4.4,
    'SSME' : 4.44, 'ssme' : 4.44,
    'Ramjet' : 7.8, 'ramjet' : 7.8,
    'J-58' : 19, 'J58' : 19, 'J 58' : 19, 'j-58' : 19, 'j58' : 19, 'j 58' : 19,
    'EJ200 reheat minimum' : 20.4, 'EJ200 reheat min' : 20.4, 'ej200 reheat minimum' : 20.4, 'ej200 reheat min' : 20.4,
    'EJ200 reheat maximum' : 21.3, 'EJ200 reheat max' : 21.3, 'ej200 reheat maximum' : 21.3, 'ej200 reheat max' : 21.3,
    'Ion' : 29, 'ion' : 29,
    'Jet' : 29, 'jet' : 29,
    'RR/SO 593' : 29.5, 'RRSO 593' : 29.5, 'RRSO593' : 29.5, 'rr/so 593' : 29.5, 'rrso 593' : 29.5, 'rrso593' : 29.5,
    'VASIMR minimum' : 30, 'VASIMR min' : 30, 'vasimr minimum' : 30, 'vasimr min' : 30,
    'EJ200 dry minimum' : 44, 'EJ200 dry min' : 44, 'ej200 dry minimum' : 44, 'ej200 dry min' : 44,
    'EJ200 dry maximum' : 48, 'EJ200 dry max' : 48, 'ej200 dry maximum' : 48, 'ej200 dry max' : 48,
    'Boeing CF6' : 58.4, 'Boeing cf6' : 58.4, 'boeing CF6' : 58.4, 'boeing cf6' : 58.4,
    'GE CF6' : 115, 'GE cf6' : 115, 'ge CF6' : 115, 'ge cf6' : 115,
    'VASIMR maximum' : 120, 'VASIMR max' : 120, 'vasimr maximum' : 120, 'vasimr max' : 120,
    'Magnetoplasmic' : 160, 'magnetoplasmic' : 160,
    'Electrostatic Ion' : 210, 'electrostatic ion' : 210
}

def check_test():
    print("Testing? y/n")
    test = str(input())
    if test == 'y':
        print("Test active")
        testing_flag = True
    else:
        print("Test inactive")
        testing_flag = False
    return testing_flag

def printslow(testing_flag, text):
    if testing_flag == True:
        print(text)
    else:
        for x in text:
            sys.stdout.write(x)
            sys.stdout.flush()
            time.sleep(0.05)
        print('\n')

def get_inputs(testing_flag, PAYLOAD, eng_dict_print, eng_dict):
    eng_vel_list = []
    eng_size_list = []
    key_list = []
    eng_type_num = 0
    for key, value in eng_dict.items():
        key_list.append(key)
    printslow(testing_flag, "Input total rocket mass, including fuel, in Kg (numbers only, must be at least " + str(PAYLOAD) + " Kg).")
    rocket_mass_total = int(input())
    while rocket_mass_total < PAYLOAD:
        printslow(testing_flag, "Error: rocket mass too small. Must be at least " + str(PAYLOAD) + " Kg. Please try again.")
        rocket_mass_total = int(input())
        if rocket_mass_total >= PAYLOAD:
            break
    printslow(testing_flag, "Valid rocket mass.")
    print("------- \n")
    printslow(testing_flag, "Input total fuel mass in Kg (numbers only, must be less than or equal to " + str(0.9 * rocket_mass_total) + " Kg).")
    fuel_mass_total = int(input())
    while rocket_mass_total - fuel_mass_total < (0.1 * fuel_mass_total):
        printslow(testing_flag, "Error: fuel mass too large for rocket. Must be less than or equal to " + str(0.9 * rocket_mass_total) + " Kg). Please try again.")
        fuel_mass_total = int(input())
        if rocket_mass_total - fuel_mass_total >= (0.1 * fuel_mass_total):
            break
    printslow(testing_flag, "Valid fuel mass.")
    print("------- \n")
    printslow(testing_flag, "Input number of engines (numbers only).")
    printslow(testing_flag, "Note that you will have to individually define these in a bit.")
    eng_num = int(input())
    while eng_num == 0:
        printslow(testing_flag, "Error: engine number cannot be 0. Please try again.")
        eng_num = int(input())
        if eng_num != 0:
            break
    printslow(testing_flag, "Calculating for " + str(eng_num) + " engines.")
    printslow(testing_flag, "Engine type options (19)\n\nName - Exhaust Velocity in Km/s")
    for key, value in eng_dict_print.items():
        printslow(testing_flag, str(key) + " - " + str(value))
    print("------- \n")
    eng_size_total = 0
    eng_size_left = 100
    eng_iter = eng_num
    for x in range(eng_num):
        printslow(testing_flag, "Input type of engine #" + str(eng_num - eng_iter + 1))
        printslow(testing_flag, "Type only name (exact capitalization doesn't matter)")
        eng_type = str(input())
        while eng_type not in eng_dict:
            printslow(testing_flag, "Error: invalid engine type. Please try again.")
            eng_type = str(input())
            if eng_type in eng_dict:
                break
        eng_vel_list.append(eng_dict[eng_type])
        if eng_iter != 1:
            printslow(testing_flag, "Input size of engine #" + str(eng_num - eng_iter + 1) + " as percent of total fuel.")
            printslow(testing_flag, "Type only numbers (no percent sign).")
            printslow(testing_flag, "Percent of total fuel left: " + str(eng_size_left) + "% (" + str(fuel_mass_total * (eng_size_left/100)) + " Kg).")
            eng_size = int(input())
            while eng_size > eng_size_left:
                printslow(testing_flag, "Error: not enough available fuel. Please try again.")
                eng_size = int(input())
            while eng_size == 0:
                printslow(testing_flag, "Error: fuel percentage cannot be 0. Please try again.")
                eng_size = int(input())
        else:
            printslow(testing_flag, "Last engine uses remaining fuel: " + str(eng_size_left) + "% (" + str(fuel_mass_total * (eng_size_left/100)) + " Kg).")
            eng_size = eng_size_left
        eng_size_list.append(eng_size)
        eng_size_total += eng_size
        eng_size_left = 100 - eng_size_total
        printslow(testing_flag, "Engine #" + str(eng_num - eng_iter + 1) + " recorded.")
        printslow(testing_flag, "Type: " + str(eng_type) + ", size: " + str(eng_size) + "% of fuel or " + str(fuel_mass_total * (eng_size/100)) + " Kg.")
        print("------- \n")
        eng_iter -= 1
    if eng_size_total != 100:
        printslow(testing_flag, "Error: engine sizes do not add up to 100%. Program error.")
    else:
        printslow(testing_flag, "Valid engine sizes.")
    print("------- \n")
    return rocket_mass_total, fuel_mass_total, eng_num, eng_size_list, eng_vel_list

def calculate(PAYLOAD, VEL_TARG, testing_flag, rocket_mass_total, fuel_mass_total, eng_num, eng_size_list, eng_vel_list):
    vel_burnout_total = 0
    rocket_mass_struct = rocket_mass_total - fuel_mass_total
    rocket_mass_left = rocket_mass_total + PAYLOAD
    stages_list = []
    current_list = []
    struct_list = []
    pay_list = []
    vel_list = []
    for eng in range(eng_num):
        eng_display = eng + 1
        stages_list.append(eng_display)
        printslow(testing_flag, "Calculating for stage #" + str(eng_display) + ".")
        eng_mass_fuel = fuel_mass_total * (eng_size_list[eng]/100)
        printslow(testing_flag, "Fuel engine mass for engine #" + str(eng_display) + ": " + str(eng_mass_fuel) + " Kg.")
        eng_mass_struct = rocket_mass_struct * (eng_size_list[eng]/100)
        printslow(testing_flag, "Structural engine mass for engine #" + str(eng_display) + ": " + str(eng_mass_struct) + " Kg.")
        current_eng_mass = eng_mass_fuel + eng_mass_struct
        current_list.append(current_eng_mass)
        printslow(testing_flag, "Mass of current stage: " + str(current_eng_mass) + " Kg.")
        rocket_mass_left -= current_eng_mass
        printslow(testing_flag, "Engine #" + str(eng_display) + " pushing " + str(rocket_mass_left) + " Kg.")
        struct_ratio = (eng_mass_struct)/(current_eng_mass)
        struct_list.append(struct_ratio)
        printslow(testing_flag, "Structural ratio: " + str(struct_ratio))
        pay_ratio = (rocket_mass_left)/(current_eng_mass)
        pay_list.append(pay_ratio)
        printslow(testing_flag, "Payload ratio: " + str(pay_ratio))
        eng_vel = eng_vel_list[eng]
        vel_burnout_eng = eng_vel * (math.log(struct_ratio + ((1 - struct_ratio) * pay_ratio)))
        vel_list.append(vel_burnout_eng)
        vel_burnout_total += vel_burnout_eng
        printslow(testing_flag, "Engine #" + str(eng_display) + " velocity at burnout: " + str(vel_burnout_eng) + " Km/s.")
        print("------- \n")
    printslow(testing_flag, "Total velocity at burnout: " + str(vel_burnout_total) + " Km/s.")
    if vel_burnout_total >= VEL_TARG:
        vel_excess = vel_burnout_total - VEL_TARG
        printslow(testing_flag, "Escaped sun with " + str(vel_excess) + " Km/s.")
    else:
        vel_short = VEL_TARG - vel_burnout_total
        printslow(testing_flag, "Did not escape by " + str(vel_short) + " Km/s.")
    print("------- \n")
    calc_done = True
    return calc_done, stages_list, current_list, struct_list, pay_list, vel_list

def plot_values(stages_list, current_list, struct_list, pay_list, vel_list):
    plot.figure(1)
    plot.title("Stage Mass Over Time")
    plot.plot(stages_list, current_list, 'b^-', label = "Stage Mass")
    plot.legend(loc = "upper right")
    plot.xlabel("Stage Number")
    plot.ylabel("Mass in Kg")
    plot.figure(2)
    plot.title("Structural and Payload Ratio by Stage")
    plot.plot(stages_list, struct_list, 'g^-', label = "Structural Ratio")
    plot.plot(stages_list, pay_list, 'k^-', label = "Payload Ratio")
    plot.legend(loc = "center left")
    plot.xlabel("Stage Number")
    plot.ylabel("Ratio")
    plot.figure(3)
    plot.title("Burnout Velocity by Stage")
    plot.plot(stages_list, vel_list, 'r^-', label = "Velocity")
    plot.legend(loc = "upper left")
    plot.xlabel("Stage Number")
    plot.ylabel("Velocity in Km/s")
    plot.show()

if __name__ == "__main__":
    while True:
        testing_flag = check_test()
        printslow(testing_flag, "This program only uses engine velocities and ignores specific impulses, so it is not technically an accurate simulation of a rocket launch.")
        printslow(testing_flag, "This also assumes that engines instantly use all of their fuel to acheive burnout velocity, are promptly jettisonned, and the next engine lit.")
        printslow(testing_flag, "Please give inputs as numbers only or exactly as shown.")
        rocket_mass_total, fuel_mass_total, eng_num, eng_size_list, eng_vel_list = get_inputs(testing_flag, PAYLOAD, eng_dict_print, eng_dict)
        calc_done, stages_list, current_list, struct_list, pay_list, vel_list = calculate(PAYLOAD, VEL_TARG, testing_flag, rocket_mass_total, fuel_mass_total, eng_num, eng_size_list, eng_vel_list)
        if calc_done == True:
            plot_values(stages_list, current_list, struct_list, pay_list, vel_list)
            break
