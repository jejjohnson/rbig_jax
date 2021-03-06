# JAX SETTINGS
import jax
import jax.numpy as np
# Plot Functions
import matplotlib.pyplot as plt
import numpy as onp
import seaborn as sns
from scipy.stats import beta

from rbig_jax.data import get_classic
from rbig_jax.transforms.gaussian import get_gauss_params, init_params_hist

sns.reset_defaults()
sns.set_context(context="talk", font_scale=0.7)



# =========================
# Original Data
# =========================

data = get_classic(1_000).T

# ========================
# PLOT
# ========================
fig = plt.figure(figsize=(5, 5))

color = "blue"
title = "Original Data"
g = sns.jointplot(x=data[0], y=data[1], kind="hex", color=color)
plt.xlabel("X")
plt.ylabel("Y")
plt.suptitle(title)
plt.tight_layout()
plt.savefig("scripts/demo2d_mg_x.png")

# ========================
# Forward Transformation
# ========================

# initialize parameters getter function
apply_func = init_params_hist(10, 1_000, 1e-5)

# get gaussian params
X_transform, Xldj, params, forward_func, inverse_func = get_gauss_params(
    data, apply_func
)

color = "Red"
title = "Transformed Data"
g = sns.jointplot(x=X_transform[0], y=X_transform[1], kind="hex", color=color)
plt.xlabel("X")
plt.ylabel("Y")
plt.suptitle(title)
plt.tight_layout()
plt.savefig("scripts/demo2d_mg_xg.png")

color = "Red"
title = "Jacobian X"
g = sns.jointplot(x=Xldj[0], y=Xldj[1], kind="hex", color=color)
plt.xlabel("X")
plt.ylabel("Y")
plt.suptitle(title)
plt.tight_layout()
plt.savefig("scripts/demo2d_mg_dx.png")

# ===========================
# Forward Transformation
# ===========================
X_transform, Xldj = forward_func(data, params)

color = "Red"
title = "Transformed Data"
g = sns.jointplot(x=X_transform[0], y=X_transform[1], kind="hex", color=color)
plt.xlabel("X")
plt.ylabel("Y")
plt.suptitle(title)
plt.tight_layout()
plt.savefig("scripts/demo2d_mg_xg_forward.png")

# ===========================
# Inverse Transformation
# ===========================

X_approx = inverse_func(X_transform, params)
print("!", X_approx.shape)
color = "Red"
title = "Approximate Original Data"
g = sns.jointplot(x=X_approx[0], y=X_approx[1], kind="hex", color=color)
plt.xlabel("X")
plt.ylabel("Y")
plt.suptitle(title)
plt.tight_layout()
plt.savefig("scripts/demo2d_mg_x_approx.png")
