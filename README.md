
### Installation

Install pipenv and postgresql, then type:

```sh
pipenv shell
pipenv install
```

After that, use following commands to configure your instance. Replace data accordingly.
```sh
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres
export OMDB_API_KEY=your_key
```

Once done, let's run django development server:

```sh
python3 manage.py collectstatic
python3 manage.py migrate
python3 manage.py test
python3 manage.py runserver
```

Open web browser and test API.

