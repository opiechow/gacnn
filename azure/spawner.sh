#!/bin/bash
for region in northeurope westeurope francecentral eastus eastus2
do
  for i in {1..4}
  do
    name=$region"worker"$i
    az vm create --location $region --size Standard_DS1_v2 --resource-group gacnn --name $name --image microsoft-dsvm:linux-data-science-vm-ubuntu:linuxdsvmubuntu:18.06.02 --admin-username valef --ssh-key-value id_windows.pub --no-wait
  done
done
