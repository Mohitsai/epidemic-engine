#!/bin/bash

echo "Attempting to run:"
echo "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \\"
echo "          -file $MAPPER -mapper $MAPPER \\"
echo "          -file $REDUCER -reducer $REDUCER \\"
echo "          -input $INPUT -output output"

echo "
 _   _ ____    __  __ ____  
| | | |  _ \  |  \/  |  _ \ 
| |_| | |_) | | |\/| | |_) |
|  _  |  _ <  | |  | |  _ < 
|_| |_|_| \_\ |_|  |_|_| \_\
"

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -file $MAPPER -mapper $MAPPER \
    -file $REDUCER -reducer $REDUCER \
    -input $INPUT -output /output

echo "Location Map-Reducer completed"


# echo Attempting to run (no hadoop test):
# echo "cat $INPUT | ./$MAPPER | sort | ./$REDUCER > ./output"

# cat $INPUT | ./$MAPPER | sort | ./$REDUCER > ./local-output-reduced
# hadoop fs -rm -r /local-output-reduced || :
# hadoop fs -put ./local-output-reduced /local-output-reduced

# echo Completed