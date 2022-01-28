import subprocess
import platform
import concurrent
def macOS()->None:
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
   trackData = False
   fileName = None
   userInput = input("Would you like to save data to .csv format (y for yes, all other inputs considered no): ")
   if(userInput == 'y' or userInput == 'Y'):
      trackData = True
      print("data trracking activated, data will be saved every 5 minutes!")
      fileName = input("please enter the name of the file you would like (do not include file extension): ")
      print("file will be saved in the directory the script was run in named SystemPerformanceData.csv")
   command = "sudo powermetrics -n 1 --samplers cpu_power".split()
   while(True):
      p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
      print("Elapsed Time: "+str(elapsedTime)+" s")
      print("energy used : "+str(energyUsed) + ' Joules')
      print("current CPU power draw : "+str(CPUPower[len(CPUPower)-1]/1000)+" Watts")
      print("current GPU power draw : "+str(GPUPower[len(GPUPower)-1]/1000)+" Watts")
      print("max CPU power draw : "+str(max(CPUPower)/1000)+" Watts")
      print("max GPU power draw : "+str(max(GPUPower)/1000)+" Watts")
      counter = counter + 1
if(__name__ == "__main__"):
   if(platform.system() == "Darwin"):
      macOS()