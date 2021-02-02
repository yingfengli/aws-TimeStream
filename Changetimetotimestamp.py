import datetime
import time


class Changetimetotimestamp:
   def get_float_time_stamp():
       datetime_now = datetime.datetime.now()
       return datetime_now.timestamp()

   def get_time_stamp16():
       #--16bit eg:1540281250399895    -ln
       datetime_now = datetime.datetime.now()
       print(datetime_now)

       # 10bit
       date_stamp = str(int(time.mktime(datetime_now.timetuple())))

       # 6bit，millisecond
       data_microsecond = str("%06d"%datetime_now.microsecond)

       date_stamp = date_stamp+data_microsecond
       return int(date_stamp)

   def get_time_stamp10(s_1):
       # 13 bits timestamp   eg:1540281250399895
       datetime_now = datetime.datetime.now()
       #print("datetime_now:")
       #print(datetime_now)
       #datetime_now = date("2020-10-22 08:14:20.113713")
       #datetime_now = date("2020-10-22 08:14:20.113713")
       datetime_now = datetime.datetime.strptime(s_1, '%Y-%m-%d %H:%M:%S')

       # 10bit
       date_stamp = str(int(time.mktime(datetime_now.timetuple())))

       # 3bit millisecond
       #data_microsecond = str("%06d"%datetime_now.microsecond)[0:3]

       #date_stamp = date_stamp+data_microsecond
       #print(date_stamp)
       return int(date_stamp)

   def get_time_stamp13(s_1):
       # 13 bits timestamp   eg:1540281250399895
       datetime_now = datetime.datetime.now()
       #print("datetime_now:")
       #print(datetime_now)
       #datetime_now = date("2020-10-22 08:14:20.113713")
       #datetime_now = date("2020-10-22 08:14:20.113713")
       datetime_now = datetime.datetime.strptime(s_1, '%Y-%m-%d %H:%M:%S')

       # 10bit
       date_stamp = str(int(time.mktime(datetime_now.timetuple())))

       # 3bit millisecond
       data_microsecond = str("%06d"%datetime_now.microsecond)[0:3]

       date_stamp = date_stamp+data_microsecond
       #print(date_stamp)
       return int(date_stamp)

   def stampToTime(stamp):
       datatime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(str(stamp)[0:10])))
       datatime = datatime+'.'+str(stamp)[10:]
       return datatime

if __name__ == '__main__':
    a1 = Changetimetotimestamp.get_time_stamp16()
    print(a1)
    print(Changetimetotimestamp.stampToTime(a1))
    a2 = Changetimetotimestamp.get_time_stamp13('2020-10-20 13:01:01')
    print(a2)
    print(Changetimetotimestamp.stampToTime(a2))
