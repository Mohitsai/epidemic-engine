FROM eengine-hadoop-base

# create a directory for the app
RUN mkdir /app
WORKDIR /app
# add the mapper, reducer
ADD mapper.py ./
ADD reducer.py ./
RUN chmod a+x ./*
ADD simulated_health_events.csv ./

ENV MAPPER="mapper.py"
ENV REDUCER="reducer.py"
ENV INPUT="/input/simulated_health_events.csv"

ADD run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
