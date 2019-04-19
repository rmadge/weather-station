import collections

# 33k, 6.57k, 8.2k, 891, 1k, 688, 2.2k, 1.41k, 3.9k, 3.14k, 16k, 14.12k, 120k, 42.12k, 64.9k, 21.88k
resistances = [33000, 6570, 8200, 891, 1000, 688, 2200, 1410, 3900, 3140, 16000, 14120, 120000, 42120, 64900, 21880]
volts = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 1.2, 1.4, 1.8, 2.0, 2.2, 2.5, 2.7, 2.8, 2.9]

def voltage_divider(r1, r2, vin):
    vout = (vin * r1)/(r1 + r2)    
    return round(vout, 1)

volts_resistence = {}
for x in range(len(resistances)):
    vout = voltage_divider(4700, resistances[x], 3.3)
    volts_resistence[vout] = resistances[x]
    print(resistances[x], vout)

print(collections.OrderedDict(sorted(volts_resistence.items())))

# r1 = 33K ohms, r2 = 10K, vin = 5V = 3.837V (OUT)
#print(voltage_divider(33000, 10000, 5.0))