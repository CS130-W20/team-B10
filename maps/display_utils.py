import datetime
from collections import namedtuple
Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
attr_info = namedtuple('attr_info', ['name','location'])
def format_schedule(start_date, end_date, attractions, schedule, tpa, tpr, hotel_name, wake, sleep):
    events_list = []
    
    start = {'title': hotel_name, 'start':start_date+"T00:00:00", 'end':start_date+"T"+wake}
    events_list.append(start)
    cur_time = datetime.datetime.strptime(start_date+"T"+wake, '%Y-%m-%dT%H:%M:%S')
    for day in schedule:
        for events in day:
            if isinstance(events, (int, float)):
                cur_time += datetime.timedelta(hours=events)
            else:
                name = attractions[events.places_id].name
                start_time = cur_time.strftime('%Y-%m-%dT%H:%M:%S')
                if events.is_restaurant:
                    cur_time += datetime.timedelta(hours=tpr)
                    name = 'Eat at: ' + name
                else:
                    cur_time += datetime.timedelta(hours=tpa)
                end_time = cur_time.strftime('%Y-%m-%dT%H:%M:%S')
                event = {'title': name, 'start':start_time, 'end':end_time}
                events_list.append(event)
        sleep_date = cur_time.strftime('%Y-%m-%d')
        cur_time += datetime.timedelta(days=1)
        wake_datetime = cur_time.strftime('%Y-%m-%d')+"T"+wake
        cur_time = datetime.datetime.strptime(wake_datetime, '%Y-%m-%dT%H:%M:%S')
        end_day = {'title': hotel_name, 'start':sleep_date+"T"+sleep, 'end':wake_datetime}
        events_list.append(end_day)
    return events_list
    
def main():
    sample = [[0.29140672058361233, Attraction(places_id='abc', lat=3.321948489954936, lon=-4.931563542804515, score=7.761329698240371, is_restaurant=False), 0.14609907173092168, Attraction(places_id='def', lat=2.311880741996689, lon=-8.17104514814322, score=7.9007184435880164, is_restaurant=False)]]
    attractions = {'abc': attr_info('disney', 'anaheim'), 'def': attr_info('chick-fil-a', 'westwood')}
    print(format_schedule("2020-03-08", "2020-03-10", attractions, sample, 0, 0, "Budapest", "08:00:00", "22:00:00"))
#     print(attractions['abc'].name)
    #print(datetime.strptime("2020-03-08" + "T" + "08:00:00", '%Y-%m-%dT%H:%M:%S'))
    
    
    
if __name__ == '__main__':
    main()