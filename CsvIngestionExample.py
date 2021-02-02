import csv
import time
from Constant import DATABASE_NAME, TABLE_NAME
from Changetimetotimestamp import Changetimetotimestamp


class CsvIngestionExample:
    def __init__(self, client):
        self.client = client

    def bulk_write_records(self, filepath):
        with open(filepath, 'r') as csv_file:
            # creating a csv reader object
            csv_reader = csv.reader(csv_file)

            records = []
            current_time = self._current_milli_time()
            counter = 0

            # extracting each data row one by one
            for row in csv_reader:
                dimensions = [
                    {'Name': row[0], 'Value': row[1]}
#                    {'Name': row[2], 'Value': row[3]},
#                    {'Name': row[4], 'Value': row[5]}
                ]

                record_time = current_time - (counter * 50)
                #print(str(Changetimetotimestamp.get_time_stamp13(row[3])))
                record = {
                    'Dimensions': dimensions,
                    #'Time': str(row[3]),
                    'Time': str(Changetimetotimestamp.get_time_stamp10(row[3])),
                    'TimeUnit': 'SECONDS',
                    'MeasureName': row[4],
                    'MeasureValue': row[5],
                    'MeasureValueType': row[6]
                    #'Time': str(record_time)
                    #'Time': str(Changetimetotimestamp.get_time_stamp13(row[3]))
                }
                records.append(record)
                counter = counter + 1

                if len(records) == 100:
                    self._submit_batch(records, counter)
                    records = []

            if len(records) != 0:
                self._submit_batch(records, counter)

            print("Ingested %d records" % counter)

    def _submit_batch(self, records, counter):
        try:
            result = self.client.write_records(DatabaseName=DATABASE_NAME, TableName=TABLE_NAME,
                                               Records=records, CommonAttributes={})
            print("Processed [%d] records. WriteRecords Status: [%s]" % (counter,

                                                                         result['ResponseMetadata']['HTTPStatusCode']))
        except Exception as err:
            print("Error:", err)

    @staticmethod
    def _current_milli_time():
        return int(round(time.time() * 1000))
