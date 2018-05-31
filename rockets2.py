import math
import matplotlib.pyplot as plt
import time
import sys

VEL_TARG = 42 # target velocity in Km/s
PAYLOAD = 1000 # payload mass in Kg
rocket_mass_total = 0 # total rocket mass including fuel and payload in Kg
fuel_total = 0 # total fuel mass in Kg
eng_mass_struct = 0 # single engine structure mass in Kg
eng_mass_fuel = 0 # single engine fuel mass in Kg
eng_num = 0 # number of engines
eng_type_input = None # type of engine to be used, refers to eng_dict
eng_vel = None # burnout velocity of engine, as given by eng_dict
eng_vel_list = [] # list of burnout velocities
eng_size_list = [] # list of engine sizes
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
stage_mass = 0 # mass of current stage including fuel plus all stages above in Kg
vel_burnout_total = 0 # total velocity at burnout of final engine
vel_burnout_eng = 0 # velocity at burnout of single engine
calc_done = False # calculation done flag
stages_list = [] # list of number of stages left
current_list = [] # list of mass of current stages
next_list = [] # list of mass of next stages
E_k_list = [] # list of structural ratios
P_k_list = [] # list of payload ratios
vel_list = [] # list of velocities at burnout
testing_flag = None # to bypass printslow if testing because it gets annoying

def check_test():
    print("Testing? y/n")
    test = str(input())
    if test == 'y':
        testing_flag = True
    else:
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

def get_inputs(PAYLOAD, eng_vel_list, eng_size_list, eng_dict, testing_flag):
    printslow(testing_flag, "Input total rocket mass, in Kg (numbers only, must be greater than or equal to " + str(PAYLOAD) + " Kg).")
    rocket_mass_total = int(input()) # store total rocket mass
    while rocket_mass_total < PAYLOAD:
        printslow(testing_flag, "Error: rocket mass too small.")
        rocket_mass_total = int(input())
        if rocket_mass_total >= PAYLOAD:
            break
    printslow(testing_flag, "Rocket mass acceptable.")
    print("-------" + '\n')
    printslow(testing_flag, "Input total fuel mass, in Kg (numbers only, must be less than or equal to 90% of rocket mass).")
    printslow(testing_flag, "Max fuel mass: " + str(0.9 * rocket_mass_total) + " Kg.")
    fuel_total = int(input()) # store total fuel mass
    while rocket_mass_total - fuel_total < (0.1 * fuel_total):
        printslow(testing_flag, "Error: rocket mass is too small or fuel mass too large. Please try again.")
        fuel_total = int(input())
        if rocket_mass_total - fuel_total >= (0.1 * fuel_total):
            break
    # if the rocket mass is less than 10% of the fuel mass or if the rocket mass is less than the payload
    printslow(testing_flag, "Rocket and fuel masses acceptable.")
    print("-------" + '\n')
    printslow(testing_flag, "Input number of engines (numbers only).")
    printslow(testing_flag, "Note that you will have to individually set all of these. Recommended maximum: 5 engines.")
    eng_num = int(input()) # store number of engines
    eng_iter = eng_num
    printslow(testing_flag, "Engine type options: " + '\n' + '\n' + "Name - Exhaust Velocity in Km/s.")
    for key, value in eng_dict_print.items():
        printslow(testing_flag, str(key) + ' - ' + str(value)) # to print names and velocities of engines
    print("-------" + '\n')
    eng_size_total = 0
    eng_size_left = 100
    for x in range(eng_num):
        printslow(testing_flag, "Input type of engine #" + str(eng_num - eng_iter + 1) + " (type only name).")
        eng_type_input = str(input()) # receive type of engine
        eng_vel_list.append(eng_dict[eng_type_input]) # use type of engine to find engine velocity
        if eng_iter != 1:
            printslow(testing_flag, "Input size of engine #" + str(eng_num - eng_iter + 1) + " as percentage of total fuel (numbers only).")
            printslow(testing_flag, "Percent of total fuel left: " + str(eng_size_left) + "% (" + str(fuel_total * (eng_size_left/100)) + " Kg).")
            eng_size_input = int(input()) # to store size
            if eng_size_input > eng_size_left:
                printslow(testing_flag, "Error: not enough available fuel. Please try again.")
                eng_size_input = int(input())
            if eng_size_input == 0:
                printslow(testing_flag, "Error: fuel percentage cannot be 0. Please try again.")
                eng_size_input = int(input())
        else:
            printslow(testing_flag, "Last engine uses all available fuel: " + str(eng_size_left) + "% (" + str(fuel_total * (eng_size_left/100)) + " Kg).")
            eng_size_input = eng_size_left
        eng_size_list.append(eng_size_input) # to store size of engine
        eng_size_total += eng_size_input # to check sizes add up to 100%
        eng_size_left = 100 - eng_size_total
        printslow(testing_flag, "Engine #" + str(eng_num - eng_iter + 1) + " recorded.")
        print("-------" + '\n')
        eng_iter -= 1
    if eng_size_total != 100:
        printslow(testing_flag, "Error: engine sizes do not equal 100%")
    else:
        printslow(testing_flag, "Engine sizes acceptable")
    print("-------" + '\n')
    return rocket_mass_total, fuel_total, eng_num, eng_vel_list

def calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, VEL_TARG, testing_flag):
    vel_burnout_temp = [] # to store velocities
    vel_burnout_total = 0
    i = 0 # to iterate over list of velocities, starting at index 0
    stages_left = eng_num # each engine is a stage
    eng_iter = eng_num
    printslow(testing_flag, str(stages_left) + " stages.")
    for n in range(eng_num): # iterate over number of stages
        eng_mass_fuel = fuel_total * (eng_size_list[n]/100) # find mass of fuel per engine
        printslow(testing_flag, "Fuel engine mass for engine #" + str(eng_num - eng_iter + 1) + ": " + str(eng_mass_fuel) + " Kg.")
        eng_mass_struct = (rocket_mass_total * (eng_size_list[n]/100)) - eng_mass_fuel # find mass of engine without fuel
        printslow(testing_flag, "Structural engine mass for engine #" + str(eng_num - eng_iter + 1) + ": " + str(eng_mass_struct) + " Kg.")
        eng_vel = eng_vel_list[n]
        stages_list.append(eng_num - eng_iter + 1) # to graph by stage later
        printslow(testing_flag, "Calculating for stage #" + str(eng_num - eng_iter + 1) + ".")
        current_stage_mass = (rocket_mass_total * (eng_size_list[n]/100)) + PAYLOAD
        # current stage mass is the mass of an engine times the number of stages left plus the mass of the payload
        printslow(testing_flag, "Mass of current stage: " + str(current_stage_mass) + " Kg.")
        if eng_iter != eng_num:
            next_stage_mass = current_stage_mass - ((rocket_mass_total * (eng_size_list[n+1]/100)))
        else:
            next_stage_mass = PAYLOAD
        # next stage mass is the mass of an engine times the number of stages left minus the current plus the mass of the payload
        printslow(testing_flag, "Mass of next stage: " + str(next_stage_mass) + " Kg.")
        current_list.append(current_stage_mass) # to graph masses by stage later
        next_list.append(next_stage_mass) # to graph masses by stage later
        E_k = ((eng_mass_struct)/(eng_mass_struct + eng_mass_fuel))
        # structural ratio of a stage is the structural mass of an engine divided by the total mass of an engine
        printslow(testing_flag, "Structural ratio: " + str(E_k) + ".")
        E_k_list.append(E_k) # to graph ratios by stage later
        P_k = ((next_stage_mass)/(current_stage_mass))
        # payload ratio of a stage is the mass of the next stage divided by the mass of the current stage
        # payload ratio defines how much mass the engine has to push
        printslow(testing_flag, "Payload ratio: " + str(P_k) + ".")
        P_k_list.append(P_k) # to graph ratios by stage later
        vel_burnout_eng = -eng_vel * math.log((E_k + ((1 - E_k) * P_k)))
        # the velocity of burnout of an engine is the negative velocity of exhaust of the engine times
        # the log of the structural ratio plus one minus the structural ratio times the payload ratio
        printslow(testing_flag, "Engine #" + str(eng_num - eng_iter + 1) + " velocity at burnout: " + str(vel_burnout_eng) + ".")
        vel_burnout_temp.append(vel_burnout_eng) # to store velocity by stage and add up later
        vel_list.append(vel_burnout_eng) # to graph the burnout velocities later
        vel_burnout_total += (vel_burnout_eng) # add up velocities from each stage
        stages_left -= 1 # once the engine burns out it is jettisonned
        eng_iter -= 1
        if stages_left == -1:
            break
        print("-------" + '\n')
    printslow(testing_flag, "Total velocity at burnout: " + str(vel_burnout_total) + " Km/s.")
    if vel_burnout_total >= VEL_TARG: # if the total burnout velocity is greater than 42 Km/s
        vel_excess = vel_burnout_total - VEL_TARG # the rocket escaped therefore there is excess velocity
        printslow(testing_flag, "Escaped sun with " + str(vel_excess) + " Km/s.")
    else: # if the total burnout velocity is less than 42 Km/s
        vel_short = VEL_TARG - vel_burnout_total # the rocket didn't escape therefore it fell short
        printslow(testing_flag, "Did not escape by " + str(vel_short) + " Km/s.")
    print("-------" + '\n')
    calc_done = True # flag to show calculate fully ran
    return calc_done, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list
    # total velocity at burnout returned to check if rocket escaped the sun
    # lists returned to plot later

def plot_values(stages_list, current_list, next_list, E_k_list, P_k_list, vel_list):
    # Figure 1: Current and Next Stage Mass by Stage
    plt.figure(1)
    plt.title("Current and Next Stage Mass by Stage")
    plt.plot(stages_list, current_list, 'b^-', label = "Current Stage Mass")
    plt.plot(stages_list, next_list, 'r^-', label = "Next Stage Mass")
    plt.legend(loc = 'upper right')
    plt.xlabel('Stage Number')
    plt.ylabel('Mass in Kg')
    # Figure 2: Structural and Payload Ratio by Stage
    plt.figure(2)
    plt.title("Structural and Payload Ratio by Stage")
    plt.plot(stages_list, E_k_list, 'g^-', label = "Structural Ratio")
    plt.plot(stages_list, P_k_list, 'k^-', label = "Payload Ratio")
    plt.legend(loc = 'center left')
    plt.xlabel('Stage Number')
    plt.ylabel('Ratio')
    # Figure 3: Burnout Velocity by Stage
    plt.figure(3)
    plt.title("Burnout Velocity by Stage")
    plt.plot(stages_list, vel_list, 'k^-', label = "Velocity")
    plt.legend(loc = 'upper left')
    plt.xlabel('Stage Number')
    plt.ylabel('Velocity in Km/s')
    plt.show()

if __name__ == '__main__':
    while True:
        testing_flag = check_test()
        printslow(testing_flag, "This program only uses engine velocities and ignores specific impulses, so it is not technically an accurate simulation of a rocket launch.")
        printslow(testing_flag, "This also assumes that engines instantly use all of their fuel to acheive burnout velocity, are promptly jettisonned, and the next engine lit.")
        printslow(testing_flag, "Please give inputs as numbers only or exactly as shown.")
        rocket_mass_total, fuel_total, eng_num, eng_vel_list = get_inputs(PAYLOAD, eng_vel_list, eng_size_list, eng_dict, testing_flag)
        calc_done, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list = calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, VEL_TARG, testing_flag)
        plot_values(stages_list, current_list, next_list, E_k_list, P_k_list, vel_list)
        if calc_done == True:
            break
