from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from hr.models import appointment
from hr.serializer import AppointmentSerializer
# Create your views here.


@api_view(['GET'])
def get_appointments(request):
    """
    Get All appointments
    type:1 is candidate, 2 is interviewer
    """
    if request.method == 'GET':
        appointments = appointment.objects.all()
        appointments_list = list(appointments.values())
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })






@api_view(['POST'])
def get_possible_appointments(request):
    """
    Get possible appointments
    {
    "candidate_id":1,
    "interviewer_id":2
    }
    """
    if request.method == 'POST':
        appointments = appointment.objects.all()
        appointments_list = list(appointments.values())

        ap_int_times = []
        ap_cnd_times = []
        ap_cnd_times_temp = []
        ap_int_times_temp = []
        ap_times_list = []
        possible_intervals = []
        candidate_id =  request.data['candidate_id'] if 'candidate_id' in request.data else None
        interviewer_id = request.data['interviewer_id'] if 'interviewer_id' in request.data else None

        if candidate_id not in [ap['id'] for ap in appointments_list]:
            return Response({
                'status': 'error',
                'message': 'candidate_id not found'
            })

        if interviewer_id not in [ap['id'] for ap in appointments_list]:
            return Response({
                'status': 'error',
                'message': 'interviewer_id not found'
            })




        if candidate_id and interviewer_id:

            for appointment1 in appointments_list:
                if appointment1['id'] == candidate_id:
                    ap_cnd_times.append(appointment1['start_time'])
                    ap_cnd_times.append(appointment1['end_time'])
                    for ap in ap_cnd_times:
                        ap = ap.split(' ')
                        if ap[1] == "PM":
                            if ap[0] == "12":
                                ap[0] = int(ap[0])
                                ap_cnd_times_temp.append(ap[0])
                            else:
                                ap[0] = int(ap[0]) + 12
                                ap_cnd_times_temp.append(ap[0])
                        else:
                            if ap[0] == 12:
                                ap[0] = 0
                                ap_cnd_times_temp.append(ap[0])
                            else:
                                ap[0] = int(ap[0])
                                ap_cnd_times_temp.append(ap[0])
                    ap_times_list.append(ap_cnd_times_temp)


            for appointment1  in appointments_list:
                if appointment1['id'] == interviewer_id:
                    ap_int_times.append(appointment1['start_time'])
                    ap_int_times.append(appointment1['end_time'])
                    for ap in ap_int_times:
                        ap = ap.split(' ')
                        if ap[1] == "PM":
                            if ap[0] == "12":
                                ap[0] = int(ap[0])
                                ap_int_times_temp.append(ap[0])
                            else:
                                ap[0] = int(ap[0]) + 12
                                ap_int_times_temp.append(ap[0])
                        else:
                            if ap[0] == 12:
                                ap[0] = 0
                                ap_int_times_temp.append(ap[0])
                            else:
                                ap[0] = int(ap[0])
                                ap_int_times_temp.append(ap[0])

                    ap_times_list.append(ap_int_times_temp)

            possible_intervals = solve(ap_times_list)

        else:
            return Response({
                'status': 'error',
                'message': 'Please provide candidate and interviewer id'
            })

        if possible_intervals:
            if possible_intervals[0] == possible_intervals[1]:
                return Response({
                    'status': 'success',
                    'data': 'No possible appointments'
                })
            else:
                return Response({
                    'status': 'success hjhj',
                    'data': convert(possible_intervals)
                })
        else:
            return Response({
                'status': 'fail',
                'data': 'No possible appointments'
            })

def convert(list):
    return (*list, )

def solve(intervals):
      start, end = intervals.pop()
      while intervals:
         start_temp, end_temp = intervals.pop()
         start = max(start, start_temp)
         end = min(end, end_temp)
      return [start, end]

@api_view(['POST'])
def create_appointment(request):
    """
    Create HR data
    {
        "name":"candidate1",
        "type":1,
        "start_time":"10 AM",
        "end_time":"11 AM"
    }
    {
        "name":"interviewer",
        "type":2,
        "start_time":"10 AM",
        "end_time":"12 PM"
    }


    """
    if request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        start_time  = request.data['start_time'].split(' ')
        end_time = request.data['end_time'].split(' ')
        if start_time[1] == 'PM':
            if start_time[0] == '12':
                start_time[0] = 12
            else:
                start_time[0] = int(start_time[0]) + 12
        else:
            if start_time[0] == '12':
                start_time[0] = 0
            else:
                start_time[0] = int(start_time[0])

        if end_time[1] == 'PM':
            if end_time[0] == '12':
                end_time[0] = 12
            else:
                end_time[0] = int(end_time[0]) + 12
        else:
            if end_time[0] == '12':
                end_time[0] = 0
            else:
                end_time[0] = int(end_time[0])

        if end_time[0] < start_time[0]:
            return Response({
                'status': 'fail',
                'data': 'End time should be greater than start time'
            })


        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Appointment not created'
        })

@api_view(['DELETE'])
def delete_all(request):
    """
    Delete all appointments
    """
    if request.method == 'DELETE':
        appointments = appointment.objects.all()
        appointments.delete()
        return Response({
            'status': 'success',
            'message': 'All appointments deleted'
        })


