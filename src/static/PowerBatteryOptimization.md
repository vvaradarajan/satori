<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML"></script>
## Optimizing Battery use in the Power Grid

### Overview:
The approach is to write out the equations for the total cost over a period.
The cost savings will be the same for each period, and the natural period
is 24 hrs (Conceptually the period of the power consumption/
congestion based pricing).
Then this total cost is minimized.
The problem is modelled as a set of linear equations with constraints. The optimization solution is then just evaluation at each of the constraint extremes and choosing the best one.

### Equations:
Glossary: Letters that are lower-case are functions of t (time).
p = power consumption
pb = power from battery
r = cost of unit power (In congestion pricing, varies over time)

c = cost over a period (This is the cost we want to minimize)
T = period (i.e. 24 hrs)

** Equ 1:**
\`c = int_0^T  (p-pb)r\ dt\`  
(i.e p-pb = power taken from grid, r = cost/unit )

** Equ 2:**
\`int_0^T pb\ dt = 0\`  
(i.e. over a period, the battery must charge/discharge equally)

** Equ 3:** This is rate tier equation. For this purpose, assume 2 tier pricing:
RA = pricing for tier a. tier a is time period 0 to TA  
RB = pricing for tier b. tier b is time period TA to T  
The function r is then:  
\`r=RA \  where\ 0<t<TA\`  
\`r=RB \  where\ TA<t<T\`   

### Derivations:
Substitute Equ 3 into Equ 1 for r

\`c = int_0^(TA) (p-pb)RA\ dt  + int_(TA)^T (p-pb)RB\ dt\`
  \`= int_0^(TA) (p)RA\ dt + int_(TA)^T (p)RB\ dt \` ==> only based on p
  \`  - (int_0^(TA) (pb)RA\ dt + int_(TA)^T (pb)RB\ dt))\` ==> based on pb

Note that the first part of the equation is only dependent on the p (the power consumption) and therefore not relevant to optimization, since p cannot be controlled.
The second part of the equation depends on pb (the battery power) which can be controlled, and therefore optimized.

The problem is then to maximize:
** Equ 4:**
\`c = int_0^(TA) (pb)RA\ dt + int_(TA)^T (pb)RB dt\`

pb = battery power output. This has some physical constraints:  
PMIN < pb < PMAX (The max/min power output from the battery)

This is in addition to the constraint in Eqn 2.

*** Assumption: ***
Intuitively, we can assume that pb will have a constant value in each pricing interval (0 to TA, TA to T). So:  
PTA = pb  value from 0 to TA.  
PTB = pb value from TA to T.

Equ 4 then becomes:

\`PTA.RA.TA + PTB.RB.(T-TA)\`  

and we have constraint (Equ 2):
\`int_0^T Pb\ dt =0\` ==> \`PTA.TA + PTB.(T-TA) = 0\` ==>  
\` PTB= - (PTA.TA)/(T-TA)\`  

Substituting the value of PTB in the above equation 4:

\`PTA.RA.TA - (PTA.TA)/(T-TA).RB.(T-TA) = PTA.(RA.TA - RB.TA)\`

This value needs to be maximized. Here only PTA can be changed (and assume RA > RB). Therefore we just need to find the max for the extreme values of PTA.
The extreme values are:  
\`PTA = PMAX\` ==> now calculate PTB using \`PTB= - (PTA*TA)/(T-TA)\`  
If PTB not between PMIN and PMAX, then set PTB = PMIN and calculate PTA.

This gives the values for PTA and PTB.

### Application Examples

1. Flat rate pricing (no Tiers) and no Solar power. In this case RA=RB.
Using Equ 4, we have to maximize PTA*(RA*TA- RB*TA).
If RA=RB, this is just 0 and cannot be maximized.  The physical interpretation is that there is no value to the battery.

2. Two Tiers with one the double of the other: \`RA=2.RB\`  
We have to maximize:  
\` PTA.(RA.TA- RB.TA)  => PTA.(2.RB.TA-RB.TA) =>
PTA.RB.TA\`  
The highest value is when \`PTA = PMAX\`  
Then \`PTB= -(PTA.TA)/(T-TA)\`  
The constraint PTB > PMIN requires verification. If this is not satisified, then we set PTB=PMIN and determine the value of PTA.

3. Power Consumption falls below PTA. This is another constraint that PTA < p. (i.e. battery output cannot exceed power consumption)
Here then entire power required is supplied by the battery. The equations will reduce to PTA supplying all the power and PTB just charging the battery during the lower rates.

4. Battery Capacity constraint. This is further constraint in which the total energy in the battery cannot exceed the capacity.
C = battery Capacity  
e = current battery energy  
EI = energy in battery at start of cycle.  
EMIN = minimum energy required in the battery.  
For the two tier scenario the equations have to be split by time of the tiers, which corresponds to the charging and the discharging cycles. PTB is the charging and PTA is the discharge.
We can set EI=EMIN at the start of the charging cycle. Then
e = PTB(T-TA) + EI < C.
and
e = PTA(T) > EMIN
These constraints also have to be applied when maximizing Equ 4.

5. Inclusion of Solar Energy Source.  A simple way of accounting for this is to modify Eqn 2: \`int_0^T Pb\ dt =0\`  (i.e. over a period, the battery must charge/discharge equally) to
\`int_0^T Pb\ dt = -S\`  (i.e. over a period, the battery must charge/discharge equal to the Solar power input).  The rest of the derivations as similar to examples 1-4.  
...
and e < C for all t.
