import numpy as np
import sklearn.linear_model


def get_diffusion_constant(
    log_df, transition_time=None, time_col="v_time", msd_col="c_msd[4]"
):
    if transition_time is None:
        transition_time = len(log_df) // 2

    linear_df = log_df.iloc[transition_time:]
    time = np.array(linear_df[time_col])
    msd = np.array(linear_df[msd_col])

    clf = sklearn.linear_model.LinearRegression().fit(
        time[:, np.newaxis], msd[:, np.newaxis]
    )

    D = clf.coef_[0, 0] / 6
    D_int = clf.intercept_[0]

    super_df = log_df[
        (log_df[time_col] < transition_time) & (log_df[time_col] > 0)
    ]
    time = np.log(super_df[time_col])
    msd = np.log(super_df[msd_col])

    clf = sklearn.linear_model.LinearRegression().fit(
        time[:, np.newaxis], msd[:, np.newaxis]
    )

    alpha = clf.coef_[0, 0]
    alpha_int = clf.intercept_[0]

    return D, D_int, alpha, alpha_int
