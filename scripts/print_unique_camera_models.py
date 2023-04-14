import csv


def main():
    with open('../data/camera_models.csv', newline='',
              encoding='utf-8') as csvfile:
        camera_models = set()
        reader = csv.DictReader(csvfile)
        for row in reader:
            make = row['make']
            model = row['model']
            camera_model = make + '_' + model
            camera_model = camera_model.replace(' ', '_')
            camera_models.add(camera_model)
        camera_models = list(camera_models)
        camera_models.sort()
        for model in camera_models:
            print(model)


if __name__ == '__main__':
    main()