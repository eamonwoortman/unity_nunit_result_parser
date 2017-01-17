# unity_nunit_result_printer
A Unity NUnit Test result parser which prints the results to the console


Usage
-----
To use the python script, simply provide a path to the Unity NUnit result XML file

For example:

		unity_nunit_printer.py /home/eamon/nunit-output/unit_test_results.xml

If you want to use the Docker image, bind a folder containing the result file and supply the container file path.


	docker run -v /home/eamon/nunit-output/:/input \  
				eamonwoortman/unity_nunit_printer \
				python /app/unity_nunit_printer.py /input/unit_test_results.xml