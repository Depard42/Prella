docker run -d \
-p 80:8123 \
--name=prella \
-e PRELLA_LOGIN=1 -e PRELLA_PASSWORD=1 \
-v ./backup:/Prella/backup \
--restart=always \
prella