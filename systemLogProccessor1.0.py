path = '/Users/stefanbalta/Documents/codes/systemLogger/systemLogs.log'
inputFile = open(path, 'r')
rawData = inputFile.readlines()
for i in range(0, len(rawData)):
    rawData[i] = rawData[i].strip("\n")
rawData = list(filter(None, rawData))
macModel = rawData[0][rawData[0].index(":")+1:]
osVersion = rawData[1][rawData[1].index(":")+1:]
bootTime = rawData[3][rawData[3].index(":")+1:]
efficiencyCoreFrequencies = []
powerCoreFrequencies = []
systemInstructionsRetired = []
ANEPower = []
DRAMPower = []
CPUPower = []
GPUPower = []
PackagePower = []
for i in range(0, (len(rawData)-4)//45):
    efficiencyCoreFrequencies.append(int(rawData[7+45*i][rawData[7+45*i].index(":")+1:len(rawData[7+45*i])-3]))
    powerCoreFrequencies.append(int(rawData[25+45*i][rawData[25+45*i].index(":")+1:len(rawData[25+45*i])-3]))
    systemInstructionsRetired.append(float(rawData[42+45*i][rawData[42+45*i].index(":")+1:len(rawData[42+45*i])-4])*10**int((rawData[42+45*i][len(rawData[42+45*i])-2:])))
    ANEPower.append(int(rawData[44+45*i][rawData[44+45*i].index(":")+1:len(rawData[44+45*i])-3]))
    DRAMPower.append(int(rawData[45+45*i][rawData[45+45*i].index(":")+1:len(rawData[45+45*i])-3]))
    CPUPower.append(int(rawData[46+45*i][rawData[46+45*i].index(":")+1:len(rawData[46+45*i])-3]))
    GPUPower.append(int(rawData[47+45*i][rawData[47+45*i].index(":")+1:len(rawData[47+45*i])-3]))
    PackagePower.append(int(rawData[48+45*i][rawData[48+45*i].index(":")+1:len(rawData[48+45*i])-3]))
elapsedTime = (len(rawData)-4)/45
averagePower = (sum(PackagePower)/elapsedTime)/1000
energyUsed =  (sum(PackagePower))/1000
instructionsRetired = sum(systemInstructionsRetired)
instructionsRetiredPerSecond = instructionsRetired/(elapsedTime)
maxEfficiencyFrequency = max(efficiencyCoreFrequencies)
minEfficiencyFrequency = min(efficiencyCoreFrequencies)
averageEfficiencyFrequency = sum(efficiencyCoreFrequencies)/elapsedTime
maxPowerFrequency = max(powerCoreFrequencies)
minPowerFrequency = min(powerCoreFrequencies)
averagePowerFrequency = sum(powerCoreFrequencies)/elapsedTime
cpuEnergyUsed = sum(CPUPower)/1000
gpuEnergyUsed = sum(GPUPower)/1000
aneEnergyUsed = sum(ANEPower)/1000
dramEnergyUsed = sum(DRAMPower)/1000
percentageOfEnergyUsedByCPU = cpuEnergyUsed/energyUsed *100
percentageOfEnergyUsedByGPU = gpuEnergyUsed/energyUsed *100
percentageOfEnergyUsedByDRAM = dramEnergyUsed/energyUsed *100
percentageOfEnergyUsedByANE = aneEnergyUsed/energyUsed *100