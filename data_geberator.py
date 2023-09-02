from faker import Faker
import argparse
import csv
import os
import datetime

#create fake data to test data loader for incremental load
def create_person_fake_data(data_length):
    fake = Faker()
    fake_data = []
    for i in range(data_length):
        fake_data.append(
            {
                "id": i,
                "name": fake.name(),
                "adress": fake.address().replace("\n", " "),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "job": fake.job(),
                "last_modified": fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
            }
        )
    return fake_data

#write fake data to csv file
def write_fake_data_to_csv(data, file_name, data_path):

    # create directory if not exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)
  
  
    with open(os.path.join(data_path, file_name), "w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=data[0].keys(),
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )

        writer.writeheader()
        for row in data:
            writer.writerow(row)

def simulate_update_data( file_name, data_path, num_update=1):
    # read data from csv file
    # update the job column and last_modified column
    # write data to csv file

    # check if file exist
    if not os.path.exists(os.path.join(data_path, file_name)):
        raise Exception("File not found")
    
    # read data from csv file
    with open(os.path.join(data_path, file_name), "r") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    faker = Faker()
    # update the job column and last_modified column for num_update rows
    for i in range(num_update):
        data[i]["job"] = faker.job()
        data[i]["last_modified"] = datetime.datetime.now()
    
    # write data to csv file
    with open(os.path.join(data_path, file_name), "w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=data[0].keys(),
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )

        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_length", type=int, default=10)
    parser.add_argument("--data_path", type=str, default="data/source/customer")
    parser.add_argument("--file_name", type=str, default="person.csv")
    parser.add_argument("--action", type=str, default="update")
    args = parser.parse_args()

    if args.action == "create":
       fake_data = create_person_fake_data(args.data_length)
       write_fake_data_to_csv(fake_data, file_name=args.file_name, data_path=args.data_path)
    elif args.action == "update":
       simulate_update_data( file_name=args.file_name, data_path=args.data_path, num_update=1)