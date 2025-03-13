FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8 AS eengine-hadoop-base
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip vim

FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8 AS eengine-hadoop-namenode
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip vim

FROM bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8 AS eengine-hadoop-datanode
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip vim

FROM bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8 AS eengine-hadoop-resourcemanager
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip vim

FROM bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8 AS eengine-hadoop-nodemanager
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip vim

FROM bde2020/hadoop-historyserver:2.0.0-hadoop3.2.1-java8 AS eengine-hadoop-historyserver
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip vim
