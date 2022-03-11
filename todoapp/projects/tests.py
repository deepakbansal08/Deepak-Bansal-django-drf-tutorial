from rest_framework.test import APITestCase


class ProjectMemberAPIViewSetCreateTestCase(APITestCase):
    def test_project_id_absent(self):
        """
        Test to verify a post call with project id not present
        """
        user_data = {
            'user_ids' : []
        }
        response = self.client.post('/api/projects/projects/', user_data)
        self.assertEqual(400, response.status_code)

    def test_user_ids_absent(self):
        """
        Test to verify a post call with user ids not present
        """
        response = self.client.post('/api/projects/projects/?project_id=1')
        self.assertEqual(400, response.status_code)

    def test_successfully_added_members(self):
        """
        Test to verify a post call that successfully adds members
        """
        user_data = {
            'user_ids' : []
        }
        response = self.client.post(
            '/api/projects/projects/?project_id=1', user_data)
        print(response.data)
        self.assertEqual(201, response.status_code)


class ProjectMemberAPIViewSetDeleteTestCase(APITestCase):
    def test_user_ids_absent(self):
        """
        Test to verify a post call with user ids not present
        """
        response = self.client.post('/api/projects/projects/1/')
        self.assertEqual(400, response.status_code)

    def test_successfully_removed_members(self):
        """
        Test to verify a post call that successfully removes members
        """
        user_data = {
            'user_ids' : [1,2]
        }
        response = self.client.post('/api/projects/projects/1/', user_data)
        print(response.data)
        self.assertEqual(200, response.status_code)
