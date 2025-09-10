Unified FastAPI backend
======================

This project combines three existing FastAPI-based starters and adds a placeholder for the Django-based calendar (exodus-calendar-starter) which still needs porting.

Structure:
- services/
  - fluent_api/       (copied from fluent-api-starter/app)
  - monitorlab_dashboard/ (copied from monitorlab-dashboard-starter/app)
  - ninewatt_recommendation/ (copied from ninewatt-recommendation-starter/app)
  - exodus-calendar/  (placeholder router to port Django app into FastAPI)
- main.py             (unified FastAPI app)
- requirements.txt

How to run (development):
1. Create virtualenv and install requirements.txt
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
2. From this directory, run:
   python main.py

Notes / Next steps:
- The Django calendar app must be ported: models, serializers, migrations (migrate to SQLAlchemy or use Django ORM with ASGI adapters).
- Database settings and env vars need consolidation from the original projects' .env files located in ../unified_sources/*
# mine_pro
