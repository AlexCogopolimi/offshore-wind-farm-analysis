import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import pandas as pd

##################################################################################
# PROBLEM DATA
##################################################################################

Plant_size = 495  # MW
AEO = 1574886.03238195  # MWh/y
lyfetime = 30  # y
AMM_CIV_y = 20  # y
AMM_Equipment_y = 12  # y

# costs
CAPEX_2 = 0.4775
CAPEX_1 = 0.4442
CAPEX_0 = 0.0784
CAPEX_CIVIL = 0.2135
CAPEX_EQUIPMENT = 1 - CAPEX_CIVIL

CAPEX_OVERALL = 1403981000  # €

DECEX_BASE = 213.63  # €/kW
OPEX_BASE = 97.11  # €/kW/y

FIP = 179.45  # €/MWh
EE = 117.37  # €/MWh

# indexes
r = 0.065
TAX_rate = 0.35
Infl_rate = 0.01

year_vect = np.arange(-2, lyfetime + 3)  # from -2 to 32


##################################################################################
# ECONOMICS FUNCTION
##################################################################################

def calculate_economics(capex, opex, wacc, decex, revenues, aeo, mode='OFF'):

    AMM_civil_value = (CAPEX_CIVIL * np.sum(capex)) / AMM_CIV_y
    AMM_Equipment_value = (CAPEX_EQUIPMENT * np.sum(capex)) / AMM_Equipment_y

    AMM_civil_vect = np.zeros(len(year_vect))
    AMM_equipment_vect = np.zeros(len(year_vect))

    AMM_civil_vect[3:(AMM_CIV_y + 3)] = AMM_civil_value
    AMM_equipment_vect[3:(AMM_Equipment_y + 3)] = AMM_Equipment_value
    AMM_overall = AMM_equipment_vect + AMM_civil_vect

    Profit = revenues - opex - AMM_overall
    Taxes = TAX_rate * Profit

    EXPANDITURE = capex + opex + decex + Taxes
    CF = revenues - EXPANDITURE

    discount_denominators = ((1 + wacc) ** year_vect)

    DCF = CF / discount_denominators
    CDCF = np.cumsum(DCF)
    NPV = CDCF[-1]

    def NPV_for_lcoe(guess_price):
        price_vect = np.ones(len(year_vect)) * guess_price
        REV_LCOE = price_vect * aeo
        PROFIT_LCOE = REV_LCOE - opex - AMM_overall
        taxes_LCOE = PROFIT_LCOE * TAX_rate
        EXPANDITURE_LCOE = capex + opex + decex + taxes_LCOE
        CF_LCOE = REV_LCOE - EXPANDITURE_LCOE
        DCF_LCOE = CF_LCOE / discount_denominators
        CDCF_LCOE = np.cumsum(DCF_LCOE)
        return CDCF_LCOE[-1]

    def NPV_for_irr(guess_wacc):
        denom = ((1 + guess_wacc) ** year_vect)
        DCF_IRR = CF / denom
        CDCF_IRR = np.cumsum(DCF_IRR)
        return CDCF_IRR[-1]

    LCOE = brentq(NPV_for_lcoe, 0, 350)
    IRR = brentq(NPV_for_irr, 0.005, 0.15)
    PBT = np.argmax(CDCF > 0) - 2

    if mode == 'OFF':
        return NPV, LCOE, IRR, PBT, CDCF
    else:
        result_complete = [year_vect, revenues, capex, opex, AMM_overall,
                           Taxes, Profit, EXPANDITURE, CF, CDCF]
        return result_complete


##################################################################################
# HELPERS: build vectors
##################################################################################

def build_base_case(use_fip=True):
    capex = np.zeros(len(year_vect))
    capex[0] = CAPEX_2 * CAPEX_OVERALL
    capex[1] = CAPEX_1 * CAPEX_OVERALL
    capex[2] = CAPEX_0 * CAPEX_OVERALL

    opex = np.zeros(len(year_vect))
    for i in range(3, len(opex) - 2):
        opex[i] = Plant_size * 1000 * OPEX_BASE * ((1 + Infl_rate) ** (i - 3))

    decex = np.zeros(len(year_vect))
    decex[-2] = DECEX_BASE * Plant_size * 1000 * 0.5
    decex[-1] = DECEX_BASE * Plant_size * 1000 * 0.5

    aeo = np.zeros(len(year_vect))
    aeo[3:-2] = AEO

    revenues = np.zeros(len(year_vect))
    for i in range(3, len(opex) - 2):
        if use_fip and i < 29:
            price = FIP
        else:
            price = EE
        revenues[i] = price * aeo[i]   # <-- corretto: dipende da aeo

    wacc = np.ones(len(year_vect)) * r

    return capex, opex, decex, aeo, revenues, wacc


def build_upgrade_case(use_fip=True):
    capex = np.zeros(len(year_vect))
    capex[0] = CAPEX_2 * CAPEX_OVERALL
    capex[1] = CAPEX_1 * CAPEX_OVERALL
    capex[2] = CAPEX_0 * CAPEX_OVERALL

    def opex_fun(x):
        return (0.0000028*x**6 - 0.0002638*x**5 + 0.0098668*x**4
                - 0.1889131*x**3 + 1.9838511*x**2 - 11.6865898*x + 107.0016702)

    opex = np.zeros(len(year_vect))
    for i in range(3, len(opex) - 2):
        opex[i] = opex_fun(i - 2)

    decex = np.zeros(len(year_vect))
    decex[-2] = DECEX_BASE * Plant_size * 1000 * 0.5
    decex[-1] = DECEX_BASE * Plant_size * 1000 * 0.5

    aeo = np.zeros(len(year_vect))
    for i in range(len(aeo)):
        if 2 < i < 33:
            aeo[i] = (1580 - 9.2213 * (i - 2)) * 1000

    revenues = np.zeros(len(year_vect))
    for i in range(3, len(opex) - 2):
        if use_fip and i < 29:
            price = FIP
        else:
            price = EE
        revenues[i] = price * aeo[i]

    wacc = np.ones(len(year_vect)) * r

    return capex, opex, decex, aeo, revenues, wacc


##################################################################################
# RUN BASE + UPGRADE (with FIP)
##################################################################################

capex_b, opex_b, decex_b, aeo_b, rev_b, wacc_b = build_base_case(use_fip=True)
NPV_b, LCOE_b, IRR_b, PBT_b, CDCF_b = calculate_economics(capex_b, opex_b, wacc_b, decex_b, rev_b, aeo_b)
print(f'BASE: NPV={NPV_b:.4e}, LCOE={LCOE_b:.2f}, IRR={IRR_b:.4f}, PBT={PBT_b}')

capex_u, opex_u, decex_u, aeo_u, rev_u, wacc_u = build_upgrade_case(use_fip=True)
NPV_u, LCOE_u, IRR_u, PBT_u, CDCF_u = calculate_economics(capex_u, opex_u, wacc_u, decex_u, rev_u, aeo_u)
print(f'UPGRADE: NPV={NPV_u:.4e}, LCOE={LCOE_u:.2f}, IRR={IRR_u:.4f}, PBT={PBT_u}')


##################################################################################
# PLOT CDCF BASE and UPGRADE
##################################################################################

def plot_cdccf_single(CDCF, title):
    plt.figure(figsize=(11, 5))
    plt.bar(year_vect, CDCF/1e6, alpha=0.8)
    plt.axhline(0, color='red', linestyle='--', linewidth=1.3)
    plt.title(title)
    plt.xlabel("years")
    plt.ylabel("CDCF [M€]")
    plt.xticks(np.arange(min(year_vect), max(year_vect)+1, 2))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


plot_cdccf_single(CDCF_b, "BASE - Cumulative discounted cash flow")
plot_cdccf_single(CDCF_u, "UPGRADE - Cumulative discounted cash flow")


##################################################################################
# COMPARISON BASE vs UPGRADE (with FIP)
##################################################################################

plt.figure(figsize=(12, 6))
plt.bar(year_vect-0.2, CDCF_u/1e6, width=0.4, label="CDCF_upgrade")
plt.bar(year_vect+0.2, CDCF_b/1e6, width=0.4, label="CDCF_base")
plt.axhline(0, color='black', linewidth=1)
plt.title("comparison BASE vs UPGRADE scenarios")
plt.xlabel("years")
plt.ylabel("CDCF [M€]")
plt.xticks(np.arange(min(year_vect), max(year_vect)+1, 2))
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


##################################################################################
# COMPARISON BASE vs UPGRADE (NO FIP)
##################################################################################

capex_bNF, opex_bNF, decex_bNF, aeo_bNF, rev_bNF, wacc_bNF = build_base_case(use_fip=False)
_, _, _, _, CDCF_bNF = calculate_economics(capex_bNF, opex_bNF, wacc_bNF, decex_bNF, rev_bNF, aeo_bNF)

capex_uNF, opex_uNF, decex_uNF, aeo_uNF, rev_uNF, wacc_uNF = build_upgrade_case(use_fip=False)
_, _, _, _, CDCF_uNF = calculate_economics(capex_uNF, opex_uNF, wacc_uNF, decex_uNF, rev_uNF, aeo_uNF)

plt.figure(figsize=(12, 6))
plt.bar(year_vect-0.2, CDCF_uNF/1e6, width=0.4, label="UPGRADE")
plt.bar(year_vect+0.2, CDCF_bNF/1e6, width=0.4, label="BASE")
plt.axhline(0, color='black', linewidth=1)
plt.title("comparison BASE vs UPGRADE scenarios no FIP")
plt.xlabel("years")
plt.ylabel("CDCF [M€]")
plt.xticks(np.arange(min(year_vect), max(year_vect)+1, 2))
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

plot_cdccf_single(CDCF_bNF, "BASE no-FIP - Cumulative discounted cash flow")
plot_cdccf_single(CDCF_uNF, "UPGRADE no-FIP - Cumulative discounted cash flow")


##################################################################################
# SENSITIVITY ANALYSIS (generic)
##################################################################################

def sensitivity_analysis(param_name, build_case_fun, apply_fun):
    sens = np.array([0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2])
    npv_vect, lcoe_vect, irr_vect, pbt_vect = [], [], [], []

    capex, opex, decex, aeo, revenues, wacc = build_case_fun(use_fip=True)

    for f in sens:
        capex_s, opex_s, decex_s, aeo_s, rev_s, wacc_s = apply_fun(
            capex.copy(), opex.copy(), decex.copy(), aeo.copy(), revenues.copy(), wacc.copy(), f
        )
        NPV, LCOE, IRR, PBT, _ = calculate_economics(capex_s, opex_s, wacc_s, decex_s, rev_s, aeo_s)

        npv_vect.append(NPV)
        lcoe_vect.append(LCOE)
        irr_vect.append(IRR)
        pbt_vect.append(PBT)

    # plots
    fig, axs = plt.subplots(2,2, figsize=(10,7))
    axs[0,0].plot(sens*100, np.array(npv_vect)/1e6, marker='o', label=f'NPV variation with {param_name}')
    axs[0,1].plot(sens*100, np.array(lcoe_vect), marker='o', label=f'LCOE variation with {param_name}')
    axs[1,0].plot(sens*100, np.array(irr_vect)*100, marker='o', label=f'IRR variation with {param_name}')
    axs[1,1].plot(sens*100, np.array(pbt_vect), marker='o', label=f'PBT variation with {param_name}')

    for ax in axs.ravel():
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        ax.set_xlabel('%')

    axs[0,0].set_ylabel('M€')
    axs[0,1].set_ylabel('€/MWh')
    axs[1,0].set_ylabel('%')
    axs[1,1].set_ylabel('years')

    plt.tight_layout()
    plt.show()


# ---- Apply functions for each parameter ----
def apply_capex(capex, opex, decex, aeo, rev, wacc, f):
    capex *= f
    return capex, opex, decex, aeo, rev, wacc

def apply_opex(capex, opex, decex, aeo, rev, wacc, f):
    opex *= f
    return capex, opex, decex, aeo, rev, wacc

def apply_decex(capex, opex, decex, aeo, rev, wacc, f):
    decex *= f
    return capex, opex, decex, aeo, rev, wacc

def apply_wacc(capex, opex, decex, aeo, rev, wacc, f):
    wacc *= f
    return capex, opex, decex, aeo, rev, wacc

def apply_aeo(capex, opex, decex, aeo, rev, wacc, f):
    aeo *= f
    rev *= f
    return capex, opex, decex, aeo, rev, wacc


##################################################################################
# RUN SENSITIVITY (BASE CASE)
##################################################################################

sensitivity_analysis("capex", build_base_case, apply_capex)
sensitivity_analysis("opex", build_base_case, apply_opex)
sensitivity_analysis("decex", build_base_case, apply_decex)
sensitivity_analysis("wacc", build_base_case, apply_wacc)
sensitivity_analysis("AEO", build_base_case, apply_aeo)