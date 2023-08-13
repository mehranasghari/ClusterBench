docker exec test bash -c "swift-ring-builder /rings/account.builder" > ./account.txt
docker exec test bash -c "swift-ring-builder /rings/object.builder" > ./object.txt
docker exec test bash -c "swift-ring-builder /rings/container.builder" > ./container.txt