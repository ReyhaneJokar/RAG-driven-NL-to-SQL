import sys
import argparse
from src.db_utils import connect_db
from src.qa import interactive_loop

def main():
    parser = argparse.ArgumentParser(description='RAG-driven NL2SQL')
    parser.add_argument('--conn', required=True, help='Database connection string')
    args = parser.parse_args()

    try:
        engine = connect_db(args.conn)
        print("✅ Successfully connected to the database.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

    # run QA loop
    interp = interactive_loop(engine)
    interp.run()


if __name__ == '__main__':
    main()





# python -m src.main --conn postgresql://postgres:rag1234jkr@db.fpqsbfbgeyxevqussnte.supabase.co:5432/postgres

# python -m src.main --conn "postgresql://myuser:mypassword@localhost:54332/mydatabase"


## adventureworks
#  python -m src.main --conn "mssql+pyodbc://sa:YourPass123@localhost/AdventureWorks2019?driver=ODBC+Driver+17+for+SQL+Server"
