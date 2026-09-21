#/bin/bash
echo "model,time" > runtime.csv
for GLM in [R0-9]*.glm; do
	MODEL=${GLM%.*}
	if [ ! -f $MODEL/results.csv.gz ]; then
		echo "Running $GLM..."
		echo -n $GLM, >> runtime.csv
		/usr/bin/time -a -o runtime.csv gridlabd -D model=$MODEL study_model.glm
		rm $MODEL/*.csv
	fi
done
