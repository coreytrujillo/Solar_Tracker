# Light Tower
AIN_D = 'AIN9' # Direct LT AIN
AIN_NS = 'AIN10' # NS LT AIN
AIN_EW = 'AIN11' # EW LT AIN

###################################
# Tracker Variables
###################################
# Optimal light tower values (mV)
LTNS_opt = 5.5
LTEW_opt = 5.5

# Cycle Time (sec)
cycletime = 30

# Light Tower variances and boundaries
LTNS_var_N = 0.5#0.40
LTNS_var_S = LTNS_var_N
LTEW_var_E = 1
LTEW_var_W = 2.5
LTNS_backstop = 0.05
LTEW_backstop = 0.4

# NSEW Relay Controls
FIOS = 'FIO2' # South
FION = 'FIO3' # North
FIOW = 'FIO4' # West
FIOE = 'FIO5' # East

# Light Tower move and stop values
LT_moveN = LTNS_opt - LTNS_var_S
LT_moveS = LTNS_opt + LTNS_var_N
LT_moveE = LTEW_opt + LTEW_var_W
LT_moveW = LTEW_opt - LTEW_var_E
LT_stopN = LT_moveS - LTNS_backstop
LT_stopS = LT_moveN + LTNS_backstop
LT_stopE = LT_moveW + LTEW_backstop
LT_stopW = LT_moveE - LTEW_backstop