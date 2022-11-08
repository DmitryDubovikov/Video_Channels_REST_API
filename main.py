from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

api = Api(app)
db = SQLAlchemy(app)

class Video_model(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer)
    likes = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f'video {self.name}: {self.views} views, {self.likes} likes'

# # only once: python main.py
# with app.app_context():
#     db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='name of the video', location='form', required=True)
video_put_args.add_argument('views', type=int, help='views of the video', location='form', required=True)
video_put_args.add_argument('likes', type=int, help='likes of the video', location='form', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='name of the video', location='form')
video_update_args.add_argument('views', type=int, help='views of the video', location='form')
video_update_args.add_argument('likes', type=int, help='likes of the video', location='form')

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
}

class Video(Resource):
    
    @marshal_with(resource_fields)
    def get(self, video_id):        
        video = Video_model.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message=f'video with id {video_id} does not exist')
        else:
            return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = Video_model.query.filter_by(id=video_id).first()
        if video:
            abort(409, message=f'video with id {video_id} already exists')
        else:
            video = Video_model(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
            db.session.add(video)
            db.session.commit()
            return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        video = Video_model.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message=f'video with id {video_id} does not exist, cannot update')
        else:
            if args['name']:
                video.name = args['name']
            if args['views']:
                video.views = args['views']
            if args['likes']:
                video.likes = args['likes']
            
            db.session.commit()
            return video


    def delete(self, video_id):
        video = Video_model.query.get(video_id)
        if video is None:
            return {"error": "not found"}
        db.session.delete(video)
        db.session.commit()
        return {"message": "video deleted"}

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)