from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import ProjectMember
from projects.serializers import ProjectMemberSerializer

class ProjectMemberApiViewSet(ModelViewSet):
    permission_classes = []
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer    
    """
       constraints
        - a user can be a member of max 2 projects only
        - a project can have at max N members defined in database for each project
       functionalities
       - add users to projects

         Request
         { user_ids: [1,2,...n] }
         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }
         following are the possible status messages
         case1: if user is added successfully then - "Member added Successfully"
         case2: if user is already a member then - "User is already a Member"
         case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

         there will be many other cases think of that

       - update to remove users from projects

         Request
         { user_ids: [1,2,...n] }

         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }

         there will be many other cases think of that and share on forum
    """
    def create(self, request):
        query_params = request.query_params
        data = request.data
        serializer = self.serializer_class(data=data, context={"project_id": query_params.get("project_id")})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
