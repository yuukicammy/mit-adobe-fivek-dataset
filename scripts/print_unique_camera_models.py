"""Show unique camera models in MIT-Adobe FiveK Dataset

License:
    Copyright (c) 2023 yuukicammy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import csv


def main():
    with open("./data/camera_models.csv", newline="",
              encoding="utf-8") as csvfile:
        camera_models = set()
        reader = csv.DictReader(csvfile)
        for row in reader:
            make = row["make"]
            model = row["model"]
            camera_model = make + "_" + model
            camera_model = camera_model.replace(" ", "_")
            camera_models.add(camera_model)
        camera_models = list(camera_models)
        camera_models.sort()
        for model in camera_models:
            print(model)


if __name__ == "__main__":
    main()
