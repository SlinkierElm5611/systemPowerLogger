import subprocess
import platform
import threading
class dataClass:
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
   elapsedTime = None
def exportData(data :dataClass, filename :str)->None:
   outputString = ''
   if(data.counter == 12):
      outputString = outputString + "Pacakge Power,CPU Power,GPU Power,ANE Power,DRAM Power,High Efficiency Core Frequencies,High Performance Core Frequencies,System Instructions Retired\n"
   for i in range(0, 12):
      outputString = outputString + str(data.PackagePower[len(data.PackagePower) - 12 + i]) + ','
      outputString = outputString + str(data.CPUPower[len(data.CPUPower) - 12 + i]) + ','
      outputString = outputString + str(data.GPUPower[len(data.GPUPower) - 12 + i]) + ','
      outputString = outputString + str(data.ANEPower[len(data.ANEPower) - 12 + i]) + ','
      outputString = outputString + str(data.DRAMPower[len(data.DRAMPower) - 12 + i]) + ','
      outputString = outputString + str(data.efficiencyCoreFrequencies[len(data.efficiencyCoreFrequencies) -12 + i]) + ','
      outputString = outputString + str(data.powerCoreFrequencies[len(data.powerCoreFrequencies) - 12 + i ]) + ','
      outputString = outputString + str(data.systemInstructionsRetired[len(data.systemInstructionsRetired) - 12 + i]) + ','
      outputString = outputString + '\n'
   writingFile = open(filename, 'a')
   writingFile.write(outputString)
   writingFile.close()
   print(outputString)
   return None
def macOS()->None:
   data = dataClass()
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
      x = threading.Thread(target=exportData, args=(data, fileName))
      if(data.counter >= 1 and data.counter%12 == 0 and trackData == True):
         x.start()
      p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
      if(data.counter >= 1 and data.counter%12 == 0 and trackData == True):
         x.join()
      rawData = p.communicate()[0].split("\n")
      for i in range(0, len(rawData)):
         rawData[i] = rawData[i].strip("\n")
      rawData = list(filter(None, rawData))
      data.efficiencyCoreFrequencies.append(int(rawData[7][rawData[7].index(":")+1:len(rawData[7])-3]))
      data.powerCoreFrequencies.append(int(rawData[25][rawData[25].index(":")+1:len(rawData[25])-3]))
      data.systemInstructionsRetired.append(float(rawData[42][rawData[42].index(":")+1:len(rawData[42])-4])*10**int((rawData[42][len(rawData[42])-2:])))
      data.ANEPower.append(int(rawData[44][rawData[44].index(":")+1:len(rawData[44])-3]))
      data.DRAMPower.append(int(rawData[45][rawData[45].index(":")+1:len(rawData[45])-3]))
      data.CPUPower.append(int(rawData[46][rawData[46].index(":")+1:len(rawData[46])-3]))
      data.GPUPower.append(int(rawData[47][rawData[47].index(":")+1:len(rawData[47])-3]))
      data.PackagePower.append(int(rawData[48][rawData[48].index(":")+1:len(rawData[48])-3]))
      data.elapsedTime = data.counter * 5
      data.averagePower = (sum(data.PackagePower)/data.elapsedTime)/1000
      data.energyUsed =  (sum(data.PackagePower)*5)/1000
      data.instructionsRetired = sum(data.systemInstructionsRetired)
      data.instructionsRetiredPerSecond = data.instructionsRetired/(data.elapsedTime)
      data.maxEfficiencyFrequency = max(data.efficiencyCoreFrequencies)
      data.minEfficiencyFrequency = min(data.efficiencyCoreFrequencies)
      data.averageEfficiencyFrequency = sum(data.efficiencyCoreFrequencies)/data.counter
      data.maxPowerFrequency = max(data.powerCoreFrequencies)
      data.minPowerFrequency = min(data.powerCoreFrequencies)
      data.averagePowerFrequency = sum(data.powerCoreFrequencies)/data.counter
      data.cpuEnergyUsed = sum(data.CPUPower)/1000
      data.gpuEnergyUsed = sum(data.GPUPower)/1000
      data.aneEnergyUsed = sum(data.ANEPower)/1000
      data.dramEnergyUsed = sum(data.DRAMPower)/1000
      data.percentageOfEnergyUsedByCPU = data.cpuEnergyUsed/data.energyUsed *100
      data.percentageOfEnergyUsedByGPU = data.gpuEnergyUsed/data.energyUsed *100
      data.percentageOfEnergyUsedByDRAM = data.dramEnergyUsed/data.energyUsed *100
      data.percentageOfEnergyUsedByANE = data.aneEnergyUsed/data.energyUsed *100
      print("Elapsed Time: "+str(data.elapsedTime)+" s")
      print("energy used : "+str(data.energyUsed) + ' Joules')
      print("current CPU power draw : "+str(data.CPUPower[len(data.CPUPower)-1]/1000)+" Watts")
      print("current GPU power draw : "+str(data.GPUPower[len(data.GPUPower)-1]/1000)+" Watts")
      print("max CPU power draw : "+str(max(data.CPUPower)/1000)+" Watts")
      print("max GPU power draw : "+str(max(data.GPUPower)/1000)+" Watts")
      data.counter = data.counter + 1
if(__name__ == "__main__"):
   if(platform.system() == "Darwin"):
      macOS()