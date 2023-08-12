# handeling ssh-copy-id
scp ./prerequisite/script.sh storage2:/ #mv script to vm
docker cp /script.sh storage:/ #cp script to container
docker exec -it storage bash -c " /script.sh" # runnig it from outside of container
docker cp storage:/script.sh ./test.sh # mv result to local vm path
scp ./test.sh mc:/root/cosBench/ClusterBench/conf #mv files to mc

