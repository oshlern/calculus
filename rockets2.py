# TO DO LIST
# - let user decide same/different engine types
# - let user decide same/different engine sizes
# - check that calculation is going for all stages including stages_left = 0
#       i think it is but i can't actually tell
# - calibrate with known escaping engines

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
eng_dict = { # dictionary of types of engines and exhaust velocity in Km/s
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
    'Photonic' : 299792.458
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
    print("Input total rocket mass, in Kg (numbers only, must be larger than 1000 Kg)")
    rocket_mass_total = int(input()) # store total rocket mass
    print("Input total fuel mass, in Kg (numbers only)")
    fuel_total = int(input()) # store total fuel mass
    print("Input number of engines (numbers only)")
    eng_num = int(input()) # store number of engines
    print("Input type of engine (type only name with exact capitalization)")
    print("Options: " + '\n' + "Name - Exhaust Velocity in Km/s")
    for key, value in eng_dict.items():
        print(str(key) + ' - ' + str(value)) # to print names and velocities of engines
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
    print("Fuel engine mass: " + str(eng_mass_fuel) + " Kg.")
    eng_mass_struct = (rocket_mass_total - PAYLOAD) - eng_mass_fuel/eng_num # find mass of engine without fuel
    print("Structural engine mass: " + str(eng_mass_struct) + " Kg.")
    stages_left = eng_num # each engine is a stage
    print(str(stages_left) + " stages.")
    vel_burnout_temp = [] # to store velocities
    i = 0 # to iterate over list of velocities, starting at index 0
    for n in range(eng_num): # iterate over each stage
        stages_list.append(stages_left) # to graph by stage later
        print("Calculating for stage #" + str(stages_left) + ".")
        current_stage_mass = (eng_mass_struct + eng_mass_fuel) * (stages_left) + PAYLOAD
        # current stage mass is the mass of an engine times the number of stages left plus the mass of the payload
        print("Mass of current stage: " + str(current_stage_mass) + " Kg.")
        next_stage_mass = (eng_mass_struct + eng_mass_fuel) * (stages_left - 1) + PAYLOAD
        # next stage mass is the mass of an engine times the number of stages left minus the current plus the mass of the payload
        print("Mass of next stage: " + str(next_stage_mass) + " Kg.")
        if current_stage_mass == next_stage_mass == PAYLOAD:
            break
        current_list.append(current_stage_mass) # to graph masses by stage later
        next_list.append(next_stage_mass) # to graph masses by stage later
        E_k = ((eng_mass_struct)/(eng_mass_struct + eng_mass_fuel))
        # structural ratio of a stage is the structural mass of an engine divided by the total mass of an engine
        print("Structural ratio: " + str(E_k) + ".")
        E_k_list.append(E_k) # to graph ratios by stage later
        P_k = ((next_stage_mass)/(current_stage_mass))
        # payload ratio of a stage is the mass of the next stage divided by the mass of the current stage
        # payload ratio defines how much mass the engine has to push
        print("Payload ratio: " + str(P_k) + ".")
        P_k_list.append(P_k) # to graph ratios by stage later
        vel_burnout_eng = -eng_vel * math.log((E_k + ((1 - E_k) * P_k)))
        # the velocity of burnout of an engine is the negative velocity of exhaust of the engine times
        # the log of the structural ratio plus one minus the structural ratio times the payload ratio
        print("Single engine velocity at burnout: " + str(vel_burnout_eng) + ".")
        vel_burnout_temp.append(vel_burnout_eng) # to store velocity by stage and add up later
        vel_list.append(vel_burnout_eng) # to graph the burnout velocities later
        stages_left = stages_left - 1 # once the engine burns out it is jettisonned
        if stages_left == -1:
            break
        print("-------")
    for x in vel_burnout_temp: # iterate over each stage
        vel_burnout_total += (vel_burnout_temp[i]) # add up velocities from each stage
        i += 1 # move to next stage
    print("Total velocity at burnout: " + str(vel_burnout_total) + " Km/s.")
    return vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list
    # total velocity at burnout returned to check if rocket escaped the sun
    # lists returned to plot later

def plot_values(stages_list, current_list, next_list, E_k_list, P_k_list, vel_list):
    # Figure 1: Current and Next Stage Mass by Stage
    plt.figure(1)
    plt.title("Current and Next Stage Mass by Stage")
    plt.plot(stages_list, current_list, 'b^-', label = "Current Stage Mass")
    plt.plot(stages_list, next_list, 'r^-', label = "Next Stage Mass")
    plt.legend(loc = 'upper right')
    plt.xlabel('Stages Left')
    plt.ylabel('Mass in Kg')
    plt.gca().invert_xaxis() # stages count down to 0, so invert to read from left to right
    # Figure 2: Structural and Payload Ratio by Stage
    plt.figure(2)
    plt.title("Structural and Payload Ratio by Stage")
    plt.plot(stages_list, E_k_list, 'g^-', label = "Structural Ratio")
    plt.plot(stages_list, P_k_list, 'k^-', label = "Payload Ratio")
    plt.legend(loc = 'center left')
    plt.xlabel('Stages Left')
    plt.ylabel('Ratio')
    plt.gca().invert_xaxis()
    # Figure 3: Burnout Velocity by Stage
    plt.figure(3)
    plt.title("Burnout Velocity by Stage")
    plt.plot(stages_list, vel_list, 'k^-', label = "Velocity")
    plt.legend(loc = 'upper left')
    plt.xlabel('Stages left')
    plt.ylabel('Velocity in Km/s')
    plt.gca().invert_xaxis()
    plt.show()

def check_answer(VEL_TARG, vel_burnout_total, calc_done):
    if vel_burnout_total >= VEL_TARG:
        vel_excess = vel_burnout_total - VEL_TARG
        print("Escaped sun with " + str(vel_excess) + " Km/s.")
    else:
        vel_short = VEL_TARG - vel_burnout_total
        print("Did not escape by " + str(vel_short) + " Km/s.")
    calc_done = True
    return calc_done

if __name__ == '__main__':
    while True:
        print("Currently only using engine velocities and ignoring specific impulse.")
        print("Please give inputs as numbers only or exactly as shown.")
        rocket_mass_total, fuel_total, eng_num, eng_vel = get_inputs()
        have_error = check_inputs(rocket_mass_total, fuel_total, have_error, PAYLOAD)
        if have_error == True:
            break
        vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list = calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, vel_burnout_total, stages_list, current_list, next_list, E_k_list, P_k_list, vel_list)
        calc_done = check_answer(VEL_TARG, vel_burnout_total, calc_done)
        plot_values(stages_list, current_list, next_list, E_k_list, P_k_list, vel_list)
        if calc_done == True:
            break
