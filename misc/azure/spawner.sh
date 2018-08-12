#!/bin/bash
for region in northeurope westeurope francecentral eastus eastus2
do
  for i in {1..4}
  do
    name=$region"worker"$i
    az vm create --location $region --size Standard_DS1_v2 --resource-group gacnn --name $name --image Canonical:UbuntuServer:17.10:latest --admin-username valef --ssh-key-value id_windows.pub --no-wait
  done
done
