from TuningFork import *

thick = 1/2 # inches
t_wide = 1/4

matter = {"Steel": Steel,
          "Brass": Brass,
          "Aluminum": Aluminum,
          "Lead": Lead}

rect_forks = {}
for key, val in matter.items():
    rect_forks[key] = RectangularTine(in2m(thick), in2m(t_wide), val)

f = 523.3

print("To make a tuning fork for {}Hz out of {}\" stock with {}\" think rectangual tines"
      .format(f, thick, t_wide) )
print("A tine (or prong) of the following length is required:\n");

for key, val in rect_forks.items():
    t_len = calc_fork_len(f, val)
    print("\t{}: {:0.3f} inches ({:0.2f} mm)".format(key, m2in(t_len), t_len*1000))
print("\n\n")




print("... And for a tuning fork for the same frequency with cylindrical tines of radius {}\"\n"
      .format(t_wide))

cyl_forks = {}
for key, val in matter.items():
    cyl_forks[key] = CylindricalTine(in2m(t_wide), val)

for key, val in cyl_forks.items():
    t_len = calc_fork_len(f, val)
    print("\t{}: {:0.3f} inches ({:0.2f} mm)".format(key, m2in(t_len), t_len*1000))

