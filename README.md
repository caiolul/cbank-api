<p align="center">
  <img src=".github/images/logo.png">
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
  <code>database</code>
  <br />
  <code>email and password</code>
  <br />
  <code>hash key</code>
    <br />
    <br />
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
- update user
- login
- transfer
- deposit
- withdrawn

## Feature

- Sending emails when you sign up for the app

<p align="center">
  <img src=".github/images/email_example.jpeg" height=500>
</p>
