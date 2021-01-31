# Rate Interactive Tool
### Use this tool to recieve physiological data, summary reports, and availability plots for a certain time frame. Below are instructions on how to use the tool

- **How to run:**
- Use the following command to forward port 5000 of Pegasus:
>>ssh -L 5000:localhost:5000 <Your NetID>@BMEN-M0XB163326.engr.tamu.edu

- Navigate to directory:
>> cd /home/data/RATE

- Enable singularity container:
>> singularity shell /home/data/containers/rate.sif

- Navigate to directory where the 'rate_interactive_tool' is located. For example:
>> cd /home/data/RATE/scripts/rate_interactive_tool

- Use the following command to run the flask app:
>> ./run-tool

- If run correctly, the following message should appear and the URL provided can be input into local browser:
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

- **Tips while using tool**
- Choose tool and then choose necessary time frame
- For summary report, input file path of where the file needs to be saved. For example:
>> /home/ugrads/s/surya44/

- **Common Errors**
- If an error occurs saying "Process is already in use", follow the steps listed below:
1. Run the following command to retrieve all the processes that are running
>> ps -fA | grep python
2. Find the ID number (second column) of the process that is labeled "flask run" and use the following command to terminate. Replace PID with ID number
>> kill -9 pid