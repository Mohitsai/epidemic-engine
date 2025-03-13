#!/bin/bash

echo "Attempting to run:"
echo "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \\"
echo "          -file $MAPPER -mapper $MAPPER \\"
echo "          -file $REDUCER -reducer $REDUCER \\"
echo "          -input $INPUT -output output"

echo : "
 _____                 _      ____                  _            
| ____|_   _____ _ __ | |_   / ___|___  _   _ _ __ | |_ ___ _ __ 
|  _| \ \ / / _ \ '_ \| __| | |   / _ \| | | | '_ \| __/ _ \ '__|
| |___ \ V /  __/ | | | |_  | |__| (_) | |_| | | | | ||  __/ |   
|_____| \_/ \___|_| |_|\__|  \____\___/ \__,_|_| |_|\__\___|_|   
"

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -file $MAPPER -mapper $MAPPER \
    -file $REDUCER -reducer $REDUCER \
    -input $INPUT -output /output

echo "Event Counter completed"

# echo Attempting to run (no hadoop test):
# echo "cat $INPUT | ./$MAPPER | sort | ./$REDUCER > ./output"

# cat $INPUT | ./$MAPPER | sort | ./$REDUCER > ./local-output-reduced
# hadoop fs -rm -r /local-output-reduced || :
# hadoop fs -put ./local-output-reduced /local-output-reduced

# echo Completed