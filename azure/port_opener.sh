#!/bin/bash
for region in northeurope westeurope francecentral eastus eastus2
do
  for i in {1..4}
  do
    name=$region"worker"$i
    az vm open-port --port 4123-4124 --resource-group gacnn --name $name
  done
done
