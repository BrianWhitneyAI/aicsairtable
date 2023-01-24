import os

from aics_airtable_core import (
    airtable_download,
    convert_to_dataframe,
    upload_pandas_dataframe,
)
from dotenv import load_dotenv
import numpy as np


def update_current(env_vars: str):
    try:
        load_dotenv(env_vars)

    except Exception as e:
        raise EnvironmentError(
            "The specified env_var is invalid and failed with " + str(e)
        )

    # Check that all variables from .env are  present
    if (
        any(
            [
                os.getenv("AIRTABLE_API_KEY"),
                os.getenv("ARGOLIGHT_POWER_MONTHLY_BASE_KEY"),
                os.getenv("LASERPOWER_DASHBOARD_TABLE"),
            ]
        )
        == "None"
    ):
        raise EnvironmentError(
            "Environment variables were not loaded correctly. Some values may be missing."
        )

    dashboard = airtable_download(
        table=os.getenv("LASERPOWER_DASHBOARD_TABLE"),
        params_dict={},
        api_key=os.getenv("AIRTABLE_API_KEY"),
        base_id=os.getenv("ARGOLIGHT_POWER_MONTHLY_BASE_KEY"),
    )

    dashboard_df = convert_to_dataframe(dashboard)

    systems = dashboard_df["System"].astype("category").cat.categories
    for system in systems:
        system_df = dashboard_df[dashboard_df["System"] == system]
        wavelengths = system_df["Wavelength (nm)"].astype("category").cat.categories
        for wavelength in wavelengths:
            wavelength_df = system_df[system_df["Wavelength (nm)"] == wavelength]
            if not wavelength_df.empty:
                most_recent_date = wavelength_df["Date"].max()
                wavelength_df["Current"] = np.where(
                    wavelength_df["Date"] == most_recent_date, True, False
                )
                dashboard_df.update(wavelength_df)

    upload_pandas_dataframe(
        pandas_dataframe=dashboard_df,
        table=os.getenv("LASERPOWER_DASHBOARD_TABLE"),
        api_key=os.getenv("AIRTABLE_API_KEY"),
        base_id=os.getenv("ARGOLIGHT_POWER_MONTHLY_BASE_KEY"),
    )
