# -*- coding: utf-8 -*-
from watson_developer_cloud import AssistantV1
import bmemcached
import os


API_USER_NAME = os.getenv('IBM_API_USER_NAME', None)
API_PASSWORD = os.getenv('IBM_API_PASSWORD', None)


class IbmAssistant:

    assistant = AssistantV1(
        username=API_USER_NAME,
        password=API_PASSWORD,
        version='2018-07-10')

    workspace_id = '1ef0a9c1-f07e-4bb7-adfc-0d0f3fb6ff4a'
    mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
                           os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                           os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

    def list_workspace(self):
        return self.assistant.list_workspaces()

    def message_request(self, message):
        conversation_id = self.mc.get('conversation_id')
        print('CONVER_ID-init')
        print(conversation_id)
        response = self.assistant.message(
            workspace_id=self.workspace_id,
            input={
                'text': message
            },
            alternate_intents=True,
            context={
                'conversation_id': self.conversation_id,
                'metadata': {
                    'deployment': 'myDeployment'
                }
            })
        print(response)
        conversation_id = response.get('context').get('conversation_id')
        print('CONVER ID:')
        print(conversation_id)
        self.mc.set('conversation_id', conversation_id)
        return response.get('output').get('generic')[0].get('text')
