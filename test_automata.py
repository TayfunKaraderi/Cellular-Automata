# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:38:45 2018

@author: karad
"""

import numpy as np
import automata

Tl_1 = [[False, False, False, False, False], [False, True, True, True, False], [False, False, False, True, False], [False, False, True, False, False], [False, False, False, False, False]]
Ol_1 = np.array([[0, 0, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

Tlp_1 = np.array([[1,1,1],[0,0,0],[0,0,0]])
Olp_1 = np.array([[1,1,1],[1,1,1],[1,1,1]])
Olp_2 = np.array([[0,0,0],[0,0,0],[0,0,0]])

TlF_1 = [[1,1,1],[0,0,0],[0,0,0]]
OlF_1 = np.array([[0,1,0],[0,1,0],[0,0,0]])
OlF_2 = np.array([[False,False,False],[False,False,False],[False,False,False]])


Ts_1 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 5, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
Os_1 = np.array([[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])

Ts_2 = [[0,0,16],[0,0,0],[16,0,0]]
Os_2 = np.array([[2,1,2],[1,0,1],[2,1,2]])

Tl3dF_1 = [[[0,0,0],[0,1,0],[0,0,0]], [[0,1,0],[1,0,1],[0,1,0]], [[0,0,0],[0,0,0],[0,0,0]]]
Ol3dF_1 = np.array([[[0,0,0],[0,1,0],[0,0,0]], [[0,0,0],[0,1,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]])
Ol3dF_2 = np.array([[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]])

Tl3dL_1 = [[[False,False,False],[False,True,False],[False,False,False]], [[False,True,False],[True,False,True],[False,True,False]], [[False,False,False],[False,False,False],[False,False,False]]]
Ol3dT_1 = np.array([[[True,True,True],[True,True,True],[True,True,True]], [[True,True,True],[True,True,True],[True,True,True]], [[True,True,True],[True,True,True],[True,True,True]]])
Ol3dT_2 = np.array([[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]])

hex1 = [[True, False], [True, True, False], [True, False]]
hext1 = [[0, 1], [1, 1, 0], [0, 1]]
hext2 = [[0, 0], [0, 1, 0], [0, 0]]
hext3 = [[0, 0], [0, 0, 0], [0, 0]]

hex2 = [[0,0,0,0],[0,0,0,0,0],[0,1,1,0],[0,0,0,0,0]]
hex2t1 = [[0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0, 0]]
hex2t2 = [[0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0, 0]]
hex2t3 = [[0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0, 0]]

def test_life():
    Output = automata.life(Tl_1, 4, True) # glider
    Out1 = automata.life(Tlp_1, 1, True)
    Out2 = automata.life(Tlp_1, 2, True)
    
    Out3 = automata.life(TlF_1, 1, False)
    Out4 = automata.life(TlF_1, 2, False)
    
    for i in range(5):
        for j in range(5):
            assert Output[i,j] == Ol_1[i,j]
            
    for i in range(3):
        for j in range(3):
            assert Out1[i,j] == Olp_1[i,j]
            assert Out2[i, j] == Olp_2[i,j]
            assert Out3[i, j] == OlF_1[i,j]
            assert Out4[i, j] == OlF_2[i,j]

def test_sandpile():
    Output = automata.sandpile(Ts_1)
    Output2 = automata.sandpile(Ts_2)
    
    for i in range(4):
        for j in range(4):
            assert Output[i,j] == Os_1[i,j]
            
    for i in range(3):
        for j in range(3):
            assert Output2[i,j] == Os_2[i,j]

def test_life3d():
    Output1 = automata.life3d(Tl3dL_1, 1, False)
    Output2 = automata.life3d(Tl3dL_1, 2, False)
    Output3 = automata.life3d(Tl3dL_1, 1, True)
    Output4 = automata.life3d(Tl3dL_1, 2, True)
    
    for i in range(3):
        for j in range(3):
            for k in range(3):
                assert Output1[i,j,k] == Ol3dF_1[i,j,k]
                assert Output2[i,j,k] == Ol3dF_2[i,j,k]
                assert Output3[i,j,k] == Ol3dT_1[i,j,k]
                assert Output4[i,j,k] == Ol3dT_2[i,j,k]


def test_lifehex():
    Output1 = automata.lifehex(hex1, 1)
    Output2 = automata.lifehex(hex1, 2)
    Output3 = automata.lifehex(hex1, 3)
    
    for i in range(3):
        if i%2:
            for j in range(3):
                assert Output1[i][j] == hext1[i][j]
                assert Output2[i][j] == hext2[i][j]
                assert Output3[i][j] == hext3[i][j]
        if not i%2:
            for j in range(2):
                assert Output1[i][j] == hext1[i][j]
                assert Output2[i][j] == hext2[i][j]
                assert Output3[i][j] == hext3[i][j]