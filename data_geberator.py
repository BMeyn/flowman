from faker import Faker

#create fake data to test data loader for incremental load
def create_fake_data(data_length):
    fake = Faker()
    fake_data = []
    for i in range(data_length):
        fake_data.append(
            {
                "id": i,
                "name": fake.name(),
                "adress": fake.address(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "job": fake.job(),
                "last_updated": fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
            }
        )
    return fake_data

#write fake data to csv file

def write_fake_data_to_csv(data, file_name):
    import csv
    with open(file_name, "w") as f:
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
    fake_data = create_fake_data(100)
    write_fake_data_to_csv(fake_data, "fake_data.csv")