# NFL Data Pipeline Project

## Overview
This project aims to orchestrate and automate the workflow of ingesting, transforming, and visualizing NFL play-by-play data from the 2013 season using a modern data stack comprising Terraform, Airflow, dbt, Google Cloud Platform (GCP), and Looker Studio.

### Components
- **Terraform**: Used for provisioning and managing the infrastructure on GCP in a declarative manner.
- **Airflow**: Orchestrates the pipeline for ingesting data into a Google Cloud Bucket and then loading it into BigQuery.
- **dbt (Data Build Tool)**: Transforms the ingested data within BigQuery to prepare it for analysis and visualization.
- **Looker Studio (formerly Google Data Studio)**: Visualizes the transformed data through a dashboard for insights into the NFL play-by-play data.

## Project Setup and Installation
Here's whath I did:
- Setting up a GCP environment.
- Configured Terraform (check .tf files).
- Set up Airflow (check out the nfl_data_pipeline.py file)).
- Configured dbt, including setting up a `profiles.yml` and creating models (check out summarize_play_by_game.sql in the 'models' folder).
- Looker Studio dashboard:  https://lookerstudio.google.com/reporting/55388976-42bb-470c-bbbf-347ee5d5ce23.

## Contributing
Please contribute if you'd like!

## Author
- Amit Kooner
