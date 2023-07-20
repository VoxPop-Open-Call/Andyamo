FROM python:3.9-bullseye

MAINTAINER Yann Feunteun <yfe@protonmail>

RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.77.0/source/boost_1_77_0.tar.bz2


RUN apt update && apt install -y python3.9-dev

RUN tar --bzip2 -xf boost_1_77_0.tar.bz2 

RUN cd boost_1_77_0 && ./bootstrap.sh --with-python-version=3.9 && ./b2
#apt-get install -y --no-install-recommends libboost-all-dev

RUN cp /boost_1_77_0/stage/lib/libboost_python39.so.1.77.0 /usr/lib

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY generate_graph.py generate_graph.py
COPY generator.py generator.py
COPY access.py access.py
COPY export_clean_splitted.json data.json


RUN python generate_graph.py
#COPY test.cc test.cc

RUN g++ -Ofast -c -fPIC -I/boost_1_77_0/ -I/usr/include/python3.9/  foot.cpp -o c_foot.o
RUN g++ -Ofast -c -fPIC -I/boost_1_77_0/ -I/usr/include/python3.9/  manual_wheelchair.cpp -o c_manual_wheelchair.o
RUN g++ -Ofast -c -fPIC -I/boost_1_77_0/ -I/usr/include/python3.9/  electric_wheelchair.cpp -o c_electric_wheelchair.o



RUN g++ -Ofast -L/boost_1_77_0/stage/lib -shared -Wl,-soname,test.so -o c_foot.so c_foot.o   -lboost_python39  -lpython3.9
RUN g++ -Ofast -L/boost_1_77_0/stage/lib -shared -Wl,-soname,test.so -o c_manual_wheelchair.so c_manual_wheelchair.o   -lboost_python39  -lpython3.9
RUN g++ -Ofast -L/boost_1_77_0/stage/lib -shared -Wl,-soname,test.so -o c_electric_wheelchair.so c_electric_wheelchair.o   -lboost_python39  -lpython3.9

COPY protos protos
RUN python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/route_service.proto

COPY server.py /

EXPOSE 50051

ENTRYPOINT python server.py
