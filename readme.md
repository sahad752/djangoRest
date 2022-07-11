
#
create virtual enviroment by -  python3  -m venv venv

activate virtual env 

. env/bin/activate

Install requirements by 

pip install -r requirements.txt

run project by python manage.py runserver


can access api on 127.0.0.1:8000

####

API ENDPOINTS :

GET /appointmets  - get all appointments - GET METHOD 
POST/ create - create appointment  - POST METHOD
body
{
"name":"candidate1",
"type":1,
"start_time":"10 AM",
"end_time":"11 AM"
}

POST /possible_appointments
body
{
"candidate_id":3,
"interviewer_id":4
}




