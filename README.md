<p align="center">
  <img src="https://media.discordapp.net/attachments/340263600142942209/837872644187357264/Logo_with_name-removebg-preview.png">
</p>
<p align="center">
    Api developed with python using the starlette.io framework
    <br />
  </p>

## Run project

<div>
  <p>Install dependencies</p>
    <code>poetry shell</code>
    <br />
    <code>poetry install</code>
     <br />
     <br />
  <p>Create the .env file with your database and key configuration</p>
  <p>Upgrade database</p>
   <code>alembic upgrade head</code>
     <br />
     <br />
  <p>Run app</p>
   <code>uvicorn src.app:app --reload</code>
     <br />
     <br />
</div>

## Routes in app

- add user
- login
- transfer
- deposit
- withdrawn
