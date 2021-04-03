# POLY_CY101_client_Server

note to self : the bad guy should be using 


## to reset the commands vectors 
curl -X PUT -d userID=257.257.257.257 -d commandID=192.168.0.142 http[:]//c2.bianisoft.com:8081/



## to get all the results
http[:]//c2.bianisoft.com:8081/?userID=257.257.257.257



## To connect to the EC2 instance 
ssh -i "kpTestPython.pem" ec2-user@ec2-44-225-50-145.us-west-2.compute.amazonaws.com
