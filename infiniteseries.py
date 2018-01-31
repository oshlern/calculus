# importing things for later
import matplotlib.pyplot as plt
import math

a_null = 0 # because multiplying by 0 breaks it
a_one = -1/(math.sqrt(3)) # to start from
constant = -1/(math.sqrt(3)) # to multiply each term by
num_iteration = 10 # can be changed
outputs = [a_null] # to store outputs
labelled_outputs = ["a0: " + str(a_null)] # for easier reading
sum_outputs = [] # to store sum
infinite_sum = 0
flag = "no"

def sequence(a_one, constant, num_iteration, outputs, labelled_outputs, sum_outputs):
    a_value = a_one # to define a_value
    for x in range(num_iteration):  # to calculate a number of terms
        outputs.append(a_value) # to record a value before it gets changed
        print("incoming a value")
        print(a_value)
        labelled_outputs.append("a" + str(x) + ": " + str(a_value))
        a_value = constant * a_value # evaluating equation
        print("evaluated a value")
        print(a_value)
        sum_outputs.append(a_value)
    # returning a bunch of things
    print("returning things")
    return outputs, labelled_outputs, sum_outputs

def infinite(infinite_sum, sum_outputs, flag):
    infinite_sum = math.fsum(sum_outputs)
    print("evaluated infinite sum")
    flag = "yes"
    return infinite_sum, flag

if __name__ == "__main__":
    outputs, labelled_outputs, sum_outputs = sequence(a_one, constant, num_iteration, outputs, labelled_outputs, sum_outputs) # calculate sequence
    infinite(infinite_sum, sum_outputs, flag)
    print("did it work {}".format(flag))
    print("labelled outputs = {}".format(labelled_outputs))
    print("sum outputs = {}".format(sum_outputs))
    print("infinite sum = {} ".format(infinite_sum))
    plt.plot(sum_outputs, "-r") # plot the outputs
    plt.savefig('/Users/laumitt/Desktop/outputs_plot.png') # to save the graph
