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

def clear(all_seqs):
    all_seqs = []
    print("all_seqs clear")

# This plots everything
def plot_all():
    for output in all_seqs: # for every list of outputs in all_seqs
        plt.plot(output) # plot the output

if __name__ == "__main__":
    # Question 1 Part 1
    clear(all_seqs)

    print("Question 1 - plot and plot1")
    plt.plot(sequence_maker(p_value,konstant,30),"r-") # to graph sequence
    plt.savefig('/Users/laumitt/Desktop/plot.png') # to save the graph

    # Question 1 Part 2

    clear(all_seqs)

    # adding lists of outputs for different p values
    for i in range(100):
        p_value = 0
        all_seqs.append(sequence_maker(p_value, 1.5, 30))
        p_value = p_value + 0.01

        # adding lists of outputs for different k values
    for i in range(200):
        k = 1
        all_seqs.append(sequence_maker(0.5, k, 30))
        k = k + 0.01

    plot_all()
    plt.savefig('/Users/laumitt/Desktop/plot1.png')

    # Question 2

    clear(all_seqs)

    print("Question 2 - plot2")
    for i in range(20):
        all_seqs.append(sequence_maker(p_value=0.5, konstant=3.2+(i*0.01), num_iteration=1000))

    plot_all()
    plt.savefig('/Users/laumitt/Desktop/plot2.png')
