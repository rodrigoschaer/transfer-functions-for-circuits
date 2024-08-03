NETLIST = """
* Example Circuit
Vs V1 0 DC 0
RB V1 V2 RB
r_pi V2 V3 r_pi
I1 V3 0 DC gm*V_be
RC V3 V0 RC
"""
