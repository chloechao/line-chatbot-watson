# -*- coding: utf-8 -*-
from watson_developer_cloud import AssistantV1
import os


API_USER_NAME = os.getenv('IBM_API_USER_NAME', None)
API_PASSWORD = os.getenv('IBM_API_PASSWORD', None)


class IbmAssistant:

    assistant = AssistantV1(
        username=API_USER_NAME,
        password=API_PASSWORD,
        version='2018-07-10')

    workspace_id = '1ef0a9c1-f07e-4bb7-adfc-0d0f3fb6ff4a'

    def list_workspace(self):
        return self.assistant.list_workspaces()

    def message_request(self, message):
        response = self.assistant.message(
            workspace_id=self.workspace_id,
            input={
                'text': message
            },
            "alternate_intents": True,
            context={
                'metadata': {
                    'deployment': 'myDeployment'
                }
            })
        print(response)
        return response.get('output').get('generic')[0].get('text')
