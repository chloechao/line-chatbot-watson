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
    mc.delete('context')

    def list_workspace(self):
        return self.assistant.list_workspaces()

    def message_request(self, message):
        conversation_id = self.mc.get('conversation_id')
        context = self.mc.get('context', dict())
        context['timezone'] = 'Asia/Tokyo'
        context['no_reservation'] = True

        print('CONVER_ID-init')
        print(conversation_id)
        print(context)
        response = self.assistant.message(
            workspace_id=self.workspace_id,
            input={
                'text': message
            },
            alternate_intents=True,
            context=context,
            )
        print(response)
        conversation_id = response.get('context').get('conversation_id')
        context = response.get('context')
        print('CONVER ID:')
        print(conversation_id)
        print(context)
        self.mc.set('conversation_id', conversation_id)
        self.mc.set('context', context)
        return response.get('output').get('generic')[0].get('text')
