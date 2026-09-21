#/bin/bash

trap 'exit' SIGINT

echo "model,time" > runtime.csv
for GLM in $(cat study_list.csv); do
	MODEL=$(basename ${GLM%.*})
	if [ ! -f $MODEL/$MODEL.glm ]; then
		/bin/echo -n Downloading $GLM...
		( mkdir -p $MODEL ; cd $MODEL ; gridlabd model get ${GLM%.*} )
		/bin/echo ok
	fi
	if [ ! -f $MODEL/results.csv.gz ]; then
		echo "Running $GLM..."
		/bin/echo -n $MODEL, >> runtime.csv
		/usr/bin/time -a -o runtime.csv gridlabd -D model=$MODEL study_model.glm
		rm $MODEL/*.csv
	fi
done
