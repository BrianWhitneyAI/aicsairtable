import os

from aicsairtable import (
    ArgoPowerMetrics,
    update_current,
)

ROOT_DIR = (
    "/allen/aics/microscopy/PRODUCTION/OpticalControl/ArgoLight/ArgoPower_Monthly"
)
ENV_VARS = "/allen/aics/microscopy/brian_whitney/repos/aicsairtable/.env"

for path, subdirs, files in os.walk(ROOT_DIR):
    for file in files:
        file_path = os.path.join(path, file)
        if ".csv" in file_path and "%" not in file_path:
            print(f"attempting to process file{file}")
            try:
                datasheets = ArgoPowerMetrics(file_path=file_path)
                datasheets.upload(env_vars=ENV_VARS)
                print(f"sucessfully formatted file: {file}")
            except ValueError:
                print(f"file:{file} is improperly formatted")
            except IndexError:
                print(f"file:{file} is improperly formatted")
            except KeyError:
                print(f"file: {file} is not an ArgoPower metric sheet")

update_current(ENV_VARS)
