---
description: How to run the ERP backend development server
---

1. Navigate to the backend directory
2. Activate the virtual environment
3. Install requirements
4. Run migrations
   // turbo
5. Start the server

```bash
cd /home/abcd/projects/erp-system/backend
source ../venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
