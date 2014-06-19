#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import web
from datetime import datetime


import settings
import utils


db = web.database(**settings.DB_CONN)
render = utils.render.workreports


def create_project(userid, name, participants, description):
    db.insert('projects', userid=userid, created_time=datetime.now(),
              name=name, participants=participants, status=0,
              description=description)


def remove_project(project_id):
    db.delete('projects', where='id=$project_id', vars=dict(project_id=project_id))


def create_task(project_id, userid, name, description, priority,
                plan_working_day, deadline):
    db.insert('project_tasks', project_id=project_id, userid=userid,
              created_time=datetime.now(), name=name, description=description,
              progress=0, priority=priority, plan_working_day=plan_working_day,
              deadline=deadline, begin_time=0, done_time=0,
              state=0)


def remove_task(task_id):
    db.delete('project_tasks', where='id=$task_id', vars=dict(task_id=task_id))


def set_task_progress(project_id, task_id, progress):
    db.update('project_tasks', where="project_id=$project_id and id=$task_id",
              vars=dict(project_id=project_id, task_id=task_id),
              progress=progress)


def begin_task(project_id, task_id):
    db.update('project_tasks', where="project_id=$project_id and task_id=$task_id",
              vars=dict(project_id=project_id, task_id=task_id),
              begin_time=datetime.now())


def done_task(project_id, task_id):
    db.update('project_tasks', where="project_id=$project_id and id=$task_id",
              vars=dict(project_id=project_id, task_id=task_id),
              done_time=datetime.now(), state=1)


def create_tasklog(project_id, task_id, userid, progress, last_week_progress,
                   next_week_plan, others):
    db.insert('project_logs', project_id=project_id, task_id=task_id,
              userid=userid, created_time=datetime.now(), progress=progress,
              last_week_progress=last_week_progress, next_week_plan=next_week_plan,
              others=others
              )


def get_projects():
    return db.select('projects', where='status=0', order='name')


def get_tasks(project_id, state=0):
    return db.select('project_tasks', where='project_id=$project_id and state=$state',
                     vars=dict(project_id=project_id, state=state), order='name')


def get_lastest_log(project_id, task_id):
    logs = db.select('project_logs',
                     where='project_id=$project_id and task_id=$task_id',
                     vars=dict(project_id=project_id, task_id=task_id),
                     order='id desc', limit=1)
    return logs[0] if logs else None


def get_project(project_id):
    project_id = int(project_id)
    rows = db.select('projects', where='id=$project_id', order='name',
                     vars=dict(project_id=project_id), limit=1)
    return rows[0] if rows else None


def get_task(task_id):
    task_id = int(task_id)
    rows = db.select('project_tasks', where='id=$task_id', order='name',
                     vars=dict(task_id=task_id), limit=1)
    return rows[0] if rows else None


def get_all_summary():
    ret = []
    projects = get_projects()
    for project in projects:
        task_items = []
        for task in get_tasks(project.id):
            log = get_lastest_log(project.id, task.id)
            task_items.append({"task": task, 'log': log})
        ret.append({'project': project, 'tasks': task_items})

    return ret


class IndexHandler(object):
    def GET(self):
        summarys = get_all_summary()
        return render.index(summarys)


class CreateProjectHandler(object):
    def GET(self):
        return render.create_project()

    def POST(self):
        i = web.input()
        create_project(0, name=i.name, participants=i.participants,
                       description=i.description)
        return web.seeother('/')


class CreateTaskHandler(object):
    def GET(self, project_id):
        project = get_project(project_id)
        return render.create_task(project)

    def POST(self, project_id):
        i = web.input()
        create_task(project_id=project_id, userid=0, name=i.task_name,
                    description=i.description, priority=i.priority,
                    plan_working_day=i.plan_working_day, deadline=i.deadline)
        return web.seeother('/')


class CreateTaskLogHandler(object):
    def GET(self, project_id, task_id):
        project = get_project(project_id)
        task = get_task(task_id)
        log = get_lastest_log(project_id, task_id)
        return render.create_task_log(project, task, log)

    def POST(self, project_id, task_id):
        i = web.input()
        create_tasklog(project_id=project_id, task_id=task_id, userid=0,
                       progress=i.progress, last_week_progress=i.last_week_progress,
                       next_week_plan=i.next_week_plan, others=i.others)
        set_task_progress(project_id, task_id, i.progress)
        return web.seeother('/')


class ReportHandler(object):
    def GET(self):
        summarys = get_all_summary()
        return render.reports(summarys)


class RemoveProjectHandler(object):
    def GET(self, project_id):
        project = get_project(project_id)
        return render.remove_project(project)

    def POST(self, project_id):
        remove_project(project_id)
        return web.seeother('/')


class RemoveTaskHandler(object):
    def GET(self, project_id, task_id):
        task = get_task(task_id)
        return render.remove_task(task)

    def POST(self, project_id, task_id):
        remove_task(task_id)
        return web.seeother('/')


class DoneTaskHandler(object):
    def GET(self, project_id, task_id):
        task = get_task(task_id)
        return render.done_task(task)

    def POST(self, project_id, task_id):
        done_task(project_id, task_id)
        return web.seeother('/')



urls = ["/", IndexHandler,
        "/create_project", CreateProjectHandler,
        "/create_task/(\d+)", CreateTaskHandler,
        "/create_task_log/(\d+)/(\d+)", CreateTaskLogHandler,
        "/remove_task/(\d+)/(\d+)", RemoveTaskHandler,
        "/done_task/(\d+)/(\d+)", DoneTaskHandler,
        "/remove_project/(\d+)", RemoveProjectHandler,
        ]


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
