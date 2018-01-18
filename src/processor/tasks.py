from core.celery import app


@app.task(name='pull-xref-events')
def pull_xref_events():

    pass
