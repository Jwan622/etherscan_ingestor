# Notes on project design

We're going to design our app into a few parts.

1. An ingestor. 
- python click/typer commands that can be run via a scheduler (cron or airflow). I'm using click/typer so that they can be run via Bash which is often the command environment for schedulers.

2. A database to store data from the ingestor
- we do need a database to store data as per the requirements. I think we can just a docker contianer with postgres.

3. A frontend to display the data.
- might be a single page app without a server. I don't think we need a server if we use Next.js which utilizes server side rendering.
- might be a single page app without a server. I don't think we need a server if we use Next.js which utilizes server side rendering.
- I really need to consider how to display the data. It's kind of tricky and complex! A few thoughts:
  - display paginated records per from account
  - from that page, you can click an account to see another account's paginated records
  - there's a button to see aggregated data per from account
  - a helpful search bar for accounts and date to start from

