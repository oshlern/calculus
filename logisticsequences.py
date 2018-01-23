# based on code written in collaboration with Peter and Lucas

import matplotlib.pyplot as plt
p_value = .5 # defined as 1/2 in question
konstant = 1.5 # defined so k is between 1 and 3
num_iteration = 30 # defined so function calculates 30 times
all_seqs = [] # to store all sequences (list of lists)

# This generates an array for the equation based on the values provided
def sequence_maker(p_value, konstant, num_iteration):
    output_seq = [] # to store outputs
    for x in range (num_iteration):  # to calculate a number of terms
        output_seq.append(p_value) # to record p value before it gets changed
        p_value = konstant * p_value*(1 - p_value) # evaluating equation
    return output_seq # after 30 rounds, return output list

# This plots everything
def plot_all():
  for output in all_seqs: # for every list of outputs in all_seqs
    plt.plot(output) # plot the output

plt.plot(sequence_maker(p_value,konstant,30),"r-") # to graph sequence

plt.savefig('/Users/laumitt/Desktop/plot.png')
