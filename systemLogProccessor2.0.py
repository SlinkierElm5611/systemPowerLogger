import subprocess
import platform
def macOS():
   efficiencyCoreFrequencies = []
   powerCoreFrequencies = []
   systemInstructionsRetired = []
   ANEPower = []
   DRAMPower = []
   CPUPower = []
   GPUPower = []
   PackagePower = []
   counter = 1
   macModel = None
   osVersion = None
   bootTime = None
   elapsedTime = None
   averagePower = None
   energyUsed = None
   instructionsRetired = None
   instructionsRetiredPerSecond = None
   maxEfficiencyFrequency = None
   minEfficiencyFrequency = None
   maxPowerFrequency = None
   minPowerFrequency = None
   averageEfficiencyFrequency = None
   averagePowerFrequency = None
   cpuEnergyUsed = None
   gpuEnergyUsed = None
   aneEnergyUsed = None
   dramEnergyUsed = None
   percentageOfEnergyUsedByANE = None
   percentageOfEnergyUsedByCPU = None
   percentageOfEnergyUsedByGPU = None
   percentageOfEnergyUsedByDRAM = None
   sudoPass = input("please enter sudo password:")
   while(True):
      command = "sudo powermetrics -n 1 --samplers cpu_power".split() #each set of data is good for 5 seconds
      p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
      sudoPrompt = p.communicate(sudoPass+"\n")[1]
      rawData = p.communicate()[0].split("\n")
      for i in range(0, len(rawData)):
         rawData[i] = rawData[i].strip("\n")
      rawData = list(filter(None, rawData))
      efficiencyCoreFrequencies.append(int(rawData[7][rawData[7].index(":")+1:len(rawData[7])-3]))
      powerCoreFrequencies.append(int(rawData[25][rawData[25].index(":")+1:len(rawData[25])-3]))
      systemInstructionsRetired.append(float(rawData[42][rawData[42].index(":")+1:len(rawData[42])-4])*10**int((rawData[42][len(rawData[42])-2:])))
      ANEPower.append(int(rawData[44][rawData[44].index(":")+1:len(rawData[44])-3]))
      DRAMPower.append(int(rawData[45][rawData[45].index(":")+1:len(rawData[45])-3]))
      CPUPower.append(int(rawData[46][rawData[46].index(":")+1:len(rawData[46])-3]))
      GPUPower.append(int(rawData[47][rawData[47].index(":")+1:len(rawData[47])-3]))
      PackagePower.append(int(rawData[48][rawData[48].index(":")+1:len(rawData[48])-3]))
      elapsedTime = counter * 5
      averagePower = (sum(PackagePower)/elapsedTime)/1000
      energyUsed =  (sum(PackagePower)*5)/1000
      instructionsRetired = sum(systemInstructionsRetired)
      instructionsRetiredPerSecond = instructionsRetired/(elapsedTime)
      maxEfficiencyFrequency = max(efficiencyCoreFrequencies)
      minEfficiencyFrequency = min(efficiencyCoreFrequencies)
      averageEfficiencyFrequency = sum(efficiencyCoreFrequencies)/counter
      maxPowerFrequency = max(powerCoreFrequencies)
      minPowerFrequency = min(powerCoreFrequencies)
      averagePowerFrequency = sum(powerCoreFrequencies)/counter
      cpuEnergyUsed = sum(CPUPower)/1000
      gpuEnergyUsed = sum(GPUPower)/1000
      aneEnergyUsed = sum(ANEPower)/1000
      dramEnergyUsed = sum(DRAMPower)/1000
      percentageOfEnergyUsedByCPU = cpuEnergyUsed/energyUsed *100
      percentageOfEnergyUsedByGPU = gpuEnergyUsed/energyUsed *100
      percentageOfEnergyUsedByDRAM = dramEnergyUsed/energyUsed *100
      percentageOfEnergyUsedByANE = aneEnergyUsed/energyUsed *100
      print(elapsedTime)
      print(energyUsed)
      counter = counter + 1
if(platform.system() == "Darwin"):
   macOS()