import math

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
vel_burnout_total = 0
vel_burnout_eng = 0
have_error = False
calc_done = False

def get_inputs():
    print("total rocket mass, in Kg")
    rocket_mass_total = int(input())
    print("total fuel mass, in Kg")
    fuel_total = int(input())
    print("number of engines")
    eng_num = int(input())
    print("type of engine")
    print("options: " + str(eng_dict))
    eng_type_input = str(input())
    eng_vel = eng_dict[eng_type_input]
    return rocket_mass_total, fuel_total, eng_num, eng_vel

def check_inputs(rocket_mass_total, fuel_total, have_error, PAYLOAD):
    if rocket_mass_total - fuel_total < (0.1 * fuel_total) or rocket_mass_total < PAYLOAD:
        print("error: rocket mass too small")
        have_error = True
    else:
        print("rocket mass acceptable")
        have_error = False
    return have_error

def calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, vel_burnout_total):
    eng_mass_fuel = fuel_total/eng_num
    print("eng_mass_fuel " + str(eng_mass_fuel))
    eng_mass_struct = (rocket_mass_total - PAYLOAD) - eng_mass_fuel/eng_num
    print("eng_mass_struct " + str(eng_mass_struct))
    stages_left = eng_num
    print("stages_left " + str(stages_left))
    vel_burnout_temp = []
    vel_burnout_neg = 0
    i = 0
    for n in range(eng_num):
        current_stage_mass = (eng_mass_struct + eng_mass_fuel) * (stages_left) + PAYLOAD
        print("current_stage_mass " + str(current_stage_mass))
        next_stage_mass = (eng_mass_struct + eng_mass_fuel) * (stages_left - 1) + PAYLOAD
        print("next_stage_mass " + str(next_stage_mass))
        E_k = ((eng_mass_struct)/(eng_mass_struct + eng_mass_fuel))
        print("E_k " + str(E_k))
        P_k = ((next_stage_mass)/(current_stage_mass))
        print("P_k " + str(P_k))
        vel_burnout_eng = math.log(E_k + ((1 - E_k) * P_k))
        print("vel_burnout_eng " + str(vel_burnout_eng))
        vel_burnout_temp.append(vel_burnout_eng)
        stages_left -= 1
        print("stages_left " + str(stages_left))
    for x in vel_burnout_temp:
        vel_burnout_neg += (vel_burnout_temp[i])
        i += 1
    vel_burnout_total = -vel_burnout_neg
    print("vel_burnout_total " + str(vel_burnout_total))
    return vel_burnout_total

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
        vel_burnout_total = calculate(rocket_mass_total, fuel_total, eng_num, eng_vel, PAYLOAD, vel_burnout_total)
        calc_done = check_answer(VEL_TARG, vel_burnout_total, calc_done)
        if calc_done == True:
            break
