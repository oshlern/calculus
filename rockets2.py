import math
import matplotlib.pyplot as plt

VEL_TARG = 42 # target velocity in Km/s
PAYLOAD = 1000 # payload mass in Kg
rocket_mass_total = 0 # total rocket mass including fuel and payload in Kg
fuel_total = 0 # total fuel mass in Kg
eng_mass_struct = 0 # single engine structure mass in Kg
eng_mass_fuel = 0 # single engine fuel mass in Kg
eng_num = 0 # number of engines
eng_type_input = None # type of engine to be used, refers to eng_dict
eng_vel = None # burnout velocity of engine, as given by eng_dict
eng_dict = { # dictionary of types of engines and max velocity in Km/s
    'jet' : 29,
    'solid' : 2.5,
    'liquid' : 4.4,
    'ion' : 29,
    'electrostatic ion' : 210,
    'magnetoplasmic' : 160,
    'photonic' : 299792.458
}
stage_mass = 0 # mass of current stage including fuel plus all stages above in Kg
vel_burnout_total = 0 # total velocity at burnout of final engine
vel_burnout_eng = 0 # velocity at burnout of single engine
have_error = False # error flag
calc_done = False # calculation done flag
stages_list = [] # list of number of stages left
current_list = [] # list of mass of current stages
next_list = [] # list of mass of next stages
E_k_list = [] # list of structural ratios
P_k_list = [] # list of payload ratios
vel_list = [] # list of velocities at burnout

def get_inputs():
    print("Input total rocket mass, in Kg")
    rocket_mass_total = int(input()) # store total rocket mass
    print("Input total fuel mass, in Kg")
    fuel_total = int(input()) # store total fuel mass
    print("Input number of engines")
    eng_num = int(input()) # store number of engines
    print("Input type of engine")
    print("Options: " + str(eng_dict))
    eng_type_input = str(input()) # receive type of engine
    eng_vel = eng_dict[eng_type_input] # use type of engine to find engine velocity
    return rocket_mass_total, fuel_total, eng_num, eng_vel

def check_inputs(rocket_mass_total, fuel_total, have_error, PAYLOAD):
    if rocket_mass_total - fuel_total < (0.1 * fuel_total) or rocket_mass_total < PAYLOAD:
    # if the rocket mass is less than 10% of the fuel mass or if the rocket mass is less than the payload
        print("Error: rocket mass is too small")
        have_error = True # flag to stop program
    else:
        print("Rocket mass is acceptable")
        have_error = False # continue with program
    return have_error

def calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list):
    eng_mass_fuel = fuel_total/eng_num # find mass of fuel per engine
    print("eng_mass_fuel " + str(eng_mass_fuel))
    eng_mass_struct = (rocket_mass_total - PAYLOAD) - eng_mass_fuel/eng_num # find mass of engine without fuel
    print("eng_mass_struct " + str(eng_mass_struct))
    stages_left = eng_num # each engine is a stage
    print("stages_left " + str(stages_left))
    vel_burnout_temp = [] # list to store all velocities independently
    vel_burnout_neg = 0
    i = 0
    for n in range(eng_num): # jen's suggestion for changing engine size: for size in [list of things that can change]
        stages_list.append(stages_left)
        current_stage_mass = (eng_mass_struct + eng_mass_fuel) * (stages_left) + PAYLOAD
        print("current_stage_mass " + str(current_stage_mass))
        next_stage_mass = (eng_mass_struct + eng_mass_fuel) * (stages_left - 1) + PAYLOAD
        print("next_stage_mass " + str(next_stage_mass))
        current_list.append(current_stage_mass)
        next_list.append(next_stage_mass)
        E_k = ((eng_mass_struct)/(eng_mass_struct + eng_mass_fuel))
        print("E_k " + str(E_k))
        E_k_list.append(E_k)
        P_k = ((next_stage_mass)/(current_stage_mass))
        print("P_k " + str(P_k))
        P_k_list.append(P_k)
        vel_burnout_eng = -eng_vel * math.log((E_k + ((1 - E_k) * P_k)))
        print("vel_burnout_eng " + str(vel_burnout_eng))
        vel_burnout_temp.append(vel_burnout_eng)
        vel_list.append(vel_burnout_eng)
        stages_left -= 1
        print("stages_left " + str(stages_left))
    for x in vel_burnout_temp:
        vel_burnout_total += (vel_burnout_temp[i])
        i += 1
    print("vel_burnout_total " + str(vel_burnout_total))
    return vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list

def plot_values(stages_list, current_list, next_list, E_k_list, P_k_list, vel_list, eng_num):
    plt.figure(1)
    plt.plot(stages_list, current_list, 'b-', stages_list, next_list, 'r-')
    plt.xlabel('number of stages')
    plt.ylabel('mass in Kg')
    print("figure 1 is current stage mass (blue) and next stage mass (red) by stage")
    plt.figure(2)
    plt.plot(stages_list, E_k_list, 'g-', stages_list, P_k_list, 'k-')
    plt.xlabel('number of stages')
    plt.ylabel('ratio')
    print("figure 2 is structural ratio (green) and payload ratio (black) by stage")
    plt.figure(3)
    plt.plot(stages_list, vel_list, 'k-')
    plt.xlabel('number of stages')
    plt.ylabel('velocity in Km/s')
    print("figure 3 is velocity (black) by stage")
    plt.show()

def check_answer(VEL_TARG, vel_burnout_total, calc_done):
    if vel_burnout_total >= VEL_TARG:
        vel_excess = vel_burnout_total - VEL_TARG
        print("escaped sun with " + str(vel_excess) + " Km/s")
    else:
        vel_short = VEL_TARG - vel_burnout_total
        print("did not escape by " + str(vel_short) + " Km/s")
    calc_done = True
    return calc_done

if __name__ == '__main__':
    while True:
        print("currently only using engine velocities and ignoring specific impulse")
        rocket_mass_total, fuel_total, eng_num, eng_vel = get_inputs()
        have_error = check_inputs(rocket_mass_total, fuel_total, have_error, PAYLOAD)
        if have_error == True:
            break
        vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list = calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list)
        calc_done = check_answer(VEL_TARG, vel_burnout_total, calc_done)
        print("read graphs right to left and close all to finish program")
        plot_values(stages_list, current_list, next_list, E_k_list, P_k_list, vel_list, eng_num)
        if calc_done == True:
            break
