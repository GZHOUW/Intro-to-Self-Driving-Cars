# Differentiation
def get_derivative(data, times):
    # TODO - try your best to implement this code yourself!
    #        if you get really stuck feel free to go back
    #        to the previous notebook for a hint.
    derList = []
    for i in range(len(times)-1):
        derList.append((data[i+1] - data[i])/(times[i+1] - times[i]))
    return derList


# Integration
def get_integral(data, times):
    intList = []
    int_i = 0
    for i in range(len(data)-1):
        int_i += (times[i+1] - times[i]) * data[i]
        intList.append(int_i)
    return intList
