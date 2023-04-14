from meetingModel import MeetingModel
from numpy import linspace
import matplotlib.pyplot as plt
     
################# main #################

model = MeetingModel(consoleOutput=False, graphOutput=False)
model.loadTestNames()
mass_M, mass_G,_,B = model.processModel()

B.draw()
plt.show(block=False)

plt.figure()
plt.hist([m.current_priority for m in mass_M], bins=linspace(-1-0.5, len(mass_G)+1+0.5      ))
plt.hist([m.current_priority for m in mass_M if m.current_priority==-1], bins=linspace(-1-0.5, len(mass_G)+1+0.5      ))
# plt.axis([-2,55,0,55])
plt.figure()
plt.hist([g.current_priority for g in mass_G],  bins=linspace(-1-0.5, len(mass_M)+1+0.5      ))
plt.hist([g.current_priority for g in mass_G if g.current_priority==-1], bins=linspace(-1-0.5, len(mass_M)+1+0.5      ))
# plt.axis([-2,55,0,55])
plt.show()










