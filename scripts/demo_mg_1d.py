# JAX SETTINGS
import jax
import jax.numpy as np
# MATPLOTLIB Settings
import matplotlib.pyplot as plt
import numpy as onp
import seaborn as sns
from scipy.stats import beta

from rbig_jax.transforms.gaussian import (get_gauss_params_1d,
                                          init_params_hist_1d)
from rbig_jax.transforms.marginal import (forward_gaussianization,
                                          inverse_gaussianization)

sns.reset_defaults()
sns.set_context(context="talk", font_scale=0.7)


# ============================
# Generate Data
# ============================
n_samples = 1_000

a, b = 3.0, 10.0
data_dist = beta(a, b)


x_samples = data_dist.rvs(n_samples, 123)

plt.figure()
plt.hist(x_samples, bins=100)
plt.savefig("scripts/demo1d_x.png")

x_samples = x_samples.astype(np.float32)
x_samples = np.array(x_samples)

# ===============================
# Forward transformation
# ===============================

# initialize parameters getter function
apply_func = init_params_hist_1d(10, 1_000, 1e-5)

# get gaussian params
X_g, Xldj, params, forward_func, inverse_func = get_gauss_params_1d(
    x_samples, apply_func
)


plt.figure()
plt.hist(X_g, bins=100)
plt.savefig("scripts/demo1d_xg.png")

plt.figure()
plt.hist(Xldj, bins=100)
plt.savefig("scripts/demo1d_dx.png")

# # Check forward transformation function
X_g, Xldj = forward_func(x_samples, params)

plt.figure()
plt.hist(X_g, bins=100)
plt.savefig("scripts/demo1d_xg_forward.png")

# ===================================
# Inverse Transformation
# ===================================

# Inverse Gaussian CDF (CDF function)
X_approx = inverse_func(X_g, params)

# # inverse uniformization (quantile function)
# X_approx = inverse_uniformization_1d(X_u_approx, params)


plt.figure()
plt.hist(X_approx, bins=100)
plt.savefig("scripts/demo1d_x_approx.png")


# ===================================
# Samples
# ===================================


# sample from a gaussian distribution
X_g_samples = onp.random.randn(10_000)

# Inverse Gaussian CDF (CDF function)
X_samples = inverse_func(X_g_samples, params)

# # inverse uniformization (quantile function)
# X_approx = inverse_uniformization_1d(X_u_approx, params)


plt.figure()
plt.hist(X_samples, bins=100)
plt.savefig("scripts/demo1d_x_samples.png")

# ===================================
# Probabilities
# ===================================

X_lprob = jax.scipy.stats.norm.logpdf(X_g) + Xldj

plt.figure()
plt.hist(X_lprob, bins=100)
plt.savefig("scripts/demo1d_xlp_approx.png")

plt.figure()
plt.hist(data_dist.logpdf(x_samples), bins=100)
plt.savefig("scripts/demo1d_xlp.png")

print(X_lprob.sum())
print(data_dist.logpdf(x_samples).sum())
