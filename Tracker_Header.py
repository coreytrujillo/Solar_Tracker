# FIO Relay Controls
FIOS = 'FIO2'
FION = 'FIO3'
FIOW = 'FIO4'
FIOE = 'FIO5'

# Optimal light tower values (mV)
LTNS_opt = 5
LTEW_opt = 6


# Light Tower variances and boundaries
LTNS_var_N = 1.5#0.40
LTNS_var_S = LTNS_var_N
LTEW_var_E = 2.5
LTEW_var_W = 2.5
LTNS_backstop = 0.05
LTEW_backstop = 0.05

# Cycle Time
cycletime = 30


# Light Tower move and stop values
LT_moveN = LTNS_opt - LTNS_var_S
LT_moveS = LTNS_opt + LTNS_var_N
LT_moveE = LTEW_opt + LTEW_var_W
LT_moveW = LTEW_opt - 1#- LTEW_var_E
LT_stopN = LT_moveS - LTNS_backstop
LT_stopS = LT_moveN + LTNS_backstop
LT_stopE = LT_moveW + LTEW_backstop
LT_stopW = LTEW_opt + 1 #LT_moveE - LTEW_backstop