from crontab import CronTab
from flask import Flask, request
from flask_restplus import Resource, Api


app = Flask(__name__)
api = Api(app, version='1.0', title='Cron API',
          description='List of api to modify cron')


@api.route('/api/v1/cron/<user>')
class Cron(Resource):

    def get(self, user):
        cron = CronTab(user=user)

        job_list = list()
        for job in cron:
            job_list.append(str(job))

        return job_list


@api.route('/api/v1/cron/add')
class CronAdd(Resource):

    def post(self):
        result = {
            'status': 1,
            'message': ''
        }

        try:
            cron = CronTab(user=request.json['user'])
            job = cron.new(command=request.json['command'], comment=request.json['comment'])
            job.setall(request.json['schedule'])
            cron.write()

        except Exception as e:
            result['status'] = 0
            result['message'] = str(e)

        return result


@api.route('/api/v1/cron/delete/all/<user>')
class CronDelete(Resource):

    def get(self, user):
        result = {
            'status': 1,
            'message': ''
        }

        try:
            cron = CronTab(user=user)
            cron.remove_all()
            cron.write()

        except Exception as e:
            result['status'] = 0
            result['message'] = str(e.message)

        return result


@api.route('/api/v1/cron/delete')
class CronDelete(Resource):

    def post(self):
        result = {
            'status': 1,
            'message': ''
        }

        try:
            cron = CronTab(user=request.json['user'])
            for job in cron:
                if job.comment == request.json['comment']:
                    cron.remove(job)
                    cron.write()

        except Exception as e:
            result['status'] = 0
            result['message'] = str(e.message)

        return result


@api.route('/api/v1/cron/update')
class CronUpdate(Resource):

    def post(self):
        result = {
            'status': 1,
            'message': ''
        }

        try:
            cron = CronTab(user=request.json['user'])
            iter = cron.find_comment(request.json['comment'])
            for item in iter:
                cron.remove(item)
                cron.write()
                job = cron.new(command=request.json['command'], comment=request.json['comment'])
                job.setall(request.json['schedule'])
                cron.write()

        except Exception as e:
            result['status'] = 0
            result['message'] = str(e.message)

        return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
