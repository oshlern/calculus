import math

GRAV_SUN = 274 # gravity of the sun in m/s^2
VEL_TARG = 42 # target velocity in Km/s
PAYLOAD = 1000 # payload mass in Kg
rocket_init = 0 # rocket mass without fuel or payload in Kg
eng_dry = 0 # single engine mass without fuel in Kg
fuel_total = 0 # total fuel mass before launch in Kg
eng_num = 0 # number of engines
isp_eng = 0 # specific impulse of one engine in Km/s
eng_eff = 0 # fuel consumption of one engine in Kg/s
fuel_per_eng = 0 # mass of fuel per engine in Kg
payload_carry = 0 # mass of rocket devoted to carrying payload in Kg
burnout_time = 0 # time until engine uses all available fuel in s

def get_inputs():
    print("rocket mass without fuel or payload, in Kg")
    rocket_init = int(input())
    print("engine mass without fuel, in Kg")
    eng_dry = int(input())
    print("total fuel mass before launch, in Kg")
    fuel_total = int(input())
#    print("number of engines")
#    eng_num = int(input())
    eng_num = 1 # for single stage
    print("specific impuls of one engine, in Km/s")
    isp_eng = int(input())
    print("engine efficiency, in Kg/s")
    eng_eff = int(input())
    return rocket_init, eng_dry, fuel_total, eng_num, isp_eng, eng_eff

def check_variables(rocket_init, fuel_total):
    if rocket_init <= (fuel_total/10):
        have_error = True
    else:
        have_error = False
    return have_error

def calc_mass(rocket_init, fuel_total, eng_dry, eng_num, eng_eff):
    fuel_per_eng = fuel_total/eng_num
    payload_carry = rocket_init - (eng_dry * eng_num)
    burnout_time = fuel_per_eng/eng_eff
    return fuel_per_eng, payload_carry, burnout_time

def calc_vel(isp_eng, fuel_total, rocket_init, payload_carry):
    max_vel = isp_eng * math.log((fuel_total + rocket_init)/(payload_carry))
    return max_vel

def print_result(fuel_per_eng, payload_carry, burnout_time, max_vel, VEL_TARG):
    print("fuel per engine: " + str(fuel_per_eng) + " Kg")
    print("payload carry mass: " + str(payload_carry) + " Kg")
    print("burnout time per engine: " + str(burnout_time) + " s")
    print("maximum velocity: " + str(max_vel) + " Km/s")
    if max_vel < VEL_TARG:
        print("did not escape sun")
    else:
        print("escaped sun!")

if __name__ == "__main__":
    while True:
        rocket_init, eng_dry, fuel_total, eng_num, vel_ex, eng_eff = get_inputs()
        have_error = check_variables(rocket_init, fuel_total)
        if have_error == True:
            print("error: rocket too low or fuel too high")
            break
        else:
            print("valid inputs")
        fuel_per_eng, payload_carry, burnout_time = calc_mass(rocket_init, fuel_total, eng_dry, eng_num, eng_eff)
        max_vel = calc_vel(vel_ex, fuel_total, rocket_init, payload_carry)
        print_result(fuel_per_eng, payload_carry, burnout_time, max_vel)
        break
