# importing things for later
import matplotlib.pyplot as plt # for plotting
import math # for summing

a_null = 0 # because multiplying by 0 breaks it
a_one = -1/(math.sqrt(3)) # to start from
constant = -1/(math.sqrt(3)) # to multiply each term by
num_iteration = 10 # can be changed
outputs = [a_null] # to store outputs
labelled_outputs = ["a0: " + str(a_null)] # for easier reading
sum_outputs = [] # to store sum
infinite_sum = 0 # declaring infinite sum for later
flag = "no" # debug flag for later

def sequence(a_one, constant, num_iteration, outputs, labelled_outputs, sum_outputs):
    a_value = a_one # to define a_value
    for x in range(num_iteration):  # to calculate a number of terms
        outputs.append(a_value) # to record a value before it gets changed
        print("incoming a value") # debug flag and label
        print(a_value) # see the a value before it gets changed
        labelled_outputs.append("a" + str(x) + ": " + str(a_value)) # add old a value to labelled outputs
        a_value = constant * a_value # evaluating equation
        print("evaluated a value") # another debug flag and label
        print(a_value) # see the a value after it gets changed
        sum_outputs.append(a_value)
    print("returning things") # another debug flag
    return outputs, labelled_outputs, sum_outputs

def infinite(infinite_sum, sum_outputs, flag):
    infinite_sum = math.fsum(sum_outputs) # add up all the outputs
    print("evaluated infinite sum") # to check that it actually ran
    flag = "yes" # if the debug flag gets changed it worked
    return infinite_sum, flag

if __name__ == "__main__":
    outputs, labelled_outputs, sum_outputs = sequence(a_one, constant, num_iteration, outputs, labelled_outputs, sum_outputs) # calculate sequence
    infinite_sum, flag = infinite(infinite_sum, sum_outputs, flag)
    print("did it work {}".format(flag)) # check the debug flag
    print("labelled outputs = {}".format(labelled_outputs)) # see the labelled outputs
    print("sum outputs = {}".format(sum_outputs)) # see the sum outputs
    print("infinite sum = {} ".format(infinite_sum)) # see the infinite sum
    plt.plot(sum_outputs, "-r") # plot the outputs
    plt.savefig('/Users/laumitt/Desktop/outputs_plot.png') # to save the graph
