import numpy as np
from Utils.load_data import load_mediamill
from Methods.SketchedIOKR import IOKR, SIOKR, ISOKR, SISOKR
from Methods.Sketch import SubSample, pSparsified
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.metrics import f1_score


# Setting random seed
np.random.seed(seed=42)


# Defining Gaussian kernel
def Gaussian_kernel(gamma):
    def Compute_Gram(X, Y):
        return rbf_kernel(X, Y, gamma=gamma)
    return Compute_Gram


# Loading dataset
X_tr, Y_tr, X_te, Y_te = load_mediamill()
n_tr = X_tr.shape[0]
n_te = X_te.shape[0]
d = Y_tr.shape[1]
l_bar = np.mean(np.sum(Y_tr, axis=1))

Y_c = np.unique(Y_tr, axis=0)


######## IOKR #######################################################################

print('IOKR in process...')

# Hyperparameters priorly obtained by inner 5-folds cv
best_L_IOKR = 1e-08
best_sx_IOKR = 100.0
best_sy_IOKR = l_bar

input_kernel = Gaussian_kernel(gamma=1/(2 * best_sx_IOKR))
output_kernel = Gaussian_kernel(gamma=1/(2 * best_sy_IOKR))


clf = IOKR(L=best_L_IOKR, input_kernel=input_kernel,
           output_kernel=output_kernel)

# KRR ################################################################################
clf.fit(X_tr, Y_tr)

Y_pred_te = clf.predict(X_te=X_te, Y_c=Y_c)

# Fitting and decoding times
fit_time_IOKR = clf.fit_time
decode_time_IOKR = clf.decode_time

f1_te_IOKR = f1_score(Y_pred_te, Y_te, average='samples')

print('Results obtained with IOKR on Mediamill dataset: ')
print('Test F1 score: ' + str(f1_te_IOKR))
print('Training time (in seconds): ' + str(fit_time_IOKR))
print('Inference time (in seconds): ' + str(decode_time_IOKR))
print('\n')

######## SIOKR #######################################################################

print('SIOKR in process...')

# Hyperparameters priorly obtained by inner 5-folds cv
best_L_SIOKR = 1e-08
best_sx_SIOKR = 100.0
best_sy_SIOKR = l_bar

input_kernel = Gaussian_kernel(gamma=1/(2 * best_sx_SIOKR))
output_kernel = Gaussian_kernel(gamma=1/(2 * best_sy_SIOKR))

# Number of replicates
n_rep = 30

f1_tes = np.zeros(n_rep)
fit_times = np.zeros(n_rep)
decode_times = np.zeros(n_rep)

# Sketch parameters
m = 8000
p = 20.0 / n_tr

rrmse_test_S = np.zeros((n_rep, d))
times_S = np.zeros(n_rep)

for j in range(n_rep):

    R = pSparsified((m, n_tr), p=p, type='Gaussian')

    clf = SIOKR(L=best_L_SIOKR,
                input_kernel=input_kernel,
                output_kernel=output_kernel,
                R=R)

    clf.fit(X_tr, Y_tr)

    Y_pred_te = clf.predict(X_te=X_te, Y_c=Y_c)

    f1_tes[j] = f1_score(Y_pred_te, Y_te, average='samples')
    fit_times[j] = clf.fit_time
    decode_times[j] = clf.decode_time

f1_mean = np.mean(f1_tes)
f1_std = 0.5 * np.std(f1_tes)

fit_time_mean = np.mean(fit_times)
fit_time_std = 0.5 * np.std(fit_times)

decode_time_mean = np.mean(decode_times)
decode_time_std = 0.5 * np.std(decode_times)


print('Results obtained with SIOKR on Mediamill dataset: ')
print('Test F1 score: ' + str(f1_mean) + ' +- ' + str(f1_std))
print('Training time (in seconds): ' + str(fit_time_mean) + ' +- ' + str(fit_time_std))
print('Inference time (in seconds): ' + str(decode_time_mean) + ' +- ' + str(decode_time_std))
print('\n')


######## ISOKR #######################################################################

print('ISOKR in process...')

# Hyperparameters priorly obtained by inner 5-folds cv
best_L_ISOKR = 1e-08
best_sx_ISOKR = 100.0
best_sy_ISOKR = 10.0

input_kernel = Gaussian_kernel(gamma=1/(2 * best_sx_ISOKR))
output_kernel = Gaussian_kernel(gamma=1/(2 * best_sy_ISOKR))

# Number of replicates
n_rep = 30

f1_tes = np.zeros(n_rep)
fit_times = np.zeros(n_rep)
decode_times = np.zeros(n_rep)

# Sketch parameters
m = 500
p = 20.0 / n_tr

rrmse_test_S = np.zeros((n_rep, d))
times_S = np.zeros(n_rep)

for j in range(n_rep):

    R = pSparsified((m, n_tr), p=p, type='Gaussian')

    clf = ISOKR(L=best_L_ISOKR,
                input_kernel=input_kernel,
                output_kernel=output_kernel,
                R=R)

    clf.fit(X_tr, Y_tr)

    Y_pred_te = clf.predict(X_te=X_te, Y_c=Y_c)

    f1_tes[j] = f1_score(Y_pred_te, Y_te, average='samples')
    fit_times[j] = clf.fit_time
    decode_times[j] = clf.decode_time

f1_mean = np.mean(f1_tes)
f1_std = 0.5 * np.std(f1_tes)

fit_time_mean = np.mean(fit_times)
fit_time_std = 0.5 * np.std(fit_times)

decode_time_mean = np.mean(decode_times)
decode_time_std = 0.5 * np.std(decode_times)


print('Results obtained with ISOKR on Mediamill dataset: ')
print('Test F1 score: ' + str(f1_mean) + ' +- ' + str(f1_std))
print('Training time (in seconds): ' + str(fit_time_mean) + ' +- ' + str(fit_time_std))
print('Inference time (in seconds): ' + str(decode_time_mean) + ' +- ' + str(decode_time_std))
print('\n')


######## SISOKR #######################################################################

print('SISOKR in process...')

# Hyperparameters priorly obtained by inner 5-folds cv
best_L_SISOKR = 1e-08
best_sx_SISOKR = 100.0
best_sy_SISOKR = 10.0

input_kernel = Gaussian_kernel(gamma=1/(2 * best_sx_SISOKR))
output_kernel = Gaussian_kernel(gamma=1/(2 * best_sy_SISOKR))

# Number of replicates
n_rep = 30

f1_tes = np.zeros(n_rep)
fit_times = np.zeros(n_rep)
decode_times = np.zeros(n_rep)

# Sketch parameters
m_in = 8000
m_out = 500
p = 20.0 / n_tr

rrmse_test_S = np.zeros((n_rep, d))
times_S = np.zeros(n_rep)

for j in range(n_rep):

    R_in = SubSample((m_in, n_tr))
    R_out = pSparsified((m_out, n_tr), p=p, type='Gaussian')

    clf = SISOKR(L=best_L_SISOKR,
                input_kernel=input_kernel,
                output_kernel=output_kernel,
                R_in=R_in, R_out=R_out)

    clf.fit(X_tr, Y_tr)

    Y_pred_te = clf.predict(X_te=X_te, Y_c=Y_c)

    f1_tes[j] = f1_score(Y_pred_te, Y_te, average='samples')
    fit_times[j] = clf.fit_time
    decode_times[j] = clf.decode_time

f1_mean = np.mean(f1_tes)
f1_std = 0.5 * np.std(f1_tes)

fit_time_mean = np.mean(fit_times)
fit_time_std = 0.5 * np.std(fit_times)

decode_time_mean = np.mean(decode_times)
decode_time_std = 0.5 * np.std(decode_times)


print('Results obtained with SISOKR on Mediamill dataset: ')
print('Test F1 score: ' + str(f1_mean) + ' +- ' + str(f1_std))
print('Training time (in seconds): ' + str(fit_time_mean) + ' +- ' + str(fit_time_std))
print('Inference time (in seconds): ' + str(decode_time_mean) + ' +- ' + str(decode_time_std))
print('\n')