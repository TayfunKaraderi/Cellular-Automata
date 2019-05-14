# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 13:44:53 2018

@author: Tayfun karaderi
"""

from __future__ import division
import copy
import numpy as np
# from matplotlib import pyplot as plt


# ------------------------2.1-Abelian Sand_Pile Model--------------------------
def index_topple(X):

    """
    input: array or list of lists
    return: i, j index of of coordinates that will topple
    in 2 lists (i_index, j_index)
    """

    # if isinstance(X, list):
    X = np.array(X)

    i_index = []
    j_index = []
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            a = X[i, j]
            if a >= 4:
                i_index.append(i)
                j_index.append(j)

    return(i_index, j_index)


# ------------------------------Main Program-----------------------------------
def sandpile(X):

    """
    Parameters:
    input: X-initial configuration (Array or Lists of list)
    return: final lattice configuration as an array
    """

    # if isinstance(X, list):
    X = np.array(X)

    m = np.amax(X)
    nrow = X.shape[0]
    ncol = X.shape[1]

    while m >= 4:

        a, b = index_topple(X)

        for ii in range(len(a)):

            i = a[ii]
            j = b[ii]
            # reduce toppling pile
            X[i, j] = X[i, j] - 4

            # increase heiht of nearest neighbours (with absorbing boundaries)
            if i+1 < nrow:
                X[i+1, j] = X[i+1, j] + 1
            if i-1 >= 0:
                X[i-1, j] = X[i-1, j] + 1
            if j+1 < ncol:
                X[i, j+1] = X[i, j+1] + 1
            if j-1 >= 0:
                X[i, j-1] = X[i, j-1] + 1

        m = np.amax(X)
        # a,b = index_topple(X)

    return X
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# ------------------------------2.2-Game of Life-------------------------------
def count_live_periodic_bound(config, a, b):

    '''
    input=lattice configuration, coordinates of lattice point (a-row, b-column)
    return= # of living, dead neighbours
    '''

    # if isinstance(config, list):
    config = np.array(config)

    N = config.shape[0]
    M = config.shape[1]

    n1 = config[(a+1) % N, b]
    n2 = config[(a-1) % N, b]
    n3 = config[a, (b+1) % M]
    n4 = config[a, (b-1) % M]
    n5 = config[(a+1) % N, (b+1) % M]
    n6 = config[(a-1) % N, (b-1) % M]
    n7 = config[(a+1) % N, (b-1) % M]
    n8 = config[(a-1) % N, (b+1) % M]

    c = np.array([n1, n2, n3, n4, n5, n6, n7, n8])

    N_live_neghbours = sum(c)
    # N_dead_neghbours = 8 - sum(c)

    return N_live_neghbours


def count_live_NONperiodic_bound(config, a, b):

    '''
    input=lattice configuration (array or list of lists),
    coordinates of lattice point (a-row, b-column)

    return= # of living, dead neighbours
    '''

    # if isinstance(config, list):
    config = np.array(config)

    N = config.shape[0]
    M = config.shape[1]

    if (a+1) < N:
        n1 = config[(a+1), b]
    else:
        n1 = 0

    if (a-1) >= 0:
        n2 = config[(a-1), b]
    else:
        n2 = 0

    if (b+1) < M:
        n3 = config[a, (b+1)]
    else:
        n3 = 0

    if (b-1) >= 0:
        n4 = config[a, (b-1)]
    else:
        n4 = 0

    if (a+1) < N and (b+1) < M:
        n5 = config[(a+1), (b+1)]
    else:
        n5 = 0

    if (a-1) >= 0 and (b-1) >= 0:
        n6 = config[(a-1), (b-1)]
    else:
        n6 = 0

    if (a+1) < N and (b-1) >= 0:
        n7 = config[(a+1), (b-1)]
    else:
        n7 = 0

    if (a-1) >= 0 and (b+1) < M:
        n8 = config[(a-1), (b+1)]
    else:
        n8 = 0

    c = np.array([n1, n2, n3, n4, n5, n6, n7, n8])

    N_live_neghbours = sum(c)
    # N_dead_neghbours = 8 - sum(c)

    return N_live_neghbours


def life(initial_state, nt, periodic=False):

    '''
    Parameters:
        initial_state : array_like or list of lists (2d)
        nt:number of moves
        periodic: if true periodic boundaries, otherwise sink boundaries

    Returns:
    array_like
        Final Lattice Configuration
    '''

    # if isinstance(initial_state, list):
    initial_state = np.array(initial_state)

    N = initial_state.shape[0]
    M = initial_state.shape[1]

    ini_config = initial_state.copy()  # i dont want to update the input

# ------------------------Periodic Boundaries----------------------------------
    if periodic is True:

        # loop over time
        config_compare = ini_config.copy()
        for t in range(nt):
            # print(t+1)

            config_update = config_compare.copy()

            # loop over all lattice points
            for i in range(N):
                for j in range(M):

                    a = config_compare[i, j]

                    # Number of living, dead cell neighbours (Nl,Nd)
                    Nl = count_live_periodic_bound(config_compare, i, j)

                    # living cell rules
                    if a == 1:
                        # Cell may die from lonliness or overcrowd
                        if Nl <= 1 or Nl >= 4:
                            config_update[i, j] = False

                    # dead cell rules
                    if a == 0:
                        # the dead cell may reborn
                        if Nl == 3:
                            config_update[i, j] = True

            config_compare = config_update.copy()
# -----------------------------------------------------------------------------

# -----------------------Non Periodic Boundaries-------------------------------
    if periodic is False:

        # loop over time
        config_compare = ini_config.copy()
        for t in range(nt):
            # print(t+1)

            config_update = config_compare.copy()
            # loop over all lattice points
            for i in range(N):
                for j in range(M):
                    a = config_compare[i, j]

                    # # of liv, dead neighbours (Nl,Nd) for NONPER BC
                    Nl = count_live_NONperiodic_bound(config_compare, i, j)

                    # living cell conditions
                    if a == 1:
                        # Cell may die from lonliness or overcrowd
                        if Nl <= 1 or Nl >= 4:
                            config_update[i, j] = False

                    # dead cell condition
                    if a == 0:
                        # the dead cell may reborn
                        if Nl == 3:
                            config_update[i, j] = True

            config_compare = config_update.copy()
# -----------------------------------------------------------------------------

    return config_update


# ---------------------------2.3-Game of Life-(3D)-----------------------------
def c_live_periodic_bound3d(config, a, b, c):

    '''
    input=lattice configuration, coordinates of lattice point (a-row, b-column)
    return= # of living, dead neighbours
    '''

    # if isinstance(config, list):
    config = np.array(config)

    N = config.shape[0]
    M = config.shape[1]
    V = config.shape[2]

    n1 = config[(a+1) % N, (b), (c)]
    n2 = config[(a-1) % N, (b), (c)]
    n3 = config[(a), (b+1) % M, (c)]
    n4 = config[(a), (b-1) % M, (c)]
    n5 = config[(a+1) % N, (b+1) % M, (c)]
    n6 = config[(a-1) % N, (b-1) % M, (c)]
    n7 = config[(a+1) % N, (b-1) % M, (c)]
    n8 = config[(a-1) % N, (b+1) % M, (c)]

    n9 = config[(a+1) % N, (b), (c-1) % V]
    n10 = config[(a-1) % N, (b), (c-1) % V]
    n11 = config[(a), (b+1) % M, (c-1) % V]
    n12 = config[(a), (b-1) % M, (c-1) % V]
    n13 = config[(a+1) % N, (b+1) % M, (c-1) % V]
    n14 = config[(a-1) % N, (b-1) % M, (c-1) % V]
    n15 = config[(a+1) % N, (b-1) % M, (c-1) % V]
    n16 = config[(a-1) % N, (b+1) % M, (c-1) % V]

    n17 = config[(a+1) % N, (b), (c+1) % V]
    n18 = config[(a-1) % N, (b), (c+1) % V]
    n19 = config[(a), (b+1) % M, (c+1) % V]
    n20 = config[(a), (b-1) % M, (c+1) % V]
    n21 = config[(a+1) % N, (b+1) % M, (c+1) % V]
    n22 = config[(a-1) % N, (b-1) % M, (c+1) % V]
    n23 = config[(a+1) % N, (b-1) % M, (c+1) % V]
    n24 = config[(a-1) % N, (b+1) % M, (c+1) % V]

    n25 = config[a, b, (c+1) % V]
    n26 = config[a, b, (c-1) % V]

    c = np.array([n1, n2, n3, n4, n5, n6, n7, n8, n9,
                  n10, n11, n12, n13, n14, n15, n16,
                  n17, n18, n19, n20, n21, n22, n23, n24, n25, n26])

    N_live_neghbours = sum(c)
    # N_dead_neghbours = 8 - sum(c)
    # print(c)
    return N_live_neghbours


def c_live_Nperiodic_bound3d(config, a, b, c):

    '''
    input=lattice configuration, coordinates of lattice point (a-row, b-column)
    return= # of living, dead neighbours
    '''

    # if isinstance(config, list):
    config = np.array(config)

    N = config.shape[0]
    M = config.shape[1]
    V = config.shape[2]

    if (a+1) < N:
        n1 = config[(a+1), (b), (c)]
    else:
        n1 = 0

    if (a-1) >= 0:
        n2 = config[(a-1), (b), (c)]
    else:
        n2 = 0

    if (b+1) < M:
        n3 = config[(a), (b+1), (c)]
    else:
        n3 = 0

    if (b-1) >= 0:
        n4 = config[(a), (b-1), (c)]
    else:
        n4 = 0

    if (a+1) < N and (b+1) < M:
        n5 = config[(a+1), (b+1), (c)]
    else:
        n5 = 0

    if (a-1) >= 0 and (b-1) >= 0:
        n6 = config[(a-1), (b-1), (c)]
    else:
        n6 = 0

    if (a+1) < N and (b-1) >= 0:
        n7 = config[(a+1), (b-1), (c)]
    else:
        n7 = 0

    if (a-1) >= 0 and (b+1) < M:
        n8 = config[(a-1), (b+1), (c)]
    else:
        n8 = 0

    if (a+1) < N and (c-1) >= 0:
        n9 = config[(a+1), (b), (c-1)]
    else:
        n9 = 0

    if (a-1) >= 0 and (c-1) >= 0:
        n10 = config[(a-1), (b), (c-1)]
    else:
        n10 = 0

    if (b+1) < M and (c-1) >= 0:
        n11 = config[(a), (b+1), (c-1)]
    else:
        n11 = 0

    if (b-1) >= 0 and (c-1) >= 0:
        n12 = config[(a), (b-1), (c-1)]
    else:
        n12 = 0

    if (a+1) < N and (b+1) < M and (c-1) >= 0:
        n13 = config[(a+1), (b+1), (c-1)]
    else:
        n13 = 0

    if (a-1) >= 0 and (b-1) >= 0 and (c-1) >= 0:
        n14 = config[(a-1), (b-1), (c-1)]
    else:
        n14 = 0

    if (a+1) < N and (b-1) >= 0 and (c-1) >= 0:
        n15 = config[(a+1), (b-1), (c-1)]
    else:
        n15 = 0

    if (a-1) >= 0 and (c-1) >= 0 and (b+1) < M:
        n16 = config[(a-1), (b+1), (c-1)]
    else:
        n16 = 0

    if (a+1) < N and (c+1) < V:
        n17 = config[(a+1), (b), (c+1)]
    else:
        n17 = 0

    if (a-1) >= 0 and (c+1) < V:
        n18 = config[(a-1), (b), (c+1)]
    else:
        n18 = 0

    if (b+1) < M and (c+1) < V:
        n19 = config[(a), (b+1), (c+1)]
    else:
        n19 = 0

    if (b-1) >= 0 and (c+1) < V:
        n20 = config[(a), (b-1), (c+1)]
    else:
        n20 = 0

    if (a+1) < N and (b+1) < M and (c+1) < V:
        n21 = config[(a+1), (b+1), (c+1)]
    else:
        n21 = 0

    if (a-1) >= 0 and (b-1) >= 0 and (c+1) < V:
        n22 = config[(a-1), (b-1), (c+1)]
    else:
        n22 = 0

    if (a+1) < N and (b-1) >= 0 and (c+1) < V:
        n23 = config[(a+1), (b-1), (c+1)]
    else:
        n23 = 0

    if (a-1) >= 0 and (b+1) < M and (c+1) < V:
        n24 = config[(a-1), (b+1), (c+1)]
    else:
        n24 = 0

    if (c+1) < V:
        n25 = config[a, b, (c+1) % V]
    else:
        n25 = 0

    if (c-1) >= 0:
        n26 = config[a, b, (c-1) % V]
    else:
        n26 = 0

    c = np.array([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14,
                  n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26])

    N_live_neghbours = sum(c)
    # N_dead_neghbours = 8 - sum(c)

    return N_live_neghbours


# -------------------------------MAIN-PROGRAM----------------------------------
def life3d(initial_state, nt, periodic=False):

    '''
    Parameters:
        initial_state : array_like or list of lists (3d)
        nt:number of moves
        periodic: if true periodic boundaries, otherwise sink boundaries

    Returns:
    array_like
        Final Lattice Configuration
    '''

    if isinstance(initial_state, list):
        initial_state = np.array(initial_state)

    N = initial_state.shape[0]
    M = initial_state.shape[1]
    V = initial_state.shape[2]

    ini_config = initial_state.copy()  # i dont want to update the input

# ------------------------Periodic Boundaries----------------------------------
    if periodic is True:

        # loop over time
        config_compare = ini_config.copy()
        for t in range(nt):
            # print(t+1)

            config_update = config_compare.copy()

            # loop over all lattice points
            for i in range(N):
                for j in range(M):
                    for k in range(V):

                        a = config_compare[i, j, k]

                        # Number of living, dead cell neighbours (Nl,Nd)
                        Nl = c_live_periodic_bound3d(config_compare, i, j, k)

                        # living cell rules
                        if a == 1:
                            # Cell may die from lonliness or overcrowd
                            if Nl != 4 and Nl != 5:
                                config_update[i, j, k] = False

                        # dead cell rules
                        if a == 0:
                            # the dead cell may reborn
                            if Nl == 5:
                                config_update[i, j, k] = True

            config_compare = config_update.copy()
# -----------------------------------------------------------------------------

# -----------------------Non Periodic Boundaries-------------------------------
    if periodic is False:

        # loop over time
        config_compare = ini_config.copy()
        for t in range(nt):
            # print(t+1)

            config_update = config_compare.copy()
            # loop over all lattice points
            for i in range(N):
                for j in range(M):
                    for k in range(V):

                        a = config_compare[i, j, k]

                        # # of liv, dead neighbours (Nl,Nd) for NP BC
                        Nl = c_live_Nperiodic_bound3d(config_compare, i, j, k)

                        # living cell conditions
                        if a == 1:
                            # Cell may die from lonliness or overcrowd
                            if Nl != 4 and Nl != 5:
                                config_update[i, j, k] = False

                        # dead cell condition
                        if a == 0:
                            # the dead cell may reborn
                            if Nl == 5:
                                config_update[i, j, k] = True

            config_compare = config_update.copy()
# -----------------------------------------------------------------------------

    return config_update

# ---------------------- 2.4-Game-of-Life(hexagon) ----------------------------


def C_live_Hex(config, a, b):

    '''
    input=lattice configuration, coordinates of lattice point (a-row, b-column)
    return= # of living, dead neighbours
    '''

    if a % 2:
        try:
            n1 = config[(a)][(b+1)]
        except IndexError:
            n1 = 0
        try:
            n2 = config[(a)][(b-1)]
        except IndexError:
            n2 = 0
        if (b-1) < 0:
            n2 = 0

        try:
            n3 = config[(a+1)][(b-1)]
        except IndexError:
            n3 = 0
        if (b-1) < 0:
            n3 = 0
        try:
            n4 = config[(a+1)][(b)]
        except IndexError:
            n4 = 0

        try:
            n5 = config[(a-1)][(b-1)]
        except IndexError:
            n5 = 0
        if (a-1) < 0 or (b-1) < 0:
            n5 = 0
        try:
            n6 = config[(a-1)][(b)]
        except IndexError:
            n6 = 0
        if (a-1) < 0:
            n6 = 0

    if not a % 2:
        try:
            n1 = config[(a)][(b+1)]
        except IndexError:
            n1 = 0
        try:
            n2 = config[(a)][(b-1)]
        except IndexError:
            n2 = 0
        if (b-1) < 0:
            n2 = 0

        try:
            n3 = config[(a+1)][(b+1)]
        except IndexError:
            n3 = 0
        try:
            n4 = config[(a+1)][(b)]
        except IndexError:
            n4 = 0

        try:
            n5 = config[(a-1)][(b+1)]
        except IndexError:
            n5 = 0
        if (a-1) < 0:
            n5 = 0
        try:
            n6 = config[(a-1)][(b)]
        except IndexError:
            n6 = 0
        if (a-1) < 0:
            n6 = 0

    c = np.array([n1, n2, n3, n4, n5, n6])

    N_live_neghbours = sum(c)
    # N_dead_neghbours = 8 - sum(c)

    return N_live_neghbours


def lifehex(initial_state, nt):

    '''
    Parameters:
        initial_state : list of lists
        nt:number of moves

    Returns:
    list of lists
        Final Lattice Configuration
    '''

    # if isinstance(initial_state, list):
    #    initial_state = np.array(initial_state)

    N = len(initial_state)
    Leven = len(initial_state[0])
    Lodd = Leven + 1

    ini_config = copy.deepcopy(initial_state)  # i dont want to update input

    config_compare = copy.deepcopy(ini_config)
    for t in range(nt):
        # print(t+1)

        config_update = copy.deepcopy(config_compare)

        # loop over all lattice points
        for i in range(N):

            if not i % 2:
                # First loop over even rows
                for j in range(Leven):

                    a = config_compare[i][j]

                    # Number of living, dead cell neighbours (Nl,Nd)
                    Nl = C_live_Hex(config_compare, i, j)

                    # living cell rules
                    if a == 1:
                        # Cell may die from lonliness or overcrowd
                        if Nl != 3 and Nl != 5:
                            config_update[i][j] = False

                    # dead cell rules
                    if a == 0:
                        # the dead cell may reborn
                        if Nl == 2:
                            config_update[i][j] = True

            # Then loop over odd rows
            if i % 2:
                for j in range(Lodd):

                    a = config_compare[i][j]

                    # Number of living, dead cell neighbours (Nl,Nd)
                    Nl = C_live_Hex(config_compare, i, j)

                    # living cell rules
                    if a == 1:
                        # Cell may die from lonliness or overcrowd
                        if Nl != 3 and Nl != 5:
                            config_update[i][j] = False

                    # dead cell rules
                    if a == 0:
                        # the dead cell may reborn
                        if Nl == 2:
                            config_update[i][j] = True

        config_compare = copy.deepcopy(config_update)

    return config_update
# -----------------------------------------------------------------------------
