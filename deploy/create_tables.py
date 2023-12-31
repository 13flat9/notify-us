import sys
sys.path.append('../') # makes shared visible
from check_new_jobs.database import create_tables, create_engine

def main():
    try:
        engine = create_engine()
        create_tables(engine)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()