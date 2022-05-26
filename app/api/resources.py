from flask_restful import Resource, abort

# from app.api import app_api


# class GetAllAnnouncements(Resource):
#     def get(self):
#         """get 
        
#         Get all the announcements, in a JSON form. Then in static site,
#         we will add a parser to render like in achievements.
#         """
#         # return jsonify.
#         return_obj = []
#         for ann in Announcement.get_all():
#             return_obj.append({
#                 # "author_username" : ann.author.username,
#                 "title" : ann.title,
#                 "body" : ann.body,
#                 "timestamp" : ann.timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             })
        
#         return return_obj

# app_api.add_resource(GetAllAnnouncements, "/announcements")