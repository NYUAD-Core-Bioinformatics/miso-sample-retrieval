# miso-sample-retrieval

This repository is used to retrieve the miso sample and description information for the sequencing data from the MISO database.

To build the app, update the database information in the ```.env``` file and excecute below steps.
```
git clone https://github.com/NYUAD-Core-Bioinformatics/miso-sample-retrieval
cd miso-sample-retrieval
docker compose up -d 
```

If you want to change the port number, update it from the ```docker-compose.yml``` file. As of now it is serving on port ```8181```.

Access the application on brower via

localhost:8181 or IP-address:8181

