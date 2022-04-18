weight = 1.5
ground_flat_charges = 20
cost_ground_premium = 125

if weight > 10:
  ground_cost = weight * 4.75 + ground_flat_charges
elif weight > 6 and weight <= 10:
  ground_cost = weight * 4 + ground_flat_charges
elif weight > 2 and weight <=6:
  ground_cost = weight * 3 + ground_flat_charges
else:
  ground_cost = weight * 1.5 + ground_flat_charges



if weight > 10:
  dron_cost = weight * 14.25
elif weight > 6 and weight <= 10:
  dron_cost = weight * 12
elif weight > 2 and weight <=6:
  dron_cost = weight * 9
else:
  dron_cost = weight * 4.5

print("Package weight:" ,weight,"lb")
print("Ground cost: $",ground_cost)
print("Dron cost: $",dron_cost)
print("Ground premium: &", cost_ground_premium)