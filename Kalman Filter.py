# update mean and variance when given the mean and variance
# of belief and the mean and variance of the measurement.
# This program will update the parameters of belief function.
def update(mean, var, mean_measurement, var_measurement):
    new_mean = (var_measurement*mean+var*mean_measurement)/(var+var_measurement)
    new_var = 1/(1/var+1/var_measurement)
    return [new_mean, new_var]

#print(update(10,8,13,2))

# predict new mean and variance given the mean and variance of 
# prior belief and the mean and variance of motion.
def predict(mean, var, mean_motion, var_motion):
    new_mean = mean + mean_motion
    new_var = var + var_motion
    return [new_mean, new_var]

#print(predict(10, 4, 12, 4))

measurements = [5, 6, 7, 9, 10]
motion = [1, 1, 2, 1, 1]
measurement_sig = 4
motion_sig = 2
mu = 0
sig = 10000

#print the final values of the mean and the variance in a list [mu, sig]. 

for i in range(len(motion)):
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    [mu, sig] = predict(mu, sig, motion[i], motion_sig)
print [mu, sig]
