have_error = False
rocket_init = 0 # total dry mass of rocket
engine_num = 0 # number of engines
fuel_init = 0 # total fuel mass
payload = 10^3 # does not change
payload_carry = 0 # mass of rocket that stays with payload

def check_variables(rocket_init, fuel_init):
    if rocket_init < (fuel_init/10):
        have_error = True
    else:
        have_error = False
    return have_error

if __name__ == "__main__":
    while True:
        print("rocket init = ?")
        rocket_init = int(input())
        print("engine num = ?")
        engine_num = int(input())
        print("fuel init = ?")
        fuel_init = int(input())
        print("payload carry = ?")
        payload_carry = int(input())
        have_error = check_variables(rocket_init, fuel_init)
        if have_error == True:
            print("error: rocket too low or fuel too high")
            break
        else:
            print("no error")
            break
